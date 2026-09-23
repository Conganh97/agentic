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
| 6 | Guardrails | Done |
| 7 | Test Skill | Done |
| 8 | Frontend Skill | Done |
| 9 | DevOps Skill | Next (contract only) |
| 10 | Scrum Skill + `/scrum run` orchestrator | Done |

## Start here

1. `AGENTS.md` — rules for all agents.
2. `agentic_engineering_team_cursor_plan.md` — full plan.
3. `docs/architecture/system-overview.md` — how it works.
4. `project.md` — product repos (one per component), stack, commands.

## Setup

1. Open this folder in Cursor.
2. Install and log in to the GitHub CLI once (`brew install gh && gh auth login`) and check the
   GitHub owner, repo name and visibility in `project.md`. Product repos (one per service, one for the
   frontend) are created in `product/` (git-ignored here) and pushed by `/repo` (`scripts/repo.py`).
3. Write a requirement in `requirements/REQ-###-*.md` (from `templates/requirement.md`), set
   `status: APPROVED`, then run `/scrum run REQ-###` in a chat (or invoke each role skill yourself).
4. Enable the task workflow check once per clone: `git config core.hooksPath .githooks`
   (needs `python3`). The agent shell guard in `.cursor/hooks.json` needs `jq` and loads automatically.
