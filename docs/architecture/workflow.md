# Workflow — Task State Machine

Implementation: `orchestrator/src/main/java/com/agentic/orchestrator/workflow/TaskStateMachine.java`.

## States

`BACKLOG, READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, MERGED, TESTING, BUG,
READY_FOR_DEPLOY, DEPLOYING, RELEASED, BLOCKED`

## Transition table

| From | Allowed targets |
|------|-----------------|
| BACKLOG | READY |
| READY | IN_PROGRESS |
| IN_PROGRESS | CODE_REVIEW |
| CODE_REVIEW | CHANGES_REQUESTED, MERGED |
| CHANGES_REQUESTED | IN_PROGRESS |
| MERGED | TESTING |
| TESTING | BUG, READY_FOR_DEPLOY |
| BUG | IN_PROGRESS |
| READY_FOR_DEPLOY | DEPLOYING |
| DEPLOYING | RELEASED |
| RELEASED | — (terminal) |
| BLOCKED | — (only via explicit unblock) |

Every pair not in the table is rejected with `InvalidTransitionException`.

## BLOCKED

- Entered only through an explicit **block** action with a non-blank reason.
- Blockable states: `READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, MERGED, TESTING, BUG,
  READY_FOR_DEPLOY, DEPLOYING`. `BACKLOG` (not yet being worked on) and `RELEASED` (terminal) are not blockable.
- Left only through an explicit **unblock** action, which returns the task to the state it was blocked from.
- A blocked task rejects all normal transitions.

## Guards

- **Definition of Ready:** `BACKLOG → READY` requires at least one acceptance criterion
  (`TaskNotReadyException` otherwise).
- **Iteration counters:** `CODE_REVIEW → CHANGES_REQUESTED` increments `reviewIteration`;
  `TESTING → BUG` increments `testIteration`. Counters are never reset.
- **Retry limits** (`WorkflowLimits`, default 3/3): when a task that has already used
  `maxReviewIterations` requests changes again (or `maxTestIterations` for BUG), `TaskService`
  blocks it for human intervention instead of applying the transition.

## Immutability

`Task` has no setters and a private constructor. New tasks always start in `BACKLOG`.
Every state change returns a new `Task`; only `TaskService` persists it.

## Not yet covered (later phases)

- Which agent is allowed to request which transition (Phase 2/5 — permission model).
- Audit history of transitions (observability).
- Branch / pull request fields (Phase 4/6).
- Concurrency control on persistence (when a real database is introduced).
