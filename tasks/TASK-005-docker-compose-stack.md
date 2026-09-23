---
id: TASK-005
title: task-service Docker and database compose
type: TASK
priority: MEDIUM
status: BACKLOG
assignee: DEVOPS
parent: REQ-001
depends_on: [TASK-003]
sprint:
branch:
merge_commit:
release:
review_iteration: 0
test_iteration: 0
blocked_from:
approved_by:
updated: 2026-09-23 17:00
---

## Description

Add a production-style Dockerfile and Docker Compose for PostgreSQL + `task-service` in the task-service repo.

## Acceptance Criteria
- [ ] AC-1 `docker compose build` in `task-service` completes for the application image
- [ ] AC-2 `docker compose up` starts PostgreSQL and `task-service`; `GET /actuator/health` returns UP on the published port
- [ ] AC-3 Smoke: `POST /api/v1/tasks` then `GET /api/v1/tasks` via published port succeeds; data survives compose restart with the Postgres volume
- [ ] AC-4 `task-service` README documents compose build/run/stop and env vars (DB URL, ports)

## Design (SA)

See `docs/design/REQ-001-design.md` §5–§7 (FR-12, NFR-3).
Repo: task-service (existing)
- Multi-stage JVM Dockerfile; compose services `postgres` + `task-service`; named volume for Postgres.
- No secrets in git; credentials via compose env defaults suitable for local dev only.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 17:00 | — | BACKLOG | SA | Created from REQ-001 design |
