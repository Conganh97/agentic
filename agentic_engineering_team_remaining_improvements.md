# Agentic Engineering Team — Remaining Improvements

This file contains **only the items that are not yet fully implemented or should be improved** in the current framework.

Already completed and intentionally excluded:
- Workspace foundation
- Task format
- Basic workflow rule
- Role contracts
- SA analyze
- Backend skill
- SA review + merge
- Pre-commit / shell guardrails
- Test skill
- Frontend skill
- Basic Scrum orchestration
- `/repo` create/push
- Git main-branch protection

---

# P0 — Must Fix Before Calling the Workflow Robust

## 1. Harden the State Machine

### Problem

The current workflow has the main task states, but transition authority and transition evidence need to be made explicit and enforced consistently.

### TODO

- [x] Define exact allowed transitions for every task state.
- [x] Define which role is allowed to perform each transition.
- [x] Prevent agents from directly changing states they do not own.
- [x] Add `FAILED` as a state separate from `BUG`.
- [x] Define recovery behavior for every failure state.
- [x] Enforce review/test retry limits at the workflow level, not only in prompts.

### Target

```text
BACKLOG
→ READY
→ IN_PROGRESS
→ CODE_REVIEW
→ CHANGES_REQUESTED
→ IN_PROGRESS
→ CODE_REVIEW
→ MERGED
→ TESTING
→ BUG
→ IN_PROGRESS
→ CODE_REVIEW
→ MERGED
→ TESTING
→ READY_FOR_DEPLOY
→ DEPLOYING
→ RELEASED
```

Execution failure should be separate:

```text
FAILED
→ retry / recover / BLOCKED
```

---

# P0 — Orchestrator Hardening

## 2. Make `/scrum run` a True State-Machine Executor

### Problem

`/scrum run` exists, but it should be treated as the central execution engine rather than a sequence of role instructions.

### TODO

- [x] Read current requirement/task state before every action.
- [x] Determine the next action from state + dependencies.
- [x] Validate preconditions before dispatching an agent.
- [x] Dispatch the correct role.
- [x] Validate the agent's output artifacts.
- [x] Perform the state transition only after validation.
- [x] Continue until terminal state or human gate.
- [x] Never assume that the previous step succeeded.
- [x] Resume from current state if Cursor stops or the run is interrupted.

### Target

```text
read state
    ↓
validate
    ↓
find next action
    ↓
dispatch agent
    ↓
validate output
    ↓
record transition
    ↓
repeat
```

---

# P0 — Task Dependencies

## 3. Build a Real Dependency Graph

### Problem

`depends_on` exists, but the orchestrator needs to actively use it to determine what can run.

### TODO

- [x] Validate `depends_on`.
- [x] Prevent a task from becoming `READY` while required dependencies are incomplete.
- [x] Make `/scrum next` dependency-aware.
- [x] Make `/scrum run` dependency-aware.
- [x] Detect circular dependencies.
- [x] Select actionable tasks automatically.
- [x] Allow independent BE/FE tasks to execute in parallel.

### Example

```text
TASK-001 Database
       │
       ▼
TASK-002 Backend
       │
       ├──────────┐
       ▼          ▼
TASK-003 FE    TASK-004 Test
```

The orchestrator must not start TASK-003 before TASK-002 if that dependency exists.

---

# P0 — Test Traceability

## 4. Connect Acceptance Criteria to Test Cases

### Problem

The current Test role can validate the requirement, but the workflow should have machine-readable traceability.

### TODO

- [x] Give every acceptance criterion an ID.
- [x] Example: `AC-001`, `AC-002`, `AC-003`.
- [x] Create test-case artifacts.
- [x] Map each test case to one or more ACs.
- [x] Require evidence for important test results.
- [x] Prevent `READY_FOR_DEPLOY` if required ACs are not covered.
- [x] Store PASS / FAIL / NOT_APPLICABLE explicitly.

### Target

```text
REQ-001
   │
   ├── AC-001
   ├── AC-002
   └── AC-003
         │
         ▼
       Tests
         │
         ▼
      Evidence
```

---

# P0 — Bug Lifecycle

## 5. Make BUG a Separate Artifact

### Problem

`BUG` should not only be a task state. A failed test needs a persistent defect record.

### TODO

- [x] Create `bugs/BUG-###.md`.
- [x] Link BUG → requirement.
- [x] Link BUG → task.
- [x] Link BUG → failed AC.
- [x] Store expected vs actual behavior.
- [x] Store reproduction steps.
- [x] Store test evidence.
- [x] Store fix commit.
- [x] Require regression testing before closing the BUG.

### Target

```text
TEST
 ↓
FAIL
 ↓
BUG-001
 ↓
IN_PROGRESS
 ↓
CODE_REVIEW
 ↓
MERGED
 ↓
REGRESSION_TESTING
 ↓
CLOSED
```

---

# P0 — Artifact Validation

## 6. Make Agent Handoffs Artifact-Based

### Problem

Fresh subagents are good, but they must communicate through repository artifacts rather than conversation context.

### TODO

Define required input/output artifacts for each role.

### SA → BE / FE

```text
REQ
+
design
+
TASK
+
dependencies
+
technical acceptance criteria
```

### BE / FE → SA Review

```text
TASK
+
code
+
tests
+
branch/commit evidence
```

### SA → TEST

```text
REQ
+
AC
+
TASK
+
merged commit
```

### TEST → Scrum

```text
test report
+
AC results
+
evidence
+
BUG references
```

---

# P0 — Git / Merge Integrity

## 7. Strengthen the Existing Merge Invariant

The existing Git guardrails are good; add stronger workflow validation.

### TODO

- [x] A task may become `MERGED` only after an explicit SA approval artifact.
- [x] Store `merge_commit` in the task.
- [x] Verify `merge_commit` exists on `main`.
- [x] Verify the merge was `--no-ff`.
- [x] Reject `MERGED` state if evidence is missing.
- [x] Make TEST always test the merged revision, not the feature branch.

### Target

```text
Feature Branch
      ↓
SA Review
      ↓
APPROVED
      ↓
--no-ff MERGE
      ↓
main
      ↓
TEST
```

---

# P1 — Requirement Consistency

## 8. Add Requirement Revisioning

### Problem

A requirement can potentially change while agents are implementing it.

### TODO

Add:

```yaml
revision: 1
```

and optionally:

```yaml
content_hash: sha256:...
```

Tasks should record:

```yaml
requirement: REQ-001
requirement_revision: 1
```

If the requirement changes:

```text
REQ revision 1
      ↓
REQ revision 2
```

the orchestrator must detect that existing tasks were created against an older revision.

### Expected behavior

```text
BLOCKED
reason: requirement_changed
```

Do not silently continue.

---

# P1 — Human Risk Gates

## 9. Add Generic Human Approval Gates

### Problem

Not every change should be autonomous.

### TODO

Stop the workflow for:

- [x] Destructive DB migration.
- [x] Dropping tables/columns.
- [x] Breaking API changes.
- [x] Security-sensitive changes.
- [x] Authentication/authorization changes.
- [x] Data deletion.
- [x] Infrastructure destruction.
- [x] Major architecture changes.
- [x] Production deployment.

Use:

```yaml
human_gate:
  required: true
  reason:
  approved_by:
  approved_at:
```

---

# P1 — Parallel Execution

## 10. Parallelize Independent BE / FE Tasks

### Problem

The current flow describes BE/FE implementation but does not fully define safe parallel execution.

### TODO

- [x] Detect independent tasks.
- [x] Dispatch independent tasks in parallel.
- [x] Keep dependent tasks sequential.
- [x] Detect potential repository/file conflicts.
- [x] Wait for all required tasks before SA review.

### Target

```text
             SA
              │
       ┌──────┴──────┐
       ▼             ▼
      BE             FE
       │             │
       └──────┬──────┘
              ▼
          SA REVIEW
```

---

# P1 — Failure Recovery

## 11. Separate BUG from Execution Failure

### BUG

Product behavior is wrong.

Examples:

```text
Wrong API response
Incorrect business rule
UI behavior does not match AC
```

### FAILED

The workflow itself could not execute.

Examples:

```text
Build failure
Git conflict
Docker unavailable
Dependency download failure
Permission failure
Test environment unavailable
```

### TODO

- [x] Add `FAILED` state.
- [x] Store failure type.
- [x] Store failure step.
- [x] Store retry count.
- [x] Store last failure message.
- [x] Mark whether the failure is recoverable.
- [x] Resume from the failed step.

Example:

```yaml
failure:
  type:
  step:
  message:
  retry_count:
  recoverable:
```

---

# P1 — Recovery / Resume

## 12. Make `/scrum run` Idempotent and Resumable

### TODO

Test scenarios:

- [x] Cursor closes during SA analysis.
- [x] Cursor closes during BE implementation.
- [x] Agent permission is rejected.
- [x] Git push fails.
- [x] SA review fails.
- [x] Test fails.
- [x] Docker fails.
- [x] A task becomes BLOCKED.

Then run:

```text
/scrum run REQ-001
```

Expected behavior:

```text
resume from current valid state
```

not:

```text
start everything again
```

---

# P1 — Transition Evidence

## 13. Add Evidence to Every Important Transition

Example:

```yaml
transition:
  from: CODE_REVIEW
  to: MERGED
  actor: SCRUM
  timestamp:
  evidence:
    review: reviews/TASK-001-review-02.md
    merge_commit: abc123
```

For TEST:

```yaml
transition:
  from: TESTING
  to: READY_FOR_DEPLOY
  actor: TEST
  timestamp:
  evidence:
    report: tests/TASK-001-report.md
```

### TODO

- [x] Define evidence requirements per transition.
- [x] Validate evidence before state change.
- [x] Store evidence references in task/history.

---

# P1 — Requirement Lifecycle

## 14. Track Requirement-Level Progress

The current task state machine is detailed, but the requirement should also have a lifecycle.

Suggested:

```text
DRAFT
→ APPROVED
→ ANALYZING
→ ANALYZED
→ IN_PROGRESS
→ TESTING
→ READY_FOR_RELEASE
→ RELEASED
```

Also:

```text
BLOCKED
CANCELLED
```

### TODO

- [x] Update requirement template.
- [x] Update Scrum report.
- [x] Derive requirement status from task progress where appropriate.
- [x] Prevent requirement from being marked complete while required tasks remain incomplete.

---

# P2 — Reporting / Observability

## 15. Improve `/scrum report`

Add:

- [x] Review rounds.
- [x] Test rounds.
- [x] BUG count.
- [x] FAILED count.
- [x] Blocked tasks.
- [x] Cycle time.
- [x] Retry count.
- [x] Human gates.
- [x] Dependency blockers.

---

## 16. Improve Execution History

Every transition should contain:

```text
run_id
timestamp
actor
requirement
task
from
to
reason
evidence
```

Example:

```text
RUN-001
REQ-001
TASK-002
BE
IN_PROGRESS → CODE_REVIEW
reason: implementation completed
evidence: commit abc123
```

---

# P2 — Sprint Separation

## 17. Keep Sprint Planning Separate from Execution

Recommended:

```text
Product Backlog
      ↓
Sprint Planning
      ↓
Sprint
      ↓
Requirement
      ↓
/scrum run
      ↓
Engineering Workflow
```

### TODO

- [x] Keep `/scrum run` focused on execution.
- [x] Use Sprint for planning/prioritization.
- [x] Link requirements/tasks to a Sprint when applicable.
- [x] Do not make Sprint state a prerequisite for autonomous requirement execution unless explicitly required.

---

# P1 — Phase 9 DevOps

## 18. Implement DevOps

Current status: contract only.

### TODO

### CI

```text
Checkout
→ Build
→ Unit Test
→ Integration Test
→ Static Analysis
→ Package
→ Docker Build
```

### Deployment

```text
READY_FOR_DEPLOY
→ DEPLOYING
→ DEPLOYED
→ RELEASED
```

### Environments

```text
DEV
STG
UAT
PROD
```

### Production

Require:

```yaml
approved_by:
approved_at:
```

### Rollback

Track:

```text
previous_version
current_version
rollback_version
rollback_reason
```

---

# Recommended Order

Do not implement everything at once.

## Step 1 — Workflow Core

- [x] 1. Harden State Machine — `FAILED` + recovery; hook enforces table (`workflow.mdc`, `check_transitions.py`)
- [x] 2. Harden `/scrum run` — read/validate/next/dispatch/validate loop; resume from disk (scrum skill)
- [x] 3. Dependency Graph — `scripts/deps.py`; READY/IN_PROGRESS require deps MERGED-or-later
- [x] 7. Git / Merge Integrity — `merge_commit` sha + latest Review APPROVED; TEST on `main`
- [x] 13. Transition Evidence — workflow §8; History Note required by the hook

## Step 2 — Quality Loop

- [x] 4. AC → Test Traceability — `AC-001` ids; TEST maps pass/fail; READY_FOR_DEPLOY rejects unchecked ACs
- [x] 5. BUG Lifecycle — `templates/bug.md`, `bugs/`; TEST creates a file on FAIL
- [x] 6. Artifact-Based Handoff — `docs/standards/artifacts.md` + reviews/tests/runs files

## Step 3 — Autonomous Execution

- [x] 8. Requirement Revisioning — `revision` / `requirement_revision`; run stops on mismatch
- [x] 9. Human Risk Gates — `human_gate` + `approved_by`; run waits
- [x] 10. Parallel Execution — independent READY tasks in different repos may dispatch together
- [x] 11. Failure Recovery — `FAILED` / `failed_from` / `failure`
- [x] 12. Resume / Idempotency — `/scrum run` continues from current status
- [x] 14. Requirement Lifecycle — template statuses; report roll-up (no auto-write yet)

## Step 4 — DevOps

- [ ] 18. CI/CD
- [ ] Deployment
- [ ] Environment management
- [ ] Production approval
- [ ] Rollback

## Step 5 — Polish

- [x] 15. Scrum Reporting — FAILED, bugs, human gates, dep blockers
- [x] 16. Execution History — `runs/journal.md` + `scripts/run_log.py` (`run_id` in each row)
- [x] 17. Sprint Separation — sprint is planning only; run does not require a sprint

---

# Target After Improvements

```text
                         HUMAN
                           │
                     APPROVE REQ
                           │
                           ▼
                    /scrum run REQ
                           │
                           ▼
                    ORCHESTRATOR
                           │
                           ▼
                           SA
                    Design + Tasks
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
                 BE                 FE
                  │                 │
                  └────────┬────────┘
                           ▼
                       SA REVIEW
                       /                       CHANGES       APPROVED
                   │              │
                   └──────┐       ▼
                          │      MERGE
                          │       │
                          │       ▼
                          │      TEST
                          │       │
                          │    ┌──┴──┐
                          │    ▼     ▼
                          │   BUG   PASS
                          │    │     │
                          └────┘     ▼
                              READY_FOR_DEPLOY
                                      │
                                      ▼
                                    DEVOPS
                                      │
                                  RELEASED
```

The key goal is:

```text
One requirement
      ↓
One `/scrum run`
      ↓
Autonomous execution
      ↓
Human only at explicit gates
      ↓
Complete Markdown + Git audit trail
```
