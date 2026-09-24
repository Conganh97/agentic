#!/usr/bin/env python3
"""Task dependency graph. Used by check_transitions.py and `python3 scripts/deps.py`.

Usage:
  python3 scripts/deps.py              print graph + cycles + actionable
  python3 scripts/deps.py --json       machine-readable
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TASK_ID = re.compile(r"TASK-\d{3,}")
DONE = {
    "MERGED",
    "TESTING",
    "BUG",
    "READY_FOR_DEPLOY",
    "DEPLOYING",
    "RELEASED",
}

def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    fields: dict[str, str] = {}
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def parse_depends(value: str) -> list[str]:
    if not value:
        return []
    return TASK_ID.findall(value)


def load_tasks(root: pathlib.Path | None = None) -> dict[str, dict]:
    base = root or ROOT
    tasks: dict[str, dict] = {}
    for path in sorted((base / "tasks").glob("TASK-*.md")):
        fields = frontmatter(path.read_text())
        tid = fields.get("id") or path.stem.split("-", 2)[0] + "-" + path.stem.split("-")[1]
        tasks[tid] = {
            "id": tid,
            "path": str(path.relative_to(base)),
            "status": fields.get("status", ""),
            "assignee": fields.get("assignee", ""),
            "priority": fields.get("priority", ""),
            "parent": fields.get("parent", ""),
            "depends_on": parse_depends(fields.get("depends_on", "")),
            "human_gate": fields.get("human_gate", ""),
            "requirement_revision": fields.get("requirement_revision", ""),
            "repo": fields.get("repo", ""),
            "review_iteration": fields.get("review_iteration", "0"),
            "test_iteration": fields.get("test_iteration", "0"),
            "failed_from": fields.get("failed_from", ""),
            "approved_by": fields.get("approved_by", ""),
        }
    return tasks


def cycles(tasks: dict[str, dict]) -> list[list[str]]:
    graph = {tid: info["depends_on"] for tid, info in tasks.items()}
    found: list[list[str]] = []
    visiting: list[str] = []
    seen: set[str] = set()

    def walk(node: str) -> None:
        if node in visiting:
            found.append(visiting[visiting.index(node) :] + [node])
            return
        if node in seen or node not in graph:
            return
        visiting.append(node)
        for nxt in graph[node]:
            walk(nxt)
        visiting.pop()
        seen.add(node)

    for tid in graph:
        walk(tid)
    return found


def missing_refs(tasks: dict[str, dict]) -> list[str]:
    ids = set(tasks)
    errors = []
    for tid, info in tasks.items():
        for dep in info["depends_on"]:
            if dep not in ids:
                errors.append(f"{tid} depends_on {dep} (no such task)")
    return errors


def incomplete_deps(tasks: dict[str, dict], tid: str) -> list[str]:
    info = tasks.get(tid)
    if not info:
        return [f"unknown task {tid}"]
    return [
        f"{dep} ({tasks[dep]['status']})" if dep in tasks else f"{dep} (missing)"
        for dep in info["depends_on"]
        if dep not in tasks or tasks[dep]["status"] not in DONE
    ]


def deps_ready(tasks: dict[str, dict], tid: str) -> bool:
    return not incomplete_deps(tasks, tid)


def actionable(tasks: dict[str, dict]) -> list[dict]:
    """Tasks whose depends_on are MERGED-or-later (or empty)."""
    return [info for tid, info in sorted(tasks.items()) if deps_ready(tasks, tid)]


def main(argv: list[str]) -> int:
    tasks = load_tasks()
    payload = {
        "cycles": cycles(tasks),
        "missing": missing_refs(tasks),
        "actionable": [t["id"] for t in actionable(tasks)],
        "blocked_by_deps": {
            tid: incomplete_deps(tasks, tid)
            for tid in tasks
            if incomplete_deps(tasks, tid)
        },
    }
    if "--json" in argv:
        print(json.dumps(payload, indent=2))
        return 1 if payload["cycles"] or payload["missing"] else 0
    if payload["cycles"]:
        print("Cycles:")
        for cyc in payload["cycles"]:
            print("  " + " → ".join(cyc))
    if payload["missing"]:
        print("Missing:")
        for m in payload["missing"]:
            print(f"  {m}")
    print("Actionable (deps MERGED or later):")
    for tid in payload["actionable"]:
        t = tasks[tid]
        print(f"  {tid} {t['status']} {t['assignee']}")
    if payload["blocked_by_deps"]:
        print("Waiting on dependencies:")
        for tid, deps in payload["blocked_by_deps"].items():
            print(f"  {tid}: {', '.join(deps)}")
    return 1 if payload["cycles"] or payload["missing"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
