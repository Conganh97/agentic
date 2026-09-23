# AGENTS.md — Project-wide Rules

These rules apply to every contributor: humans, Cursor, and the agents built by this project.
The full plan lives in `agentic_engineering_team_cursor_plan.md`. The architecture summary lives in
`docs/architecture/system-overview.md`.

## 1. What this project is

A workflow-driven platform that runs an agentic software engineering team
(Scrum, SA, BE, FE, Test, DevOps agents) from requirement to release.

**The Orchestrator owns state and controls transitions. Agents provide intelligence and execution.**

## 2. Current phase

**Phase 2 — Agent Contract (done).** Next: Phase 3 — SA Agent.
Workflow rules: `docs/architecture/workflow.md`. Agent contract: `docs/architecture/agent-contract.md`.
Build/test: `cd orchestrator && ./mvnw test`.

Update this section whenever a phase starts or finishes.

## 3. Core principles

1. Agent = intelligence
2. Workflow = control
3. Tools = capability
4. Knowledge = context
5. Policy = constraints
6. State = source of truth

## 4. Hard rules (never violate)

- Agents never bypass workflow states and never set task state directly; only the Orchestrator transitions state.
- Agents never merge their own PRs and never approve their own code.
- No production deployment without an explicit human approval gate.
- Every task has acceptance criteria before it enters `READY`.
- Every code change passes code review before `MERGED`.
- Test failures produce actionable bugs/tasks.
- Review and test loops have a maximum retry count.
- Workflow decisions use structured, schema-validated data — never free-form text.
- Repository state comes from tools, never from agent assumptions.
- Important decisions are auditable (who, what, when, why).
- Never load the entire repository into an agent context; retrieve only relevant context.
- Never commit secrets, credentials, or `.env` files.

## 5. How to work in this repository (Cursor workflow)

1. Build one phase at a time. Do not implement future phases early.
2. Inspect existing architecture and docs before coding.
3. Use small, scoped changes: Inspect → Plan → Implement → Test → Review diff → Commit.
4. Every implementation step ships with tests.
5. Create modules/directories only when their phase starts.
6. Do not add infrastructure (Kafka, Redis, Temporal, Kubernetes, ...) until a phase requires it.
7. Keep docs synchronized with code. An architectural change requires an ADR in `docs/adr/`.
8. Commit after each stable milestone.

## 6. Where things live

| Path | Purpose |
|------|---------|
| `docs/architecture/` | System architecture (start with `system-overview.md`) |
| `docs/adr/` | Architecture Decision Records |
| `docs/standards/` | Coding, testing, and DevOps standards |
| `docs/requirements/` | Input requirements |
| `orchestrator/` | Workflow Orchestrator (created in Phase 1) |
| `agents/<role>/` | Agent implementations (created in the agent's phase) |
| `tools/` | Tool layer: git, shell, CI adapters (created when needed) |
| `knowledge/` | Knowledge sources for agent context (created when needed) |

## 7. Standards

Follow the relevant file in `docs/standards/`:

- Java / backend code: `docs/standards/backend.md`
- Tests: `docs/standards/testing.md`
- Frontend: `docs/standards/frontend.md`
- DevOps: `docs/standards/devops.md`

## 8. Definition of Ready / Done

- **Ready:** requirement clear, owner/agent known, acceptance criteria exist, dependencies identified,
  required design exists, scope understood.
- **Done (when applicable):** acceptance criteria satisfied, tests pass, code review approved,
  no blocking static analysis or security issues, docs updated, deployment completed if required.
