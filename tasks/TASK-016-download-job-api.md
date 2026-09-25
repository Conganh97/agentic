---
id: TASK-016
title: Download job API, async dispatch, and cancel
type: TASK
priority: HIGH
status: BACKLOG
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
depends_on: [TASK-011]
sprint:
branch:
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
updated: 2026-09-25 16:33
---

## Description

Expose `POST /api/v1/downloads`, `GET /api/v1/downloads/{downloadId}`, and
`POST /api/v1/downloads/{downloadId}/cancel`. Create returns 202 without waiting for bytes.
Validate `source=DOUYIN` and allowed hosts (design NFR-13). Dispatch work on `TaskExecutor`.
Mark stale RUNNING jobs FAILED (NFR-4). Execution/provider/storage wiring is TASK-017; this task
may persist PENDING and enqueue a no-op or stub runner.

## Acceptance Criteria
- [ ] AC-002 The service exposes an API for creating a video download job.
- [ ] AC-003 Download jobs execute asynchronously.
- [ ] AC-004 A valid public Douyin video URL can be submitted for downloading.
- [ ] AC-035 Download job status can be queried through an API.
- [ ] AC-048 The service exposes a stable contract that can later be consumed by n8n or another orchestration service.

## Design (SA)

`docs/design/REQ-002-design.md` §6 API, FR-2, FR-3, FR-13 (status), FR-18, NFR-1, NFR-4, NFR-13.
OpenAPI must list these operations (contract for n8n). RFC 9457 errors. Cancel: 409 if already
terminal COMPLETED/FAILED/CANCELLED. Stale `RUNNING` older than `downloader.job.stale-after`
(default 30m) marked FAILED on create/status or `@Scheduled` sweep. AC-036 metadata fields after
COMPLETED are filled by TASK-017.

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
