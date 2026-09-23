---
id: TASK-003
title: Task service REST API and persistence
type: TASK
priority: MEDIUM
status: MERGED
assignee: BE
parent: REQ-001
depends_on: []
sprint:
branch: feature/TASK-003-task-service-api
merge_commit: 5500599
release:
review_iteration: 1
test_iteration: 0
blocked_from:
approved_by:
updated: 2026-09-23 17:11
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

### Iteration 1 (initial)
- Branch: `feature/TASK-003-task-service-api` @ 41db5fa
- Changed: `product/services/task-service/` (Spring Boot 4 scaffold, Flyway `V1__init.sql`, REST `/api/v1/tasks`, tests)
- Tests: `./mvnw -q verify` in `task-service` → pass (10 run, 3 skipped without Docker)
- Notes: local git repo only — `gh auth login` then `python3 scripts/repo.py create task-service --type be` to register GitHub remote; push failed (not registered). Testcontainers integration tests skipped (Docker unavailable).

### Iteration 2 (review round 1)
- Branch: `feature/TASK-003-task-service-api` @ 4242d6c
- Changed: `src/test/java/com/product/task/api/TaskControllerWebMvcTest.java`, `src/test/java/com/product/task/service/TaskServiceTest.java`
- Tests: `./mvnw -q verify` in `task-service` → pass (15 run, 3 skipped without Docker)
- Notes: SA comments #1–#5 addressed (404 PATCH/DELETE, PUT 404 ProblemDetail, missing title POST, PATCH TODO, list order via `TaskServiceTest`); push failed (task-service not in `project.md` registry).

## Review (SA)

### Round 1 — CHANGES_REQUESTED
Reviewed: feature/TASK-003-task-service-api @ 41db5fa · Build/tests: `./mvnw -q verify` PASS (10 run, 3 skipped — Docker unavailable)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | src/test/java/com/product/task/api/TaskControllerWebMvcTest.java | MAJOR | AC-5: add MockMvc tests for `PATCH` and `DELETE` on unknown `id` returning 404 with `application/problem+json` (mirror `getTaskWhenMissingReturns404ProblemDetail`). |
| 2 | src/test/java/com/product/task/api/TaskControllerWebMvcTest.java:147 | MAJOR | AC-5: `updateWhenMissingReturns404` asserts status only; also expect ProblemDetail content type like other 404 cases. |
| 3 | src/test/java/com/product/task/api/TaskControllerWebMvcTest.java | MAJOR | AC-1: list ordering by `createdAt` desc is only covered in `TaskRepositoryIntegrationTest`; add a test that would fail if `TaskService.listTasks` stopped using `findAllByOrderByCreatedAtDesc` (e.g. `@WebMvcTest` with real ordering via mocked repo returning two tasks, or a focused `TaskService` unit test). |
| 4 | src/test/java/com/product/task/api/TaskControllerWebMvcTest.java | MAJOR | AC-3: add POST with missing/null `title` (e.g. `{}`) expecting 400 `application/problem+json`, not only blank whitespace. |
| 5 | src/test/java/com/product/task/api/TaskControllerWebMvcTest.java | MAJOR | AC-4: add PATCH with `{ "status": "TODO" }` (revert from COMPLETED) so both allowed status values are exercised at the API layer. |

### Round 2 — APPROVED
Reviewed: feature/TASK-003-task-service-api @ 4242d6c · Build/tests: `./mvnw -q verify` PASS (15 run, 3 skipped — Docker unavailable)
Previous round: #1–#5 resolved
No comments.

Merged 5500599.
Push failed: task-service is not registered in project.md

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 17:00 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-23 17:01 | BACKLOG | READY | SCRUM | DoR met |
| 2026-09-23 17:04 | READY | IN_PROGRESS | BE | feature/TASK-003-task-service-api |
| 2026-09-23 17:07 | IN_PROGRESS | CODE_REVIEW | BE | task-service API ready for SA |
| 2026-09-23 17:08 | CODE_REVIEW | CHANGES_REQUESTED | SA | 5 MAJOR test gaps (AC-1, AC-3–AC-5) |
| 2026-09-23 17:09 | CHANGES_REQUESTED | IN_PROGRESS | BE | address SA review round 1 test gaps |
| 2026-09-23 17:10 | IN_PROGRESS | CODE_REVIEW | BE | WebMvc/service tests for AC-1, AC-3–AC-5 |
| 2026-09-23 17:11 | CODE_REVIEW | MERGED | SA | approved round 2; merged 5500599 |
