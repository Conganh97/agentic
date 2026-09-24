---
id: TASK-005
title: Frontend feed create like profile
type: TASK
priority: HIGH
status: CODE_REVIEW
assignee: FE
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo: frontend
work_type: FRONTEND
requires_uxui: true
uxui_task: TASK-001
uxui_design: docs/design/ux/REQ-001-ux.md
uxui_review: docs/design/ux/reviews/TASK-005-review-1.md
figma: https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma?node-id=1-18
depends_on: [TASK-001, TASK-003, TASK-004]
sprint:
branch: feature/TASK-005-luma-feed-ui
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
updated: 2026-09-24 15:55
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

### Iteration 1 (feed / create / like / profile)
- Branch: `feature/TASK-005-luma-feed-ui` @ 0604394
- Changed: `src/pages/{Feed,Create,Profile}Page.tsx`, `src/features/{feed,create,profile}/`, `src/shared/api/client.ts`, `src/shared/ui/Field.tsx`
- Tests: FE verify → pass (23)
- Notes: TanStack Query vs TASK-003; photo-first PhotoCard, HeartLike, square ProfileTile; Figma MCP rate-limited so implemented from `docs/design/ux/REQ-001-ux.md` + frames 1:18/1:21/1:24; pushed via repo.py

## UX/UI Review

### Iteration 1 (2026-09-24 15:55)
- Review: `docs/design/ux/reviews/TASK-005-review-1.md` APPROVED
- Compared: spec + running `/feed` `/create` `/u/luna` `/u/emptyreview` on `feature/TASK-005-luma-feed-ui` @ 0604394 (mobile 390 + desktop 1280); Figma MCP rate-limited

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001; repo frontend; requires_uxui; deps TASK-001, TASK-003, TASK-004 |
| 2026-09-24 15:40 | BACKLOG | READY | SCRUM | DoR met; deps TASK-001 MERGED, TASK-003/004 READY_FOR_DEPLOY |
| 2026-09-24 15:42 | READY | IN_PROGRESS | FE | branch feature/TASK-005-luma-feed-ui |
| 2026-09-24 15:47 | IN_PROGRESS | CODE_REVIEW | FE | product 0604394; FE verify pass (23); pushed feature/TASK-005-luma-feed-ui |
