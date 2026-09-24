---
id: TASK-005
title: Frontend feed create like profile
type: TASK
priority: HIGH
status: READY_FOR_DEPLOY
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
merge_commit: ab07b1702e6d70511ba29bf003513c495dda3213
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
updated: 2026-09-24 16:04
---

## Description

Implement Luma home feed, create-post, like/unlike, and profile grid in `product/frontend` per
TASK-001 + Figma. Use TanStack Query against the TASK-003 API. Photo-first density; square tiles
on profile. Seeded feed must be visible on first local run.

## Acceptance Criteria

- [x] AC-001 `/feed` lists posts newest-first with image, caption, author avatar/name, like count,
      and liked state; first local run against a seeded API is not an empty feed.
- [x] AC-002 Signed-in member publishes from `/create` (file or HTTPS URL + caption 1–2200); the
      new post appears at the top of `/feed`. Signed-out visit redirects to `/sign-in`.
- [x] AC-003 Like and unlike toggle the heart and change the displayed count by exactly one
      without a full page reload.
- [x] AC-004 `/u/:username` shows username, avatar, bio, and that user's post grid. A member with
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

### Round 1 — APPROVED
Reviewed: `feature/TASK-005-luma-feed-ui` @ `0604394` · Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (23)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | ProfileView.tsx | MINOR | Overlay is a Mantine `Modal` whose title repeats the author already on `PhotoCard`. UX asked for a simple image+caption+heart overlay; UX/UI review already logged this as MINOR. |
| 2 | useFeed.ts | MINOR | `useCreatePost` prepends the new card then `invalidateQueries(feedQueryKey)`, so the optimistic first row can refetch immediately. Harmless if the API returns the same post first. |

Merged `ab07b1702e6d70511ba29bf003513c495dda3213`.

## Test (TEST)

### Run 1 — PASS
- Tested: main @ ab07b1702e6d70511ba29bf003513c495dda3213 (contains merge_commit)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (23)
- AC-001 pass — browser `/feed` 6 seeded cards newest-first; images load; caption/author/likes
- AC-002 pass — signed-out `/create` → `/sign-in`; luna HTTPS create → toast Shared + first on `/feed`
- AC-003 pass — like 0→1 then unlike 1→0; no full reload (same navigation entry)
- AC-004 pass — `/u/luna` grid; `/u/empty005` empty; 9 skeletons; 404 + network EmptyStates
- Evidence: `tests/TASK-005-run-1.md`

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001; repo frontend; requires_uxui; deps TASK-001, TASK-003, TASK-004 |
| 2026-09-24 15:40 | BACKLOG | READY | SCRUM | DoR met; deps TASK-001 MERGED, TASK-003/004 READY_FOR_DEPLOY |
| 2026-09-24 15:42 | READY | IN_PROGRESS | FE | branch feature/TASK-005-luma-feed-ui |
| 2026-09-24 15:47 | IN_PROGRESS | CODE_REVIEW | FE | product 0604394; FE verify pass (23); pushed feature/TASK-005-luma-feed-ui |
| 2026-09-24 15:57 | CODE_REVIEW | MERGED | SA | reviews/TASK-005-round-1.md APPROVED; merge_commit=ab07b1702e6d70511ba29bf003513c495dda3213 (--no-ff, two parents); FE verify PASS (23); uxui_review APPROVED |
| 2026-09-24 15:58 | MERGED | TESTING | TEST | merge_commit=ab07b1702e6d70511ba29bf003513c495dda3213 is ancestor of frontend main @ ab07b1702e6d70511ba29bf003513c495dda3213 |
| 2026-09-24 16:04 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-005-run-1.md PASS; AC-001..AC-004 checked; tested sha=ab07b1702e6d70511ba29bf003513c495dda3213 ancestor of main |
