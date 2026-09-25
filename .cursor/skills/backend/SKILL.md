---
name: backend
description: Backend developer for Java 21 Spring services. Implements a BE task on a feature branch from the SA design (SA chooses DB/security/etc.), verifies, hands off to SA. Use when invoked as /backend, e.g. "/backend TASK-003".
disable-model-invocation: true
---

# Backend (BE)

Role: `BE`. `AGENTS.md` + `.cursor/rules/workflow.mdc`.

**Reads:** task, SA design §5–§7 (stack + API + data), `docs/standards/backend.md`, `project.md`, relevant service files + tests, `depends_on` frontmatter.

**Writes:** one `product/services/<name>-service` on the task branch; Implementation + frontmatter + History + board.

**Transitions:** READY / CHANGES_REQUESTED / BUG → IN_PROGRESS → CODE_REVIEW | FAILED. Never merge; never edit `product/frontend/`. Do not check task AC boxes (TEST only).

**Transition discipline:** workflow §5. Role + guard + §8 evidence. Never `--no-verify`. `NEEDS_INPUT` is an outcome, not a status.

### FAILED recovery

`FAILED` is recovery, not a restart. Read `failed_from`, fix the tooling/env/process issue, then
`FAILED → failed_from` via the protocol. Do not force `FAILED → IN_PROGRESS` unless `failed_from`
is `IN_PROGRESS`. Product defects are `BUG`, not `FAILED`.

## `/backend TASK-###`

1. **Check.** Assignee `BE`. Deps MERGED-or-later. Missing service repo → wait if a DEVOPS
   bootstrap for it is READY or IN_PROGRESS; otherwise fallback `/repo create <name>-service be`
   only for a component named in the approved design. Dirty tree → `NEEDS_INPUT`.
2. **Branch.** READY → `feature/TASK-###-<slug>` from `main`. Loops reuse `branch`. BUG → `fix/TASK-###-<slug>`.
   FAILED → keep the existing `branch` and return to `failed_from`.
3. **Start.** IN_PROGRESS if `failed_from` is `IN_PROGRESS` or the task is READY / CHANGES_REQUESTED / BUG.
4. **Implement.** Smallest change for AC + design. Package-by-feature (`docs/standards/backend.md`). New service → design’s starters, not a hardcoded kit. Tests ≥1/AC. API/data/architecture gap → `BLOCKED` for SA. CORS (if browser): both `localhost` and `127.0.0.1`.
5. **Verify.** `./mvnw -q verify`. 3 fails → FAILED (`failed_from: IN_PROGRESS`).
6. **Commit / push** `scripts/repo.py push <name>-service --branch <branch>`; checkout `main`.
7. **Handoff.** Iteration; IN_PROGRESS → CODE_REVIEW. Next: `/sa review`.

```markdown
### Iteration N (…)
- Branch: `feature/TASK-###-slug` @ <sha>
- Changed: `…/<feature>/api/…`
- Tests: `./mvnw -q verify` → pass (<n>)
- Notes: …
```
