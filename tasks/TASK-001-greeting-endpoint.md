---
id: TASK-001
title: Greeting service with greeting endpoint
type: TASK
priority: MEDIUM
status: CODE_REVIEW
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
updated: 2026-09-23 13:53
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

### Iteration 1 (initial)
- Branch: `feature/TASK-001-greeting-endpoint` @ 89299f8
- Changed: `services/greeting-service/` (new): `pom.xml`, `mvnw`, `.mvn/wrapper/`, `README.md`,
  `src/main/java/com/product/greeting/{GreetingApplication, api/GreetingController, api/GreetingResponse, api/ApiExceptionHandler}.java`,
  `src/main/resources/application.yml`,
  `src/test/java/com/product/greeting/{HealthEndpointTest, api/GreetingControllerTest}.java`
- Tests: `./mvnw -q verify` in `services/greeting-service` → pass (4 tests: AC-1 `greetingReturnsHelloMessage`,
  AC-2 `nameLongerThanFiftyCharactersReturns400ProblemDetail` + boundary `nameWithFiftyCharactersIsAccepted`,
  AC-3 `healthEndpointReturnsUp`)
- Notes: `@Size(max = 50)` on the `@PathVariable` uses Spring MVC built-in method validation (no `@Validated`),
  raising `HandlerMethodValidationException`; `ApiExceptionHandler` extends `ResponseEntityExceptionHandler`,
  which renders it (and `MethodArgumentNotValidException`) as `application/problem+json` 400.
  No `service/` layer: the design places the greeting logic in the controller and there is no business logic
  beyond string formatting. Port `8081` overridable via `SERVER_PORT`; only the `health` actuator endpoint is exposed.
  Health test uses `@SpringBootTest` + MockMvc (mock environment), not a real server port.

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 13:50 | — | BACKLOG | HUMAN (test) | Phase 4 test task |
| 2026-09-23 13:50 | BACKLOG | READY | HUMAN (test) | DoR satisfied |
| 2026-09-23 13:45 | READY | IN_PROGRESS | BE | Branch `feature/TASK-001-greeting-endpoint` created |
| 2026-09-23 13:53 | IN_PROGRESS | CODE_REVIEW | BE | greeting-service implemented @ 89299f8; verify pass (4 tests) |
