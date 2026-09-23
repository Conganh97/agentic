---
id: TASK-002
title: Greeting language parameter
type: TASK
priority: MEDIUM
status: IN_PROGRESS
assignee: BE
parent: REQ-000
depends_on: [TASK-001]
sprint:
branch: feature/TASK-002-greeting-language
merge_commit:
release:
review_iteration: 0
test_iteration: 0
blocked_from:
approved_by:
updated: 2026-09-23 14:11
---

## Description
Add an optional `lang` query parameter to the greeting endpoint of `greeting-service`.

## Acceptance Criteria
- [ ] AC-1 `GET /api/v1/greetings/An?lang=vi` returns 200 with `{"message":"Xin chào, An!"}`
- [ ] AC-2 Without `lang`, or with `lang=en`, the response is unchanged: `{"message":"Hello, An!"}`
- [ ] AC-3 An unsupported `lang` (e.g. `lang=fr`) returns 400 as a `ProblemDetail` JSON body

## Design (SA)
Extend `services/greeting-service` (TASK-001).
- `enum Language { EN, VI }` with the greeting template; parse `lang` case-insensitively.
- Unsupported value → 400 `ProblemDetail` through the existing `ApiExceptionHandler`.
- No API version change: the parameter is optional and backward compatible.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 14:10 | — | BACKLOG | HUMAN (test) | Phase 5 test task |
| 2026-09-23 14:10 | BACKLOG | READY | HUMAN (test) | DoR satisfied |
| 2026-09-23 14:11 | READY | IN_PROGRESS | BE | Started on `feature/TASK-002-greeting-language` |
