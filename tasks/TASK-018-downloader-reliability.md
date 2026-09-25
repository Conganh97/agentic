---
id: TASK-018
title: Download retry, timeout, rate, and concurrency
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
depends_on: [TASK-014, TASK-017]
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

Add in-process retry, rate limit, concurrency, and download timeout around provider HTTP and byte
fetch (configuration properties; no Redis, no extra resilience library). Retry timeout, connection
reset, 429, and 5xx only. Permanent 4xx (except 429), invalid content, and oversize must not loop.

## Acceptance Criteria
- [ ] AC-025 Transient provider/network failures are retried according to configuration.
- [ ] AC-026 Permanent failures are not retried indefinitely.
- [ ] AC-027 Download timeout is configurable.
- [ ] AC-028 Download concurrency is configurable.
- [ ] AC-029 Provider request rate is configurable.

## Design (SA)

`docs/design/REQ-002-design.md` NFR-2, NFR-3, FR-9, FR-10. Defaults: 2 req/s, concurrency 2,
provider HTTP 30s, download 120s, max 3 attempts, backoff 1s/2s/4s. Honor `Retry-After` when
present. Tests use WireMock scenarios; never call the real provider.

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
