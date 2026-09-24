# Agentic Engineering Team (Cursor-native)

A role-based AI team (Scrum, SA, Product QA, UX/UI, Backend, Frontend, Test, DevOps) that delivers
software from requirement to release **using only Cursor, markdown and git**. No Jira, no GitHub PRs,
no platform database: task state is YAML in `tasks/`, audit is History + one git commit per transition.

```
HUMAN writes REQ → approve → /scrum run REQ-###
        │
        ├─ SA ⇄ PQA plan loop → ANALYZED (+ sprint if >5 unfinished)
        ├─ UX/UI ∥ BE          (UI work: spec + Figma; APIs in parallel)
        ├─ PQA reviews UX contract (not SA)
        ├─ FE implements the UX contract
        ├─ PQA visual review → SA code review + merge
        ├─ TEST accept (per task)
        ├─ PQA accept increment (or fail → SA fix tasks / side sprint)
        └─ READY_FOR_DEPLOY → (Phase 9) deploy
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
| — | UX/UI role + Figma MCP (ADR-0008) | Done |
| — | Product QA: plan loop, UX review, increment accept (ADR-0010) | Done |
| — | Stack policy: Java 21 + Spring, React locked; SA chooses the rest (ADR-0009) | Done |
| — | Sprints on `/scrum run` when unfinished tasks > 5 | Done |
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

6. Figma (UX/UI visual review): Cursor Settings → Tools & MCP → **Connect** next to `figma`,
   or `/add-plugin figma`. Config is `.cursor/mcp.json` (`https://mcp.figma.com/mcp`).

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

The main chat stays SCRUM. It dispatches a **fresh subagent per role per step** (SA, PQA, BE, FE, TEST)
until the requirement is done or a human gate is hit. Typical path:

| Step | Who | What happens |
|------|-----|----------------|
| Analyze | SA ⇄ PQA | Design `DRAFT` + tasks; PQA plan loop; then `ANALYZED` |
| Sprint | Scrum | If unfinished tasks > 5: `sprints/SPRINT-##.md`, only that increment is pulled |
| Design | UX/UI | Markdown in `docs/design/ux/` + Figma (dense, sellable). PQA reviews the contract |
| Ready | Scrum | Definition of Ready (+ sprint scope) → `READY` (REQ must be `ANALYZED`) |
| Implement | BE / FE | Feature branch; FE follows UX/Figma + SA kit |
| UX review | PQA | FE / UX_UI `CODE_REVIEW` vs spec/Figma + density bar, before SA |
| Review | SA | **Code** only. Approve or request changes (max 3). `--no-ff` merge (not UX_UI) |
| Test | TEST | Black-box against ACs. Pass → `READY_FOR_DEPLOY`. Fail → `BUG` (max 3) |
| Accept | PQA | Whole increment. Fail → SA fix tasks / optional side sprint |
| Deploy | DEVOPS | **Not implemented yet.** After PQA accept the run marks deploy *waiting* |

Or invoke each role yourself (one chat = one role on one task):

```
/sa analyze REQ-###
/scrum ready TASK-###
/backend TASK-###
/sa review TASK-###
/tester TASK-###
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
/scrum report REQ-###
```

Same data from the shell: `python3 scripts/next.py`, `python3 scripts/scrum_report.py`,
`python3 scripts/deps.py`, `python3 scripts/req.py check`.

## Skills

Skills live in `.cursor/skills/<name>/SKILL.md`. They do not auto-invoke (`disable-model-invocation`).

| Command | Role | When |
|---------|------|------|
| `/scrum run [REQ-###]` | Scrum | Orchestrate; plans a sprint first if unfinished tasks > 5 |
| `/scrum next [REQ-###]` | Scrum | Recommend the next step (no writes) |
| `/scrum ready TASK-###` | Scrum | BACKLOG → READY if DoR + sprint scope hold |
| `/scrum unblock TASK-### <note>` | Scrum | Only when you ask |
| `/scrum sprint` / `sprint close` | Scrum | Plan or close `sprints/SPRINT-##.md` |
| `/scrum sync` | Scrum | Regenerate `tasks/board.md` |
| `/scrum report [REQ-###]` | Scrum | Progress from History |
| `/sa analyze REQ-###` | SA | Design + stack + tasks; REQ stays `ANALYZING` until PQA plan |
| `/sa review TASK-###` | SA | Code review, request changes, or merge (not UX_UI) |
| `/pqa plan REQ-###` | PQA | Approve or bounce the SA plan |
| `/pqa review TASK-###` | PQA | UX contract merge or FE visual review |
| `/pqa accept REQ-###` | PQA | Increment accept after every task is done |
| `/uxui TASK-###` | UX/UI | Markdown design contract + Figma file |
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

See `project.md` and ADR-0009. **Locked:** Java 21 + Spring, React. Everything else is SA’s
choice in the requirement design (UI kit, DB, …).

## Project map

This repo is the **team control plane**. Product code is not here (`product/` is git-ignored).

```
agentic/
├── AGENTS.md, README.md, project.md
├── requirements/     tasks/     sprints/     bugs/
├── reviews/          tests/     runs/        releases/
├── docs/             memory/    templates/   scripts/
├── .cursor/          .githooks/ product/
└── plans (*.md at repo root)
```

### Root files

| File | What it is |
|------|------------|
| `README.md` | This guide: how to run the team and what each part is |
| `AGENTS.md` | Hard rules every agent must follow (state, roles, commits, no secrets) |
| `project.md` | Product registry, locked vs SA-chosen stack, commands, local env notes |
| `agentic_engineering_team_cursor_plan.md` | Original build plan (phases 0–10) |
| `agentic_engineering_team_uxui_update.md` | Spec that added the UX/UI role |
| `agentic_engineering_team_remaining_improvements.md` | Later improvement notes |

### Work items (state)

| Path | What it is |
|------|------------|
| `requirements/REQ-###-*.md` | Human input. SA analyzes only after `status: APPROVED`. Hash/revision via `req.py` |
| `tasks/TASK-###-*.md` | **Source of truth.** YAML `status` is the state machine. One file per task |
| `tasks/board.md` | Index generated by `sync_board.py` — do not edit rows by hand |
| `sprints/SPRINT-##.md` | Increment when unfinished tasks > 5. `/scrum run` only pulls `sprint:` matching ACTIVE |
| `bugs/BUG-###-*.md` | Product defect from a FAIL test run (not a workflow crash) |
| `reviews/TASK-###-round-N.md` | SA review evidence required for MERGED / CHANGES_REQUESTED |
| `tests/TASK-###-run-N.md` | TEST evidence required for READY_FOR_DEPLOY / BUG |
| `runs/RUN-###.md` + `journal.md` | `/scrum run` audit (one file per run + append-only log) |
| `releases/` | Release notes (used when DevOps ships; empty until Phase 9) |

### Docs and memory

| Path | What it is |
|------|------------|
| `docs/architecture/system-overview.md` | How markdown + git + skills replace an orchestrator service |
| `docs/design/REQ-###-design.md` | SA architecture, API, data, **stack table §5**, task breakdown |
| `docs/design/ux/` | UX/UI machine contract: spec, tokens, pages, reviews + Figma URL |
| `docs/adr/` | Decisions. Locked stack: 0003/0009. Repos: 0004. UX/UI: 0008. PQA: 0010. 0006 superseded |
| `docs/standards/backend.md` | Java package-by-feature layout, REST, CORS |
| `docs/standards/frontend.md` | React `app/pages/features/shared` layout, quality bar |
| `docs/standards/ux-ui.md` | When UX/UI runs, Figma MCP, density, what FE must implement |
| `docs/standards/product-qa.md` | Plan loop, visual review, increment accept (PQA) |
| `docs/standards/testing.md` | Acceptance vs unit tests; BUG vs FAILED |
| `docs/standards/artifacts.md` | Required files for each handoff (`/scrum run` checks these) |
| `memory/decisions.md` | Index of ADRs (append-only) |
| `memory/lessons.md` | Recurring review/test pitfalls (SA/TEST/UX read this) |

### Templates (copy, never edit in place for a real item)

| File | Used for |
|------|----------|
| `templates/requirement.md` | New REQ |
| `templates/task.md` | New TASK (frontmatter includes `work_type`, `requires_uxui`, `figma`) |
| `templates/design.md` | SA design |
| `templates/ux-spec.md` / `ux-page.md` / `ux-review.md` | UX/UI artifacts |
| `templates/pqa-plan.md` / `pqa-accept.md` | PQA plan and increment accept |
| `templates/review-round.md` | SA review file |
| `templates/test-report.md` | TEST run file |
| `templates/bug.md` | Product bug |
| `templates/sprint.md` | Sprint |
| `templates/run.md` | `/scrum run` journal file |
| `templates/examples/TASK-000-example.md` | Filled example of a full task lifecycle |

### Agents and guardrails

| Path | What it is |
|------|------------|
| `.cursor/skills/scrum/` | Orchestrator: run / next / ready / sprint / report |
| `.cursor/skills/sa/` | Analyze REQ → design+tasks; review+merge |
| `.cursor/skills/ux-ui/` | Design contract + Figma; review FE |
| `.cursor/skills/backend/` | Java 21 Spring implementation |
| `.cursor/skills/frontend/` | React implementation from UX/Figma |
| `.cursor/skills/tester/` | Black-box accept after MERGED |
| `.cursor/skills/devops/` | Deploy contract (Phase 9 not built) |
| `.cursor/skills/repo/` | Create/push product GitHub repos |
| `.cursor/rules/workflow.mdc` | Allowed transitions, who may change `status`, evidence |
| `.cursor/rules/task-files.mdc` | Task file format (frontmatter, History) |
| `.cursor/hooks.json` + `hooks/guard-shell.sh` | Blocks dangerous shell (`rm -rf`, force-push, raw `git push` to product `main`) |
| `.cursor/mcp.json` | Official Figma remote MCP (`https://mcp.figma.com/mcp`) |
| `.githooks/pre-commit` | `check_transitions.py` + `req.py check` + board freshness |

### Scripts

| Script | What it is |
|--------|------------|
| `scripts/next.py` | Deterministic next step (analyze → sprint → review → implement → test → deploy) |
| `scripts/sprint.py` | Large-work policy: need sprint? proposed scope? (`SMALL_MAX=5`, `SPRINT_CAP=6`) |
| `scripts/deps.py` | Task graph, cycles, “deps MERGED or later” |
| `scripts/parallel.py` | Which READY tasks may run at the same time (different repos, no dep edge) |
| `scripts/sync_board.py` | Rebuild `tasks/board.md` |
| `scripts/check_transitions.py` | Pre-commit: illegal status changes, review/test limits, merge sha |
| `scripts/req.py` | Requirement `content_hash` / `revision` / all-children-released |
| `scripts/gate_scan.py` | Flags auth/migration/breaking-API text → `human_gate` required |
| `scripts/repo.py` | Create/push component repos; write the `project.md` registry |
| `scripts/run_log.py` | Append a row to `runs/journal.md` |
| `scripts/scrum_report.py` | Counts, blockers, cycle time |
| `scripts/test_workflow.py` | Unit tests for the guards above |

### Product code

`product/` is **not** committed here. Each component is its own git repo + private GitHub remote
(`product-<name>`). Layout after `/repo create`:

```
product/services/<name>-service/   # Java 21 + Spring, package by feature
product/frontend/                  # React, src/{app,pages,features,shared}
```

Create/push only via `scripts/repo.py`. `main` only after an SA `--no-ff` merge recorded as
`merge_commit`.

### Roles (who owns what)

| Role | Owns | Does not |
|------|------|----------|
| HUMAN | Write/approve REQ, `approved_by`, unblock | Agent work |
| SCRUM | Board, sprint, READY, `/scrum run` | Code, designs, reviews |
| SA | Architecture, stack choice, tasks, merge | Product file edits |
| UX/UI | `docs/design/ux/` + Figma | Product implementation |
| BE / FE | Feature branches in their repo | Merge, approve own work |
| TEST | Acceptance vs AC | Commits in `product/` |
| DEVOPS | Deploy (not built yet) | PROD without `approved_by` |

Hard rules: `AGENTS.md`. Architecture: `docs/architecture/system-overview.md`.

## What you still do by hand

- Write and **approve** requirements.
- Install `gh` and log in once; confirm owner / visibility in `project.md`.
- Connect Figma MCP once (Settings → Tools & MCP) so UX/UI can create files you can review.
- Unblock tasks and set `approved_by` for PROD.
- Phase 9 (CI + Docker Compose deploy) is not built — a run stops at `READY_FOR_DEPLOY`.
