#!/usr/bin/env python3
"""Requirement hash, revision vs tasks, and completion guards.

Usage:
  python3 scripts/req.py hash <requirements/REQ-###-*.md>
  python3 scripts/req.py check           # working tree
  python3 scripts/req.py check --staged
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TASK_ID = re.compile(r"TASK-\d{3,}")
REQ_PATH = re.compile(r"^requirements/REQ-\d{3,}-[^/]+\.md$")
COMPLETE = {
    "READY_FOR_RELEASE": {"READY_FOR_DEPLOY", "DEPLOYING", "RELEASED"},
    "RELEASED": {"RELEASED"},
}
# UX_UI / DEVOPS skip TEST and stay MERGED; they still count as done for REQ completion.
SKIP_TEST_OK = {
    "READY_FOR_RELEASE": {"MERGED", "READY_FOR_DEPLOY", "DEPLOYING", "RELEASED"},
    "RELEASED": {"MERGED", "RELEASED"},
}


def frontmatter(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def body(text: str) -> str:
    parts = text.split("---", 2)
    return parts[2] if len(parts) >= 3 else text


def content_hash(text: str) -> str:
    return hashlib.sha256(body(text).encode()).hexdigest()[:16]


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def blob(ref: str, path: str) -> str | None:
    r = git("show", f"{ref}:{path}")
    return r.stdout if r.returncode == 0 else None


def load_reqs(staged: bool) -> list[tuple[str, str, str | None]]:
    """(path, new_text, old_text_or_None)."""
    out = []
    if staged:
        diff = git("diff", "--cached", "--name-status", "--no-renames").stdout
        for line in diff.splitlines():
            state, path = line.split("\t", 1)
            if not REQ_PATH.match(path):
                continue
            new = None if state == "D" else blob("", path)
            old = blob("HEAD", path) if state != "A" else None
            if new is not None:
                out.append((path, new, old))
        return out
    for path in sorted((ROOT / "requirements").glob("REQ-*.md")):
        rel = str(path.relative_to(ROOT))
        out.append((rel, path.read_text(), blob("HEAD", rel)))
    return out


def load_tasks() -> dict[str, dict]:
    tasks = {}
    for path in (ROOT / "tasks").glob("TASK-*.md"):
        f = frontmatter(path.read_text())
        tid = f.get("id")
        if tid:
            tasks[tid] = f
    return tasks


def skip_test_child(tf: dict) -> bool:
    work = (tf.get("work_type") or "").strip()
    assignee = (tf.get("assignee") or "").strip()
    return work in {"UX_UI", "DEVOPS"} or assignee in {"UX/UI", "DEVOPS"}


def allowed_child_status(req_status: str, tf: dict) -> set[str] | None:
    if req_status not in COMPLETE:
        return None
    if skip_test_child(tf):
        return SKIP_TEST_OK[req_status]
    return COMPLETE[req_status]


def check_one(path: str, new: str, old: str | None, tasks: dict[str, dict]) -> list[str]:
    errors = []
    nf = frontmatter(new)
    expected = content_hash(new)
    got = nf.get("content_hash", "")
    if got != expected:
        errors.append(f"{path}: content_hash is '{got}' but body hashes to {expected} (run: python3 scripts/req.py hash {path})")
    if old:
        of = frontmatter(old)
        body_changed = content_hash(old) != expected
        rev_old, rev_new = of.get("revision", "1"), nf.get("revision", "1")
        if body_changed and rev_new == rev_old:
            errors.append(f"{path}: requirement body changed but revision is still {rev_new}; bump revision")
    status = nf.get("status", "")
    listed = TASK_ID.findall(nf.get("tasks", ""))
    if status in COMPLETE:
        if not listed:
            errors.append(f"{path}: {status} requires tasks: [TASK-…]")
        for tid in listed:
            tf = tasks.get(tid, {})
            st = tf.get("status", "missing")
            allowed = allowed_child_status(status, tf) or COMPLETE[status]
            if st not in allowed:
                errors.append(f"{path}: cannot be {status} while {tid} is {st}")
    rid = nf.get("id", "")
    rev = nf.get("revision", "")
    for tid, tf in tasks.items():
        if tf.get("parent") != rid:
            continue
        tr = tf.get("requirement_revision", "")
        if tr and rev and tr != rev:
            errors.append(f"{path}: {tid} requirement_revision={tr} != {rid} revision={rev} (requirement_changed)")
    return errors


def main(argv: list[str]) -> int:
    if argv and argv[0] == "hash":
        if len(argv) < 2:
            print("usage: req.py hash <file>", file=sys.stderr)
            return 2
        path = pathlib.Path(argv[1])
        print(content_hash(path.read_text()))
        return 0
    staged = "--staged" in argv
    tasks = load_tasks()
    errors = []
    for path, new, old in load_reqs(staged):
        errors += check_one(path, new, old, tasks)
    if not staged:
        for path in (ROOT / "requirements").glob("REQ-*.md"):
            rel = str(path.relative_to(ROOT))
            if not any(p == rel for p, _, _ in load_reqs(False)):
                continue
    if errors:
        print("Requirement check failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
