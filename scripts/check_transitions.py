#!/usr/bin/env python3
"""Pre-commit guard: validates staged task files against .cursor/rules/workflow.mdc.

Usage: scripts/check_transitions.py   (checks staged tasks/TASK-*.md against HEAD)
Exit 1 with a list of violations if any rule is broken.
"""
import re
import subprocess
import sys

STATUSES = {
    "BACKLOG", "READY", "IN_PROGRESS", "CODE_REVIEW", "CHANGES_REQUESTED", "MERGED", "TESTING",
    "BUG", "READY_FOR_DEPLOY", "DEPLOYING", "RELEASED", "BLOCKED",
}
WORKING = STATUSES - {"BACKLOG", "RELEASED", "BLOCKED"}
ROLES = {"SCRUM", "SA", "BE", "FE", "TEST", "DEVOPS", "HUMAN"}

TRANSITIONS = {
    ("BACKLOG", "READY"): {"SCRUM", "HUMAN"},
    ("READY", "IN_PROGRESS"): {"ASSIGNEE"},
    ("IN_PROGRESS", "CODE_REVIEW"): {"ASSIGNEE"},
    ("CODE_REVIEW", "CHANGES_REQUESTED"): {"SA"},
    ("CODE_REVIEW", "MERGED"): {"SA"},
    ("CHANGES_REQUESTED", "IN_PROGRESS"): {"ASSIGNEE"},
    ("MERGED", "TESTING"): {"TEST"},
    ("TESTING", "BUG"): {"TEST"},
    ("TESTING", "READY_FOR_DEPLOY"): {"TEST"},
    ("BUG", "IN_PROGRESS"): {"ASSIGNEE"},
    ("READY_FOR_DEPLOY", "DEPLOYING"): {"DEVOPS"},
    ("DEPLOYING", "RELEASED"): {"DEVOPS"},
}

TASK_PATH = re.compile(r"^tasks/TASK-\d{3,}-[^/]+\.md$")


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


def role_of(by):
    return by.split()[0].upper() if by else ""


def as_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def check(path, old, new):
    """Return a list of violations for one task file (old is None for a new file)."""
    errors = []
    err = errors.append
    if new is None:
        return [f"{path}: task files must not be deleted"]

    nf, nh = frontmatter(new), history(new)
    status = nf.get("status", "")
    if status not in STATUSES:
        err(f"{path}: unknown status '{status}'")
        return errors

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

    allowed = TRANSITIONS.get((before, status))
    if allowed is None:
        err(f"{path}: transition {before} -> {status} is not allowed (workflow.mdc §2)")
        return errors
    if "ASSIGNEE" in allowed:
        if by != nf.get("assignee", "").upper():
            err(f"{path}: {before} -> {status} must be done by the assignee ({nf.get('assignee')}), not {row[3]}")
    elif by not in allowed:
        err(f"{path}: {before} -> {status} is not allowed for {row[3]} (allowed: {', '.join(sorted(allowed))})")

    counters = {("CODE_REVIEW", "CHANGES_REQUESTED"): "review_iteration", ("TESTING", "BUG"): "test_iteration"}
    counter = counters.get((before, status))
    if counter:
        o, n = as_int(of.get(counter)), as_int(nf.get(counter))
        if o is None or n != o + 1:
            err(f"{path}: {counter} must increase by 1 ({of.get(counter)} -> {nf.get(counter)})")
        elif o >= 3:
            err(f"{path}: {counter} limit reached; set BLOCKED instead (workflow.mdc §3)")
    if status == "MERGED" and not nf.get("merge_commit"):
        err(f"{path}: merge_commit must be set when MERGED")
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
    errors = []
    for state, path in staged_task_files():
        old = blob("HEAD", path) if has_head and state != "A" else None
        new = None if state == "D" else blob("", path)
        errors += check(path, old, new)
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
