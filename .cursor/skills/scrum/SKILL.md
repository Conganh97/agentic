---
name: scrum
description: Scrum orchestrator. /scrum run dispatches role subagents; also next, ready, sprint, report. Use when invoked as /scrum, e.g. "/scrum run REQ-002".
disable-model-invocation: true
---

# Scrum

Role: `SCRUM`. `AGENTS.md` + `.cursor/rules/workflow.mdc`. Next step is **disk**, not memory:
`python3 scripts/next.py [REQ-###]` · `deps.py --json` · `parallel.py` · `sprint.py`.

| Invocation | Does |
|------------|------|
| `/scrum run [REQ-###]` | Loop: read → validate → next → dispatch → verify artifacts |
| `/scrum next [REQ-###]` | Print next step, no writes |
| `/scrum ready TASK-###` | DoR + deps → BACKLOG → READY |
| `/scrum unblock TASK-### <note>` | Only if the user asks. BLOCKED → `blocked_from` |
| `/scrum sprint [close]` | Plan/close when unfinished > 5 (`SMALL_MAX=5`, `SPRINT_CAP=6`) |
| `/scrum sync` | `sync_board.py` |
| `/scrum report [REQ-###]` | Paste `scrum_report.py` output |

**Writes:** board (via script), `sprints/`, task `priority`/`sprint`/`assignee`, **SCRUM-owned**
transitions only (`BACKLOG → READY`, unblock, REQ `ANALYZED → IN_PROGRESS` when the first child
leaves BACKLOG), History, new tasks if asked.
**Forbidden:** AC/Design/Implementation/Review/Test/Deployment; `product/`; another role’s
execution transitions (`IN_PROGRESS`, `CODE_REVIEW`, `MERGED`, `TESTING`, `RELEASED`, …).
In `run`, other roles are always subagents. Do not check task AC boxes.

## `ready` / `sprint` / `report`

**ready:** workflow §4 + `deps.py` + sprint stamp matches ACTIVE (if any). Pass → protocol commit
`[TASK-###] BACKLOG -> READY (SCRUM): DoR met`. Fail → `NEEDS_INPUT`.

**sprint:** `sprint.py`. ≤5 unfinished → no sprint. >5 → ACTIVE file; only `sprint: SPRINT-##`
is pulled (in-flight always continues). Plan = first dep layer, `templates/sprint.md`, stamp
tasks, `chore: SPRINT-## planned`. Close when scoped tasks MERGED-or-later.

**report:** never hand-count. REQ `RELEASED` only if `req.py check` passes (DEVOPS sets it).

## `run [REQ-###]`

Stay SCRUM. Every other role = **fresh** `generalPurpose` subagent, foreground. Never reuse.
Resume from disk; do not re-do finished work. Max 30 dispatches (or the number the user gave).

**Gate:** REQ `APPROVED`+ (not DRAFT/CANCELLED). Team tree clean, `core.hooksPath=.githooks`.
`repo.py status` clean on `main`. `deps.py` no cycles. Sprint `plan`/`close_and_plan` → do
`/scrum sprint` before new BACKLOG.

**Loop**

1. `next.py` (fresh).
2. SCRUM `ready`/`sprint` → do it yourself.
3. Skip dispatch if `human_gate` and no `approved_by`, or PROD without `approved_by`. DEV and
   STG deploy **are** dispatched. Mark *waiting* and continue.
4. Two READY tasks only if `parallel.py` lists the pair (different repos, no `depends_on` edge).
5. Else dispatch with the prompt below. Log:
   `run_log.py --run RUN-### --actor <ROLE> --req … --task … --from … --to …`
   Create `runs/RUN-###.md` from `templates/run.md` at start.
6. After each dispatch, **re-read disk** (`artifacts.md`: review/test/bug/`merge_commit`).
   `git log -3 --oneline`, team clean, `repo.py status`. Status + workflow §8 evidence → continue.
   Unchanged FAILED / dirty tree / product not on `main` / hook reject → *waiting* or **stop**.
7. If the parent REQ is still `ANALYZED` and a child left BACKLOG → set REQ `IN_PROGRESS`.
8. Stop: idle, limit, or same task no progress twice.

### Execution interruption

If a tool permission/request is cancelled: treat it as an interruption; retry the same dispatch
at most once; if it still cannot proceed, report the interruption. Classify as `NEEDS_INPUT`
only when actual human input is required.

Do not re-analyze an `ANALYZED`+ REQ unless PQA asked. Do not start BE/FE/UX/UI if already
CODE_REVIEW+. UX_UI and DEVOPS bootstrap stay MERGED (no TEST). After PQA accept →
dispatch `/devops deploy` (do not RELEASE tasks yourself). Accept FAIL → SA adds tasks;
leftover > 5 → side sprint.

### Dispatch prompt

```
Workspace: <team path> (stay on current branch). Product: <path>/product (project.md registry).
You are invoked as `<command>`. Skill: /uxui → ux-ui; /pqa → product-qa; /sa → sa;
/backend → backend; /frontend → frontend; /tester → tester; /devops → devops.
Follow that SKILL.md + AGENTS.md + workflow.mdc + project.md. You did not do an earlier
role on this task. Use `date` for timestamps. Do not bypass hooks. Commit only files you change.
Reply: workflow report block, then ≤5 lines of problems.
```

### End report

```
Run:      REQ-### — <n> dispatches, stopped because <reason>
Done:     TASK-a READY_FOR_DEPLOY · …
Waiting:  TASK-c BLOCKED (…) · deploy needs approved_by · …
Human:    <one action per line>
Friction: <recurring subagent problems>
```
