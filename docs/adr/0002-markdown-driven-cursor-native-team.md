# ADR-0002: Markdown-driven, Cursor-native agent team

- **Status:** Accepted
- **Date:** 2026-09-23
- **Deciders:** Project owner
- **Supersedes:** ADR-0001

## Context

ADR-0001 planned a Java Orchestrator with a database. The owner wants to run the team using only
Cursor, without writing or maintaining platform code or infrastructure.

## Decision

1. No orchestrator code, no database, no Java/Python runtime.
2. Task state is stored in markdown task files (`status` in YAML frontmatter) — one file per task.
3. Agents are Cursor Agent sessions guided by `AGENTS.md`, a workflow rule, and one skill per role.
4. Agents change state themselves, but only through the Transition Protocol and role permissions.
5. Git is the audit log: one commit per transition, plus a History table in each task.
6. Hard guardrails use a git `pre-commit` transition check and Cursor hooks (bash scripts only).
7. Product code lives in a separate git repo in `product/`, so task state never diverges across branches.
8. No external tracker: backlog, sprints, board, code review, merge approval, bugs and releases are all
   markdown files. Merges are done locally with `git merge --no-ff` after SA approval in the task file.

## Consequences

**Positive**
- Nothing to build or host; everything is readable and editable by humans.
- Full history via git; easy to review and revert.

**Negative / risks**
- Rules are guidance; agents can make mistakes → mitigated by pre-commit check, hooks, human review.
- Scheduling is `/scrum run` (SCRUM chat dispatches role subagents from `next.py`). A human
  still starts that run and handles gates (`APPROVED`, `approved_by`, unblock).
- Concurrent edits to shared files (e.g. `board.md`) can conflict → one agent per task; board is derived.

## Alternatives considered

- **Java/Python orchestrator + DB (ADR-0001)** — rejected: requires building and maintaining a platform.
- **External tracker (Jira, GitHub/GitLab issues or PRs)** — rejected: all planning, tracking, review and
  approval stay in markdown in this repo, so there is one source of truth and no tool to integrate.
