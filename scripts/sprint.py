#!/usr/bin/env python3
"""Sprint policy for /scrum run. Small work skips sprints; large work is sliced.

Usage:
  python3 scripts/sprint.py [REQ-###]          print evaluate()
  python3 scripts/sprint.py plan [REQ-###]     print proposed task ids
"""
from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deps  # noqa: E402
from req import frontmatter  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SMALL_MAX = 5
SPRINT_CAP = 6
IN_FLIGHT = {
    "IN_PROGRESS",
    "CODE_REVIEW",
    "CHANGES_REQUESTED",
    "TESTING",
    "BUG",
    "FAILED",
}
SPRINT_FILE = re.compile(r"^SPRINT-\d{2,}\.md$")


def unfinished(tasks: dict) -> list[dict]:
    return [t for t in tasks.values() if t["status"] not in deps.DONE and t["status"] != "RELEASED"]


def needs_sprint(tasks: dict) -> bool:
    return len(unfinished(tasks)) > SMALL_MAX


def load_sprints(root: pathlib.Path | None = None) -> list[dict]:
    base = (root or ROOT) / "sprints"
    if not base.is_dir():
        return []
    out = []
    for path in sorted(base.glob("SPRINT-*.md")):
        if not SPRINT_FILE.match(path.name):
            continue
        fm = frontmatter(path.read_text())
        out.append({"id": fm.get("id") or path.stem, "status": fm.get("status", ""), "path": str(path)})
    return out


def active_sprint(sprints: list[dict] | None = None) -> dict | None:
    for s in sprints if sprints is not None else load_sprints():
        if s.get("status") == "ACTIVE":
            return s
    return None


def next_sprint_id(sprints: list[dict] | None = None) -> str:
    n = 0
    for s in sprints if sprints is not None else load_sprints():
        try:
            n = max(n, int(s["id"].split("-")[1]))
        except (IndexError, ValueError):
            pass
    return f"SPRINT-{n + 1:02d}"


def propose_scope(tasks: dict, cap: int = SPRINT_CAP) -> list[str]:
    """First dependency layer (deps MERGED-or-later or empty), cap by priority then id."""
    pool = [
        t
        for t in tasks.values()
        if t["status"] in {"BACKLOG", "READY"} and not (t.get("sprint") or "").strip()
    ]
    layer = [t for t in pool if deps.deps_ready(tasks, t["id"])]
    layer.sort(key=lambda t: ({"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(t.get("priority", ""), 9), t["id"]))
    return [t["id"] for t in layer[:cap]]


def sprint_done(tasks: dict, sprint_id: str) -> bool:
    scoped = [t for t in tasks.values() if (t.get("sprint") or "") == sprint_id]
    return bool(scoped) and all(t["status"] in deps.DONE or t["status"] == "RELEASED" for t in scoped)


def evaluate(tasks: dict, sprints: list[dict] | None = None) -> dict:
    sprints = sprints if sprints is not None else load_sprints()
    active = active_sprint(sprints)
    inflight = [t["id"] for t in tasks.values() if t["status"] in IN_FLIGHT]
    leftover = unfinished(tasks)
    needed = needs_sprint(tasks)
    proposed = propose_scope(tasks)
    if active and sprint_done(tasks, active["id"]) and leftover and not inflight:
        more = len(leftover) > SMALL_MAX
        return {
            "needed": more,
            "active": active["id"],
            "action": "close_and_plan" if more else "close",
            "proposed": proposed,
            "inflight": inflight,
            "why": f"{active['id']} scope done; {len(leftover)} tasks left",
        }
    if needed and not active and not inflight:
        return {
            "needed": True,
            "active": "",
            "action": "plan",
            "proposed": proposed,
            "inflight": inflight,
            "why": f"{len(leftover)} unfinished > {SMALL_MAX}; plan a sprint before pulling BACKLOG",
        }
    return {
        "needed": needed,
        "active": (active or {}).get("id", ""),
        "action": None,
        "proposed": proposed,
        "inflight": inflight,
        "why": "sprint ok" if active else "small work, no sprint",
    }


def in_run_scope(task: dict, ev: dict) -> bool:
    """BACKLOG/READY only if no active sprint or task.sprint matches. In-flight always allowed."""
    if task.get("status") in IN_FLIGHT:
        return True
    active = ev.get("active") or ""
    if not active:
        return not ev.get("needed")
    return (task.get("sprint") or "") == active


def main(argv: list[str]) -> int:
    req_id = None
    cmd = "status"
    for a in argv:
        if a.startswith("REQ-"):
            req_id = a
        elif a in {"plan", "status"}:
            cmd = a
    tasks = deps.load_tasks()
    if req_id:
        tasks = {k: v for k, v in tasks.items() if v.get("parent") == req_id}
    ev = evaluate(tasks)
    if cmd == "plan":
        print(" ".join(ev["proposed"]) or "(none)")
        return 0
    print(f"Needed:  {ev['needed']}")
    print(f"Active:  {ev['active'] or '—'}")
    print(f"Action:  {ev['action'] or 'none'}")
    print(f"Proposed:{' ' + ' '.join(ev['proposed']) if ev['proposed'] else ' —'}")
    print(f"Why:     {ev['why']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
