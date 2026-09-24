# AGENTS.md — Project-wide Rules

These rules apply to every Cursor agent and human working in this workspace.
Architecture: `docs/architecture/system-overview.md`. Workflow: `.cursor/rules/workflow.mdc`.

## 1. What this workspace is

An agentic software engineering team (Scrum, SA, Product QA, UX/UI, BE, FE, Test, DevOps) that runs entirely in Cursor.
There is no platform code and no database:

- **State** lives in markdown: one file per task in `tasks/`, status in its YAML frontmatter.
- **Agents** are Cursor sessions using role skills in `.cursor/skills/`.
- **Audit** is the `## History` table in each task plus one git commit per state change.
- **Product code** lives in one git repo per component under `product/` (ADR-0004, registry in
 `project.md`), created and pushed only via `/repo` (`scripts/repo.py`).

## 2. Operating model

Markdown state + role skills + `/scrum run`. Stack: ADR-0009. UX/UI: ADR-0008. Product QA: ADR-0010.
DevOps (ADR-0011): DEV / STG / PROD on this machine, GHCR images + `ops/compose`. Sprints when
unfinished tasks > 5 (`scripts/sprint.py`).
Skills: `.cursor/skills/{sa,product-qa,ux-ui,backend,frontend,tester,devops,scrum,repo}/SKILL.md`.

## 3. Hard rules (never violate)

- A task's `status` in its task file is the only source of truth.
- Change status only via the Transition Protocol (`.cursor/rules/workflow.mdc` §5) and only with
  transitions your role is allowed to perform (§2).
- Never merge your own work; never approve your own code.
- No production deployment without `approved_by` set by a human in the task file.
- A requirement is analyzed only after a human sets its `status: APPROVED`.
- A task needs acceptance criteria before `READY`.
- Every code change passes SA review before `MERGED`; `merge_commit` must be a `--no-ff` sha on `main`.
- Review and test loops are limited to 3 iterations; beyond that the task becomes `BLOCKED`.
- Product AC misses are `BUG` (+ `bugs/BUG-###.md`). Execution/tooling misses are `FAILED`.
- `depends_on` is a graph: no cycles; a task is not READY until deps are MERGED or later.
- Always read files and run `git` to learn state; never assume it.
- Read only the files your role needs (the skill contract); never load the whole repository.
- Never write secrets into markdown, commits, or chat.
- Never bypass or edit guardrails (`.githooks/`, `.cursor/hooks*`, `--no-verify`); report a blocked
 command or rejected commit to the user instead of working around it.
- No external tracker (no Jira, no GitHub/GitLab issues or PRs). Planning, tracking, review, merge
  approval and releases are recorded only in markdown files in this repo.

## 4. How to work

1. One chat = one role on one task. Exception: `/scrum run` — the main chat stays SCRUM and delegates
 every other role to a fresh subagent per step (one subagent = one role on one task).
2. Keep changes small; show the diff; commit after each stable step.
3. Do not invent task statuses or skip the transition protocol.
4. Architectural decisions go into an ADR in `docs/adr/`.

## 5. Where things live

| Path | Purpose |
|------|---------|
| `project.md` | Product repo registry, stack, commands, environments |
| `requirements/` | Input requirements (`REQ-###-*.md`) |
| `tasks/` | Task files and `board.md` |
| `bugs/` | Product defect records (`BUG-###`) |
| `reviews/` | SA review rounds (`TASK-###-round-N.md`) |
| `tests/` | TEST run reports (`TASK-###-run-N.md`) |
| `runs/` | `/scrum run` journal (`RUN-###.md`, `journal.md`) |
| `sprints/`, `releases/` | Sprint and release files |
| `ops/` | Local compose stack (DevOps). Product Docker/CI lives in each product repo |
| `docs/architecture/` | Architecture docs |
| `docs/design/` | SA designs |
| `docs/design/ux/` | UX/UI design contract and reviews (ADR-0008) |
| `docs/adr/` | Architecture Decision Records |
| `docs/standards/` | Product standards |
| `memory/` | Decisions and lessons learned |
| `.cursor/rules/`, `.cursor/skills/`, `.cursor/hooks.json` | Workflow rule, role skills, guardrails |
| `scripts/`, `.githooks/` | Task workflow check (pre-commit) |
| `product/` | Product repos, one per component (ignored here) |

## 6. Commit conventions

- Team repo, state change: `[TASK-001] IN_PROGRESS -> CODE_REVIEW (BE): short note`
- Team repo, other: `docs: ...`, `chore: ...`
- Product repos: `feat(TASK-001): ...`, `fix(TASK-001): ...`, `test(TASK-001): ...`; branches
  `feature/TASK-001-slug`, `fix/TASK-001-slug`, `test/TASK-001-slug` (TEST), `ops/TASK-001-slug` (DEVOPS)
