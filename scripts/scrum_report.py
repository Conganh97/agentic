#!/usr/bin/env python3
"""/scrum report from disk. No file writes.

Usage: python3 scripts/scrum_report.py [REQ-###]
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deps  # noqa: E402
from check_transitions import history  # noqa: E402
from req import frontmatter  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def cycle_time(rows: list[list[str]]) -> str:
    start = next((r[0] for r in rows if len(r) > 2 and r[2] == "IN_PROGRESS"), "")
    merged = next((r[0] for r in rows if len(r) > 2 and r[2] == "MERGED"), "")
    if start and merged:
        return f"{start} → {merged}"
    return "—"


def main(argv: list[str]) -> int:
    req_id = argv[0] if argv else None
    tasks = deps.load_tasks()
    if req_id:
        tasks = {k: v for k, v in tasks.items() if v.get("parent") == req_id}
    counts: dict[str, int] = {}
    for t in tasks.values():
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    bugs = list((ROOT / "bugs").glob("BUG-*.md")) if (ROOT / "bugs").exists() else []
    open_bugs = []
    for p in bugs:
        st = frontmatter(p.read_text()).get("status", "OPEN")
        if st != "CLOSED":
            open_bugs.append(p.name)
    print(f"Scope: {req_id or 'all tasks'}  ({len(tasks)} tasks)")
    print("Status:", "  ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "(none)")
    print(f"FAILED: {counts.get('FAILED', 0)}   BUG files open: {len(open_bugs)}")
    if open_bugs:
        print("  " + ", ".join(open_bugs))
    print("Blocked / FAILED / gated:")
    any_wait = False
    for t in sorted(tasks.values(), key=lambda x: x["id"]):
        path = ROOT / t["path"]
        text = path.read_text() if path.exists() else ""
        fm = frontmatter(text)
        if t["status"] == "BLOCKED":
            print(f"  {t['id']} BLOCKED from {fm.get('blocked_from', '')}")
            any_wait = True
        if t["status"] == "FAILED":
            print(f"  {t['id']} FAILED {fm.get('failure_type', '')} {fm.get('failure_message', fm.get('failure', ''))}")
            any_wait = True
        if fm.get("human_gate") and not fm.get("approved_by"):
            print(f"  {t['id']} human_gate={fm.get('human_gate')}")
            any_wait = True
        inc = deps.incomplete_deps(tasks, t["id"])
        if inc and t["status"] in {"BACKLOG", "READY"}:
            print(f"  {t['id']} waiting deps: {', '.join(inc)}")
            any_wait = True
    if not any_wait:
        print("  (none)")
    print("Per task:")
    for t in sorted(tasks.values(), key=lambda x: x["id"]):
        path = ROOT / t["path"]
        rows = history(path.read_text()) if path.exists() else []
        print(
            f"  {t['id']} {t['status']} review={t.get('review_iteration', '0')} "
            f"test={t.get('test_iteration', '0')} cycle={cycle_time(rows)}"
        )
    if req_id:
        children = list(tasks.values())
        if children and all(c["status"] == "RELEASED" for c in children):
            print(f"Requirement {req_id}: all tasks RELEASED → may set READY_FOR_RELEASE / RELEASED")
        elif children:
            print(f"Requirement {req_id}: incomplete — do not mark RELEASED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
