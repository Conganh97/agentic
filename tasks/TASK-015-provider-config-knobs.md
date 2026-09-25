---
id: TASK-015
title: Provider path, timeout, retry, and header properties
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
depends_on: [TASK-014]
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

Finish SnapTik provider configuration: `info-path`, `download-path`, `redirect-path`, provider
timeout, provider max-retries, and optional extra request headers map. Values must be overridable
by environment variables as in design §6. Do not invent or require an API key. Unit/WireMock tests
prove each knob is read and applied.

## Acceptance Criteria
- [ ] AC-011 Provider-specific endpoint/path configuration is configurable where technically appropriate.
- [ ] AC-012 Provider-specific timeout is configurable.
- [ ] AC-013 Provider-specific retry configuration is configurable.
- [ ] AC-014 Provider-specific request headers are configurable where appropriate.

## Design (SA)

`docs/design/REQ-002-design.md` §6 yaml, FR-6. Defaults: info `/douyin/info`, download `/download`,
redirect `/douyin/redirect`, timeout 30s, max-retries 3, headers empty. Optional headers are
forwarded on info POST and byte GET except that cookie/token header values must never be logged
(NFR-5). Download-level timeout/rate stay TASK-018.

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
