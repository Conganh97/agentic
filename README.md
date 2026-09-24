# Agentic Engineering Team (Cursor-native)

A role-based AI team (Scrum, SA, Backend, Frontend, Test, DevOps) that delivers software from
requirement to release **using only Cursor, markdown and git**. No Jira, no GitHub PRs, no platform
database: task state is YAML in `tasks/`, audit is History + one git commit per transition.

```
HUMAN writes REQ  →  approve  →  /scrum run REQ-###
                                      │
                    SA design + tasks → BE/FE implement → SA review + merge
                                      → TEST accept → (Phase 9) deploy
```

Product code lives in **one GitHub repo per component** under `product/` (ADR-0004). The team repo
only holds skills, rules, designs, tasks and the component registry in `project.md`.

## Status

| Phase | What it is | Status |
|-------|------------|--------|
| 0 | Workspace foundation | Done |
| 1 | Task format + workflow rule | Done |
| 2 | Role contracts | Done |
| 3 | SA analyze (design + tasks) | Done |
| 4 | Backend skill (Java 21 / Spring Boot 4) | Done |
| 5 | SA review + merge | Done |
| 6 | Guardrails (pre-commit + shell hook) | Done |
| 7 | Test skill | Done |
| 8 | Frontend skill (React + TypeScript) | Done |
| 9 | DevOps (GitHub Actions + Docker Compose) | **Not built** (contract only) |
| 10 | Scrum + `/scrum run` orchestrator | Done |
| — | `/repo` create/push product repos | Done (ADR-0004) |
| — | Workflow hardening (FAILED ≠ BUG, deps, artifacts, req hash, human gates) | Done |

## One-time setup

Do these once per machine / clone.

1. Open this folder in Cursor.
2. Enable the team-repo pre-commit hook (needs `python3`):

   ```bash
   git config core.hooksPath .githooks
   ```

   The hook runs `check_transitions.py` (task state machine) and `req.py check --staged`
   (requirement `revision` / `content_hash`). The agent shell guard (`.cursor/hooks.json`)
   needs `jq` and loads automatically.

3. Install and log in to the GitHub CLI (used only by `/repo`):

   ```bash
   brew install gh && gh auth login
   ```

4. Check `project.md` → **Repositories**: GitHub owner, repo name pattern (`product-<component>`),
   visibility (`private`). Change them before the first `/repo create` if they are wrong.

5. Local toolchain (see `project.md` → Local environment notes):

   - JDK 21+ (`JAVA_HOME` for Homebrew OpenJDK)
   - Node 25 / npm 11
   - Docker running if a service uses Testcontainers

`product/` is git-ignored here. Do not clone product repos by hand — `/repo create` does that.

## How to deliver a requirement

### 1. Write the requirement

Copy `templates/requirement.md` to `requirements/REQ-###-<kebab-slug>.md` (next free number).
Fill Goal, Scope, User Stories and business Acceptance Criteria. Leave `status: DRAFT`.
Set `content_hash` with `python3 scripts/req.py hash requirements/REQ-###-*.md`. After any
body edit, bump `revision` and recompute the hash — the hook rejects a silent content change.

### 2. Approve it (human only)

Set `status: APPROVED` in the frontmatter. SA will not analyze a `DRAFT`.

### 3. Run the team

In a **new chat**, invoke:

```
/scrum run REQ-###
```

The main chat stays SCRUM. It dispatches a **fresh subagent per role per step** (SA, BE, FE, TEST)
until the requirement is done or a human gate is hit. Typical path:

| Step | Who | What happens |
|------|-----|----------------|
| Analyze | SA | Design in `docs/design/`, BACKLOG tasks, registry of needed repos |
| Ready | Scrum | Definition of Ready → `READY` |
| Implement | BE / FE | Feature branch in the component repo, tests, push branch via `/repo` |
| Review | SA | Approve or request changes (max 3 rounds). On approve: `--no-ff` merge, push `main` |
| Test | TEST | Black-box against ACs. Pass → `READY_FOR_DEPLOY`. Fail → `BUG` (max 3 rounds) |
| Deploy | DEVOPS | **Not implemented yet.** The run marks the task *waiting* |

Or invoke each role yourself (one chat = one role on one task):

```
/sa analyze REQ-001
/scrum ready TASK-001
/backend TASK-001
/sa review TASK-001
/tester TASK-001
```

### 4. Answer when the run stops

`/scrum run` stops and asks you when:

| Gate | What you do |
|------|-------------|
| Requirement still `DRAFT` | Set `status: APPROVED` |
| `human_gate` (auth, migration, breaking API, …) | Confirm the topic on the task; only you set `approved_by` |
| Review or test limit (3) | Unblock or rewrite the task |
| `BLOCKED` | `/scrum unblock TASK-### <why>` |
| Deploy / PROD | Phase 9 not built. PROD also needs `approved_by` set by you in the task file |
| Permission prompt rejected | Re-run `/scrum run`; it retries a rejected permission once |
| Dirty tree / guardrail deny | Fix or report; do not bypass hooks |

Handoffs are files, not chat: `docs/standards/artifacts.md` (`reviews/`, `tests/`, `runs/`, `bugs/`).

Check progress any time:

```
/scrum next          # next actionable step
/scrum report        # counts, blockers, cycle time
/scrum report REQ-001
```

Same data from the shell: `python3 scripts/next.py`, `python3 scripts/scrum_report.py`,
`python3 scripts/deps.py`, `python3 scripts/req.py check`.

## Skills

Skills live in `.cursor/skills/<name>/SKILL.md`. They do not auto-invoke (`disable-model-invocation`).

| Command | Role | When |
|---------|------|------|
| `/scrum run [REQ-###]` | Scrum | Orchestrate a requirement end-to-end |
| `/scrum next [REQ-###]` | Scrum | Recommend the next step (no writes) |
| `/scrum ready TASK-###` | Scrum | BACKLOG → READY if Definition of Ready holds |
| `/scrum unblock TASK-### <note>` | Scrum | Only when you ask |
| `/scrum sprint` / `sprint close` | Scrum | Plan or close `sprints/SPRINT-##.md` |
| `/scrum sync` | Scrum | Regenerate `tasks/board.md` |
| `/scrum report [REQ-###]` | Scrum | Progress from History |
| `/sa analyze REQ-###` | SA | Design + BACKLOG tasks |
| `/sa review TASK-###` | SA | Review, request changes, or merge |
| `/backend TASK-###` | BE | Implement in `product/services/<name>-service` |
| `/frontend TASK-###` | FE | Implement in `product/frontend` |
| `/tester TASK-###` | TEST | Accept a merged task |
| `/devops deploy TASK-### <ENV>` | DevOps | Contract only until Phase 9 |
| `/repo create <component> be\|fe` | Repo | New private GitHub repo + registry row |
| `/repo push <component> [branch]` | Repo | Push a branch (`main` only after a recorded SA merge) |
| `/repo status` | Repo | Clean/dirty and unpushed `main` commits |

`/repo` is used by BE/FE/SA; you rarely invoke it yourself.

## Product repos

One private GitHub repo per component (`Conganh97/product-<component>` by default).

```
product/
├── services/
│   └── <name>-service/     # Spring Boot app (own git + remote)
└── frontend/               # React + Vite app (own git + remote)
```

Rules the scripts enforce:

- Create and push **only** via `python3 scripts/repo.py` (skill `/repo`).
- `main` is pushed only when every new first-parent commit is a `--no-ff` merge whose sha is a
  task's `merge_commit`. Direct commits on `main` are refused.
- Force-push, deleting GitHub repos, and deleting remote `main` are blocked by the shell guard.

Registry table in `project.md` is written by `repo.py create`. Do not edit it by hand.

## Workflow (state machine)

Source of truth: `status:` in `tasks/TASK-###-*.md`. Allowed transitions: `.cursor/rules/workflow.mdc`.

```
BACKLOG → READY → IN_PROGRESS → CODE_REVIEW → MERGED → TESTING → READY_FOR_DEPLOY → DEPLOYING → RELEASED
                      ▲              │                      │
                      └── CHANGES_REQUESTED                 └── BUG → IN_PROGRESS
IN_PROGRESS / TESTING / DEPLOYING → FAILED → (back to failed_from)
```

- Review loop and test loop: **max 3** iterations, then `BLOCKED`.
- Any working state can go `BLOCKED`; only an explicit unblock returns it.
- `FAILED` = workflow/tooling could not run. `BUG` = product behaviour is wrong (`bugs/BUG-###.md`).
- `/scrum run` is a state-machine executor: it re-reads disk each step and resumes; it does not restart.
- Nobody merges their own work. Nobody deploys PROD without your `approved_by`.

Definition of Ready (needed for BACKLOG → READY): `parent` set, `assignee` set, ≥1 acceptance
criterion with an id (`AC-001`, …), `depends_on` filled (or `[]`) and each dep is MERGED or later,
Design filled or linked. `scripts/gate_scan.py` also requires `human_gate` if the design/task
hits auth, migration, breaking API, or similar.

## Stack

See `project.md`, `docs/adr/0003-product-tech-stack.md`, and `docs/adr/0006-frontend-ui-kit.md`.

| Area | Choice |
|------|--------|
| Backend | Java 21, Spring Boot 4.0.8, Maven wrapper, PostgreSQL + Flyway |
| Frontend | React + TypeScript, Vite, TanStack Query, Mantine + Tabler Icons, oxlint + Prettier |
| Tests | JUnit 5 / AssertJ / Testcontainers (BE); Vitest + RTL (FE) |

## Where things live

| Path | Purpose |
|------|---------|
| `requirements/` | Input requirements (`REQ-###-*.md`) |
| `tasks/` | One file per task; `board.md` is generated |
| `bugs/` | Product defects (`BUG-###`) opened from a failing TEST run |
| `reviews/` | SA review rounds (`TASK-###-round-N.md`) |
| `tests/` | TEST run reports (`TASK-###-run-N.md`) |
| `runs/` | `/scrum run` journal (`RUN-###.md`, `journal.md`) |
| `docs/design/` | SA designs |
| `docs/adr/` | Architecture decisions (stack: 0003; UI kit: 0006) |
| `docs/standards/` | BE / FE / testing / artifact contracts |
| `memory/` | Decision index and lessons |
| `project.md` | Repos, stack, commands, local notes |
| `.cursor/skills/` | Role skills |
| `.cursor/rules/workflow.mdc` | Transition protocol |
| `templates/` | Requirement, task, design, bug, review, test report, run, sprint |
| `scripts/repo.py` | Create / push product repos |
| `scripts/sync_board.py` | Regenerate the board |
| `scripts/deps.py` | Dependency graph, cycles, actionable tasks |
| `scripts/next.py` | Deterministic next step (resume) |
| `scripts/scrum_report.py` | `/scrum report` numbers |
| `scripts/req.py` | Requirement hash / revision / completion |
| `scripts/run_log.py` | Append `runs/journal.md` |
| `scripts/parallel.py` | Safe BE/FE parallel pairs |
| `scripts/gate_scan.py` | Human-gate keywords |
| `scripts/check_transitions.py` | Pre-commit state-machine guard |
| `scripts/test_workflow.py` | Unit tests for the guards above |
| `product/` | Product repos (ignored by this repo) |

Hard rules for agents: `AGENTS.md`. Full plan: `agentic_engineering_team_cursor_plan.md`.
Architecture sketch: `docs/architecture/system-overview.md`.

## What you still do by hand

- Write and **approve** requirements.
- Install `gh` and log in once; confirm owner / visibility in `project.md`.
- Unblock tasks and set `approved_by` for PROD.
- Phase 9 (CI + Docker Compose deploy) is not built — a run stops at `READY_FOR_DEPLOY`.
