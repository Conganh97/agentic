---
id: TASK-003
title: luma-service posts likes profiles seed
type: TASK
priority: HIGH
status: CODE_REVIEW
assignee: BE
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo: luma-service
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: [TASK-002]
sprint:
branch: feature/TASK-003-luma-posts-feed
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
updated: 2026-09-24 15:17
---

## Description

On `luma-service`, add posts, likes, public profiles, image upload/serve, and demo seed. Feed and
profiles are public. Create-post and like/unlike require a valid `LUMA_SESSION`. Store HTTPS image
URLs as-is; store uploaded files under `luma.media.dir` and serve at `GET /api/v1/media/{id}`.

## Acceptance Criteria

- [ ] AC-001 `GET /api/v1/posts` returns items newest-first; each `PostCard` has `imageUrl`,
      `caption`, `author.username`, `author.avatarUrl`, `likeCount`, `likedByMe` (false when no
      session). After migrate + seed the list has ≥6 posts.
- [ ] AC-002 Signed-in `POST /api/v1/posts` (caption 1–2200 + file XOR `https://` `imageUrl`)
      returns 201 and that post is first in the feed. Missing session is 401. Bad MIME, `http://`
      URL, or file > 8 MiB is 400.
- [ ] AC-003 `PUT /api/v1/posts/{id}/likes` then `DELETE` toggles `likedByMe` and changes
      `likeCount` by exactly one; a second PUT does not increment again. No session is 401.
- [ ] AC-004 `GET /api/v1/profiles/{username}` returns username, avatarUrl, bio, postCount.
      `GET .../posts` lists that user's posts. Unknown user is 404. User with zero posts returns
      empty `items` (not 404).

## Design (SA)

`docs/design/REQ-001-design.md` §6–§7 (posts, likes, profiles, media, seed). FR-4..FR-9, NFR-2,
NFR-5, NFR-8. Depends on TASK-002 members + session. `requirement_revision: 3`,
`content_hash: 54839e9b074480c8`.

## Implementation (BE/FE)

### Iteration 1
- Branch: `feature/TASK-003-luma-posts-feed` @ f599ae5
- Changed: `post/{api,application,domain,infrastructure}`, `like/{application,domain,infrastructure}`, `media/{api,application,domain,infrastructure}`, `member/{api,application}`, Flyway `V2__posts_likes_media.sql`, `R__seed_demo.sql`
- Tests: `./mvnw -q verify` → pass (22)
- Notes: session required for create/like; public feed/profiles/media; HTTPS URLs stored as-is; uploads under `luma.media.dir`; seed `luna`/`noah` (password `demo-pass-8`) + 6 HTTPS posts; members V1 unchanged

## UX/UI Review

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001; repo luma-service; depends_on TASK-002 |
| 2026-09-24 15:08 | BACKLOG | READY | SCRUM | DoR met; deps TASK-002 READY_FOR_DEPLOY |
| 2026-09-24 15:09 | READY | IN_PROGRESS | BE | branch feature/TASK-003-luma-posts-feed |
| 2026-09-24 15:17 | IN_PROGRESS | CODE_REVIEW | BE | product f599ae5; ./mvnw -q verify pass (22) |
