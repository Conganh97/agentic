---
task: TASK-008
round: 1
decision: APPROVED
branch: feature/TASK-008-video-query-api
sha: d0b1436b4e0790094032cfb2628b2a71c8d7ffa5
updated: 2026-09-25 15:59
---

# TASK-008 Review Round 1

Reviewed: `feature/TASK-008-video-query-api` @ `d0b1436b4e0790094032cfb2628b2a71c8d7ffa5` · Build/tests: `./mvnw -q verify` PASS (100)

`project.md` verify: registry row `douyin-crawler-service` · type BE · path `product/services/douyin-crawler-service` · remote `https://github.com/Conganh97/product-douyin-crawler-service`. Stack Java 21 + Boot 4 + PostgreSQL 16 + Flyway + JPA + `ddl-auto=validate` matches design §5. Package-by-feature `video/{api,application,domain,infrastructure}`. Default `crawler.provider=mock`.

Contract vs §6 / NFR-3 / NFR-10 / FR-10: `GET /api/v1/videos` returns `{ items, nextCursor }` with optional `source`, unused `keyword`, optional `after`, `limit` default 20 max 100. Keyset SQL on `(crawled_at DESC, id DESC)` with `limit+1`; no `COUNT(*)` on `video`; Flyway `V4__video_keyset_index.sql`. `GET /api/v1/videos/{id}` returns video + latest snapshot fields. 400/404 use RFC 9457 `ProblemDetail`. OpenAPI `/v3/api-docs` documents `listVideos` and `getVideo`. Integration: Testcontainers + mock crawl job then query.

Implementation-level AC coverage on the branch: AC-018 (list/get + latest snapshot), AC-019 (keyset `nextCursor` resume), AC-020 (no `COUNT(*)` / no `total`), AC-027 (crawl-then-query Testcontainers), AC-034 (OpenAPI paths + operationIds).

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | JpaVideoMetricRepository.java | MINOR | `findLatestByVideoIds` loads every snapshot for the page then keeps the first per id |
| 2 | VideoCursor.java | MINOR | Cursor is reversible Base64 of `instant\|uuid`; design only requires opaque, not signed |
| 3 | VideoController.java | MINOR | OpenAPI `@Operation` does not declare 400/404 ProblemDetail responses (paths and operationIds are present) |

Merged `607c9c1d8cd7a795c8913d77aeb36fdeaec74261`.
