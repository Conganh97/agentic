---
id: TASK-001
title: Greeting service with greeting endpoint
type: TASK
priority: MEDIUM
status: IN_PROGRESS
assignee: BE
parent: REQ-000
depends_on: []
sprint:
branch: feature/TASK-001-greeting-endpoint
merge_commit:
release:
review_iteration: 0
test_iteration: 0
blocked_from:
approved_by:
updated: 2026-09-23 13:45
---

## Description
Create a new microservice `greeting-service` exposing a greeting endpoint. No database.

## Acceptance Criteria
- [ ] AC-1 `GET /api/v1/greetings/{name}` returns 200 with `{"message":"Hello, <name>!"}`
- [ ] AC-2 A name longer than 50 characters returns 400 as a `ProblemDetail` JSON body
- [ ] AC-3 `GET /actuator/health` returns 200 with status `UP`

## Design (SA)
New service `services/greeting-service`, package `com.product.greeting`, port 8081.
- `api/GreetingController` + `GreetingResponse` record; validation via Jakarta Validation (`@Size(max = 50)`).
- `api/ApiExceptionHandler` (`@RestControllerAdvice`) maps validation errors to `ProblemDetail` 400.
- No persistence, no other service calls.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 13:50 | — | BACKLOG | HUMAN (test) | Phase 4 test task |
| 2026-09-23 13:50 | BACKLOG | READY | HUMAN (test) | DoR satisfied |
| 2026-09-23 13:45 | READY | IN_PROGRESS | BE | Branch `feature/TASK-001-greeting-endpoint` created |
