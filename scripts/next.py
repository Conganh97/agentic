#!/usr/bin/env python3
"""Deterministic next step from disk (resume-safe). Used by /scrum next and /scrum run.

Usage: python3 scripts/next.py [REQ-###]
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deps  # noqa: E402
from req import frontmatter  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DONE = deps.DONE
PRIORITY = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def load_req(req_id: str | None) -> dict | None:
    if not req_id:
        return None
    for path in (ROOT / "requirements").glob(f"{req_id}-*.md"):
        return {"path": str(path), **frontmatter(path.read_text())}
    return None


def design_exists(req_id: str) -> bool:
    return (ROOT / "docs" / "design" / f"{req_id}-design.md").exists()


def rank(task: dict) -> tuple:
    return (PRIORITY.get(task.get("priority", ""), 9), task["id"])


def next_step(req_id: str | None = None) -> dict:
    tasks = deps.load_tasks()
    if req_id:
        tasks = {k: v for k, v in tasks.items() if v.get("parent") == req_id}
    req = load_req(req_id) if req_id else None

    if req and req.get("status") == "DRAFT":
        return {"stop": "NEEDS_INPUT", "why": f"human must approve {req_id}"}
    if req and req.get("status") in {"APPROVED", "ANALYZING"} and not design_exists(req_id or ""):
        return {"next": req_id, "role": "SA", "run": f"/sa analyze {req_id}", "why": "no design yet"}

    if req:
        rev = req.get("revision", "")
        for t in tasks.values():
            tr = t.get("requirement_revision", "")
            if tr and rev and tr != rev:
                return {
                    "stop": "BLOCKED",
                    "task": t["id"],
                    "why": "requirement_changed",
                }

    ordered = sorted(tasks.values(), key=rank)

    def first(pred):
        for t in ordered:
            if pred(t):
                return t
        return None

    t = first(lambda x: x["status"] == "CODE_REVIEW")
    if t:
        return {"next": t["id"], "role": "SA", "run": f"/sa review {t['id']}", "why": "CODE_REVIEW"}
    t = first(lambda x: x["status"] in {"MERGED", "TESTING"})
    if t:
        return {"next": t["id"], "role": "TEST", "run": f"/tester {t['id']}", "why": t["status"]}
    t = first(lambda x: x["status"] in {"CHANGES_REQUESTED", "BUG", "IN_PROGRESS", "FAILED"})
    if t:
        skill = "/frontend" if t.get("assignee") == "FE" else "/backend"
        if t["status"] == "FAILED" and t.get("failed_from") == "TESTING":
            skill = "/tester"
        return {"next": t["id"], "role": t.get("assignee") or "BE", "run": f"{skill} {t['id']}", "why": t["status"]}
    t = first(
        lambda x: x["status"] == "READY"
        and deps.deps_ready(tasks, x["id"])
        and not (x.get("human_gate") and not x.get("approved_by"))
    )
    if t:
        skill = "/frontend" if t.get("assignee") == "FE" else "/backend"
        return {"next": t["id"], "role": t.get("assignee") or "BE", "run": f"{skill} {t['id']}", "why": "READY, deps met"}
    t = first(lambda x: x["status"] == "BACKLOG" and deps.deps_ready(tasks, x["id"]))
    if t:
        return {"next": t["id"], "role": "SCRUM", "run": f"/scrum ready {t['id']}", "why": "DoR + deps"}
    t = first(lambda x: x["status"] in {"READY_FOR_DEPLOY", "DEPLOYING"})
    if t:
        return {"next": t["id"], "role": "DEVOPS", "run": f"/devops deploy {t['id']} DEV", "why": "waiting DevOps/human"}
    return {"stop": "idle", "why": "nothing actionable"}


def main(argv: list[str]) -> int:
    step = next_step(argv[0] if argv else None)
    if step.get("stop"):
        print(f"Stop: {step['stop']}")
        print(f"Why:  {step['why']}")
        return 0
    print(f"Next: {step['next']} → {step['role']}")
    print(f"Run:  {step['run']}")
    print(f"Why:  {step['why']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
