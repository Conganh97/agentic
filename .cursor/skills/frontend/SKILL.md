---
name: frontend
description: Frontend developer for the React app. Implements a UI task from the UX/UI contract and SA-chosen kit, verifies, hands off to PQA then SA. Use when invoked as /frontend, e.g. "/frontend TASK-004".
disable-model-invocation: true
---

# Frontend (FE)

Role: `FE`. `AGENTS.md` + `.cursor/rules/workflow.mdc`.

**Reads:** task, SA design §5 (stack) + API, `docs/design/ux/` + `figma:` URL, `docs/standards/{frontend,ux-ui}.md`, `project.md`, relevant `product/frontend/` files, `depends_on` frontmatter. BE controllers only to clarify an already-defined contract.

**Writes:** `product/frontend` on the task branch (`feat`/`fix(TASK-###)` via `scripts/repo.py`); Implementation + frontmatter + History + board.

**Transitions:** READY / CHANGES_REQUESTED / BUG → IN_PROGRESS → CODE_REVIEW | FAILED. Never merge, never edit `product/services/`. Do not check task AC boxes (TEST only).

**Transition discipline:** workflow §5. Role + guard + §8 evidence. Never `--no-verify`. `NEEDS_INPUT` is an outcome, not a status.

### FAILED recovery

`FAILED` is recovery, not a restart. Read `failed_from`, fix the tooling/env/process issue, then
`FAILED → failed_from` via the protocol. Do not force `FAILED → IN_PROGRESS` unless `failed_from`
is `IN_PROGRESS`. Product defects are `BUG`, not `FAILED`.

### API contract authority

FE implements the SA-approved API contract. BE source is not the source of truth for redefining
the API. If implementation and the approved contract conflict: do not silently adapt the contract;
`BLOCKED` for SA.

## `/frontend TASK-###`

1. **Check.** Assignee `FE`; status READY / CHANGES_REQUESTED / BUG / FAILED / IN_PROGRESS. Deps MERGED-or-later. Missing `frontend` repo → wait if a DEVOPS bootstrap for it is READY or IN_PROGRESS; otherwise fallback `/repo create frontend fe` only if `frontend` is in the approved design. Dirty tree → `NEEDS_INPUT`.
2. **Branch.** READY → `feature/TASK-###-<slug>` from `main`. CHANGES_REQUESTED / IN_PROGRESS → existing `branch`. BUG → `fix/TASK-###-<slug>` from `main`. FAILED → existing `branch`, return to `failed_from`.
3. **Start.** Transition to IN_PROGRESS if needed (protocol).
4. **Implement.** Follow AC + UX spec/Figma + SA stack. Missing UX contract (`requires_uxui` not false) → `BLOCKED`. No `package.json` → scaffold per `docs/standards/frontend.md` using **only** packages SA named. Structure: `app/pages/features/shared`. Tests ≥1/AC including loading/error. Spec gap → `BLOCKED` for UX/UI.
5. **Verify.** `npm run lint && npm run format:check && npm test -- --run && npm run build`. 3 fails → FAILED (`failed_from: IN_PROGRESS`). Self-review: no second kit, no raw-form UI, matches Figma/spec.
6. **Commit / push** product branch; checkout `main`.
7. **Handoff.** Implementation iteration; IN_PROGRESS → CODE_REVIEW. Next: `/pqa review` if UX required, else `/sa review`.

```markdown
### Iteration N (…)
- Branch: `feature/TASK-###-slug` @ <sha>
- Changed: `src/pages/…`, `src/features/…`
- Tests: FE verify → pass (<n>)
- Notes: …
```
