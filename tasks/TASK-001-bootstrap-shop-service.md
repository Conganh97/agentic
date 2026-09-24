---
id: TASK-001
title: Bootstrap shop-service
type: TASK
priority: CRITICAL
status: READY_FOR_DEPLOY
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: []
sprint:
branch: feature/TASK-001-bootstrap-shop-service
merge_commit: 48801b6
release:
review_iteration: 0
test_iteration: 0
blocked_from:
failed_from:
failure_type:
failure_step:
failure_message:
failure_retry: 0
failure_recoverable:
human_gate:
approved_by:
approved_at:
updated: 2026-09-24 09:34
---

## Description

Create the greenfield `shop-service` repo and a runnable Spring Boot 4.0.x app (Java 21) with
Actuator health, Flyway, PostgreSQL config, RFC 9457 `ProblemDetail` advice, and CORS for the Vite
origin. No domain APIs yet.

## Acceptance Criteria
- [x] AC-001 `python3 scripts/repo.py create shop-service` (from the team repo) registers
      `product/services/shop-service` and the service starts with
      `SERVER_PORT=18081 ./mvnw spring-boot:run` when PostgreSQL is available
- [x] AC-002 `GET /actuator/health` returns 200 with status UP when the database is reachable
- [x] AC-003 Flyway is wired (`ddl-auto=validate`); an empty or baseline `V1` migration applies on startup
- [x] AC-004 A `@RestControllerAdvice` returns RFC 9457 `ProblemDetail` for a sample 404; no stack trace in the body
- [x] AC-005 `./mvnw -q verify` passes (at least a health web-slice or context test)

## Design (SA)
See `docs/design/REQ-001-design.md` §5 and NFR-5. Repo: shop-service (new, ADR-0007).
- Package `com.product.shop`; port `${SERVER_PORT:18081}`; `docs/standards/backend.md` new-service checklist.
- Modular Boot 4 starters (webmvc, validation, actuator, data-jpa, flyway-postgresql).
- CORS + `allowCredentials` for `http://localhost:15173`. Do not add catalog or account APIs here.
- Create the GitHub repo only via `scripts/repo.py`.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-001-bootstrap-shop-service` @ 701a2e5
- Changed: `services/shop-service/pom.xml`, `src/main/java/com/product/shop/ShopApplication.java`, `api/ApiExceptionHandler.java`, `config/CorsConfig.java`, `src/main/resources/application.yml`, `db/migration/V1__baseline.sql`, `ShopApplicationTests.java`, `api/ApiExceptionHandlerTest.java`, `config/CorsConfigTest.java`
- Tests: `./mvnw -q verify` in `services/shop-service` → pass (6 tests)
- Notes: Boot 4 needs `spring-boot-starter-flyway` (not `flyway-core` alone) to activate Flyway auto-config; Testcontainers 2 artifacts are `testcontainers-postgresql` / `testcontainers-junit-jupiter`. V1 is a comment-only baseline (domain tables left to later tasks). CORS + credentials for `http://localhost:15173`. Local `spring-boot:run` still needs a PostgreSQL `shop` database. Repo created via `scripts/repo.py`; branch pushed.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-001-bootstrap-shop-service @ 701a2e5 · Build/tests: ./mvnw -q verify PASS (6 tests)
No comments.

Merged 48801b6.
Pushed main.

## Test (TEST)
### Run 1 — PASS
- Tested: main @ 48801b6 (contains merge `48801b6`), service on port 18081
- Build/tests: `./mvnw -q verify` PASS (6 tests)
- AC-001 pass — `python3 scripts/repo.py status` → shop-service registered at `product/services/shop-service`; `SERVER_PORT=18081 ./mvnw spring-boot:run` (shop PG on :15432) listening, health UP
- AC-002 pass — `curl -s localhost:18081/actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}`
- AC-003 pass — startup Flyway `Migrating schema "public" to version "1 - baseline"`; `flyway_schema_history` version=1 script=`V1__baseline.sql`; `ddl-auto: validate`
- AC-004 pass — `curl -s localhost:18081/api/v1/does-not-exist` → 404 `application/problem+json` `{"status":404,"title":"Not Found",...}`; no stack trace
- AC-005 pass — `./mvnw -q verify` → 6 tests, 0 failures
- Exploratory: CORS Vite origin 200 + credentials; other origin 403; POST /actuator/health 405 ProblemDetail; /actuator/env 404; GET / 404 no stack
- Bug (FAIL only): n/a

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:19 | BACKLOG | READY | SCRUM | DoR met; deps [] |
| 2026-09-24 09:22 | READY | IN_PROGRESS | BE | branch feature/TASK-001-bootstrap-shop-service |
| 2026-09-24 09:26 | IN_PROGRESS | CODE_REVIEW | BE | product commit 701a2e5; Implementation Iteration 1 |
| 2026-09-24 09:29 | CODE_REVIEW | MERGED | SA | merge_commit=48801b6; reviews/TASK-001-round-1.md APPROVED; --no-ff on main |
| 2026-09-24 09:32 | MERGED | TESTING | TEST | run 1; tested sha 48801b6 is ancestor of main containing merge_commit 48801b6 |
| 2026-09-24 09:34 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-001-run-1.md PASS; every AC-001..AC-005 checked; tested sha 48801b6 |
