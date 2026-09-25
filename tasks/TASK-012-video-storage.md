---
id: TASK-012
title: Storage port, volume persist, and file validation
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
depends_on: [TASK-010]
sprint: SPRINT-06
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
updated: 2026-09-25 16:55
---

## Description

Implement the `storage` feature: domain port `VideoStorage` and a local-filesystem implementation
rooted at `downloader.storage.root` (compose volume). Generate server-side keys
`videos/{yyyy}/{MM}/{id}.ext`. Reject client-supplied paths. Validate magic bytes / content type
for mp4 (and webm if advertised) and enforce configurable max size (default 500 MiB). No SnapTik
HTTP in this task.

## Acceptance Criteria
- [ ] AC-017 The downloaded file is persisted to configured storage.
- [ ] AC-018 The system stores a stable reference to the downloaded file.
- [ ] AC-030 The system validates that the downloaded response is a supported video file.
- [ ] AC-031 The system rejects unexpected content types where validation is possible.
- [ ] AC-032 The system supports a configurable maximum file size.

## Design (SA)

`docs/design/REQ-002-design.md` §5 storage, §6 `VideoStorage`, NFR-12, FR-7 (write), FR-11.
No MinIO/S3. Path traversal must be impossible (normalize under root). Tests use a temp directory.
Content-type `application/octet-stream` is allowed only when magic bytes identify a supported
video; otherwise reject.

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
