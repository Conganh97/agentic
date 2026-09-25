---
id: TASK-019
title: Idempotent downloads and public-only bounds
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
depends_on: [TASK-012, TASK-017]
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

Enforce design §7 identity: `(source, sourceIdentity)` so a second POST for the same public video
returns the existing PENDING/RUNNING/COMPLETED job and does not write another file. FAILED or
CANCELLED may start a new job. Reject non-allowed hosts. Provider 401/403/captcha-like HTML stay
permanent failures. Do not add CAPTCHA solvers, credential collection, or private-content access.

## Acceptance Criteria
- [ ] AC-033 Duplicate download requests can be detected.
- [ ] AC-034 Repeated requests for the same source video do not unnecessarily create duplicate downloaded files.
- [ ] AC-047 The implementation does not contain CAPTCHA bypass, credential/session bypass, or private-content access mechanisms.

## Design (SA)

`docs/design/REQ-002-design.md` §7 identity, FR-12, FR-17, NFR-10. Use the partial unique index
from TASK-011. Canonicalize URL (lowercase host, strip tracking params). Do not follow short-link
redirects onto login walls. Tests: two POSTs → one `storageKey`; mock/WireMock only.

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
