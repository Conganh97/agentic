# Agentic Engineering Team — Cursor-Native Plan (Markdown-driven)

## 1. Objective

Build an Agentic Software Engineering Team that manages the software lifecycle from requirement to
release, running **entirely inside Cursor**.

- No custom platform code, no database, no Java/Python orchestrator.
- **Cursor is the runtime.** Agents are Cursor Agent sessions guided by project rules and skills.
- **Markdown files are the state.** Tasks, status, designs, reviews, test results and history live in
  `.md` files in this repository.
- **Git is the audit log.** Every state change is a commit.
- **No external tracker.** No Jira, no GitHub/GitLab issues, no PR/MR tools. Backlog, sprints, board,
  reviews, bugs and releases are all markdown files (see §3.1).

Team roles:

- Scrum Agent
- Solution Architect (SA) Agent
- Backend (BE) Agent
- Frontend (FE) Agent
- Test Agent
- DevOps Agent

Core lifecycle:

Requirement → Scrum Planning → SA Analysis → Technical Design → Task Breakdown
→ BE/FE Implementation → SA Code Review ⇄ Fix Loop → Merge
→ Automation Test ⇄ Bug Fix Loop → DevOps Deployment → UAT → Release

---

# 2. Core Principles

1. Agent = intelligence (Cursor Agent + role skill)
2. Workflow = control (workflow rule + state machine in markdown)
3. Tools = capability (Cursor tools: files, terminal, git, CLI)
4. Knowledge = context (docs, ADRs, memory files)
5. Policy = constraints (AGENTS.md, rules, hooks, git pre-commit check)
6. State = source of truth (task file frontmatter)

## 2.1 Hard rules

- A task's `status` in its task file is the only source of truth for its state.
- Agents change state only through the **Transition Protocol** (§8). No other edits to `status`.
- Agents only perform transitions their role is allowed to perform (§7, §9).
- Agents never merge their own work and never approve their own code.
- No production deployment without an explicit human approval recorded in the task file.
- Every task has acceptance criteria before `READY`.
- Every code change passes SA review before `MERGED`.
- Test failures produce a bug record with reproduction steps.
- Review and test loops have a maximum iteration count (default 3); exceeding it → `BLOCKED`.
- Repository state comes from tools (read files, run `git`), never from memory or assumption.
- Load only the files listed for the role (§12). Never load the whole repository.
- All planning, tracking, review and approval happen in markdown files in this repo — never in an
  external tool.

---

# 3. How Cursor Features Map to the Architecture

| Architecture concept | Cursor implementation |
|----------------------|-----------------------|
| Project-wide rules | `AGENTS.md` (always loaded) |
| Workflow / state machine | `.cursor/rules/workflow.mdc` (`alwaysApply: true`) + task file format |
| Agents | Project skills: `.cursor/skills/<role>/SKILL.md` (sa, backend, frontend, tester, devops, scrum) |
| Orchestrator | Scrum skill (dispatcher: "what's next, who does it") + human approval |
| Task state | YAML frontmatter `status:` in `tasks/TASK-###-*.md` |
| Task overview | `tasks/board.md` (index, derived from task files) |
| Audit log | `## History` table in each task + one git commit per transition |
| Hard guardrails | `.cursor/hooks.json` (block dangerous shell commands) + git `pre-commit` check of transitions |
| Knowledge | `docs/` (architecture, ADRs, standards) + `memory/` |
| Parallel work | Multiple Cursor chats / background agents, one task each |

## 3.1 Tracker Features in Markdown (instead of Jira)

| Tracker feature | Markdown equivalent |
|-----------------|---------------------|
| Epic / Story / Task / Bug | `tasks/TASK-###-*.md` with `type:` EPIC / STORY / TASK / BUG / TECHNICAL_TASK |
| Parent / sub-task, links | `parent:` and `depends_on:` in frontmatter |
| Workflow & statuses | `status:` + `.cursor/rules/workflow.mdc` |
| Assignee | `assignee:` (role) |
| Board / backlog view | `tasks/board.md` (rows sorted by status, priority) |
| Sprint | `sprints/SPRINT-##.md` (goal, scope, dates, outcome) |
| Comments / activity | task sections (Design, Implementation, Review, Test, Deployment) + `## History` |
| Pull request / code review | Review rounds in the task file + `git diff main...branch` in `product/` |
| Merge | local `git merge --no-ff` in `product/` by SA; `merge_commit:` in frontmatter |
| Bug report | BUG task file with reproduction steps, expected vs actual, logs |
| Release / version | `releases/REL-###.md` (version, tasks included, environments, approval) |
| Reports / dashboards | Scrum `report` computed from frontmatter and History |
| Search / filters | Cursor search / `rg` over `tasks/` frontmatter |

---

# 4. Repository Structure

This repository is the **team workspace** (process + state). The **product code** lives in a separate git
repository cloned into `product/` (git-ignored here). Keeping them separate means task state is always on
`main` of the team repo, while code changes live on feature branches of the product repo.

```
agentic/                         # team workspace (this repo)
├── AGENTS.md                    # project-wide rules
├── README.md
├── project.md                   # product config: repo path, stack, commands, environments
├── agentic_engineering_team_cursor_plan.md
│
├── .cursor/
│   ├── rules/
│   │   ├── workflow.mdc         # state machine + transition protocol (always applied)
│   │   └── task-files.mdc       # task file + board format (applied to tasks/**)
│   ├── skills/
│   │   ├── sa/SKILL.md
│   │   ├── backend/SKILL.md
│   │   ├── frontend/SKILL.md
│   │   ├── tester/SKILL.md
│   │   ├── devops/SKILL.md
│   │   └── scrum/SKILL.md
│   ├── hooks.json               # guardrails
│   └── hooks/                   # hook scripts (bash)
│
├── templates/
│   ├── task.md
│   ├── requirement.md
│   ├── design.md
│   ├── sprint.md
│   ├── release.md
│   └── examples/TASK-000-example.md   # fully walked reference task
│
├── requirements/                # REQ-###-*.md (input from humans)
├── tasks/
│   ├── board.md                 # index of all tasks
│   └── TASK-###-<slug>.md       # one file per task (source of truth)
├── sprints/                     # SPRINT-##.md
├── releases/                    # REL-###.md (release notes, approvals)
│
├── docs/
│   ├── architecture/            # system-overview.md + product architecture
│   ├── design/                  # SA designs: REQ-###-design.md
│   ├── adr/                     # architecture decision records
│   └── standards/               # product coding/testing/devops standards
│
├── memory/
│   ├── decisions.md             # rejected designs, trade-offs (index of ADRs)
│   └── lessons.md               # recurring bugs, review findings, failed approaches
│
├── scripts/
│   └── check-transitions.sh     # used by git pre-commit hook
│
└── product/                     # product repo (separate git, git-ignored)
```

Create folders only when their phase starts.

---

# 5. Task File Format

`templates/task.md`:

```markdown
---
id: TASK-001
title: Login API
type: STORY            # EPIC | STORY | TASK | BUG | TECHNICAL_TASK
priority: HIGH         # LOW | MEDIUM | HIGH | CRITICAL
status: BACKLOG        # see §6
assignee: BE           # SCRUM | SA | BE | FE | TEST | DEVOPS | HUMAN
parent: REQ-001        # requirement or epic id
depends_on: []         # [TASK-002, ...]
sprint:
branch:                # feature/TASK-001-login-api
merge_commit:          # merge commit sha in product/ (set by SA on MERGED)
release:               # REL-001 (set by DEVOPS)
review_iteration: 0
test_iteration: 0
blocked_from:          # previous status when BLOCKED
approved_by:           # human name for PROD deploy approval
updated: 2026-09-23
---

## Description

## Acceptance Criteria
- [ ] AC-1 ...

## Design (SA)
Link to docs/design/... and task-specific notes.

## Implementation (BE/FE)
Branch, summary, changed files, how tested.

## Review (SA)
### Round 1 — CHANGES_REQUESTED | APPROVED
Reviewed: <branch> @ <sha> · Build/tests: PASS | FAIL
Previous round: #1 resolved, ...        (from round 2 on)
| # | File | Severity (BLOCKER/MAJOR/MINOR) | Comment |
|---|------|------|---------|

## Test (TEST)
### Run 1 — PASS | FAIL
Scope, commands, results, bugs found.

## Deployment (DEVOPS)
Environment, version, result, rollback plan.

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 10:00 | — | BACKLOG | SA | Created from REQ-001 |
```

`tasks/board.md`:

```markdown
| ID | Title | Type | Priority | Status | Assignee | Depends on | Updated |
|----|-------|------|----------|--------|----------|------------|---------|
```

Rules:
- The task file is the source of truth; `board.md` is an index and must be updated in the same commit.
- IDs are sequential: next id = highest id in `tasks/` + 1.
- Sections are append-only: add a new Review round / Test run; never rewrite previous ones.

---

# 6. Workflow State Machine

States: `BACKLOG, READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, MERGED, TESTING, BUG,
READY_FOR_DEPLOY, DEPLOYING, RELEASED, BLOCKED`

| From | To | Who | Guard |
|------|----|-----|-------|
| BACKLOG | READY | SCRUM | Definition of Ready (§10) satisfied |
| READY | IN_PROGRESS | BE / FE (assignee) | dependencies are MERGED or later |
| IN_PROGRESS | CODE_REVIEW | BE / FE | tests pass, branch pushed/committed, Implementation section filled |
| CODE_REVIEW | CHANGES_REQUESTED | SA | new Review round with ≥1 comment; `review_iteration += 1` |
| CODE_REVIEW | MERGED | SA | Review round APPROVED, no open BLOCKER; branch merged locally (`git merge --no-ff`); `merge_commit` set |
| CHANGES_REQUESTED | IN_PROGRESS | BE / FE | — |
| MERGED | TESTING | TEST | — |
| TESTING | BUG | TEST | Test run FAIL with bug details; `test_iteration += 1` |
| TESTING | READY_FOR_DEPLOY | TEST | Test run PASS, all AC checked |
| BUG | IN_PROGRESS | BE / FE | — |
| READY_FOR_DEPLOY | DEPLOYING | DEVOPS | PROD only: `approved_by` set by a human |
| DEPLOYING | RELEASED | DEVOPS | Deployment section filled, smoke check passed |
| any working state* | BLOCKED | any role | reason in History; set `blocked_from` |
| BLOCKED | `blocked_from` | HUMAN / SCRUM | explicit unblock with note; clear `blocked_from` |

\* Working states: READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, MERGED, TESTING, BUG,
READY_FOR_DEPLOY, DEPLOYING.

Any transition not in this table is forbidden (e.g. BACKLOG → MERGED, IN_PROGRESS → RELEASED).

Retry limits:
- If `review_iteration` is already 3 and SA would request changes again → `BLOCKED` instead.
- If `test_iteration` is already 3 and TEST would report BUG again → `BLOCKED` instead.

---

# 7. Roles and Permissions

| Role | Reads | Writes | Transitions | Forbidden |
|------|-------|--------|-------------|-----------|
| SCRUM | requirements, board, tasks, sprints | board, sprints, task metadata (priority, sprint, assignee) | BACKLOG→READY, unblock | code, designs, reviews |
| SA | requirement, architecture, ADRs, standards, relevant product code, diffs | designs, ADRs, new task files, Review sections, memory | CODE_REVIEW→CHANGES_REQUESTED / MERGED | editing product code |
| BE / FE | task, SA design, standards, relevant product code | product code on feature branch, Implementation section | READY/CHANGES_REQUESTED/BUG→IN_PROGRESS, IN_PROGRESS→CODE_REVIEW | merge, approve own work, change architecture without SA |
| TEST | requirement, AC, diff, existing tests | tests in product repo, Test section, bug notes, memory/lessons | MERGED→TESTING, TESTING→BUG / READY_FOR_DEPLOY | editing production code |
| DEVOPS | project.md, build/CI/deploy config, release notes | CI/deploy config, Deployment section | READY_FOR_DEPLOY→DEPLOYING→RELEASED | PROD without `approved_by` |
| HUMAN | everything | requirements, approvals | approve requirement, PROD approval, unblock | — |

---

# 8. Transition Protocol (the Agent Contract)

Every agent must follow these steps to change a task's state:

1. Read the task file fresh from disk (never rely on earlier context).
2. Check the transition is in §6 **and** allowed for your role.
3. Check the guard conditions. If not met → do not change status; explain what is missing.
4. Write your output section (Design / Implementation / Review round / Test run / Deployment).
5. Update frontmatter: `status`, counters, `blocked_from`, `branch`, `merge_commit`, `updated`.
6. Append one row to `## History`: time, from, to, role, short note.
7. Update the task's row in `tasks/board.md`.
8. Commit in the team repo: `[TASK-001] IN_PROGRESS -> CODE_REVIEW (BE): <note>`.
9. Report to the user: new status, what was done, the next role that should act.

Agent outcomes (reported in step 9 and History note):
`COMPLETED`, `FAILED`, `NEEDS_INPUT` (question for human), `BLOCKED`, `CHANGES_REQUESTED`.
On `FAILED` or `NEEDS_INPUT` the status does not change.

---

# 9. Operating Model (How to Run the Team in Cursor)

- **One chat = one role on one task.** Start a new chat per step to keep context small.
- Invoke a role by its skill, e.g.:
  - `/sa analyze REQ-001`
  - `/backend TASK-003`
  - `/sa review TASK-003`
  - `/tester TASK-003`
  - `/devops deploy TASK-003 STG`
  - `/scrum next` — reads the board and says which task and role should act next
- **Parallel work:** run several chats or background agents on different tasks. Each BE/FE task uses its
  own branch in `product/`. Only one agent edits a given task file at a time.
- **Human in the loop:** writes requirements, answers `NEEDS_INPUT`, approves PROD, unblocks tasks,
  and reviews commits.

---

# 10. Definition of Ready / Done

Ready (BACKLOG → READY):
- Requirement is clear and linked (`parent`)
- Assignee role is set
- ≥1 acceptance criterion
- Dependencies listed
- SA design exists (Design section or linked design doc)

Done (RELEASED), when applicable:
- All acceptance criteria checked
- Tests pass (unit, integration, automation)
- SA review approved, no open BLOCKER
- Deployment completed and recorded
- Docs / memory updated

---

# 11. Phase Roadmap

Each phase is a small set of markdown files. Build one phase at a time; commit after each.

## Phase 0 — Workspace Foundation

Deliver:
- `AGENTS.md`, `README.md`
- `docs/architecture/system-overview.md`
- ADR-0002 (markdown-driven, Cursor-native team)
- `project.md` (product repo path, stack, build/test commands, environments)
- `.gitignore` with `product/`

Acceptance:
- Workspace opens cleanly in Cursor; rules are explicit and understandable.

## Phase 1 — Task Format and Workflow Rule

Deliver:
- `templates/task.md`, `templates/examples/TASK-000-example.md`, `tasks/board.md`
- `.cursor/rules/workflow.mdc`: state table (§6), permissions (§7), Transition Protocol (§8)
- `.cursor/rules/task-files.mdc`: task file and board format

Acceptance:
- A sample task can be walked BACKLOG → RELEASED by following the rule manually.
- Asking an agent to make a forbidden transition (e.g. BACKLOG → MERGED) is refused.

## Phase 2 — Role Contracts

Deliver:
- Skill skeletons for all roles: purpose, files to read, output section format, allowed transitions,
  forbidden actions, outcome reporting.

Acceptance:
- Each skill states exactly what it reads, what it writes, and which transitions it may perform.

## Phase 3 — SA Skill (Analysis & Design)

Deliver:
- `templates/requirement.md`, `templates/design.md`
- `.cursor/skills/sa/SKILL.md` — analyze mode

Gate: the requirement's `status` must be `APPROVED` (set by a human). Blocking questions → design doc
with Open Questions only, `NEEDS_INPUT`, no tasks.

SA analyze produces:
- `docs/design/REQ-###-design.md`: functional/non-functional requirements, architecture, APIs,
  data model changes, dependencies, risks, assumptions, open questions, task breakdown
- Task files (BACKLOG) with acceptance criteria and assignee role
- ADR when an architectural decision is made (+ row in `memory/decisions.md`)
- Requirement set to `ANALYZED`; one commit `[REQ-###] analyzed (SA): ...`

Acceptance:
- Given a requirement, SA produces a design doc and well-formed task files; no product code changed.

## Phase 4 — Backend Skill

Deliver:
- `.cursor/skills/backend/SKILL.md`
- `docs/standards/backend.md` for the product stack
- ADR-0003 product stack: Java 21 + Spring Boot 4.0.x microservices (Maven, PostgreSQL per service, Flyway),
  React + TypeScript (Vite) frontend; FE standards follow in Phase 8
- `project.md` filled (layout `services/<name>-service/`, `frontend/`, commands, local notes)
- `product/` initialised as its own git repo (branch `main`)

BE flow: read task + design → inspect relevant product files → create branch
`feature/TASK-###-slug` → implement → run tests → review own `git diff` → commit in product repo
(push the branch only if a remote exists, as backup) → fill Implementation → IN_PROGRESS → CODE_REVIEW.
No PR/MR is created: the review happens in the task file.

Acceptance:
- BE completes a small real feature in `product/` on a branch, tests pass, task moves to CODE_REVIEW.

## Phase 5 — SA Review Skill

Deliver:
- Review mode in `.cursor/skills/sa/SKILL.md`

SA review: read task, AC, design, `git diff main...branch` → check correctness, AC coverage, standards,
security, tests → write Review round → CHANGES_REQUESTED (with comments) or APPROVED →
`git merge --no-ff` into `main` in `product/` → record `merge_commit` → MERGED. Enforce review limit.

Acceptance:
- **MVP loop works end-to-end** (§17).

## Phase 6 — Guardrails

Deliver:
- `scripts/check_transitions.py` + versioned git hook `.githooks/pre-commit`
  (`git config core.hooksPath .githooks`): rejects commits where a task's `status` changes by a transition
  not in §6 or by a role not allowed, History is edited or not appended with exactly one matching row,
  counters/limits, `blocked_from`, `merge_commit`, `release` are wrong, `approved_by` is set without a
  HUMAN History row, a new task does not start in BACKLOG, or a task file is deleted.
- `.cursor/hooks.json` `beforeShellExecution` → `.cursor/hooks/guard-shell.sh` (fail closed): deny
  `git push --force`, direct push to `main` in `product/`, `git commit --no-verify`, destructive commands
  (`rm -rf`, `DROP`, `TRUNCATE`); ask for approval on PROD deploy commands.

Acceptance:
- An invalid transition commit is rejected; a forbidden shell command is blocked.

## Phase 7 — Test Skill

Deliver:
- `.cursor/skills/tester/SKILL.md`, `docs/standards/testing.md`

Test flow: MERGED → TESTING → build + automated tests on `main` → black-box acceptance check per AC
(run the service, record command + actual output as evidence) → PASS → READY_FOR_DEPLOY, or FAIL → BUG with
reproduction steps, expected vs actual, logs. Append recurring issues to `memory/lessons.md`.
TEST does not commit to `product/`: automated tests (incl. bug regression tests) are written by BE/FE and
reviewed by SA, so every product change still passes SA review.

## Phase 8 — Frontend Skill

Deliver:
- `.cursor/skills/frontend/SKILL.md`, `docs/standards/frontend.md`
- Same boundary and flow as Backend. The first FE task creates `product/frontend/` with `create-vite`
  (react-ts); FE verify = `npm run lint && npm test -- --run && npm run build`.

## Phase 9 — DevOps Skill

Deliver:
- `.cursor/skills/devops/SKILL.md`, `docs/standards/devops.md`, `templates/release.md`

Direction (decided by the human, details in an ADR when the phase starts): CI/CD with GitHub Actions;
Docker Compose first, Kubernetes later; FE and BE may move to separate repos for deployment.

Flow: build → package → deploy DEV/STG/UAT per `project.md` → smoke check → Deployment section.
PROD only when `approved_by` is set by a human. Rollback steps recorded.
Each release is a `releases/REL-###.md` file: version, included tasks, environments deployed, approval,
rollback plan. Released tasks get `release: REL-###`.

## Phase 10 — Scrum Skill

Deliver:
- `.cursor/skills/scrum/SKILL.md`, `templates/sprint.md`

Scrum modes:
- `next`: pick the next actionable task and role (respect dependencies, priority, BLOCKED)
- `ready`: check Definition of Ready, move BACKLOG → READY
- `sprint`: create/organize `sprints/SPRINT-##.md`
- `sync`: rebuild `tasks/board.md` from task files
- `report`: progress, blockers, cycle time, review/test iterations (computed from History)

---

# 12. Context Management

Each skill lists exactly what to read. Do not read other files unless needed.

| Role | Context |
|------|---------|
| SA analyze | requirement, `docs/architecture/`, relevant ADRs, `memory/decisions.md`, product structure (listing only) |
| SA review | task file, design doc, standards, `git diff main...branch`, `memory/lessons.md` |
| BE / FE | task file, design doc, standards, files found by search in `product/`, related tests |
| TEST | requirement, task AC, diff, existing tests, `memory/lessons.md` |
| DEVOPS | `project.md`, build/CI/deploy config, task Deployment history |
| SCRUM | `tasks/board.md`, task frontmatter only, current sprint |

---

# 13. Memory Model

| Level | Where |
|-------|-------|
| Short-term | current chat + current task file |
| Project | `AGENTS.md`, `docs/architecture/`, `docs/standards/`, `project.md` |
| Decision | `docs/adr/`, `memory/decisions.md` |
| Historical | `memory/lessons.md`, task History tables, git log |

Agents append to `memory/lessons.md` when a review finding or bug is likely to recur.

---

# 14. Observability and Audit

- Every transition: History row + team-repo commit `[TASK-###] FROM -> TO (ROLE): note`.
- Every code change: product-repo commit referencing the task id.
- Metrics (computed by Scrum `report` from History): cycle time, review iterations, test iterations,
  BLOCKED count, human interventions.

---

# 15. Safety and Guardrails

| Guardrail | Mechanism |
|-----------|-----------|
| Valid transitions only | workflow rule + `pre-commit` check |
| Review/test loop limits | counters in frontmatter + rule |
| No self-merge / self-approve | role permissions; SA merges only after its own review of BE/FE work |
| PROD approval | `approved_by` field, rule + hook asks for approval |
| Destructive commands | `beforeShellExecution` hook |
| Secrets | never in markdown or commits; `.env` git-ignored |
| Scope | agents read only files listed in §12 |

---

# 16. Limitations (and Mitigations)

- **Rules are guidance, not enforcement.** An agent can still make a mistake.
  → git `pre-commit` check, hooks, and human review of commits.
- **Concurrent edits to `board.md`.** → board is only an index; `scrum sync` rebuilds it; one agent per task.
- **No automatic scheduling.** Agents run when a human starts a chat. → `scrum next` tells you what to run.
- **Context size.** → one chat per step, strict read lists.

---

# 17. MVP Completion Criteria

The following flow works end-to-end on a small real feature in `product/`:

Requirement → SA analyze → design + task → BE implement → CODE_REVIEW → SA review → CHANGES_REQUESTED
→ BE fix → SA review → APPROVED → MERGED

with a correct History table and one commit per transition.

Do not add Test, FE, DevOps, Scrum automation until this loop is stable.

---

# 18. Cursor Prompts per Phase

## Phase 1
"Read AGENTS.md and §5–§8 of the plan. Create `templates/task.md`, `tasks/board.md` and
`.cursor/rules/workflow.mdc`. Only markdown. Then create a sample task and show a forbidden transition
being refused."

## Phase 3
"Create the SA skill in analyze mode following §7, §8, §11 Phase 3 and §12. The SA must not edit
`product/`. Test it with `requirements/REQ-001-*.md`."

## Phase 4
"Create the Backend skill following §7, §8, §11 Phase 4 and §12. Test it on the first READY task."

## Phase 5
"Add review mode to the SA skill following §6 retry limits and §11 Phase 5. Run the full MVP loop."

---

# 19. Evolution (Optional, Later)

Markdown stays the only control plane. No Jira or external tracker is planned.

- Custom subagents per role for parallel execution from one chat.
- Scheduled/background agents running `scrum next` automatically.
- Search over `memory/` and history as it grows.

---

# 20. Final Engineering Principle

Do not build six independent chatbots.

Build one controlled delivery workflow where:
- markdown holds the state,
- rules and guardrails control transitions,
- skills give each agent a clear role,
- git records every decision,
- humans approve what matters.
