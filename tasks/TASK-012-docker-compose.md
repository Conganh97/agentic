---
id: TASK-012
title: Docker Compose local stack
type: TASK
priority: CRITICAL
status: BACKLOG
assignee: DEVOPS
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-001, TASK-006]
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
updated: 2026-09-24 09:15
---

## Description

Add a JVM Dockerfile for `shop-service` and a Compose stack (PostgreSQL + shop-service + frontend
static image) so the storefront runs locally with Docker. Frontend build context is
`../../frontend` (both repos cloned under `product/`). If that tree has no Dockerfile, add
`deploy/frontend.Dockerfile` in this repo and point Compose at it.

## Acceptance Criteria
- [ ] AC-001 `shop-service/Dockerfile` is multi-stage and the image listens on 18081 (or `SERVER_PORT`)
- [ ] AC-002 `docker-compose.yml` starts healthy `postgres`, `shop-service` (Flyway on boot), and
      `frontend` (SPA + `/api` proxied to shop-service)
- [ ] AC-003 `docker compose up --build -d` then `curl -sf` frontend `/` is HTTP 200 and
      `curl -sf http://localhost:18081/actuator/health` is UP
- [ ] AC-004 DB user/password come from Compose env/defaults; no secrets committed; README lists
      ports and `docker compose down`
- [ ] AC-005 Implementation notes record the two curl results

## Design (SA)
See `docs/design/REQ-001-design.md` §5 and NFR-6. Repo: shop-service (existing).
- Paths assume ADR-0007 layout under `product/`.
- Prefer unprivileged Nginx for the SPA. Not a PROD deploy.
- Do not change Java business APIs.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
