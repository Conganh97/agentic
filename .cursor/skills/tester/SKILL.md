---
name: tester
description: Test agent. Black-box accepts a merged task against its ACs, then READY_FOR_DEPLOY or BUG. Use when invoked as /tester, e.g. "/tester TASK-003".
disable-model-invocation: true
---

# TEST

Role: `TEST`. Workflow + `docs/standards/testing.md`. Never edit `product/`.

**Reads:** task (AC, merge_commit), testing standards, `project.md`, UX/Figma if UI.
**Writes:** `## Test`, AC checkboxes (only you may check/uncheck them), `tests/TASK-###-run-N.md`, `bugs/BUG-###` on FAIL.
**Transitions:** MERGED → TESTING → READY_FOR_DEPLOY | BUG | FAILED. Refuse `work_type: UX_UI` and `DEVOPS`.
**Transition discipline:** workflow §5. Never `--no-verify`. `NEEDS_INPUT` is an outcome, not a status.
`FAILED` recovers to `failed_from` (usually `TESTING`).

## `/tester TASK-###`

1. Status MERGED or TESTING. `merge_commit` ancestor of `main`. Tree clean; checkout `main`.
2. MERGED → TESTING.
3. Run `project.md` verify on touched apps. Start services (one shell; free port; health). Each AC = command + output. UI: spec/Figma, both origins, images load. Stop processes.
4. **PASS** → run file, check all AC, READY_FOR_DEPLOY. Next: PQA accept (when every sibling is done) or DEVOPS.
5. **FAIL** (product) → `test_iteration += 1` (already 3 → BLOCKED), `bugs/BUG-###`, BUG. Next: assignee.
6. Env/tooling → FAILED (`failed_from: TESTING`). Recurring lesson → `memory/lessons.md`.

```markdown
### Run N — PASS | FAIL | INCOMPLETE
- Tested: main @ <sha> (contains <merge_commit>)
- Build/tests: <cmd> PASS | FAIL
- AC-001 pass — <cmd> → …
```
