# Agentic Engineering Team

A controlled software delivery platform where specialized AI agents (Scrum, Solution Architect,
Backend, Frontend, Test, DevOps) execute the software lifecycle from requirement to release,
under a deterministic, auditable workflow owned by an Orchestrator.

## Status

| Phase | Name | Status |
|-------|------|--------|
| 0 | Repository Foundation | Done |
| 1 | Workflow Orchestrator | Next |
| 2 | Agent Contract | Planned |
| 3 | SA Agent | Planned |
| 4 | Backend Agent | Planned |
| 5 | SA Code Review | Planned |
| 6 | Git/GitLab Integration | Planned |
| 7–10 | Test, Frontend, DevOps, Scrum Agents | Planned |

MVP target: Requirement → SA → Task → BE → PR → SA Review → Fix loop → Approve → Merge.

## Start here

1. `AGENTS.md` — project-wide rules for humans and agents.
2. `docs/architecture/system-overview.md` — architecture summary.
3. `docs/adr/` — architecture decisions.
4. `docs/standards/` — coding, testing, DevOps standards.
5. `agentic_engineering_team_cursor_plan.md` — full implementation plan and roadmap.

## Tech stack (initial)

- Java 21 + Maven for the Orchestrator and agent runtime
- Spring Boot (application layer only; domain/workflow stay pure Java)
- In-memory persistence first, then H2 (local) / PostgreSQL
- Git
- JUnit 5 + AssertJ

Additional infrastructure is added only when a phase requires it (see ADR-0001).

## Repository layout

```
.
├── AGENTS.md
├── README.md
├── agentic_engineering_team_cursor_plan.md
└── docs/
    ├── architecture/system-overview.md
    ├── adr/
    ├── requirements/
    └── standards/
```

`orchestrator/`, `agents/`, `tools/`, `knowledge/`, `infrastructure/` are created when their phase starts.
