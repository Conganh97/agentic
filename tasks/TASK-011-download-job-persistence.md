---
id: TASK-011
title: Download job persistence and status model
type: TASK
priority: HIGH
status: IN_PROGRESS
assignee: BE
parent: REQ-002
requirement_revision: 1
repo: video-downloader-service
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: [TASK-010]
sprint: SPRINT-06
branch: feature/TASK-011-download-job-persistence
merge_commit:
release:
review_iteration: 0
uxui_review_iteration: 0
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
updated: 2026-09-25 17:01
---

## Description

Add the `downloadjob` persistence feature: Flyway table `download_job` as specified in design §7,
JPA mapping, and repository port. Persist source URL, provider id, start/completion (and
failed/cancelled) timestamps, and status values PENDING, RUNNING, COMPLETED, FAILED, CANCELLED.
No REST and no provider HTTP in this task. Testcontainers PostgreSQL.

## Acceptance Criteria
- [ ] AC-019 The system stores the original source URL.
- [ ] AC-020 The system stores the downloader provider used.
- [ ] AC-021 The system stores download start time and completion time.
- [ ] AC-022 The system stores download status.
- [ ] AC-023 The system can distinguish successful, failed, cancelled, and in-progress downloads.

## Design (SA)

`docs/design/REQ-002-design.md` §7, FR-8. This task owns the only v1 migration (`download_job`).
Partial unique index on `(source, source_identity)` WHERE status in PENDING/RUNNING/COMPLETED is
created here; TASK-019 uses it for idempotency. Do not log secrets. `ddl-auto=validate`.

## Implementation (BE/FE)

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 16:33 | — | BACKLOG | SA | Created from REQ-002 design revision 1 hash b06116020682e658 |
| 2026-09-25 16:59 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-010] READY_FOR_DEPLOY |
| 2026-09-25 17:01 | READY | IN_PROGRESS | BE | branch feature/TASK-011-download-job-persistence |
