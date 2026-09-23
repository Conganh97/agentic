# AGENTS.md — Project-wide Rules

These rules apply to every Cursor agent and human working in this workspace.
Full plan: `agentic_engineering_team_cursor_plan.md`. Architecture: `docs/architecture/system-overview.md`.

## 1. What this workspace is

An agentic software engineering team (Scrum, SA, BE, FE, Test, DevOps) that runs entirely in Cursor.
There is no platform code and no database:

- **State** lives in markdown: one file per task in `tasks/`, status in its YAML frontmatter.
- **Agents** are Cursor sessions using role skills in `.cursor/skills/`.
- **Audit** is the `## History` table in each task plus one git commit per state change.
- **Product code** lives in a separate git repo in `product/` (see `project.md`).

## 2. Current phase

**Phase 0 — Workspace Foundation (done).** Next: Phase 1 — Task Format and Workflow Rule.

Update this section whenever a phase starts or finishes.

## 3. Hard rules (never violate)

- A task's `status` in its task file is the only source of truth.
- Change status only via the Transition Protocol (plan §8) and only with transitions your role is
  allowed to perform (plan §6–§7).
- Never merge your own work; never approve your own code.
- No production deployment without `approved_by` set by a human in the task file.
- A task needs acceptance criteria before `READY`.
- Every code change passes SA review before `MERGED`.
- Review and test loops are limited to 3 iterations; beyond that the task becomes `BLOCKED`.
- Always read files and run `git` to learn state; never assume it.
- Read only the files your role needs (plan §12); never load the whole repository.
- Never write secrets into markdown, commits, or chat.
- No external tracker (no Jira, no GitHub/GitLab issues or PRs). Planning, tracking, review, merge
  approval and releases are recorded only in markdown files in this repo.

## 4. How to work

1. One phase at a time; do not build future phases early.
2. One chat = one role on one task.
3. Keep changes small; show the diff; commit after each stable step.
4. Create folders only when their phase starts.
5. Architectural decisions go into an ADR in `docs/adr/`.

## 5. Where things live

| Path | Purpose |
|------|---------|
| `project.md` | Product repo path, stack, commands, environments |
| `requirements/` | Input requirements (`REQ-###-*.md`) |
| `tasks/` | Task files and `board.md` (from Phase 1) |
| `sprints/`, `releases/` | Sprint and release files (from Phase 9–10) |
| `docs/architecture/` | Architecture docs |
| `docs/design/` | SA designs (from Phase 3) |
| `docs/adr/` | Architecture Decision Records |
| `docs/standards/` | Product standards (from Phase 4) |
| `memory/` | Decisions and lessons learned (from Phase 3) |
| `.cursor/rules/`, `.cursor/skills/`, `.cursor/hooks.json` | Workflow rule, role skills, guardrails |
| `product/` | Product code (separate git repo, ignored here) |

## 6. Commit conventions

- Team repo, state change: `[TASK-001] IN_PROGRESS -> CODE_REVIEW (BE): short note`
- Team repo, other: `docs: ...`, `chore: ...`
- Product repo: `feat(TASK-001): ...`, `fix(TASK-001): ...`; branches `feature/TASK-001-slug`, `fix/TASK-001-slug`
