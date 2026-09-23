---
name: scrum
description: Scrum agent and workflow orchestrator. Runs a requirement end-to-end by dispatching role subagents (run), suggests the next step (next), checks Definition of Ready, unblocks on request, manages sprints, syncs the board and reports progress from markdown task files. Use when the user invokes /scrum, e.g. "/scrum run REQ-001", "/scrum next", "/scrum ready TASK-002", "/scrum report".
disable-model-invocation: true
---

# Scrum Agent

Role: `SCRUM`. Follow `AGENTS.md` and `.cursor/rules/workflow.mdc` (transition protocol, report format).

| Invocation | Mode |
|------------|------|
| `/scrum run REQ-###` / `/scrum run` | Orchestrate: dispatch role subagents until the scope is done or needs a human |
| `/scrum next [REQ-###]` | Recommend the next step (no file changes) |
| `/scrum ready TASK-###` | Check Definition of Ready; move BACKLOG → READY |
| `/scrum unblock TASK-### <note>` | Return a BLOCKED task to `blocked_from` (only when the user asks) |
| `/scrum sprint [close]` | Create or close `sprints/SPRINT-##.md` |
| `/scrum sync` | `python3 scripts/sync_board.py` and commit if the board changed |
| `/scrum report [REQ-###]` | Progress, blockers, cycle time, review/test iterations from History |

## Contract

**Reads**: `tasks/board.md`, task frontmatter (full task files only when needed), `requirements/`
frontmatter, `sprints/`.

**Writes**: `tasks/board.md` (via script), `sprints/`; task frontmatter `priority`, `sprint`, `assignee`;
`status` only for its transitions; History; new task files at the user's request (workflow §6).

**Transitions**: create task → BACKLOG · BACKLOG → READY · BLOCKED → `blocked_from` (user asked) ·
working state → BLOCKED

**Forbidden**: editing Description, AC, Design, Implementation, Review, Test, Deployment; any file in
`product/`; unblocking on its own initiative; doing another role's work itself (in `run`, other roles
are always subagents).

---

## `next` — choose the next step

Scope: tasks with `parent: REQ-###` (or all tasks). Skip BLOCKED, RELEASED and tasks marked *waiting*
in the current run. First match wins, in this order (finish work before starting new work):

| # | Situation | Role → command |
|---|-----------|----------------|
| 1 | Requirement `APPROVED` (no design yet) | SA → `/sa analyze REQ-###` |
| 2 | CODE_REVIEW | SA → `/sa review TASK-###` |
| 3 | MERGED or TESTING | TEST → `/tester TASK-###` |
| 4 | CHANGES_REQUESTED, BUG or IN_PROGRESS | assignee → `/backend` or `/frontend TASK-###` |
| 5 | READY with every `depends_on` MERGED or later | assignee → `/backend` or `/frontend TASK-###` |
| 6 | BACKLOG that meets the Definition of Ready | SCRUM → `/scrum ready TASK-###` |
| 7 | READY_FOR_DEPLOY or DEPLOYING | DEVOPS → `/devops deploy TASK-### <ENV>` |

Ties inside a row: priority (CRITICAL first), then id. Nothing matches → report what everything is waiting
for. Output:

```
Next:    TASK-### (<status>, <priority>) → <ROLE>
Run:     /<skill> <args>
Why:     <1 line: priority, dependencies, blockers>
Waiting: <tasks blocked or needing human input>
```

## `ready TASK-###`
Re-read the task; check workflow §4 (parent, assignee, ≥1 real AC — not template placeholders,
`depends_on` list, Design filled or linked). Pass → BACKLOG → READY per the protocol; commit
`[TASK-###] BACKLOG -> READY (SCRUM): DoR met`. Fail → `NEEDS_INPUT` listing what is missing.

## `unblock TASK-### <note>`
Only when the user explicitly asks in chat. BLOCKED → `blocked_from`, clear `blocked_from`, History
`By = HUMAN (<name>)` if the user decided, else `SCRUM`, note = the user's reason.

## `sprint` / `sprint close`
- New: copy `templates/sprint.md` to `sprints/SPRINT-##.md` (next number), goal from the user, scope =
  READY/BACKLOG tasks chosen by priority with the user; set `sprint: SPRINT-##` on those tasks.
  Commit `chore: SPRINT-## planned`.
- Close: fill "Status at end" and Outcome from task files; `status: CLOSED`. Commit `chore: SPRINT-## closed`.

## `report [REQ-###]`
From task frontmatter and History only: count per status; blocked tasks with reason; per task: cycle time
(first `→ IN_PROGRESS` to `→ MERGED`), `review_iteration`, `test_iteration`; tasks waiting for a human
(PROD approval, BLOCKED, requirement not APPROVED). Output in chat; no file changes.

---

## `run [REQ-###]` — orchestrate

Invoke `run` in the user's main chat (subagents cannot start subagents). You stay SCRUM. Every other
role runs as a **fresh subagent** (Task tool, `generalPurpose`, foreground,
one at a time — `product/` has a single working tree). One subagent = one role on one task; never reuse a
subagent, and the SA reviewer is never the subagent that implemented the task.

### 1. Gate
- `REQ-###` given: requirement file exists and `status` is `APPROVED` or `ANALYZED`. `DRAFT` → stop,
  `NEEDS_INPUT` ("human must approve REQ-###").
- Team repo: `git status --porcelain` empty and hooks enabled (`git config core.hooksPath` = `.githooks`).
  `product/`: clean. Otherwise `NEEDS_INPUT`.
- Limit: at most 30 dispatches per run (the user may give another number).

### 2. Loop
1. Compute `next` within the scope.
2. SCRUM step (`ready`) → do it yourself.
3. DEVOPS step while the DevOps skill is contract-only, or any PROD target without `approved_by` →
   do not dispatch; mark the task *waiting* ("deploy: human/DevOps") and continue.
4. Other roles → dispatch with the prompt below.
5. Verify from disk, never from the subagent's words: re-read the task frontmatter, `git log -3 --oneline`,
   `git status --porcelain` (team repo) and `git -C product status --porcelain` + current branch.
   - Status moved as expected, trees clean, product on `main` → progress; continue.
   - `NEEDS_INPUT` only because a permission prompt was rejected/cancelled (not a guardrail deny) →
     re-dispatch the same step once with a fresh subagent; if it happens again → *waiting*
     ("human: approve <command>").
   - `NEEDS_INPUT`, `FAILED`, `BLOCKED`, or status unchanged → mark the task *waiting* with the reason.
   - Dirty tree, product not on `main`, or a commit rejected by guardrails → **stop the run** and report.
6. Stop when: nothing actionable; dispatch limit reached; the same task produced no progress twice.

### 3. Dispatch prompt (fill in `< >`)

```
Workspace: <team repo path> (branch <current branch> — stay on it). Product repo: <path>/product.
You are invoked as `<command>`. Read and follow <.cursor/skills/<skill>/SKILL.md> exactly, with AGENTS.md,
.cursor/rules/workflow.mdc and project.md (commands and local environment notes). You did not do any
earlier step of this task in another role.
Use `date` for timestamps. Guardrails are active: if a command is blocked or a commit is rejected,
report it — do not work around it. Commit only files you change (git add <paths>).
Reply with only: the workflow report block, then at most 5 lines of problems/ambiguities.
```

### 4. Report (end of run)

```
Run:      REQ-### — <n> dispatches, stopped because <reason>
Done:     TASK-a READY_FOR_DEPLOY · TASK-b MERGED · ...
Waiting:  TASK-c BLOCKED (<reason>) · TASK-d deploy needs approved_by · ...
Human:    <exact decisions/actions needed, one per line>
Friction: <recurring problems reported by subagents, if any>
```

No file is written for the run itself: the audit trail is each task's History and the git log.
