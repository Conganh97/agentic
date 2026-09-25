---
id: TASK-013
title: Provider port, mock, and configuration switch
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

Implement the `provider` feature port `VideoDownloadProvider`, a deterministic
`MockVideoDownloadProvider`, and factory/config selection via `downloader.provider`. Application
code must not depend on a SnapTik/VieSnap class. Default `downloader.provider=mock` in `test`.
No real HTTP to VieSnap or montague.ie.

## Acceptance Criteria
- [ ] AC-008 Provider-specific implementation is isolated from the application/domain layer.
- [ ] AC-009 The provider can be changed through configuration without changing application business logic.
- [ ] AC-044 Integration tests do not require the real SnapTik service.
- [ ] AC-045 A mock downloader provider is available for automated tests.

## Design (SA)

`docs/design/REQ-002-design.md` §6 ports, FR-5, NFR-11. Mock returns a small valid mp4 byte array
and metadata (`providerId=MOCK`). Tests assert application packages do not import infrastructure
SnapTik types. IT/wiring uses the mock only.

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
