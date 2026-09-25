#!/usr/bin/env python3
"""Unit tests for check_transitions.check and deps (no git required)."""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_transitions as ct  # noqa: E402
import deps  # noqa: E402


def task(
    status="BACKLOG",
    assignee="BE",
    depends="[]",
    merge="",
    review="",
    impl="",
    test="",
    ac="- [ ] AC-001 example\n",
    extra="",
    hid="TASK-001",
    history=None,
):
    hist = history or [
        "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
    ]
    return f"""---
id: {hid}
title: t
type: TASK
priority: MEDIUM
status: {status}
assignee: {assignee}
parent: REQ-001
depends_on: {depends}
branch: feature/TASK-001-t
merge_commit: {merge}
review_iteration: 0
test_iteration: 0
blocked_from:
failed_from:
failure:
{extra}updated: 2026-01-01 00:00
---

## Description
x

## Acceptance Criteria
{ac}
## Design (SA)
See design.

## Implementation (BE/FE)
{impl}
## Review (SA)
{review}
## Test (TEST)
{test}
## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
""" + "\n".join(hist) + "\n"


class CheckTests(unittest.TestCase):
    def test_new_must_be_backlog(self):
        errors = ct.check("tasks/TASK-001-x.md", None, task(status="READY"), {})
        self.assertTrue(any("BACKLOG" in e for e in errors))

    def test_forbidden_transition(self):
        old = task(status="BACKLOG")
        new = task(
            status="MERGED",
            merge="abc1234",
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 01:00 | BACKLOG | MERGED | SA | nope |",
            ],
        )
        errors = ct.check("tasks/TASK-001-x.md", old, new, {"TASK-001": "MERGED"})
        self.assertTrue(any("not allowed" in e for e in errors))

    def test_ready_blocked_by_deps(self):
        old = task(status="BACKLOG", depends="[TASK-002]")
        new = task(
            status="READY",
            depends="[TASK-002]",
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 01:00 | BACKLOG | READY | SCRUM | DoR met |",
            ],
        )
        errors = ct.check(
            "tasks/TASK-001-x.md",
            old,
            new,
            {"TASK-001": "READY", "TASK-002": "IN_PROGRESS"},
        )
        self.assertTrue(any("depends_on" in e for e in errors))

    def test_ready_when_dep_merged(self):
        old = task(status="BACKLOG", depends="[TASK-002]")
        new = task(
            status="READY",
            depends="[TASK-002]",
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 01:00 | BACKLOG | READY | SCRUM | DoR met |",
            ],
        )
        errors = ct.check(
            "tasks/TASK-001-x.md",
            old,
            new,
            {"TASK-001": "READY", "TASK-002": "MERGED"},
        )
        self.assertEqual(errors, [])

    def test_merged_needs_sha_and_approval(self):
        old = task(status="CODE_REVIEW")
        new = task(
            status="MERGED",
            merge="not-a-sha",
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 02:00 | CODE_REVIEW | MERGED | SA | merged |",
            ],
        )
        errors = ct.check("tasks/TASK-001-x.md", old, new, {"TASK-001": "MERGED"})
        self.assertTrue(any("merge_commit" in e for e in errors))
        self.assertTrue(any("APPROVED" in e for e in errors))

    def test_failed_requires_fields(self):
        old = task(status="IN_PROGRESS")
        new = task(
            status="FAILED",
            extra=(
                "failed_from: IN_PROGRESS\n"
                "failure_type: build\n"
                "failure_step: verify\n"
                "failure_message: mvn down\n"
                "failure_retry: 1\n"
                "failure_recoverable: true\n"
            ),
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 03:00 | IN_PROGRESS | FAILED | BE | mvn verify failed |",
            ],
        )
        errors = ct.check("tasks/TASK-001-x.md", old, new, {"TASK-001": "FAILED"})
        self.assertEqual(errors, [])

    def test_empty_history_note_rejected(self):
        old = task(status="BACKLOG")
        new = task(
            status="READY",
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 01:00 | BACKLOG | READY | SCRUM | — |",
            ],
        )
        errors = ct.check("tasks/TASK-001-x.md", old, new, {"TASK-001": "READY"})
        self.assertTrue(any("Note" in e for e in errors))


class DepsTests(unittest.TestCase):
    def test_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "tasks").mkdir()
            (root / "tasks" / "TASK-001-a.md").write_text(
                "---\nid: TASK-001\nstatus: BACKLOG\ndepends_on: [TASK-002]\n---\n"
            )
            (root / "tasks" / "TASK-002-b.md").write_text(
                "---\nid: TASK-002\nstatus: BACKLOG\ndepends_on: [TASK-001]\n---\n"
            )
            tasks = deps.load_tasks(root)
            self.assertTrue(deps.cycles(tasks))

    def test_actionable(self):
        tasks = {
            "TASK-001": {"id": "TASK-001", "status": "MERGED", "depends_on": [], "assignee": "BE", "priority": "", "parent": "", "path": "", "human_gate": "", "requirement_revision": ""},
            "TASK-002": {"id": "TASK-002", "status": "BACKLOG", "depends_on": ["TASK-001"], "assignee": "FE", "priority": "", "parent": "", "path": "", "human_gate": "", "requirement_revision": ""},
            "TASK-003": {"id": "TASK-003", "status": "BACKLOG", "depends_on": ["TASK-004"], "assignee": "FE", "priority": "", "parent": "", "path": "", "human_gate": "", "requirement_revision": ""},
        }
        ids = {t["id"] for t in deps.actionable(tasks)}
        self.assertIn("TASK-001", ids)
        self.assertIn("TASK-002", ids)
        self.assertNotIn("TASK-003", ids)


class GateAndReqTests(unittest.TestCase):
    def test_gate_scan_auth(self):
        import gate_scan
        self.assertIn("auth", gate_scan.scan("Add authentication and /login"))
        self.assertEqual(gate_scan.scan("plain list page"), [])

    def test_content_hash_stable(self):
        import req
        text = "---\nid: REQ-001\n---\n\n## Goal\nHello\n"
        self.assertEqual(req.content_hash(text), req.content_hash(text))
        self.assertNotEqual(req.content_hash(text), req.content_hash(text + "x"))

    def test_req_released_blocked(self):
        import req
        req_text = """---
id: REQ-001
status: RELEASED
revision: 1
content_hash: x
tasks: [TASK-001]
---

body
"""
        # hash will fail + TASK-001 missing/not RELEASED
        errors = req.check_one("requirements/REQ-001-x.md", req_text, None, {"TASK-001": {"status": "BACKLOG", "parent": "REQ-001", "requirement_revision": "1"}})
        self.assertTrue(any("RELEASED" in e for e in errors))

    def test_req_ready_for_release_allows_uxui_merged(self):
        import req
        req_text = """---
id: REQ-001
status: READY_FOR_RELEASE
revision: 1
content_hash: PLACEHOLDER
tasks: [TASK-001, TASK-002]
---

body
"""
        req_text = req_text.replace("PLACEHOLDER", req.content_hash(req_text))
        tasks = {
            "TASK-001": {"status": "MERGED", "work_type": "UX_UI", "assignee": "UX/UI", "parent": "REQ-001"},
            "TASK-002": {"status": "READY_FOR_DEPLOY", "work_type": "BACKEND", "assignee": "BE", "parent": "REQ-001"},
        }
        self.assertEqual(req.check_one("requirements/REQ-001-x.md", req_text, None, tasks), [])

    def test_uxui_cannot_request_code_review_changes(self):
        old = task(status="CODE_REVIEW")
        new = task(
            status="CHANGES_REQUESTED",
            extra="work_type: UX_UI\nuxui_review_iteration: 1\n",
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 02:00 | CODE_REVIEW | CHANGES_REQUESTED | UX/UI | density |",
            ],
        )
        errors = ct.check("tasks/TASK-001-x.md", old, new, {"TASK-001": "CHANGES_REQUESTED"})
        self.assertTrue(any("not allowed" in e for e in errors))

    def test_next_idle_empty(self):
        import next as nxt
        step = nxt.next_step("REQ-999")
        self.assertEqual(step.get("stop"), "idle")

    def test_command_for_roles(self):
        import next as nxt
        self.assertEqual(nxt.command_for({"id": "TASK-002", "assignee": "UX/UI"}), ("UX/UI", "/uxui TASK-002"))
        self.assertEqual(nxt.command_for({"id": "TASK-004", "assignee": "FE"}), ("FE", "/frontend TASK-004"))
        self.assertEqual(nxt.command_for({"id": "TASK-003", "assignee": "BE"}), ("BE", "/backend TASK-003"))
        self.assertEqual(nxt.command_for({"id": "TASK-012", "assignee": "DEVOPS"}), ("DEVOPS", "/devops TASK-012"))

    def test_uxui_review_gate(self):
        import next as nxt
        self.assertTrue(nxt.needs_uxui_review({"status": "CODE_REVIEW", "work_type": "FRONTEND", "uxui_review": ""}))
        self.assertFalse(nxt.needs_uxui_review({
            "status": "CODE_REVIEW", "work_type": "FRONTEND",
            "uxui_review": "docs/design/ux/reviews/TASK-004-review-01.md",
        }))
        self.assertFalse(nxt.needs_uxui_review({
            "status": "CODE_REVIEW", "assignee": "UX/UI", "work_type": "UX_UI",
        }))
        self.assertFalse(nxt.needs_uxui_review({
            "status": "CODE_REVIEW", "assignee": "FE", "requires_uxui": "false",
        }))
        self.assertTrue(nxt.skip_test({"work_type": "UX_UI", "status": "MERGED", "assignee": "UX/UI"}))
        self.assertTrue(nxt.skip_test({"work_type": "DEVOPS", "status": "MERGED", "assignee": "DEVOPS"}))
        self.assertFalse(nxt.skip_test({"work_type": "BACKEND", "status": "MERGED"}))
        self.assertTrue(nxt.child_done_for_accept({"work_type": "DEVOPS", "status": "MERGED"}))
        self.assertTrue(nxt.needs_pqa_visual_review({
            "status": "CODE_REVIEW", "work_type": "FRONTEND", "uxui_review": "",
        }))

    def test_pqa_plan_and_accept_gates(self):
        import next as nxt
        from unittest.mock import patch
        self.assertTrue(nxt.needs_sa_analyze({"status": "APPROVED"}, "REQ-999"))
        self.assertFalse(nxt.needs_pqa_plan({"status": "ANALYZING", "pqa_plan": ""}, "REQ-999"))
        with patch.object(nxt, "design_exists", return_value=True):
            self.assertTrue(nxt.needs_pqa_plan({"status": "ANALYZING", "pqa_plan": ""}, "REQ-000"))
        self.assertFalse(nxt.req_analyzed({"status": "ANALYZING"}))
        self.assertTrue(nxt.req_analyzed({"status": "ANALYZED"}))
        tasks = {
            "TASK-001": {"id": "TASK-001", "status": "MERGED", "work_type": "UX_UI", "assignee": "UX/UI"},
            "TASK-002": {"id": "TASK-002", "status": "READY_FOR_DEPLOY", "work_type": "BACKEND"},
        }
        self.assertTrue(nxt.needs_pqa_accept({"status": "ANALYZED", "pqa_accept": ""}, tasks))
        self.assertFalse(nxt.needs_pqa_accept({"status": "ANALYZING", "pqa_accept": ""}, tasks))

    def test_sprint_policy(self):
        import sprint as sp

        small = {
            f"TASK-00{i}": {
                "id": f"TASK-00{i}",
                "status": "BACKLOG",
                "depends_on": [],
                "priority": "HIGH",
                "sprint": "",
            }
            for i in range(1, 4)
        }
        self.assertFalse(sp.needs_sprint(small))
        self.assertEqual(sp.evaluate(small, [])["action"], None)

        big = {
            f"TASK-{i:03d}": {
                "id": f"TASK-{i:03d}",
                "status": "BACKLOG",
                "depends_on": [] if i <= 2 else [f"TASK-{i-1:03d}"],
                "priority": "HIGH",
                "sprint": "",
            }
            for i in range(1, 8)
        }
        ev = sp.evaluate(big, [])
        self.assertTrue(ev["needed"])
        self.assertEqual(ev["action"], "plan")
        self.assertEqual(ev["proposed"], ["TASK-001", "TASK-002"])

        inflight = dict(big)
        inflight["TASK-001"] = {**big["TASK-001"], "status": "IN_PROGRESS"}
        self.assertIsNone(sp.evaluate(inflight, [])["action"])

        active = [{"id": "SPRINT-01", "status": "ACTIVE"}]
        scoped = {
            "TASK-001": {"id": "TASK-001", "status": "MERGED", "depends_on": [], "priority": "HIGH", "sprint": "SPRINT-01"},
            "TASK-002": {"id": "TASK-002", "status": "BACKLOG", "depends_on": [], "priority": "HIGH", "sprint": ""},
            "TASK-003": {"id": "TASK-003", "status": "BACKLOG", "depends_on": [], "priority": "HIGH", "sprint": ""},
            "TASK-004": {"id": "TASK-004", "status": "BACKLOG", "depends_on": [], "priority": "HIGH", "sprint": ""},
            "TASK-005": {"id": "TASK-005", "status": "BACKLOG", "depends_on": [], "priority": "HIGH", "sprint": ""},
            "TASK-006": {"id": "TASK-006", "status": "BACKLOG", "depends_on": [], "priority": "HIGH", "sprint": ""},
        }
        ev2 = sp.evaluate(scoped, active)
        self.assertEqual(ev2["action"], "close")
        big_left = dict(scoped)
        big_left["TASK-007"] = {"id": "TASK-007", "status": "BACKLOG", "depends_on": [], "priority": "HIGH", "sprint": ""}
        self.assertEqual(sp.evaluate(big_left, active)["action"], "close_and_plan")
        self.assertTrue(sp.in_run_scope({"status": "IN_PROGRESS", "sprint": ""}, ev2))
        self.assertFalse(sp.in_run_scope({"status": "BACKLOG", "sprint": ""}, {"needed": True, "active": "SPRINT-01"}))
        self.assertTrue(sp.in_run_scope({"status": "BACKLOG", "sprint": "SPRINT-01"}, {"needed": True, "active": "SPRINT-01"}))

    def test_merged_ui_needs_uxui_review(self):
        old = task(status="CODE_REVIEW")
        new = task(
            status="MERGED",
            merge="abc1234",
            extra="requires_uxui: true\nuxui_review:\n",
            review="### Round 1 — APPROVED\nNo comments.\n",
            history=[
                "| 2026-01-01 00:00 | — | BACKLOG | SA | Created |",
                "| 2026-01-01 02:00 | CODE_REVIEW | MERGED | SA | merged abc1234 |",
            ],
        )
        errors = ct.check("tasks/TASK-001-x.md", old, new, {"TASK-001": "MERGED"})
        self.assertTrue(any("PQA visual review" in e or "UX/UI review" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
