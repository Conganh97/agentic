---
id: TASK-004
title: Discovery port, mock, and public keyword provider
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
depends_on: [TASK-002]
sprint: SPRINT-03
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
updated: 2026-09-25 14:59
---

## Description

Implement the `discovery` feature: domain port `VideoDiscoveryProvider`, a deterministic
`MockVideoDiscoveryProvider`, and a `PublicKeywordDiscoveryProvider` that performs unauthenticated
public GETs via `RestClient` and maps available metadata. Application code must not depend on the
HTTP class. Default `crawler.provider=mock` in `test`.

## Acceptance Criteria
- [ ] AC-004 The crawler can discover public Douyin videos using at least one supported discovery strategy.
- [ ] AC-005 Discovered videos contain the required metadata when that metadata is publicly available.
- [ ] AC-028 Integration tests can run without requiring a real Douyin account.
- [ ] AC-029 A mock discovery provider is available for automated tests.
- [ ] AC-031 The crawler implementation is isolated behind an abstraction that allows another provider implementation to be introduced later.

## Design (SA)

`docs/design/REQ-001-design.md` §5, §6 port, FR-4, FR-5, FR-12, FR-13. Strategy v1 = `KEYWORD`.
Required fields as in design §6. Tests use the mock and/or WireMock; they must not call Douyin.
HTTP impl on 401/403/captcha-like HTML returns a permanent item/provider failure — no bypass.

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
| 2026-09-25 14:59 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002] MERGED |
