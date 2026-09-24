---
id: TASK-005
title: Frontend feed create like profile
type: TASK
priority: HIGH
status: READY
assignee: FE
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo: frontend
work_type: FRONTEND
requires_uxui: true
uxui_task: TASK-001
uxui_design:
uxui_review:
figma:
depends_on: [TASK-001, TASK-003, TASK-004]
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
updated: 2026-09-24 15:40
---

## Description

Implement Luma home feed, create-post, like/unlike, and profile grid in `product/frontend` per
TASK-001 + Figma. Use TanStack Query against the TASK-003 API. Photo-first density; square tiles
on profile. Seeded feed must be visible on first local run.

## Acceptance Criteria

- [ ] AC-001 `/feed` lists posts newest-first with image, caption, author avatar/name, like count,
      and liked state; first local run against a seeded API is not an empty feed.
- [ ] AC-002 Signed-in member publishes from `/create` (file or HTTPS URL + caption 1–2200); the
      new post appears at the top of `/feed`. Signed-out visit redirects to `/sign-in`.
- [ ] AC-003 Like and unlike toggle the heart and change the displayed count by exactly one
      without a full page reload.
- [ ] AC-004 `/u/:username` shows username, avatar, bio, and that user's post grid. A member with
      no posts shows the designed empty state. Loading and error states match the UX spec (not a
      blank page).

## Design (SA)

`docs/design/REQ-001-design.md` §6 and §13 routes `/feed`, `/create`, `/u/:username`. FR-4..FR-8,
NFR-6. `requires_uxui: true`; `depends_on` TASK-001, TASK-003, TASK-004.
`requirement_revision: 3`, `content_hash: 54839e9b074480c8`.

## Implementation (BE/FE)

## UX/UI Review

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001; repo frontend; requires_uxui; deps TASK-001, TASK-003, TASK-004 |
| 2026-09-24 15:40 | BACKLOG | READY | SCRUM | DoR met; deps TASK-001 MERGED, TASK-003/004 READY_FOR_DEPLOY |
