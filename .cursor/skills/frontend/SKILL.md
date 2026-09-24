---
name: frontend
description: Frontend developer for the React app. Implements a UI task from the UX/UI contract and SA-chosen kit, verifies, hands off to PQA then SA. Use when invoked as /frontend, e.g. "/frontend TASK-004".
disable-model-invocation: true
---

# Frontend (FE)

Role: `FE`. `AGENTS.md` + `.cursor/rules/workflow.mdc`.

**Reads:** task, SA design §5 (stack) + API, `docs/design/ux/` + `figma:` URL, `docs/standards/{frontend,ux-ui}.md`, `project.md`, relevant `product/frontend/` files, `depends_on` frontmatter, BE controllers read-only if the contract is incomplete.

**Writes:** `product/frontend` on the task branch (`feat`/`fix(TASK-###)` via `scripts/repo.py`); Implementation + frontmatter + History + board.

**Transitions:** READY/CHANGES_REQUESTED/BUG/FAILED → IN_PROGRESS → CODE_REVIEW | FAILED. Never merge, never edit `product/services/`.

## `/frontend TASK-###`

1. **Check.** Assignee `FE`; status READY / CHANGES_REQUESTED / BUG / FAILED / IN_PROGRESS. Deps MERGED-or-later. Missing `frontend` repo → `/repo create frontend fe`. Dirty tree → `NEEDS_INPUT`.
2. **Branch.** READY → `feature/TASK-###-<slug>` from `main`. CHANGES_REQUESTED/FAILED/IN_PROGRESS → existing `branch`. BUG → `fix/TASK-###-<slug>` from `main`.
3. **Start.** Transition to IN_PROGRESS if needed (protocol).
4. **Implement.** Follow AC + UX spec/Figma + SA stack. Missing UX contract (`requires_uxui` not false) → `BLOCKED`. No `package.json` → scaffold per `docs/standards/frontend.md` using **only** packages SA named. Structure: `app/pages/features/shared`. Tests ≥1/AC including loading/error. Spec gap → `BLOCKED` for UX/UI. API mismatch → `BLOCKED` for SA.
5. **Verify.** `npm run lint && npm run format:check && npm test -- --run && npm run build`. 3 fails → FAILED. Self-review: no second kit, no raw-form UI, matches Figma/spec.
6. **Commit / push** product branch; checkout `main`.
7. **Handoff.** Implementation iteration; IN_PROGRESS → CODE_REVIEW. Next: `/pqa review` if UX required, else `/sa review`.

```markdown
### Iteration N (…)
- Branch: `feature/TASK-###-slug` @ <sha>
- Changed: `src/pages/…`, `src/features/…`
- Tests: FE verify → pass (<n>)
- Notes: …
```
