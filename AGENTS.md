# AGENTS.md — Project-wide Rules

Architecture: `docs/architecture/system-overview.md`. Workflow: `.cursor/rules/workflow.mdc`.

## 1. Workspace

Markdown + git only. No Jira, no GitHub PRs, no extra DB.

- **State** = `status:` on `tasks/TASK-###-*.md`.
- **Agents** = Cursor chats using `.cursor/skills/<role>/SKILL.md`.
- **Audit** = task `## History` + one commit per state change.
- **Product** = one git repo per component under `product/` (ADR-0004, registry in `project.md`).
  Create/push only via `/repo` (`scripts/repo.py`).

Stack ADR-0009 (Java 21 + Spring, React). UX ADR-0008. PQA ADR-0010. DevOps ADR-0011
(DEV/STG/PROD on this machine, GHCR + `ops/compose`). Sprint if unfinished tasks > 5.

## 2. Hard rules

- Change `status` only via workflow §5, only transitions your role may do (§2).
- `NEEDS_INPUT` is an outcome, never a task status. `FAILED` recovers to `failed_from`.
- Never merge or approve your own work. Never set `approved_by`.
- No PROD deploy without human `approved_by`.
- Analyze a REQ only after human `APPROVED`. READY needs `AC-###`. TEST owns AC checkboxes.
- Code `MERGED` only after SA `--no-ff`; `merge_commit` is that sha on `main`.
- Review/test loops max 3 → then `BLOCKED`. Product miss = `BUG`. Tooling miss = `FAILED`.
- `depends_on` is a graph (no cycles). READY only when every dep is MERGED or later.
- Read only files your skill lists. Learn state from disk + `git`, never assume.
- No secrets in markdown/commits/chat. No bypass of `.githooks/` / `--no-verify`.
- Planning, review, merge, release live only in this repo’s markdown.
- Conflicts: escalate to the owning role (workflow §12); do not rewrite another role’s artifact.

## 3. How to work

One chat = one role on one task. Exception: `/scrum run` stays SCRUM and dispatches a fresh
subagent per other role/step. Small diffs. Commit after each stable step. New architecture → ADR.

## 4. Paths

`project.md` · `requirements/` · `tasks/` · `bugs/` · `reviews/` · `tests/` · `runs/` ·
`sprints/` · `releases/` · `ops/` · `docs/{architecture,design,design/ux,adr,standards}/` ·
`memory/` · `.cursor/{rules,skills,hooks.json}` · `scripts/` · `.githooks/` · `product/` (ignored)

## 5. Commits

- Team state: `[TASK-001] IN_PROGRESS -> CODE_REVIEW (BE): short note`
- Team other: `docs:` / `chore:`
- Product: `feat|fix|test(TASK-001): …` on `feature|fix|test|ops/TASK-001-slug`
