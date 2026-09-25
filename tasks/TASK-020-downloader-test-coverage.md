---
id: TASK-020
title: Unit and integration coverage for download lifecycle
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
depends_on: [TASK-018, TASK-019]
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

Close remaining test gaps so `./mvnw -q verify` covers provider selection, job lifecycle, retry,
validation, and idempotency at unit level, and persistence plus job lifecycle at integration level.
Tests must use mock and/or WireMock + Testcontainers PostgreSQL only — never `*.viesnap.com` or
`montague.ie`.

## Acceptance Criteria
- [ ] AC-042 Unit tests cover provider selection, job lifecycle, retry behaviour, validation, and idempotency.
- [ ] AC-043 Integration tests cover persistence and download job lifecycle.

## Design (SA)

`docs/design/REQ-002-design.md` FR-15, NFR-9. This task adds any missing tests; it does not invent
new product APIs. Assert no test or main code calls the real VieSnap hosts.

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
