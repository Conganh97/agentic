# Agentic Engineering Team — Cursor Implementation Plan

## 1. Objective

Build an Agentic Software Engineering Team that can manage a software development lifecycle from requirement to release.

The team consists of:

- Scrum Agent
- Solution Architect (SA) Agent
- Backend (BE) Agent
- Frontend (FE) Agent
- Test Agent
- DevOps Agent

Core lifecycle:

Requirement
→ Scrum Planning
→ SA Analysis
→ Architecture / Technical Design
→ Task Breakdown
→ BE / FE Implementation
→ SA Code Review
→ Fix Loop
→ Merge
→ Automation Test
→ Bug Fix Loop
→ DevOps Deployment
→ UAT
→ Release

The system must be workflow-driven. Agents provide intelligence and execution; the Orchestrator owns state and controls transitions.

---

# 2. Core Architecture Principles

## 2.1 Six core principles

1. Agent = intelligence
2. Workflow = control
3. Tools = capability
4. Knowledge = context
5. Policy = constraints
6. State = source of truth

## 2.2 Important rules

- Agents must never bypass workflow states.
- Agents must not arbitrarily modify task state.
- Agents must not merge their own PRs.
- Agents must not deploy production without an explicit approval gate.
- Every task must have acceptance criteria.
- Every code change must pass code review.
- Test failures must produce actionable bugs/tasks.
- Review and test loops must have a maximum retry count.
- All important decisions must be auditable.
- Prefer deterministic workflow execution over free-form agent collaboration.
- Do not allow an agent to invent repository state; repository state must come from tools.
- Avoid loading the entire repository into an agent context. Retrieve only relevant context.

---

# 3. Recommended Initial Stack

## Agent Layer

Python for the initial agent runtime.

Reason:
- Mature LLM/agent ecosystem
- Easy tool integration
- Good support for structured outputs
- Easy experimentation

## Control / Platform Layer

Initially keep the implementation simple.

Recommended future production stack:

- Java 21
- Spring Boot
- PostgreSQL
- Redis
- Kafka
- Temporal or an equivalent durable workflow engine

Do NOT introduce all infrastructure in Phase 1.

Start with:

- Python
- PostgreSQL or SQLite for local development
- Git
- Unit tests

Add Kafka, Redis, Temporal, Kubernetes, etc. only when required by the next phase.

---

# 4. Repository Structure

Initial repository:

agentic-engineering-team/

├── AGENTS.md
├── README.md
├── .gitignore
│
├── docs/
│   ├── architecture/
│   │   ├── system-overview.md
│   │   ├── agent-contract.md
│   │   ├── workflow.md
│   │   └── security.md
│   │
│   ├── requirements/
│   │
│   ├── adr/
│   │
│   └── standards/
│       ├── backend.md
│       ├── frontend.md
│       ├── testing.md
│       └── devops.md
│
├── orchestrator/
│   ├── app/
│   │   ├── domain/
│   │   ├── workflow/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── main.py
│   └── tests/
│
├── agents/
│   ├── sa/
│   ├── backend/
│   ├── frontend/
│   ├── tester/
│   ├── devops/
│   └── scrum/
│
├── tools/
│
├── knowledge/
│
└── infrastructure/

Do not create every implementation directory immediately. Create modules when their phase starts.

---

# 5. Workflow State Machine

Initial states:

- BACKLOG
- READY
- IN_PROGRESS
- CODE_REVIEW
- CHANGES_REQUESTED
- MERGED
- TESTING
- BUG
- READY_FOR_DEPLOY
- DEPLOYING
- RELEASED
- BLOCKED

Primary flow:

BACKLOG
→ READY
→ IN_PROGRESS
→ CODE_REVIEW
→ MERGED
→ TESTING
→ READY_FOR_DEPLOY
→ DEPLOYING
→ RELEASED

Review failure:

CODE_REVIEW
→ CHANGES_REQUESTED
→ IN_PROGRESS
→ CODE_REVIEW

Test failure:

TESTING
→ BUG
→ IN_PROGRESS
→ CODE_REVIEW
→ MERGED
→ TESTING

Blocked flow:

Any eligible state
→ BLOCKED

BLOCKED must require an explicit unblock action.

---

# 6. State Transition Rules

Allowed:

BACKLOG → READY

READY → IN_PROGRESS

IN_PROGRESS → CODE_REVIEW

CODE_REVIEW → CHANGES_REQUESTED

CODE_REVIEW → MERGED

CHANGES_REQUESTED → IN_PROGRESS

MERGED → TESTING

TESTING → BUG

TESTING → READY_FOR_DEPLOY

BUG → IN_PROGRESS

READY_FOR_DEPLOY → DEPLOYING

DEPLOYING → RELEASED

Eligible states → BLOCKED

BLOCKED → previous valid working state

Disallowed examples:

BACKLOG → MERGED
BACKLOG → RELEASED
IN_PROGRESS → RELEASED
CODE_REVIEW → RELEASED
TESTING → RELEASED
BE Agent → MERGED directly
Test Agent → RELEASED directly

All transitions must be validated by the Orchestrator.

---

# 7. Task Domain Model

Initial Task should contain:

- id
- title
- description
- type
- priority
- status
- assignee_agent
- parent_task_id
- dependencies
- acceptance_criteria
- created_at
- updated_at
- sprint_id
- repository
- branch
- pull_request
- review_iteration
- test_iteration
- metadata

Task types:

- EPIC
- STORY
- TASK
- BUG
- TECHNICAL_TASK

Priority:

- LOW
- MEDIUM
- HIGH
- CRITICAL

---

# 8. Agent Contract

Agents must communicate using structured data.

Do not rely on free-form text for workflow decisions.

Generic:

{
  "agent": "SA",
  "task_id": "TASK-123",
  "status": "COMPLETED",
  "result": {}
}

Possible agent execution statuses:

- COMPLETED
- FAILED
- NEEDS_INPUT
- BLOCKED
- CHANGES_REQUESTED

Agent results must be validated against schemas.

---

# 9. Permission Model

## SA Agent

Allowed:

- Read requirements
- Read repository
- Read architecture
- Read ADRs
- Create technical design
- Create tasks
- Review code
- Request changes
- Approve code review

Not allowed:

- Modify production code
- Merge its own implementation
- Deploy production

## BE Agent

Allowed:

- Read repository
- Search code
- Modify feature branch
- Run tests
- Commit
- Push
- Create PR

Not allowed:

- Merge PR
- Approve own PR
- Deploy production
- Change architecture without SA approval

## FE Agent

Same boundary as BE Agent.

## Test Agent

Allowed:

- Read requirements
- Read acceptance criteria
- Read implementation
- Create tests
- Execute tests
- Analyze failures
- Create bug reports

Not allowed:

- Merge production code
- Deploy production

## DevOps Agent

Allowed:

- Build
- Package
- Create container images
- Push images
- Deploy DEV
- Deploy STG
- Deploy UAT according to policy
- Roll back according to policy

Production deployment must require explicit approval.

## Scrum Agent

Allowed:

- Create Epic
- Create Story
- Create Task
- Create Bug
- Organize Sprint
- Track progress
- Track dependencies
- Generate reports

---

# 10. Phase Roadmap

## Phase 0 — Repository Foundation

Goal:

Create the repository structure and project rules.

Deliver:

- AGENTS.md
- README.md
- system-overview.md
- coding standards
- initial ADR

No agent implementation yet.

Acceptance criteria:

- Repository opens cleanly in Cursor
- Architecture documentation is understandable
- Coding rules are explicit

---

# Phase 1 — Workflow Orchestrator

Goal:

Build a deterministic Task State Machine.

Implement:

- Task domain model
- TaskState enum
- State transition rules
- Transition validation
- Task service
- Unit tests

Do not implement agents yet.

Acceptance criteria:

- Every valid transition passes
- Every invalid transition is rejected
- State cannot be changed arbitrarily
- Tests cover all transitions
- No unnecessary dependencies

Cursor task:

"Read AGENTS.md and docs/architecture/system-overview.md. Implement only the Task domain model and deterministic state machine. Do not implement agents, database, Git integration, or LLM integration. Write comprehensive unit tests."

---

# Phase 2 — Agent Contract

Goal:

Define how agents communicate with the Orchestrator.

Implement:

- BaseAgent interface/protocol
- AgentRequest
- AgentResponse
- Result schemas
- Validation
- Error model
- Agent execution lifecycle

Acceptance criteria:

- Invalid agent responses are rejected
- Agent result is structured
- Orchestrator remains the source of truth

---

# Phase 3 — SA Agent

Goal:

Create the first useful engineering agent.

SA responsibilities:

1. Analyze requirements
2. Identify functional requirements
3. Identify non-functional requirements
4. Design architecture
5. Identify dependencies
6. Define APIs
7. Define data model changes
8. Define risks
9. Create implementation tasks
10. Define acceptance criteria

SA must not implement feature code.

Expected output:

Architecture Design
+
Task Breakdown
+
Acceptance Criteria
+
Technical Risks

Acceptance criteria:

Given a requirement, SA produces a structured technical plan.

---

# Phase 4 — Backend Agent

Goal:

Implement a real coding agent.

BE workflow:

Task
→ Read SA Design
→ Inspect Repository
→ Identify Relevant Files
→ Implement
→ Run Tests
→ Review Git Diff
→ Commit
→ Push Branch
→ Create PR

Tool capabilities:

- read_file
- search_code
- list_files
- edit_file
- run_command
- run_tests
- git_status
- git_diff
- git_commit
- git_push
- create_pull_request

Restrictions:

- No merge
- No production deployment
- No architecture changes without approval

Acceptance criteria:

BE can complete a small real feature in a controlled repository and create a PR.

---

# Phase 5 — SA Code Review

Goal:

Automate code review by SA.

Review context:

- Requirement
- Acceptance Criteria
- Architecture
- ADR
- PR diff
- Tests
- Relevant source code

Review output:

{
  "decision": "APPROVED | CHANGES_REQUESTED",
  "issues": [
    {
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "file": "...",
      "line": 123,
      "issue": "...",
      "recommendation": "..."
    }
  ]
}

Review loop:

BE
→ PR
→ SA Review

If rejected:

SA
→ CHANGES_REQUESTED
→ BE
→ new commit
→ SA Review

Maximum review iterations:

3

After maximum retries:

BLOCKED
→ human intervention

Acceptance criteria:

- SA can identify functional and architectural issues
- Review result is structured
- Review loop cannot become infinite
- Approved PR can proceed to merge

---

# Phase 6 — Git/GitLab Integration

Implement:

- Repository abstraction
- Branch creation
- Commit
- Push
- PR creation
- PR diff retrieval
- PR status
- Merge operation controlled by SA/Orchestrator

Important:

Agents do not directly mutate workflow state.

Git/GitLab state and workflow state must be synchronized by the Orchestrator.

---

# Phase 7 — Test Agent

Goal:

Automate testing after merge.

Input:

- Requirement
- Acceptance Criteria
- Architecture
- Changed files
- Existing tests

Test Agent responsibilities:

1. Generate test cases
2. Generate/update automation
3. Run tests
4. Analyze failures
5. Classify failures
6. Create bugs

Test categories:

- Unit
- Integration
- API
- E2E
- Regression
- Concurrency
- Idempotency
- Performance where applicable

Output:

PASSED

or

FAILED + structured bug report

Test failure flow:

TESTING
→ BUG
→ IN_PROGRESS
→ BE/FE
→ CODE_REVIEW
→ MERGED
→ TESTING

Maximum test-fix iterations should be configurable.

---

# Phase 8 — Frontend Agent

FE responsibilities:

- Analyze UI requirements
- Understand API contracts
- Inspect existing components
- Implement UI
- Write/update frontend tests
- Run lint/build/test
- Create PR

Flow:

SA
→ FE Task
→ FE
→ PR
→ SA Review
→ Merge
→ Test

FE must respect SA architecture and API contracts.

---

# Phase 9 — DevOps Agent

Goal:

Automate deployment.

Flow:

TEST PASS
→ READY_FOR_DEPLOY
→ DEV
→ Smoke Test
→ STG
→ UAT
→ Release

Capabilities:

- Build
- Docker image
- Registry
- CI/CD
- Environment variables
- Kubernetes
- Helm
- Deployment status
- Rollback

Production deployment requires explicit approval.

---

# Phase 10 — Scrum Agent

Responsibilities:

- Epic management
- Story creation
- Task creation
- Sprint planning
- Priority
- Dependencies
- Sprint progress
- Definition of Ready
- Definition of Done
- Sprint review
- Retrospective summary

Example:

Sprint
→ Stories
→ Tasks
→ Agent execution
→ Progress
→ Blockers
→ Completion

---

# 11. Definition of Ready

A task can enter READY only when:

- Requirement is clear
- Owner/agent is known
- Acceptance criteria exist
- Dependencies are identified
- Required architecture/design exists
- Scope is understood

---

# 12. Definition of Done

A task is Done only when applicable:

- Requirement satisfied
- Acceptance criteria satisfied
- Implementation complete
- Unit tests pass
- Integration tests pass
- Code review approved
- No blocking static analysis issues
- Security checks pass
- Automation tests pass
- Regression tests pass
- Documentation updated
- Deployment completed if required

---

# 13. Knowledge Architecture

Do not implement complex RAG in the first phase.

Initial knowledge sources:

- AGENTS.md
- Architecture docs
- ADRs
- Coding standards
- Requirements
- Existing tests

Later add:

- Vector search
- Code indexing
- Dependency graph
- Historical PRs
- Historical bugs
- Historical code reviews

Recommended evolution:

Phase 1:
Files + structured context

Phase 2:
PostgreSQL + pgvector

Phase 3:
Code index / AST / Tree-sitter

Phase 4:
Graph database if dependency relationships require it

---

# 14. Context Management

Do not send the entire repository to an agent.

Use targeted context.

SA context:

- Requirement
- Architecture
- ADR
- Relevant repository structure
- Database schema
- API specification
- Standards

BE context:

- Task
- Acceptance criteria
- SA design
- Relevant files
- Related tests
- API contract
- Database schema

FE context:

- Task
- UI requirements
- API contract
- Relevant components
- Existing tests

TEST context:

- Requirement
- Acceptance criteria
- Changed files
- Existing tests
- API contract

DEVOPS context:

- Build configuration
- Docker
- Kubernetes
- CI/CD
- Environment configuration
- Release metadata

---

# 15. Memory Model

Use four levels:

## Short-term memory

Current task, current conversation, current PR, current error.

## Project memory

Architecture, coding conventions, repository structure.

## Decision memory

ADR, rejected designs, architectural trade-offs.

## Historical memory

Previous bugs, reviews, performance issues, failed approaches.

---

# 16. Observability

Every agent execution must be auditable.

Capture:

- task_id
- agent
- execution_id
- start_time
- end_time
- model
- tool calls
- result
- errors
- retry count
- token/cost metadata where available
- state transition

Useful metrics:

- task cycle time
- PR review iterations
- agent retry count
- test failure rate
- bug escape rate
- human intervention rate
- agent execution cost
- time per task

---

# 17. Safety and Guardrails

Hard limits:

- Maximum SA review iterations
- Maximum test-fix iterations
- Maximum tool execution time
- Maximum shell command scope
- Production deployment approval
- Database destructive command protection
- Secret access protection
- Restricted filesystem paths

Agents must not have unrestricted shell access in production.

---

# 18. Cursor Development Rules

When using Cursor:

1. Build one phase at a time.
2. Ask Cursor to inspect existing architecture before coding.
3. Use small implementation prompts.
4. Require tests with every implementation step.
5. Review the generated diff after every major change.
6. Do not ask Cursor to build the entire platform in one prompt.
7. Commit after each stable milestone.
8. Keep architecture documentation synchronized with implementation.
9. Use AGENTS.md as the project-wide rule.
10. Use separate agent-specific instructions when necessary.

Recommended Cursor workflow:

Prompt
→ Inspect
→ Plan
→ Implement
→ Test
→ Review Diff
→ Commit
→ Next step

---

# 19. First Cursor Prompts

## Prompt 1 — Architecture analysis

Read AGENTS.md and docs/architecture/system-overview.md.

Do not modify any files.

Analyze the current architecture requirements and propose the implementation plan for Phase 1: Workflow Orchestrator and Task State Machine.

Return:

1. Folder structure
2. Domain model
3. State machine
4. Valid transitions
5. Invalid transitions
6. Responsibilities
7. Testing strategy
8. Risks

Do not implement anything.

---

## Prompt 2 — Implement state machine

Read AGENTS.md and the approved architecture.

Implement only Phase 1.

Requirements:

- Task domain model
- TaskState enum
- State transition rules
- Transition validation
- Unit tests
- Invalid transition tests

Do not implement:

- Agents
- LLM
- Database
- Git integration
- CI/CD

Keep the implementation deterministic and minimal.

---

## Prompt 3 — Review Phase 1

Review the implementation against:

- AGENTS.md
- system-overview.md
- workflow requirements

Check:

- Architecture violations
- Invalid transitions
- Missing tests
- Over-engineering
- Unnecessary dependencies
- Maintainability

Do not modify files.

Return findings grouped by severity.

---

## Prompt 4 — Agent Contract

Implement Phase 2: Agent Contract.

Create:

- AgentRequest
- AgentResponse
- AgentStatus
- Structured result models
- Validation
- Error model
- Unit tests

Do not implement actual LLM agents yet.

The Orchestrator must remain the source of truth for workflow state.

---

## Prompt 5 — SA Agent

Implement Phase 3: SA Agent.

The SA Agent must:

- Analyze requirements
- Produce functional requirements
- Produce non-functional requirements
- Design architecture
- Identify dependencies
- Produce technical tasks
- Produce acceptance criteria
- Identify risks

The SA Agent must not modify application source code.

All outputs must be structured and validated.

---

## Prompt 6 — Backend Agent

Implement Phase 4: Backend Agent.

The agent must:

- Read task
- Read SA design
- Inspect repository
- Identify relevant files
- Implement changes
- Run tests
- Review git diff
- Create feature branch
- Commit changes
- Push changes
- Create PR

It must not:

- Merge its own PR
- Deploy production
- Bypass SA review
- Change architecture without approval

---

# 20. MVP Completion Criteria

MVP is complete when the following flow works end-to-end:

User Requirement
→ SA Agent
→ Architecture
→ Task
→ BE Agent
→ Code
→ PR
→ SA Review
→ CHANGES_REQUESTED
→ BE Fix
→ SA Review
→ APPROVED
→ Merge

The system must be able to demonstrate this flow on a small real feature.

Do not add FE, Test, DevOps, Scrum, RAG, or Kubernetes until this loop is stable.

---

# 21. Production Evolution

After MVP:

1. Add Test Agent
2. Add FE Agent
3. Add DevOps Agent
4. Add Scrum Agent
5. Add persistent workflow engine
6. Add PostgreSQL
7. Add Redis
8. Add Kafka/event-driven execution
9. Add knowledge/RAG
10. Add code graph
11. Add observability
12. Add human approval gates
13. Add multi-project support
14. Add cost controls
15. Add security policies

---

# 22. Target Final Architecture

                    USER
                      |
                      v
              ┌───────────────┐
              │ Scrum Agent   │
              └───────┬───────┘
                      |
                      v
              ┌───────────────┐
              │ Orchestrator  │
              │ State Machine │
              └───────┬───────┘
                      |
        ┌─────────────┼─────────────┐
        |             |             |
        v             v             v
       SA            BE            FE
        |             |             |
        └─────────────┼─────────────┘
                      |
                      v
                 SA Review
                      |
                 ┌────┴────┐
                 |         |
                FAIL      PASS
                 |         |
                 v         v
                Fix       Merge
                 |         |
                 └────┐    |
                      |    v
                      |   TEST
                      |    |
                      | ┌──┴──┐
                      | |     |
                      |FAIL  PASS
                      | |     |
                      | v     v
                      | BUG  DEVOPS
                      |       |
                      └───────┘
                              |
                         DEV/STG/UAT
                              |
                           RELEASE

Supporting layers:

- Tool Layer
- Knowledge Layer
- Policy Layer
- Observability Layer
- Audit Layer

---

# 23. Final Engineering Principle

Do not build six independent chatbots.

Build one controlled software delivery platform with specialized agents.

The Orchestrator controls:

- Who works
- When they work
- What context they receive
- What tools they can use
- What state the task is in
- Whether the next step is allowed

Agents control:

- Analysis
- Design
- Coding
- Review
- Testing
- Deployment operations

The system should progressively move from:

Human-driven
→ Agent-assisted
→ Agent-orchestrated
→ Highly autonomous

while keeping deterministic workflow, auditability, permissions, and human approval gates.
