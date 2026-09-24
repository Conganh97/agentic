---
id: TASK-001
title: Bootstrap shop-service
type: TASK
priority: CRITICAL
status: MERGED
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
updated: 2026-09-24 09:29
---

## Description

Create the greenfield `shop-service` repo and a runnable Spring Boot 4.0.x app (Java 21) with
Actuator health, Flyway, PostgreSQL config, RFC 9457 `ProblemDetail` advice, and CORS for the Vite
origin. No domain APIs yet.

## Acceptance Criteria
- [ ] AC-001 `python3 scripts/repo.py create shop-service` (from the team repo) registers
      `product/services/shop-service` and the service starts with
      `SERVER_PORT=18081 ./mvnw spring-boot:run` when PostgreSQL is available
- [ ] AC-002 `GET /actuator/health` returns 200 with status UP when the database is reachable
- [ ] AC-003 Flyway is wired (`ddl-auto=validate`); an empty or baseline `V1` migration applies on startup
- [ ] AC-004 A `@RestControllerAdvice` returns RFC 9457 `ProblemDetail` for a sample 404; no stack trace in the body
- [ ] AC-005 `./mvnw -q verify` passes (at least a health web-slice or context test)

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

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:19 | BACKLOG | READY | SCRUM | DoR met; deps [] |
| 2026-09-24 09:22 | READY | IN_PROGRESS | BE | branch feature/TASK-001-bootstrap-shop-service |
| 2026-09-24 09:26 | IN_PROGRESS | CODE_REVIEW | BE | product commit 701a2e5; Implementation Iteration 1 |
| 2026-09-24 09:29 | CODE_REVIEW | MERGED | SA | merge_commit=48801b6; reviews/TASK-001-round-1.md APPROVED; --no-ff on main |
