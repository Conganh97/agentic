---
id: TASK-008
title: Video query API, keyset pagination, and crawl integration tests
type: TASK
priority: HIGH
status: RELEASED
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
depends_on: [TASK-003, TASK-006]
sprint:
branch: feature/TASK-008-video-query-api
merge_commit: 607c9c1d8cd7a795c8913d77aeb36fdeaec74261
release: DEV
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
updated: 2026-09-25 16:19
---

## Description

Add `GET /api/v1/videos` and `GET /api/v1/videos/{id}` with keyset pagination (no `COUNT(*)` on
`video` for normal paging). Freeze the REST contract for later orchestration. Add Testcontainers
integration tests that run a crawl job (mock provider) and then query persisted videos.

## Acceptance Criteria
- [x] AC-018 Crawled videos can be queried through an API.
- [x] AC-019 Video querying supports pagination.
- [x] AC-020 The implementation does not depend on expensive full-table COUNT queries for normal high-volume pagination.
- [x] AC-027 Integration tests verify PostgreSQL persistence and crawl-job behaviour.
- [x] AC-034 The service exposes a stable contract that can later be consumed by an orchestration layer such as n8n.

## Design (SA)

`docs/design/REQ-001-design.md` §6 video endpoints, NFR-3, NFR-10, FR-10. Cursor on
`(crawled_at DESC, id DESC)`. Default limit 20, max 100. OpenAPI must document these paths.
Integration tests: Testcontainers + `crawler.provider=mock` only.

## Implementation (BE/FE)

### Iteration 1 (video query API)
- Branch: `feature/TASK-008-video-query-api` @ d0b1436
- Changed: `video/{api,application,domain,infrastructure}`, `V4__video_keyset_index.sql`, `ApiExceptionHandler`
- Tests: `./mvnw -q verify` → pass (100)
- Notes: GET `/api/v1/videos` keyset on `(crawled_at DESC, id DESC)`, default limit 20 max 100, opaque `nextCursor`, no `COUNT(*)` on `video`. GET `/api/v1/videos/{id}` returns latest snapshot fields. OpenAPI documents both paths (`listVideos`, `getVideo`). Integration: Testcontainers + `crawler.provider=mock` crawl job then query.

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

### Round 1 — APPROVED
Reviewed: feature/TASK-008-video-query-api @ `d0b1436b4e0790094032cfb2628b2a71c8d7ffa5` · Build/tests: `./mvnw -q verify` PASS (100)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | JpaVideoMetricRepository.java | MINOR | `findLatestByVideoIds` loads every snapshot for the page then keeps the first per id |
| 2 | VideoCursor.java | MINOR | Cursor is reversible Base64 of `instant\|uuid`; design only requires opaque, not signed |
| 3 | VideoController.java | MINOR | OpenAPI `@Operation` does not declare 400/404 ProblemDetail responses (paths and operationIds are present) |

## Test (TEST)

### Run 1 — PASS
- Tested: main @ 607c9c1d8cd7a795c8913d77aeb36fdeaec74261 (contains merge_commit)
- Build/tests: `./mvnw -q verify` PASS (100; Testcontainers PostgreSQL 16.15; Flyway v4)
- AC-018 pass — mock POST `/api/v1/crawl-jobs` keyword `task008-ac018` limit 5 → GET `/api/v1/videos` 5 `mock-task008-ac018-*`; GET by id 200 latest snapshot
- AC-019 pass — `limit=2` returns `nextCursor`; `after=` resumes next two items; no `total`
- AC-020 pass — list SQL `ORDER BY crawled_at DESC, id DESC LIMIT ?`; no `COUNT(` in JDBC log; index `idx_video_crawled_at_id`
- AC-027 pass — `VideoCrawlQueryIntegrationTest` crawl-then-query on Testcontainers; compose Postgres 5 persisted rows
- AC-034 pass — `GET /v3/api-docs` OpenAPI 3.1.0 paths `listVideos` / `getVideo` + `nextCursor`
- Evidence: `tests/TASK-008-run-1.md`

## Deployment (DEVOPS)

### DEV — 2026-09-25 16:19 — OK
- Images: `ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1` and `:dev`
- Command: reused healthy `ops/compose/dev.yml` (TASK-002 image already up; `python3 scripts/deploy.py --env DEV --component douyin-crawler-service` not re-run)
- Smoke: `http://127.0.0.1:18081/actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}`; POST `/api/v1/crawl-jobs` keyword `task008-dev-smoke` limit 3 → 202 `{"jobId":"7836aa7a-…","status":"PENDING"}`; GET same job → 200 `COMPLETED` `discovered=3` `persisted=3`; GET `/api/v1/videos?limit=3` → 200 `items` `mock-task008-dev-smoke-3`..`-1` + `nextCursor`
- Rollback: `docker compose -f ops/compose/dev.yml up -d` with the previous tag

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 15:51 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-003, TASK-006] READY_FOR_DEPLOY |
| 2026-09-25 15:53 | READY | IN_PROGRESS | BE | branch feature/TASK-008-video-query-api from product main a79b495 |
| 2026-09-25 15:57 | IN_PROGRESS | CODE_REVIEW | BE | product sha d0b1436b4e0790094032cfb2628b2a71c8d7ffa5; Implementation iteration 1; ./mvnw -q verify pass (100) |
| 2026-09-25 15:59 | CODE_REVIEW | MERGED | SA | reviews/TASK-008-round-1.md APPROVED; merge_commit 607c9c1d8cd7a795c8913d77aeb36fdeaec74261 (--no-ff, parents a79b495 + d0b1436); ./mvnw -q verify PASS (100) |
| 2026-09-25 16:00 | MERGED | TESTING | TEST | tested sha 607c9c1d8cd7a795c8913d77aeb36fdeaec74261 is product main HEAD and contains merge_commit; run 1 started |
| 2026-09-25 16:03 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-008-run-1.md PASS; AC-018 AC-019 AC-020 AC-027 AC-034 checked; ./mvnw -q verify PASS (100); mock crawl + GET /api/v1/videos keyset + GET by id; OpenAPI 3.1.0 |
| 2026-09-25 16:19 | READY_FOR_DEPLOY | DEPLOYING | DEVOPS | DEV deploy started; PQA accept APPROVED docs/design/reviews/REQ-001-accept-1.md; reuse healthy compose ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1 |
| 2026-09-25 16:19 | DEPLOYING | RELEASED | DEVOPS | DEV compose reused OK; image ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1; smoke GET http://127.0.0.1:18081/actuator/health → 200 status=UP; POST /api/v1/crawl-jobs → 202 PENDING; GET COMPLETED discovered=3 persisted=3; GET /api/v1/videos?limit=3 → 200 mock-task008-dev-smoke-* + nextCursor; release=DEV |
