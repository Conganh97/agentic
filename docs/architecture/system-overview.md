# System Overview

## 1. Purpose

Automate the software development lifecycle with a team of specialized agents, while keeping
control, state, and approvals in a deterministic workflow.

```
Requirement → Scrum Planning → SA Analysis → Technical Design → Task Breakdown
→ BE/FE Implementation → SA Code Review ⇄ Fix Loop → Merge
→ Automation Test ⇄ Bug Fix Loop → DevOps Deployment → UAT → Release
```

## 2. Architecture at a glance

```
                USER
                  │
            ┌─────▼──────┐
            │ Scrum Agent│
            └─────┬──────┘
                  │
       ┌──────────▼──────────┐
       │    Orchestrator     │  ← owns task state, transitions, retries, approvals
       │   (State Machine)   │
       └──────────┬──────────┘
        ┌─────────┼─────────┐
        ▼         ▼         ▼
       SA        BE        FE          ← agents: analysis, design, coding
        └─────────┼─────────┘
                  ▼
              SA Review ── FAIL ──► Fix (back to BE/FE)
                  │ PASS
                  ▼
                Merge → TEST ── FAIL ──► BUG (back to BE/FE)
                          │ PASS
                          ▼
                       DevOps → DEV / STG / UAT → RELEASE (approval gate)

Supporting layers: Tool · Knowledge · Policy · Observability · Audit
```

## 3. Components

| Component | Responsibility |
|-----------|----------------|
| Orchestrator | Single source of truth for task state. Validates every transition, enforces retry limits and approval gates, decides which agent runs next and with which context and tools. |
| Agents | Stateless workers. Receive a structured request, return a structured, schema-validated response. Never mutate workflow state directly. |
| Tool Layer | Controlled capabilities (git, shell, test runner, CI, deployment). Access is scoped per agent by the Permission Model. |
| Knowledge Layer | Provides targeted context: AGENTS.md, architecture docs, ADRs, standards, requirements, relevant code. Files first; vector/code index later. |
| Policy Layer | Permissions, hard limits, approval gates, restricted paths, secret protection. |
| Observability / Audit | Records every agent execution and state transition. |

## 4. Agent roles and boundaries

| Agent | Does | Must not |
|-------|------|----------|
| Scrum | Create epics/stories/tasks/bugs, organize sprints, track progress and dependencies, report | Change code or task state outside the workflow |
| SA | Analyze requirements, technical design, task breakdown, acceptance criteria, code review (approve / request changes) | Modify production code, merge its own implementation, deploy production |
| BE / FE | Read repo, modify feature branch, run tests, commit, push, create PR | Merge PR, approve own PR, deploy production, change architecture without SA approval |
| Test | Create and run tests, analyze failures, create bug reports | Merge production code, deploy production |
| DevOps | Build, package, images, deploy DEV/STG/UAT per policy, rollback per policy | Deploy production without explicit approval |

## 5. Workflow state machine

States: `BACKLOG, READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, MERGED, TESTING, BUG,
READY_FOR_DEPLOY, DEPLOYING, RELEASED, BLOCKED`.

Allowed transitions:

```
BACKLOG           → READY
READY             → IN_PROGRESS
IN_PROGRESS       → CODE_REVIEW
CODE_REVIEW       → CHANGES_REQUESTED | MERGED
CHANGES_REQUESTED → IN_PROGRESS
MERGED            → TESTING
TESTING           → BUG | READY_FOR_DEPLOY
BUG               → IN_PROGRESS
READY_FOR_DEPLOY  → DEPLOYING
DEPLOYING         → RELEASED
<eligible state>  → BLOCKED
BLOCKED           → previous valid working state (explicit unblock only)
```

Anything else is rejected by the Orchestrator (e.g. `BACKLOG → MERGED`, `IN_PROGRESS → RELEASED`).
Detailed rules will be specified in `docs/architecture/workflow.md` during Phase 1.

## 6. Task domain model (initial)

`id, title, description, type, priority, status, assignee_agent, parent_task_id, dependencies,
acceptance_criteria, created_at, updated_at, sprint_id, repository, branch, pull_request,
review_iteration, test_iteration, metadata`

- Types: `EPIC, STORY, TASK, BUG, TECHNICAL_TASK`
- Priority: `LOW, MEDIUM, HIGH, CRITICAL`

## 7. Agent contract (summary)

Agents exchange structured data only:

```json
{ "agent": "SA", "task_id": "TASK-123", "status": "COMPLETED", "result": {} }
```

Execution statuses: `COMPLETED, FAILED, NEEDS_INPUT, BLOCKED, CHANGES_REQUESTED`.
Responses are validated against schemas. Full contract: `docs/architecture/agent-contract.md` (Phase 2).

## 8. Guardrails

- Max SA review iterations and max test-fix iterations (exceeding → `BLOCKED`, human intervention).
- Max tool execution time and restricted shell scope.
- Production deployment requires explicit approval.
- Destructive database commands are blocked.
- Secrets are never exposed to agent context.
- Restricted filesystem paths per agent.

## 9. Observability

Every agent execution records: `task_id, agent, execution_id, start_time, end_time, model,
tool calls, result, errors, retry count, token/cost metadata, state transition`.

## 10. Evolution

MVP loop first (SA → BE → SA Review → Merge). Then Test, FE, DevOps, Scrum agents; then
persistent workflow engine, PostgreSQL, Redis, event bus, RAG, code graph, security policies.
See `agentic_engineering_team_cursor_plan.md` §10 and §21.
