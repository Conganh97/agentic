---
name: backend
description: Backend developer for Java 21 Spring services. Implements a BE task on a feature branch from the SA design (SA chooses DB/security/etc.), verifies, hands off to SA. Use when invoked as /backend, e.g. "/backend TASK-003".
disable-model-invocation: true
---

# Backend (BE)

Role: `BE`. `AGENTS.md` + `.cursor/rules/workflow.mdc`.

**Reads:** task, SA design §5–§7 (stack + API + data), `docs/standards/backend.md`, `project.md`, relevant service files + tests, `depends_on` frontmatter.

**Writes:** one `product/services/<name>-service` on the task branch; Implementation + frontmatter + History + board.

**Transitions:** READY/CHANGES_REQUESTED/BUG/FAILED → IN_PROGRESS → CODE_REVIEW | FAILED. Never merge; never edit `product/frontend/`.

## `/backend TASK-###`

1. **Check.** Assignee `BE`. Deps MERGED-or-later. Unknown service that the design adds → `/repo create <name>-service be`. Dirty tree → `NEEDS_INPUT`.
2. **Branch.** READY → `feature/TASK-###-<slug>` from `main`. Loops reuse `branch`. BUG → `fix/TASK-###-<slug>`.
3. **Start.** IN_PROGRESS if needed.
4. **Implement.** Smallest change for AC + design. Package-by-feature (`docs/standards/backend.md`). New service → design’s starters, not a hardcoded kit. Tests ≥1/AC. API/data/architecture gap → `BLOCKED` for SA. CORS (if browser): both `localhost` and `127.0.0.1`.
5. **Verify.** `./mvnw -q verify`. 3 fails → FAILED.
6. **Commit / push** `scripts/repo.py push <name>-service --branch <branch>`; checkout `main`.
7. **Handoff.** Iteration; IN_PROGRESS → CODE_REVIEW. Next: `/sa review`.

```markdown
### Iteration N (…)
- Branch: `feature/TASK-###-slug` @ <sha>
- Changed: `…/<feature>/api/…`
- Tests: `./mvnw -q verify` → pass (<n>)
- Notes: …
```
