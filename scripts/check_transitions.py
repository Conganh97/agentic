#!/usr/bin/env python3
"""Pre-commit guard: validates staged task files against .cursor/rules/workflow.mdc.

Usage: scripts/check_transitions.py   (checks staged tasks/TASK-*.md against HEAD)
Exit 1 with a list of violations if any rule is broken.
"""
import pathlib
import re
import subprocess
import sys

STATUSES = {
    "BACKLOG", "READY", "IN_PROGRESS", "CODE_REVIEW", "CHANGES_REQUESTED", "MERGED", "TESTING",
    "BUG", "FAILED", "READY_FOR_DEPLOY", "DEPLOYING", "RELEASED", "BLOCKED",
}
WORKING = STATUSES - {"BACKLOG", "RELEASED", "BLOCKED"}
FAILED_FROM = {"IN_PROGRESS", "TESTING", "DEPLOYING"}
ROLES = {"SCRUM", "SA", "PQA", "UX/UI", "BE", "FE", "TEST", "DEVOPS", "HUMAN"}
DONE = {"MERGED", "TESTING", "BUG", "READY_FOR_DEPLOY", "DEPLOYING", "RELEASED"}
MERGE_SHA = re.compile(r"^[0-9a-f]{7,40}$")

TRANSITIONS = {
    ("BACKLOG", "READY"): {"SCRUM", "HUMAN"},
    ("READY", "IN_PROGRESS"): {"ASSIGNEE"},
    ("IN_PROGRESS", "CODE_REVIEW"): {"ASSIGNEE"},
    ("IN_PROGRESS", "FAILED"): {"ASSIGNEE"},
    ("CODE_REVIEW", "CHANGES_REQUESTED"): {"SA", "PQA"},
    ("CODE_REVIEW", "MERGED"): {"SA", "PQA"},
    ("CHANGES_REQUESTED", "IN_PROGRESS"): {"ASSIGNEE"},
    ("MERGED", "TESTING"): {"TEST"},
    ("TESTING", "BUG"): {"TEST"},
    ("TESTING", "READY_FOR_DEPLOY"): {"TEST"},
    ("TESTING", "FAILED"): {"TEST"},
    ("BUG", "IN_PROGRESS"): {"ASSIGNEE"},
    ("FAILED", "IN_PROGRESS"): {"ASSIGNEE", "SCRUM", "HUMAN"},
    ("FAILED", "TESTING"): {"TEST", "SCRUM", "HUMAN"},
    ("FAILED", "DEPLOYING"): {"DEVOPS", "SCRUM", "HUMAN"},
    ("READY_FOR_DEPLOY", "DEPLOYING"): {"DEVOPS"},
    ("DEPLOYING", "RELEASED"): {"DEVOPS"},
    ("DEPLOYING", "FAILED"): {"DEVOPS"},
}

TASK_PATH = re.compile(r"^tasks/TASK-\d{3,}-[^/]+\.md$")
TASK_ID = re.compile(r"TASK-\d{3,}")
ROOT = pathlib.Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False)


def frontmatter(text):
    lines = text.splitlines()
    fields = {}
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def history(text):
    rows, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## History"
            continue
        if inside and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0] != "Time" and not set(cells[0]) <= set("-: "):
                rows.append(cells)
    return rows


def section(text, heading):
    lines = text.splitlines()
    out, inside = [], False
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == heading
            continue
        if inside:
            out.append(line)
    return "\n".join(out)


def last_review_approved(text):
    rounds = re.findall(r"^### Round \d+ — (\w+)", section(text, "## Review (SA)"), re.M)
    return bool(rounds) and rounds[-1] == "APPROVED"


def last_test_pass(text):
    runs = re.findall(r"^### Run \d+ — (\w+)", section(text, "## Test (TEST)"), re.M)
    return bool(runs) and runs[-1] == "PASS"


def has_iteration(text):
    return bool(re.search(r"^### Iteration ", section(text, "## Implementation (BE/FE)"), re.M))


def flag_true(value):
    return (value or "").strip().lower() in {"true", "yes", "1"}


def flag_false(value):
    return (value or "").strip().lower() in {"false", "no", "0"}


def is_uxui_work(fields):
    return (fields.get("work_type") or "").strip() == "UX_UI" or fields.get("assignee") == "UX/UI"


def uxui_required(fields):
    if flag_false(fields.get("requires_uxui")):
        return False
    if flag_true(fields.get("requires_uxui")):
        return True
    return (fields.get("work_type") or "").strip() == "FRONTEND"


def last_uxui_review_approved(fields):
    path = (fields.get("uxui_review") or "").strip()
    if not path:
        return False
    full = ROOT / path
    if not full.is_file():
        return False
    status = frontmatter(full.read_text()).get("status", "")
    return status == "APPROVED"


def ac_ids(text):
    return re.findall(r"AC-\d+", section(text, "## Acceptance Criteria"))


def ac_unchecked(text):
    return re.findall(r"^- \[ \] (AC-\d+)", section(text, "## Acceptance Criteria"), re.M)


def role_of(by):
    return by.split()[0].upper() if by else ""


def as_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_depends(value):
    return TASK_ID.findall(value or "")


def all_task_status(overrides):
    """id → status from working tree, overlaying staged/new text in overrides {path: text}."""
    statuses = {}
    tasks_dir = ROOT / "tasks"
    if tasks_dir.is_dir():
        for path in tasks_dir.glob("TASK-*.md"):
            rel = f"tasks/{path.name}"
            text = overrides[rel] if rel in overrides else path.read_text()
            fields = frontmatter(text)
            tid = fields.get("id")
            if tid:
                statuses[tid] = fields.get("status", "")
    for rel, text in overrides.items():
        fields = frontmatter(text)
        tid = fields.get("id")
        if tid:
            statuses[tid] = fields.get("status", "")
    return statuses


def dep_errors(path, nf, statuses):
    errors = []
    deps = parse_depends(nf.get("depends_on", ""))
    tid = nf.get("id", "")
    for dep in deps:
        if dep == tid:
            errors.append(f"{path}: depends_on must not include itself")
        elif dep not in statuses:
            errors.append(f"{path}: depends_on {dep} does not exist")
    return errors


def deps_incomplete(nf, statuses):
    return [
        f"{dep} ({statuses.get(dep, 'missing')})"
        for dep in parse_depends(nf.get("depends_on", ""))
        if statuses.get(dep) not in DONE
    ]


def check(path, old, new, statuses=None):
    """Return a list of violations for one task file (old is None for a new file)."""
    errors = []
    err = errors.append
    if new is None:
        return []

    nf, nh = frontmatter(new), history(new)
    status = nf.get("status", "")
    statuses = statuses or {nf.get("id", ""): status}
    if status not in STATUSES:
        err(f"{path}: unknown status '{status}'")
        return errors

    errors += dep_errors(path, nf, statuses)

    if old is None:
        if status != "BACKLOG":
            err(f"{path}: a new task must start in BACKLOG (found {status})")
        if not nh or nh[-1][1:3] != ["—", "BACKLOG"]:
            err(f"{path}: a new task needs a History row '— → BACKLOG'")
        return errors

    of, oh = frontmatter(old), history(old)
    before = of.get("status", "")

    if nh[: len(oh)] != oh:
        err(f"{path}: History is append-only; existing rows were changed or removed")
        return errors
    added = nh[len(oh):]

    if nf.get("approved_by", "") != of.get("approved_by", "") and nf.get("approved_by"):
        if not any(role_of(r[3] if len(r) > 3 else "") == "HUMAN" for r in added):
            err(f"{path}: approved_by may only be set with a History row By = HUMAN (<name>)")

    if status == before:
        for row in added:
            if len(row) < 5 or row[1] != row[2] or row[1] != status:
                err(f"{path}: History row {row} records a status change, but status is still {status}")
        return errors

    if len(added) != 1:
        err(f"{path}: {before} -> {status} needs exactly one new History row (found {len(added)})")
        return errors
    row = added[0]
    if len(row) < 5:
        err(f"{path}: History row must have 5 columns: Time | From | To | By | Note")
        return errors
    if row[1] != before or row[2] != status:
        err(f"{path}: History row says {row[1]} -> {row[2]}, frontmatter says {before} -> {status}")
    by = role_of(row[3])
    if by not in ROLES:
        err(f"{path}: unknown role '{row[3]}' in History")
    if not row[4] or row[4] in {"—", "-", "todo"}:
        err(f"{path}: History Note must record evidence/reason for {before} -> {status}")

    if status == "BLOCKED":
        if before not in WORKING:
            err(f"{path}: {before} cannot be blocked")
        if nf.get("blocked_from") != before:
            err(f"{path}: blocked_from must be {before}")
        return errors

    if before == "BLOCKED":
        if status != of.get("blocked_from"):
            err(f"{path}: BLOCKED may only return to blocked_from ({of.get('blocked_from') or 'unset'})")
        if by not in {"SCRUM", "HUMAN"}:
            err(f"{path}: only SCRUM or HUMAN may unblock (By = {row[3]})")
        if nf.get("blocked_from"):
            err(f"{path}: clear blocked_from when unblocking")
        return errors

    if status == "FAILED":
        if before not in FAILED_FROM:
            err(f"{path}: {before} cannot go to FAILED (allowed from: {', '.join(sorted(FAILED_FROM))})")
        if nf.get("failed_from") != before:
            err(f"{path}: failed_from must be {before}")
        if not (nf.get("failure_type") and nf.get("failure_step") and nf.get("failure_message")) and not nf.get("failure"):
            err(f"{path}: set failure_type, failure_step, failure_message (or legacy failure:)")
        retry = as_int(nf.get("failure_retry"))
        if retry is None:
            err(f"{path}: failure_retry must be an integer")
        elif retry >= 3:
            err(f"{path}: failure_retry limit reached; set BLOCKED instead")
        if nf.get("failure_recoverable") not in {"", "true", "false", "yes", "no"}:
            err(f"{path}: failure_recoverable must be true or false")
        allowed_fail = TRANSITIONS.get((before, "FAILED"), set())
        if "ASSIGNEE" in allowed_fail:
            if by != nf.get("assignee", "").upper() and by not in {"SCRUM", "HUMAN"}:
                err(f"{path}: {before} -> FAILED must be the assignee ({nf.get('assignee')}), not {row[3]}")
        elif by not in allowed_fail:
            err(f"{path}: {before} -> FAILED is not allowed for {row[3]}")
        return errors

    if before == "FAILED":
        expected = of.get("failed_from")
        if status != expected:
            err(f"{path}: FAILED may only return to failed_from ({expected or 'unset'})")
        recover = TRANSITIONS.get(("FAILED", status), {"ASSIGNEE", "SCRUM", "HUMAN"})
        if "ASSIGNEE" in recover and by not in recover and by != nf.get("assignee", "").upper():
            if by not in {"SCRUM", "HUMAN", "TEST", "DEVOPS"}:
                err(f"{path}: only the owning role, SCRUM or HUMAN may recover FAILED")
        if nf.get("failed_from"):
            err(f"{path}: clear failed_from when leaving FAILED")
        return errors

    allowed = TRANSITIONS.get((before, status))
    if allowed is None:
        err(f"{path}: transition {before} -> {status} is not allowed (workflow.mdc §2)")
        return errors
    if "ASSIGNEE" in allowed:
        if by != nf.get("assignee", "").upper():
            err(f"{path}: {before} -> {status} must be done by the assignee ({nf.get('assignee')}), not {row[3]}")
    elif by not in allowed:
        err(f"{path}: {before} -> {status} is not allowed for {row[3]} (allowed: {', '.join(sorted(allowed))})")

    if status in {"READY", "IN_PROGRESS"} and before in {"BACKLOG", "READY"}:
        incomplete = deps_incomplete(nf, statuses)
        if incomplete:
            err(f"{path}: {before} -> {status} blocked by depends_on: {', '.join(incomplete)}")
        parent = nf.get("parent", "")
        mine = nf.get("requirement_revision", "")
        if parent and mine:
            for req_path in (ROOT / "requirements").glob(f"{parent}-*.md"):
                prev = frontmatter(req_path.read_text()).get("revision", "")
                if prev and prev != mine:
                    err(f"{path}: requirement_changed ({parent} revision {prev} vs task {mine})")
                break
        if status == "READY":
            try:
                from gate_scan import scan
                hits = scan(new)
            except Exception:
                hits = []
            if hits and not nf.get("human_gate") and not nf.get("approved_by"):
                err(f"{path}: human_gate required for {', '.join(hits)}")

    tid = nf.get("id", "")
    if status in {"MERGED", "CHANGES_REQUESTED"}:
        visual = by == "PQA" and (is_uxui_work(nf) or uxui_required(nf))
        if visual:
            if tid and not list((ROOT / "docs" / "design" / "ux" / "reviews").glob(f"{tid}-review-*.md")):
                err(f"{path}: missing docs/design/ux/reviews/{tid}-review-N.md (copy templates/ux-review.md)")
        elif tid and not list((ROOT / "reviews").glob(f"{tid}-round-*.md")):
            err(f"{path}: missing reviews/{tid}-round-N.md (copy templates/review-round.md)")
    if status in {"READY_FOR_DEPLOY", "BUG"} and before == "TESTING":
        if tid and not list((ROOT / "tests").glob(f"{tid}-run-*.md")):
            err(f"{path}: missing tests/{tid}-run-N.md (copy templates/test-report.md)")

    if before == "CODE_REVIEW" and status == "CHANGES_REQUESTED" and by == "PQA":
        o, n = as_int(of.get("uxui_review_iteration")), as_int(nf.get("uxui_review_iteration"))
        if o is None or n != o + 1:
            err(f"{path}: uxui_review_iteration must increase by 1 ({of.get('uxui_review_iteration')} -> {nf.get('uxui_review_iteration')})")
        elif o >= 3:
            err(f"{path}: uxui_review_iteration limit reached; set BLOCKED instead (workflow.mdc §3)")
    else:
        counters = {("CODE_REVIEW", "CHANGES_REQUESTED"): "review_iteration", ("TESTING", "BUG"): "test_iteration"}
        counter = counters.get((before, status))
        if counter:
            o, n = as_int(of.get(counter)), as_int(nf.get(counter))
            if o is None or n != o + 1:
                err(f"{path}: {counter} must increase by 1 ({of.get(counter)} -> {nf.get(counter)})")
            elif o >= 3:
                err(f"{path}: {counter} limit reached; set BLOCKED instead (workflow.mdc §3)")
    if before == "CODE_REVIEW" and status == "MERGED":
        if by == "PQA" and not is_uxui_work(nf):
            err(f"{path}: PQA may only MERGED work_type UX_UI (code merge is SA)")
        if by == "SA" and is_uxui_work(nf):
            err(f"{path}: SA does not MERGED UX_UI; PQA reviews the design contract")
    if status == "MERGED":
        sha = nf.get("merge_commit", "")
        if not sha or not MERGE_SHA.match(sha):
            err(f"{path}: merge_commit must be a git sha (7–40 hex) when MERGED")
        if is_uxui_work(nf):
            if not last_uxui_review_approved(nf):
                err(f"{path}: UX_UI MERGED requires an APPROVED PQA review (uxui_review)")
        else:
            if not last_review_approved(new):
                err(f"{path}: MERGED requires the latest Review round to be APPROVED")
            if uxui_required(nf) and not last_uxui_review_approved(nf):
                err(f"{path}: MERGED requires an APPROVED PQA visual review (uxui_review)")
    if status == "CODE_REVIEW" and not has_iteration(new):
        err(f"{path}: CODE_REVIEW requires an Implementation iteration")
    if status == "CODE_REVIEW" and not nf.get("branch"):
        err(f"{path}: branch must be set when CODE_REVIEW")
    if status == "READY_FOR_DEPLOY":
        if not last_test_pass(new):
            err(f"{path}: READY_FOR_DEPLOY requires the latest Test run to be PASS")
        unchecked = ac_unchecked(new)
        if ac_ids(new) and unchecked:
            err(f"{path}: READY_FOR_DEPLOY requires every AC checked; still open: {', '.join(unchecked)}")
    if status == "RELEASED" and not nf.get("release"):
        err(f"{path}: release must be set when RELEASED")
    return errors


def staged_task_files():
    out = git("diff", "--cached", "--name-status", "--no-renames").stdout
    for line in out.splitlines():
        state, path = line.split("\t", 1)
        if TASK_PATH.match(path):
            yield state, path


def blob(ref, path):
    result = git("show", f"{ref}:{path}")
    return result.stdout if result.returncode == 0 else None


def main():
    has_head = git("rev-parse", "--verify", "-q", "HEAD").returncode == 0
    staged = list(staged_task_files())
    overrides = {}
    for state, path in staged:
        if state != "D":
            text = blob("", path)
            if text is not None:
                overrides[path] = text
    statuses = all_task_status(overrides)
    errors = []
    for state, path in staged:
        old = blob("HEAD", path) if has_head and state != "A" else None
        new = None if state == "D" else blob("", path)
        errors += check(path, old, new, statuses)
    if errors:
        print("Task workflow check failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("Fix the task file, or (HUMAN only) record the exception in History and commit with --no-verify.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
