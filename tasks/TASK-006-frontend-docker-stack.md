---
id: TASK-006
title: Frontend Docker and full-stack compose
type: TASK
priority: MEDIUM
status: BACKLOG
assignee: DEVOPS
parent: REQ-001
depends_on: [TASK-004, TASK-005]
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

Add a frontend container and extend the stack so the full task app (UI + API + PostgreSQL) runs via Docker.

## Acceptance Criteria
- [ ] AC-1 `frontend` repo Dockerfile builds a static production image successfully
- [ ] AC-2 Documented compose (or override) runs PostgreSQL, `task-service`, and frontend together
- [ ] AC-3 Smoke: user can open the published frontend URL, create a task in the UI, and see it after page reload
- [ ] AC-4 README documents full-stack Docker commands and how the UI reaches the API (proxy or `VITE_API_BASE_URL`)

## Design (SA)

See `docs/design/REQ-001-design.md` §5–§7 (FR-12, NFR-3).
Repo: frontend (existing)
- Node build stage + nginx (or similar) serve; compose extends TASK-005 stack via override file or merged compose path documented in README.
- API base URL configured for container network hostnames.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 17:00 | — | BACKLOG | SA | Created from REQ-001 design |
