---
id: REQ-001
title: Simple Task Management App
status: ANALYZED
priority: MEDIUM
owner: Product Owner
design: docs/design/REQ-001-design.md
tasks: [TASK-003, TASK-004, TASK-005, TASK-006]
updated: 2026-09-23 17:00
---

## Goal

Build a simple task management application that allows users to create, manage, and track their personal tasks.

The application helps users keep track of what they need to do and which tasks have been completed.

## Scope

- Display a list of tasks.
- Create a new task.
- Edit an existing task.
- Delete a task.
- Mark a task as completed or incomplete.
- Display the current status of each task.
- Filter tasks by status:
  - All
  - Todo
  - Completed
- Persist tasks in a database.
- Provide REST APIs for task management.
- Provide a simple web interface.
- Write unit tests for business logic.
- Write API/integration tests for the main use cases.
- Provide Docker support so the application can be built and run consistently.

## Out of Scope

- User registration and login.
- Authentication and authorization.
- Notifications.
- Realtime/WebSocket functionality.
- Assigning tasks to other users.
- Comments.
- File attachments.
- Pagination.
- Mobile applications.

## User Stories / Behaviour

- As a user, I want to create a task, so that I can record work that I need to do.
- As a user, I want to see all my tasks, so that I know what work I have.
- As a user, I want to edit a task, so that I can correct or update its information.
- As a user, I want to delete a task, so that I can remove tasks that are no longer needed.
- As a user, I want to mark a task as completed, so that I can track my progress.
- As a user, I want to mark a completed task as incomplete, so that I can continue working on it.
- As a user, I want to filter tasks by status, so that I can quickly find pending or completed tasks.

## Acceptance Criteria (business level)

- [ ] The user can view a list of all tasks.
- [ ] The user can create a new task.
- [ ] A task must have a title.
- [ ] A task may have a description.
- [ ] A newly created task has `TODO` status by default.
- [ ] The user can edit the task title and description.
- [ ] The user can delete a task.
- [ ] The user can change a task from `TODO` to `COMPLETED`.
- [ ] The user can change a task from `COMPLETED` back to `TODO`.
- [ ] The user can filter tasks by `ALL`, `TODO`, and `COMPLETED`.
- [ ] A newly created task is persisted in the database.
- [ ] Updated task information is persisted.
- [ ] A deleted task no longer appears in the task list.
- [ ] The API returns appropriate HTTP status codes for successful and failed operations.
- [ ] A task cannot be created with an empty title.
- [ ] Updating a non-existing task returns an appropriate error.
- [ ] Deleting a non-existing task returns an appropriate error.
- [ ] The backend has unit/integration tests covering the main business cases.
- [ ] The frontend has tests covering the main user interactions.
- [ ] The application can be built and run using Docker.

## Constraints

### Technology

- Backend must use Java 21 and Spring Boot.
- Database must use PostgreSQL.
- The frontend should use the existing frontend framework if one already exists.
- If there is no existing frontend, the SA should propose an appropriate framework.
- APIs must use REST/JSON.
- Do not introduce unnecessary frameworks or infrastructure.
- Follow the existing project architecture and coding standards.

### Data

A Task must contain at least:

- `id`
- `title`
- `description`
- `status`
- `createdAt`
- `updatedAt`

Task status:

```text
TODO
COMPLETED
```

### Performance

- No complex performance optimization is required for the first version.
- Task list API should respond quickly for a small dataset.
- Avoid unnecessary database queries.

### Security

- Authentication and authorization are not required for the first version.
- APIs must only expose functionality required for task management.

### Compatibility

- API and database design should allow future extension.
- Avoid hard-coding the design in a way that makes future user accounts or authentication difficult to introduce.

### Deployment

The application must be able to run using:

```text
Build
  ↓
Docker Image
  ↓
Run Application
  ↓
Connect PostgreSQL
```

## Notes

### Example Task

```text
Title:
Learn Spring Boot

Description:
Study Spring Boot REST API and build a small demo.

Status:
TODO
```

After completion:

```text
Title:
Learn Spring Boot

Description:
Study Spring Boot REST API and build a small demo.

Status:
COMPLETED
```

### Suggested API

The SA may change the API design after reviewing the existing architecture.

Possible endpoints:

```text
GET    /api/tasks
GET    /api/tasks/{id}
POST   /api/tasks
PUT    /api/tasks/{id}
DELETE /api/tasks/{id}
PATCH  /api/tasks/{id}/status
```

### Expected SA Deliverables

The SA should create:

- `docs/design/REQ-001-design.md`
- Task breakdown
- API design
- Database design
- Architecture Decision Record if required
- Backend tasks
- Frontend tasks
- Test tasks
- DevOps tasks
- Technical acceptance criteria

The SA must not implement application code during the requirement analysis and architecture phase.