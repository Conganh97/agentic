# Agentic Engineering Team (Cursor-native)

A team of role-based AI agents (Scrum, Solution Architect, Backend, Frontend, Test, DevOps) that delivers
software from requirement to release **using only Cursor, markdown files and git**.

- Tasks and their state are markdown files in `tasks/`.
- Each role is a Cursor skill in `.cursor/skills/`.
- A workflow rule defines the allowed state transitions and who may perform them.
- Every state change is recorded in the task's History table and committed to git.

## Status

| Phase | Name | Status |
|-------|------|--------|
| 0 | Workspace Foundation | Done |
| 1 | Task Format and Workflow Rule | Done |
| 2 | Role Contracts | Done |
| 3 | SA Skill (Analysis & Design) | Done |
| 4 | Backend Skill | Done |
| 5 | SA Review Skill (MVP) | Done |
| 6 | Guardrails | Next |
| 7–10 | Test, Frontend, DevOps, Scrum Skills | Planned |

## Start here

1. `AGENTS.md` — rules for all agents.
2. `agentic_engineering_team_cursor_plan.md` — full plan.
3. `docs/architecture/system-overview.md` — how it works.
4. `project.md` — configure your product repo.

## Setup

1. Open this folder in Cursor.
2. Clone your product repository into `product/` (it is git-ignored here) and fill in `project.md`.
