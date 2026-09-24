---
task: TASK-003
round: 1
decision: APPROVED
branch: feature/TASK-003-luma-posts-feed
sha: f599ae5
updated: 2026-09-24 15:20
---

# TASK-003 Review Round 1

Reviewed: `feature/TASK-003-luma-posts-feed` @ `f599ae5` · Build/tests: `./mvnw -q verify` PASS

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | PostService.java | MINOR | Application layer returns `post.api` records; prefer application DTOs if the layering is tightened later. |
| 2 | application.yaml | MINOR | Servlet multipart max is 10MB; create-post still rejects > 8 MiB in `PostService` (and maps oversized uploads to 400). |

AC-001..AC-004 met against design §6–§7: public newest-first feed with PostCard + seed ≥6; create 201 + first in feed, 401 without session, 400 for `http://` / bad MIME / >8 MiB; like PUT idempotent and DELETE ±1; profiles + author posts, 404 unknown, empty `items` when zero posts. HTTPS URLs stored as-is; uploads under `luma.media.dir` served at `GET /api/v1/media/{id}`. Session required for create/like (NFR-2). V2 schema + idempotent seed; members V1 unchanged.

Merged `9113e93db114032c2f90383a76af872709af33f3`.
