# Agentic Engineering Team

A Cursor-native team (Scrum, SA, Product QA, UX/UI, Backend, Frontend, Test, DevOps) that ships
software with **markdown + git only**. No Jira, no GitHub PRs, no extra database.

- **State** is the `status:` field in each `tasks/TASK-###-*.md`.
- **Agents** are Cursor chats using a role skill.
- **Audit** is the task History table plus one git commit per transition.
- **Product code** lives in a separate git repo per component under `product/` (git-ignored here).

Hard rules: `AGENTS.md`. Architecture: `docs/architecture/system-overview.md`.
Transitions: `.cursor/rules/workflow.mdc`.

```
HUMAN writes REQ → approve
        │
        ▼
/scrum run REQ-###
        │
        ├─ SA ⇄ PQA          plan until ANALYZED
        ├─ UX/UI ∥ BE        design + APIs
        ├─ PQA               reviews the UX contract
        ├─ FE                implements the contract
        ├─ PQA → SA          visual review, then code review + merge
        ├─ TEST              per-task acceptance
        ├─ PQA               increment accept (fail → SA fix tasks / side sprint)
        └─ DEVOPS            repos + Docker/CI + deploy DEV/STG/PROD on this machine
```

---

## How to use

### Once per machine

1. Open this folder in Cursor.
2. `git config core.hooksPath .githooks` (`python3` required).
3. `brew install gh && gh auth login` then `gh auth refresh -s write:packages` (repos + GHCR).
4. Confirm GitHub owner / `product-<component>` / visibility in `project.md`.
5. Install JDK 21+, Node, and **Docker Desktop** (Testcontainers + local deploy). Details: `project.md`.
6. Connect Figma once: Settings → Tools & MCP → **Connect** next to `figma`
   (`.cursor/mcp.json` → `https://mcp.figma.com/mcp`).
7. Optional: install a GitHub **self-hosted** Actions runner on this Mac so product `ci.yml` pushes
   images on `main`. Without it, `/devops deploy` is the pipeline.

Do not clone `product/` by hand. `/repo create` does that.

### Deliver a requirement

1. Copy `templates/requirement.md` → `requirements/REQ-###-<slug>.md`. Fill Goal, Scope, stories, ACs.
   `status: DRAFT`. Hash: `python3 scripts/req.py hash requirements/REQ-###-*.md`. After a body edit,
   bump `revision` and re-hash.
2. You set `status: APPROVED`. SA will not analyze a draft.
3. New chat: `/scrum run REQ-###`. The main chat stays SCRUM and dispatches one fresh subagent per
   role per step. Or call a role yourself (`/sa analyze REQ-###`, `/backend TASK-###`, …).
4. When the run stops, you: approve a `DRAFT` REQ, set `approved_by` on a `human_gate`, unblock
   `BLOCKED`, or approve PROD. Do not bypass hooks.

Progress: `/scrum next` · `/scrum report [REQ-###]`.

Same from the shell: `python3 scripts/next.py` · `scrum_report.py` · `deps.py` · `req.py check`.

### Commands

| Command | Role | Purpose |
|---------|------|---------|
| `/scrum run [REQ-###]` | Scrum | Run the state machine (sprint first if unfinished tasks > 5) |
| `/scrum next [REQ-###]` | Scrum | Next step, no writes |
| `/scrum ready TASK-###` | Scrum | BACKLOG → READY if Definition of Ready holds |
| `/scrum sprint` / `sprint close` | Scrum | Plan or close an increment |
| `/scrum report [REQ-###]` | Scrum | Counts and blockers |
| `/sa analyze REQ-###` | SA | Design + tasks; REQ stays `ANALYZING` until PQA plan |
| `/sa review TASK-###` | SA | Code review and merge (not UX_UI) |
| `/pqa plan REQ-###` | PQA | Approve or bounce the SA plan |
| `/pqa review TASK-###` | PQA | UX contract merge or FE visual review |
| `/pqa accept REQ-###` | PQA | Increment accept after every child task is done |
| `/uxui TASK-###` | UX/UI | Markdown + Figma contract |
| `/backend TASK-###` | BE | Implement in `product/services/<name>-service` |
| `/frontend TASK-###` | FE | Implement in `product/frontend` |
| `/tester TASK-###` | TEST | Black-box after MERGED |
| `/devops TASK-###` | DevOps | Create missing repos; write or repair Docker + GHA + compose |
| `/devops deploy TASK-### <ENV>` | DevOps | Build, push GHCR, compose up (`DEV` / `STG` / `PROD`) |
| `/repo create\|push\|status` | Repo | Product GitHub repos (`repo.py`); DevOps is the preferred creator |

One chat = one role, except `/scrum run`. Skills do not auto-invoke.

---

## Structure

```
agentic/                    ← this repo (control plane)
├── AGENTS.md               hard rules
├── project.md              product registry, stack, local commands
├── requirements/           REQ-### (human input)
├── tasks/                  TASK-### + generated board.md
├── sprints/  bugs/  reviews/  tests/  runs/  releases/
├── docs/                   architecture, ADRs, standards, designs
├── memory/                 decision / lesson index
├── templates/              copy these; do not fill them in place
├── ops/                    local compose (DEV/STG/PROD)
├── scripts/                next, deps, board, guards, repo, deploy
├── .cursor/                skills, workflow rule, hooks, Figma MCP
├── .githooks/              pre-commit
└── product/                ignored — one git repo per component
```

### Root

| Path | What it is |
|------|------------|
| `README.md` | How to use the team and what each part is |
| `AGENTS.md` | Rules every agent and human follows |
| `project.md` | Registry of product repos, locked vs SA-chosen stack, how to build/run locally |

### Work items

| Path | What it is |
|------|------------|
| `requirements/REQ-###-*.md` | What to build. Analyzed only after `APPROVED`. Hash/revision via `req.py` |
| `tasks/TASK-###-*.md` | Source of truth. YAML `status` is the state machine |
| `tasks/board.md` | Index. Generated by `sync_board.py` — do not edit rows by hand |
| `sprints/SPRINT-##.md` | Increment when unfinished work > 5. Only `sprint:` matching ACTIVE is pulled |
| `bugs/BUG-###-*.md` | Product miss vs an AC (not a tooling crash) |
| `reviews/TASK-###-round-N.md` | SA code-review evidence |
| `tests/TASK-###-run-N.md` | TEST evidence |
| `runs/RUN-###.md`, `journal.md` | `/scrum run` audit |
| `releases/` | Release notes when DevOps ships PROD |
| `ops/` | Compose stack. DevOps. Images from GHCR. Secrets in `.env.dev` / `.env.stg` / `.env.prod` |

Handoff contract: `docs/standards/artifacts.md`.

### Docs and memory

| Path | What it is |
|------|------------|
| `docs/architecture/system-overview.md` | How markdown + git + skills replace a platform |
| `docs/design/REQ-###-design.md` | SA design (stack in §5, API, data, tasks) |
| `docs/design/ux/` | UX/UI machine contract + Figma URL |
| `docs/design/reviews/` | PQA plan and increment-accept files |
| `docs/adr/` | Decisions. Locked cores 0003/0009; repos 0004; UX 0008; PQA 0010 |
| `docs/standards/` | How BE / FE / UX / PQA / TEST / DevOps write artifacts |
| `memory/decisions.md` | ADR index |
| `memory/lessons.md` | Recurring pitfalls agents should not repeat |

### Templates

Copy from `templates/` (`requirement.md`, `task.md`, `design.md`, `ux-*.md`, `pqa-*.md`,
`review-round.md`, `test-report.md`, `bug.md`, `sprint.md`, `run.md`, `release.md`, `ops/`).
`templates/examples/TASK-000-example.md` is a filled lifecycle, not a live task.

### Agents and guards

| Path | What it is |
|------|------------|
| `.cursor/skills/<role>/` | Role contract: what that chat may read, write, and transition |
| `.cursor/rules/workflow.mdc` | Who may change `status`, and what evidence is required |
| `.cursor/rules/task-files.mdc` | Task file format |
| `.cursor/hooks.json` | Shell guard (`rm -rf`, force-push, raw push of product `main`) |
| `.cursor/mcp.json` | Official Figma MCP |
| `.githooks/pre-commit` | `check_transitions.py` + `req.py` + board freshness |

### Scripts

| Script | What it is |
|--------|------------|
| `next.py` | Next actionable step from disk |
| `sprint.py` | Whether a sprint is required and what to pull |
| `deps.py` | Task graph, cycles, “deps MERGED or later” |
| `parallel.py` | Which READY tasks may run together |
| `sync_board.py` | Rebuild `tasks/board.md` |
| `check_transitions.py` | Illegal status changes, retry limits, merge sha |
| `req.py` | Requirement hash / revision / completion |
| `gate_scan.py` | Auth / migration / breaking-API text → `human_gate` |
| `repo.py` | Create and push product repos (seeds Dockerfile + GHA); write the registry |
| `deploy.py` | Build images, push GHCR, compose up (`--env DEV|STG|PROD`) |
| `run_log.py` | Append `runs/journal.md` |
| `scrum_report.py` | Counts and cycle time |
| `test_workflow.py` | Unit tests for the guards |

### Product code

Not committed here. After `/repo create`:

```
product/services/<name>-service/   # Java 21 + Spring, package by feature
product/frontend/                  # React, src/{app,pages,features,shared}
```

Create and push only via `scripts/repo.py` (DevOps preferred). Create also seeds `Dockerfile` and
`.github/workflows/ci.yml`. `main` only after an SA `--no-ff` merge recorded as `merge_commit`.
Registry rows in `project.md` are written by that script. Run the stack with `scripts/deploy.py`.

---

## Roles

| Role | Owns | Does not |
|------|------|----------|
| HUMAN | Write/approve REQ, `approved_by`, unblock | Agent work |
| SCRUM | Board, sprint, READY, `/scrum run` | Code, designs, reviews |
| SA | Architecture, stack, tasks, **code** merge | Product file edits, UX merge |
| PQA | Plan gate, UX review, increment accept | Product code, SA code merge |
| UX/UI | `docs/design/ux/` + Figma | Product implementation, approving own look |
| BE / FE | Feature branches in their repo | Merge, approve own work |
| TEST | Acceptance vs AC | Commits in `product/` |
| DEVOPS | Product repos (if missing), Dockerfile, GHA, compose, deploy | App features; PROD without `approved_by` |

---

## Workflow

Source of truth: `status:` on the task. Allowed edges: `.cursor/rules/workflow.mdc`.

```
BACKLOG → READY → IN_PROGRESS → CODE_REVIEW → MERGED → TESTING → READY_FOR_DEPLOY → DEPLOYING → RELEASED
                      ▲              │                      │
                      └── CHANGES_REQUESTED                 └── BUG → IN_PROGRESS
IN_PROGRESS / TESTING / DEPLOYING → FAILED → (back to failed_from)
```

- Review and test loops: max 3, then `BLOCKED`.
- `FAILED` = tooling could not run. `BUG` = product behaviour is wrong.
- `/scrum run` re-reads disk every step and resumes. It does not restart finished work.
- Nobody merges their own work. Nobody deploys PROD without your `approved_by`.

**Definition of Ready:** `parent`, `assignee`, ≥1 `AC-###`, `depends_on` (or `[]`) with every dep
MERGED or later, Design filled or linked. `gate_scan.py` also requires `human_gate` on auth /
migration / breaking API text.

**Stack:** Java 21 + Spring and React are locked (ADR-0009). UI kit, DB, and the rest are named by
SA in the design.

---

## What you still do

- Write and approve requirements.
- Log in `gh` once; check owner / visibility in `project.md`.
- Connect Figma MCP once.
- Unblock tasks and set `approved_by` for gates and PROD.
- Keep Docker running. After PQA accept, DevOps deploys DEV on this machine (`scripts/deploy.py`).
