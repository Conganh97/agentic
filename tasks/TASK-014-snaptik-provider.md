---
id: TASK-014
title: SnapTik VieSnap adapter using documented flow
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
depends_on: [TASK-013]
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

Implement `SnapTikVideoDownloadProvider` behind the port. Follow design §6 exactly: POST
`{api-base-url}{info-path}` with JSON `{"url":…}`, parse `qualities.best`, then GET the documented
redirect or `/download` URL from `{download-base-url}`. Default config provider is `snaptik` outside
`test`. Hosts come from properties only (no Java string literals for `viesnap.com` / `montague.ie`
base URLs). Tests use WireMock only.

## Acceptance Criteria
- [ ] AC-005 SnapTik at `montague.ie` is implemented as the default provider.
- [ ] AC-006 The implementation verifies the actual `montague.ie` request/response flow before integrating it.
- [ ] AC-007 The actual provider endpoint, HTTP method, required headers, request parameters, request body, and response parsing logic are documented in `docs/design/REQ-002-design.md`.
- [ ] AC-010 The provider base URL is configurable.
- [ ] AC-015 The system does not hard-code the SnapTik provider URL throughout the source code.

## Design (SA)

`docs/design/REQ-002-design.md` §6 Provider investigation (2026-09-25): POST
`https://api3.viesnap.com/douyin/info` (configurable), `Content-Type: application/json`,
body `{"url"}`; then GET `dl2.viesnap.com` redirect or `/download` as specified. No invented API
key. Do not implement `/stats/download` or the affiliate offer gate. 401/403/captcha-like HTML are
permanent failures. AC-006/AC-007: implement the documented flow; do not invent other endpoints.
AC-005: default `downloader.provider=snaptik` in the main/default profile (mock remains test).

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
