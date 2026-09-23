---
id: TASK-003
title: Task service REST API and persistence
type: TASK
priority: MEDIUM
status: READY
assignee: BE
parent: REQ-001
depends_on: []
sprint:
branch:
merge_commit:
release:
review_iteration: 0
test_iteration: 0
blocked_from:
approved_by:
updated: 2026-09-23 17:01
---

## Description

Create `task-service` with PostgreSQL persistence and REST APIs for listing, creating, updating, deleting,
and changing task status per REQ-001.

## Acceptance Criteria
- [ ] AC-1 `GET /api/v1/tasks` returns 200 with a JSON array of tasks ordered by `createdAt` descending
- [ ] AC-2 `POST /api/v1/tasks` with non-blank `title` returns 201, body has `status` `TODO`, persisted fields `id`, `createdAt`, `updatedAt`
- [ ] AC-3 `POST /api/v1/tasks` with blank or missing `title` returns 400 `application/problem+json`
- [ ] AC-4 `PUT /api/v1/tasks/{id}` updates title/description; `PATCH /api/v1/tasks/{id}/status` with `{ "status": "COMPLETED" }` or `"TODO"` updates status; `DELETE /api/v1/tasks/{id}` returns 204 and removes the task
- [ ] AC-5 `GET /api/v1/tasks?status=TODO|COMPLETED` filters correctly; `GET/PUT/PATCH/DELETE` for unknown `id` returns 404 ProblemDetail

## Design (SA)

See `docs/design/REQ-001-design.md` §5–§7 (FR-1–FR-10, NFR-1–NFR-5).
Repo: task-service (new)
- Create repo via repo skill; Flyway `V1__init.sql` for `task` table (UUID id).
- Layers: `api/` controllers + DTO records, `service/`, `domain/Task`, `repository/`, `ApiExceptionHandler`.
- `@WebMvcTest` for API validation/not-found; `@DataJpaTest` or Testcontainers integration for persistence/filter.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 17:00 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-23 17:01 | BACKLOG | READY | SCRUM | DoR met |
