---
id: TASK-004
title: Task management web UI
type: TASK
priority: MEDIUM
status: CHANGES_REQUESTED
assignee: FE
parent: REQ-001
depends_on: [TASK-003]
sprint:
branch: feature/TASK-004-task-management-ui
merge_commit:
release:
review_iteration: 1
test_iteration: 0
blocked_from:
approved_by:
updated: 2026-09-23 17:18
---

## Description

Scaffold `frontend` (if needed) and implement the task list, create/edit/delete, completion toggle, and
status filter against `task-service` APIs.

## Acceptance Criteria
- [ ] AC-1 Task list page loads tasks from `GET /api/v1/tasks` with loading, error, and empty states
- [ ] AC-2 User can create a task with title (required) and optional description; new task appears with TODO status
- [ ] AC-3 User can edit title/description and delete a task; UI reflects API responses
- [ ] AC-4 User can mark a task completed or revert to todo via status change aligned with backend contract
- [ ] AC-5 Filter control switches between All, Todo, and Completed and passes the correct query to the API

## Design (SA)

See `docs/design/REQ-001-design.md` §5–§7 (FR-1–FR-7, FR-11, NFR-2).
Repo: frontend (new)
- Feature module `src/features/tasks/` with Query hooks; `src/api/client.ts` and task DTO types.
- Dev proxy `/api` → `BACKEND_PORT` (default 18082); Vitest + RTL tests for create, filter, toggle complete.

## Implementation (BE/FE)

### Iteration 1 (initial)
- Branch: `feature/TASK-004-task-management-ui` @ c919214
- Changed: `frontend/src/api/`, `frontend/src/features/tasks/`, `frontend/src/app/`, `frontend/vite.config.ts`, scaffold (Vite/React/TS)
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (7 tests)
- Notes: Local `frontend` repo bootstrapped (no `gh auth` / GitHub remote yet); push failed: no `origin`. Dev proxy uses `BACKEND_PORT` default 18081 per `project.md`. Create section heading "Add task" (avoids duplicate "New task" with task title).

## Review (SA)

### Round 1 — CHANGES_REQUESTED
Reviewed: feature/TASK-004-task-management-ui @ c919214 · Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (7 tests)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | src/features/tasks/TaskForm.tsx:34,45 | MAJOR | Create and inline-edit forms both use fixed `id="task-title"` / `id="task-description"`; when a row is in edit mode, labels and ids collide on one page. Use `useId()` (or unique per-instance ids) so each field has a single associated label. |
| 2 | src/features/tasks/TaskListPage.test.tsx:179 | MAJOR | AC-5 requires All, Todo, and Completed filters with the correct API query; only Todo (`status=TODO`) is asserted. Add tests that Completed requests `status=COMPLETED` and All calls `/api/v1/tasks` without a `status` query param. |

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 17:00 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-23 17:14 | BACKLOG | READY | SCRUM | DoR met |
| 2026-09-23 17:15 | READY | IN_PROGRESS | FE | feature/TASK-004-task-management-ui |
| 2026-09-23 17:17 | IN_PROGRESS | CODE_REVIEW | FE | task UI ready for SA review |
| 2026-09-23 17:18 | CODE_REVIEW | CHANGES_REQUESTED | SA | 2 MAJOR: duplicate form ids; incomplete filter tests |
