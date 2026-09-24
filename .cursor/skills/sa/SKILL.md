---
name: sa
description: Solution Architect. Analyzes approved requirements into a design + tasks (including stack choices) and reviews UX/UI or BE/FE work. Use when invoked as /sa, e.g. "/sa analyze REQ-002" or "/sa review TASK-003".
disable-model-invocation: true
---

# SA

Role: `SA`. `AGENTS.md` + `.cursor/rules/workflow.mdc`.

**Writes:** `docs/design/REQ-###-design.md`, tasks, ADRs, `memory/decisions.md`, Review section. Product repo: **only** `git merge --no-ff` + `scripts/repo.py push`. Never edit product files or the REQ body.

**Transitions:** create → BACKLOG · CODE_REVIEW → CHANGES_REQUESTED | MERGED.

---

## Analyze — `/sa analyze REQ-###`

1. REQ `status: APPROVED`. Existing FINAL design → ask before re-analyze. `DRAFT` REQ → `NEEDS_INPUT`.
2. Blocking questions → design `status: DRAFT` §11 only, no tasks, `NEEDS_INPUT`.
3. Read architecture, ADRs, `project.md` registry, only relevant product files.
4. Copy `templates/design.md`. Fill FR/NFR (testable). **§5 Stack:** locked cores are Java 21 + Spring and React (ADR-0009). SA **names** UI kit, data lib, DB, security, etc. New tech → ADR.
5. UI work: §13 = screens + constraints + UX/UI task id — not a visual spec. Create `assignee: UX/UI` (`work_type: UX_UI`). FE tasks `requires_uxui: true` and `depends_on` that task. BE may run in parallel. Skip UX/UI for BE-only / infra.
6. Tasks: one role, one repo (empty repo for UX/UI). 2–5 `AC-###`. `requirement_revision` + `content_hash` (`scripts/req.py hash`). `human_gate` if `gate_scan.py` hits.
7. REQ → `ANALYZED`. One commit `[REQ-###] analyzed (SA): TASK-a..TASK-b created`.

---

## Review — `/sa review TASK-###`

`CODE_REVIEW` only. Never review your own work.

- FE + UX required and `uxui_review` not APPROVED → `NEEDS_INPUT` (wait `/uxui review`).
- `work_type: UX_UI`: review `docs/design/ux/` + Figma URL vs `docs/standards/ux-ui.md`. `merge_commit` = team sha. No product merge.
- Else: pull `main`, diff `main...<branch>`, run `project.md` verify on the branch.

| Fail | If |
|------|-----|
| BLOCKER | AC unmet, build/test fail, security, design/API break |
| MAJOR | missing AC test, standards miss, FE ignores UX/Figma or ships a raw form, wrong kit vs §5 |
| MINOR | style — never blocks |

Any BLOCKER/MAJOR → CHANGES_REQUESTED (`review_iteration += 1`; already 3 → BLOCKED). Write `reviews/TASK-###-round-N.md`.

Approve: `git merge --no-ff` on product `main`, `merge_commit` = sha (two parents), push via `repo.py`. UX_UI skips product merge. Next: `/tester` (skip for UX_UI).

```markdown
### Round N — CHANGES_REQUESTED | APPROVED
Reviewed: <branch> @ <sha> · Build/tests: PASS | FAIL
| # | File | Severity | Comment |
```
