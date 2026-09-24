#!/usr/bin/env python3
"""Deterministic next step from disk (resume-safe). Used by /scrum next and /scrum run.

Usage: python3 scripts/next.py [REQ-###]
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deps  # noqa: E402
import sprint  # noqa: E402
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


ANALYZED_OR_LATER = {
    "ANALYZED",
    "IN_PROGRESS",
    "TESTING",
    "READY_FOR_RELEASE",
    "RELEASED",
}
DONE_FOR_ACCEPT = {"READY_FOR_DEPLOY", "DEPLOYING", "RELEASED"}


def design_exists(req_id: str) -> bool:
    return (ROOT / "docs" / "design" / f"{req_id}-design.md").exists()


def artifact_status(rel: str) -> str:
    if not (rel or "").strip():
        return ""
    path = ROOT / rel.strip()
    if not path.is_file():
        return ""
    fields = frontmatter(path.read_text())
    return (fields.get("status") or fields.get("decision") or "").strip()


def req_analyzed(req: dict | None) -> bool:
    return bool(req) and req.get("status") in ANALYZED_OR_LATER


def parent_analyzed(task: dict, scoped_req: dict | None) -> bool:
    if scoped_req:
        return req_analyzed(scoped_req)
    parent = (task.get("parent") or "").strip()
    if not parent:
        return True
    return req_analyzed(load_req(parent))


def needs_sa_analyze(req: dict | None, req_id: str) -> bool:
    if not req or req.get("status") not in {"APPROVED", "ANALYZING"}:
        return False
    if not design_exists(req_id):
        return True
    return req.get("status") == "ANALYZING" and artifact_status(req.get("pqa_plan", "")) == "CHANGES_REQUESTED"


def needs_pqa_plan(req: dict | None, req_id: str) -> bool:
    if not req or req.get("status") != "ANALYZING" or not design_exists(req_id):
        return False
    return artifact_status(req.get("pqa_plan", "")) != "APPROVED"


def child_done_for_accept(task: dict) -> bool:
    if is_uxui_work(task):
        return task.get("status") in {"MERGED", *DONE_FOR_ACCEPT}
    return task.get("status") in DONE_FOR_ACCEPT


def needs_pqa_accept(req: dict | None, tasks: dict) -> bool:
    if not req_analyzed(req) or artifact_status(req.get("pqa_accept", "")) == "APPROVED":
        return False
    children = list(tasks.values())
    return bool(children) and all(child_done_for_accept(t) for t in children)


def rank(task: dict) -> tuple:
    return (PRIORITY.get(task.get("priority", ""), 9), task["id"])


def flag_true(value: str) -> bool:
    return (value or "").strip().lower() in {"true", "yes", "1"}


def flag_false(value: str) -> bool:
    return (value or "").strip().lower() in {"false", "no", "0"}


def is_uxui_work(task: dict) -> bool:
    return (task.get("work_type") or "").strip() == "UX_UI" or task.get("assignee") == "UX/UI"


def uxui_required(task: dict) -> bool:
    if flag_false(task.get("requires_uxui")):
        return False
    if flag_true(task.get("requires_uxui")):
        return True
    return (task.get("work_type") or "").strip() == "FRONTEND"


def needs_pqa_visual_review(task: dict) -> bool:
    """FE CODE_REVIEW waiting PQA (replaces designer self-review)."""
    if task.get("status") != "CODE_REVIEW" or is_uxui_work(task):
        return False
    if not uxui_required(task):
        return False
    return not (task.get("uxui_review") or "").strip()


def needs_uxui_review(task: dict) -> bool:
    """Alias kept for older tests; gate is PQA."""
    return needs_pqa_visual_review(task)


def skip_test(task: dict) -> bool:
    """UX/UI design tasks are done at MERGED; do not dispatch TEST."""
    return is_uxui_work(task) and task.get("status") == "MERGED"


def command_for(task: dict) -> tuple[str, str]:
    """Return (role, /skill TASK-id) for implement / resume steps."""
    assignee = (task.get("assignee") or "").strip()
    tid = task["id"]
    mapping = {
        "FE": ("FE", f"/frontend {tid}"),
        "UX/UI": ("UX/UI", f"/uxui {tid}"),
        "DEVOPS": ("DEVOPS", f"/devops {tid}"),
        "TEST": ("TEST", f"/tester {tid}"),
        "BE": ("BE", f"/backend {tid}"),
    }
    return mapping.get(assignee, ("BE", f"/backend {tid}"))


def next_step(req_id: str | None = None) -> dict:
    tasks = deps.load_tasks()
    if req_id:
        tasks = {k: v for k, v in tasks.items() if v.get("parent") == req_id}
    req = load_req(req_id) if req_id else None

    if req and req.get("status") == "DRAFT":
        return {"stop": "NEEDS_INPUT", "why": f"human must approve {req_id}"}
    if req and needs_sa_analyze(req, req_id or ""):
        why = "no design yet" if not design_exists(req_id or "") else "PQA plan CHANGES_REQUESTED"
        return {"next": req_id, "role": "SA", "run": f"/sa analyze {req_id}", "why": why}
    if req and needs_pqa_plan(req, req_id or ""):
        return {"next": req_id, "role": "PQA", "run": f"/pqa plan {req_id}", "why": "ANALYZING, plan not APPROVED"}

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
    ev = sprint.evaluate(tasks)

    def first(pred):
        for t in ordered:
            if pred(t):
                return t
        return None

    if ev.get("action") in {"plan", "close", "close_and_plan"}:
        return {
            "next": ev.get("active") or "sprint",
            "role": "SCRUM",
            "run": "/scrum sprint" if ev["action"] != "close" else "/scrum sprint close",
            "why": ev["why"],
        }

    t = first(lambda x: x["status"] == "CODE_REVIEW" and is_uxui_work(x))
    if t:
        return {
            "next": t["id"],
            "role": "PQA",
            "run": f"/pqa review {t['id']}",
            "why": "CODE_REVIEW UX_UI waiting PQA",
        }
    t = first(needs_pqa_visual_review)
    if t:
        return {
            "next": t["id"],
            "role": "PQA",
            "run": f"/pqa review {t['id']}",
            "why": "CODE_REVIEW waiting PQA visual review",
        }
    t = first(lambda x: x["status"] == "CODE_REVIEW")
    if t:
        return {"next": t["id"], "role": "SA", "run": f"/sa review {t['id']}", "why": "CODE_REVIEW"}
    t = first(lambda x: x["status"] in {"MERGED", "TESTING"} and not skip_test(x))
    if t:
        return {"next": t["id"], "role": "TEST", "run": f"/tester {t['id']}", "why": t["status"]}
    t = first(lambda x: x["status"] in {"CHANGES_REQUESTED", "BUG", "IN_PROGRESS", "FAILED"})
    if t:
        role, skill = command_for(t)
        if t["status"] == "FAILED" and t.get("failed_from") == "TESTING":
            role, skill = "TEST", f"/tester {t['id']}"
        return {"next": t["id"], "role": role, "run": skill, "why": t["status"]}
    t = first(
        lambda x: x["status"] == "READY"
        and parent_analyzed(x, req)
        and deps.deps_ready(tasks, x["id"])
        and sprint.in_run_scope(x, ev)
        and not (x.get("human_gate") and not x.get("approved_by"))
    )
    if t:
        role, skill = command_for(t)
        return {"next": t["id"], "role": role, "run": skill, "why": "READY, deps met"}
    t = first(
        lambda x: x["status"] == "BACKLOG"
        and parent_analyzed(x, req)
        and deps.deps_ready(tasks, x["id"])
        and sprint.in_run_scope(x, ev)
    )
    if t:
        return {"next": t["id"], "role": "SCRUM", "run": f"/scrum ready {t['id']}", "why": "DoR + deps"}
    accept_req = req
    accept_id = req.get("id") if req else req_id
    if not accept_req and tasks:
        parents = {t.get("parent") for t in tasks.values() if t.get("parent")}
        if len(parents) == 1:
            accept_id = next(iter(parents))
            accept_req = load_req(accept_id)
    if accept_req and needs_pqa_accept(accept_req, tasks):
        rid = accept_req.get("id") or accept_id
        return {
            "next": rid,
            "role": "PQA",
            "run": f"/pqa accept {rid}",
            "why": "increment complete; PQA accept",
        }
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
