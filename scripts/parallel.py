#!/usr/bin/env python3
"""Which READY tasks may run in parallel (different product repos, no dep edge).

Usage: python3 scripts/parallel.py
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deps  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def repo_of(tid: str, tasks: dict) -> str:
    info = tasks.get(tid) or {}
    if info.get("work_type") == "UX_UI" or info.get("assignee") == "UX/UI":
        return "ux-docs"
    path = info.get("path")
    if not path:
        return ""
    text = (ROOT / path).read_text() if (ROOT / path).exists() else ""
    for line in text.splitlines():
        if line.startswith("repo:"):
            return line.split(":", 1)[1].strip()
        if line.lower().startswith("repo:"):
            return line.split(":", 1)[1].strip()
        if line.startswith("- Repo:") or line.startswith("Repo:"):
            return line.split(":", 1)[1].strip().split()[0]
    return info.get("assignee", "")


def conflicts(a: str, b: str, tasks: dict) -> str | None:
    if a == b:
        return "same task"
    da, db = tasks[a]["depends_on"], tasks[b]["depends_on"]
    if a in db or b in da:
        return "depends_on edge"
    ra, rb = repo_of(a, tasks), repo_of(b, tasks)
    if ra and rb and ra == rb:
        return f"same repo ({ra})"
    return None


def pairs(tasks: dict) -> list[tuple[str, str]]:
    ready = [t["id"] for t in tasks.values() if t["status"] == "READY" and deps.deps_ready(tasks, t["id"])]
    out = []
    for i, a in enumerate(ready):
        for b in ready[i + 1 :]:
            if conflicts(a, b, tasks) is None:
                out.append((a, b))
    return out


def main() -> int:
    tasks = deps.load_tasks()
    found = pairs(tasks)
    if not found:
        print("No parallel pairs")
        return 0
    print("Parallel-safe READY pairs:")
    for a, b in found:
        print(f"  {a} || {b}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
