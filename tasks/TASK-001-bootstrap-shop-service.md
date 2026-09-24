---
id: TASK-001
title: Bootstrap shop-service
type: TASK
priority: CRITICAL
status: READY
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: []
sprint:
branch:
merge_commit:
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
updated: 2026-09-24 09:19
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

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:19 | BACKLOG | READY | SCRUM | DoR met; deps [] |
