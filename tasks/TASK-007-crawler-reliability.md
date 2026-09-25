---
id: TASK-007
title: Crawler retry, rate limit, and public-only bounds
type: TASK
priority: HIGH
status: READY
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: douyin-crawler-service
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: [TASK-004]
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
updated: 2026-09-25 15:29
---

## Description

Add in-process retry, rate limit, concurrency, and HTTP timeout around discovery HTTP calls
(configuration properties; no Redis, no extra resilience library). Enforce product bounds: no
video-file download and no media/AI features; the HTTP provider only uses public GETs and treats
blocked/captcha-like responses as permanent failures.

## Acceptance Criteria
- [ ] AC-014 Transient crawler failures are retried according to configurable retry settings.
- [ ] AC-015 Permanent failures are not endlessly retried.
- [ ] AC-016 Crawler request rate and concurrency are configurable.
- [ ] AC-032 The implementation does not include video downloading or any downstream AI/video-processing functionality.
- [ ] AC-033 The crawler only accesses publicly available content and does not implement credential collection, CAPTCHA solving, or platform-security bypass mechanisms.

## Design (SA)

`docs/design/REQ-001-design.md` §4 NFR-1, NFR-4, NFR-11, FR-8, FR-9, FR-14, FR-15.
Defaults: 1 req/s, concurrency 4, timeout 10s, max 3 retries on timeout/429/5xx only.
Properties under `crawler.retry.*`, `crawler.rate.*`, `crawler.concurrency`, `crawler.http.timeout`.

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
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 15:29 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-004] READY_FOR_DEPLOY |
