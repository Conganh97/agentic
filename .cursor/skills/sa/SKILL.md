---
name: sa
description: Solution Architect. Analyzes requirements into a design + tasks and reviews BE/FE code only. Product QA owns UX sign-off and the ANALYZED plan gate. Use when invoked as /sa, e.g. "/sa analyze REQ-002" or "/sa review TASK-003".
disable-model-invocation: true
---

# SA

Role: `SA`. **Writes:** design, tasks, ADRs, `memory/decisions.md`, code Review section.
Product repo: **only** `git merge --no-ff` + `scripts/repo.py push` after **code** APPROVED.
Never edit product files or the REQ body. Never merge `work_type: UX_UI` (PQA does). Never visual-approve FE.

**Transitions:** create → BACKLOG · CODE_REVIEW → CHANGES_REQUESTED | MERGED (code tasks only).

---

## Analyze — `/sa analyze REQ-###`

1. REQ `APPROVED` or `ANALYZING`. `DRAFT` → `NEEDS_INPUT`. Existing `ANALYZED` + FINAL → ask before re-analyze.
2. Blocking questions → design `DRAFT` §11 only, no new tasks, `NEEDS_INPUT`.
3. Read architecture, ADRs, `project.md`, only relevant product files.
4. Copy `templates/design.md`. Testable FR/NFR. **§5 Stack:** Java 21 + Spring, React locked (ADR-0009);
   you name kit/DB/etc. New tech → ADR.
5. UI: §13 = screens + **density constraints** + UX/UI task id — not a visual spec. Create
   `assignee: UX/UI` (`work_type: UX_UI`). FE `requires_uxui: true` and `depends_on` that task.
6. Tasks: one role, one repo. 2–5 `AC-###`. `requirement_revision` + `content_hash`. `gate_scan.py`.
7. Design stays **`DRAFT`**. REQ → **`ANALYZING`** (not `ANALYZED`). One commit
   `[REQ-###] analyzing (SA): TASK-a..TASK-b drafted`. Next: **`/pqa plan REQ-###`**.
8. If PQA plan is `CHANGES_REQUESTED`: revise design/tasks, stay `ANALYZING`, same commit style.
9. After PQA **accept FAIL**: add/adjust tasks only; do not wipe the design. Agree the fix list in
   `docs/design/reviews/REQ-###-accept-N.md`.

PQA sets `ANALYZED` + design `FINAL` when the plan is APPROVED. Do not skip that hop.

---

## Review — `/sa review TASK-###`

`CODE_REVIEW` only. Never review your own work. **Code and contract-vs-API only.**

- `work_type: UX_UI` → `NEEDS_INPUT` (wait `/pqa review`).
- FE + UX required and `uxui_review` empty → `NEEDS_INPUT` (wait `/pqa review`).
- Else: `git diff main...<branch>`, `project.md` verify on the branch.

| Fail | If |
|------|-----|
| BLOCKER | AC unmet, build/test fail, security, design/API break |
| MAJOR | missing AC test, standards miss, wrong kit vs §5, FE ignores the **written** UX contract |
| MINOR | style — never blocks. Visual density is PQA, not you |

BLOCKER/MAJOR → CHANGES_REQUESTED (`review_iteration += 1`; already 3 → BLOCKED).
`reviews/TASK-###-round-N.md`. Approve: `--no-ff` merge, `merge_commit` two parents, `repo.py` push.
Next: `/tester`.

```markdown
### Round N — CHANGES_REQUESTED | APPROVED
Reviewed: <branch> @ <sha> · Build/tests: PASS | FAIL
| # | File | Severity | Comment |
```
