---
requirement: REQ-001
round: 1
status: APPROVED
reviewer: PQA
updated: 2026-09-25 16:05
---

# REQ-001 increment accept 1

Ran: BE + DB (no FE). Product `douyin-crawler-service` `main` @ `607c9c1d8cd7a795c8913d77aeb36fdeaec74261`.
Postgres 16 in Docker (`pqa-req001-pg` on `localhost:15440`). App:
`JAVA_HOME=…/openjdk…/Home SERVER_PORT=18081 ./mvnw spring-boot:run -Dspring-boot.run.arguments=--crawler.provider=mock`.
Flyway applied v1–v4. ECS log: `Started DouyinCrawlerApplication in 3.985 seconds`; `Tomcat started on port 18081`.
No live Douyin GET. Density bar N/A (design §13 none; API-only increment).

Children on disk: TASK-001 DEVOPS `MERGED`; TASK-002..008 `READY_FOR_DEPLOY` with TEST run-1 PASS.

| AC / screen | Result | Evidence |
|-------------|--------|----------|
| Density (390 + 1280) | N/A | No UI / screens. Design §13 none. |
| AC-001 | PASS | Documented local setup started. Health 200 `{"groups":["liveness","readiness"],"status":"UP"}`. |
| AC-002 | PASS | `POST /api/v1/crawl-jobs` `{"strategy":"KEYWORD","keyword":"pqa-accept-1","limit":5}` → HTTP **202** `{"jobId":"25c26ad3-deb9-4167-b39e-2075f234da18","status":"PENDING"}`. |
| AC-003 | PASS | Same POST `/usr/bin/time -p` **real 0.16** (under NFR-2 500 ms). Body `PENDING`. Immediate GET → `RUNNING`, next poll `COMPLETED` (`startedAt`/`finishedAt` set). Request did not hold the crawl. |
| AC-004 | PASS | Mock KEYWORD discovery persisted `mock-pqa-accept-1-1`..`-5`. Port + public GET: `tests/TASK-004-run-1.md` PASS. |
| AC-005 | PASS | GET `/api/v1/videos/672fdf8f-9fbd-4ac1-97ae-ee14580e29d7` → `source=DOUYIN` `sourceVideoId=mock-pqa-accept-1-5` `canonicalUrl` `authorId` `authorName` `title` `publishedAt` `durationSeconds=15` `coverImageUrl` `likeCount=500` `commentCount=50` `shareCount=25` `collectCount=10` `crawledAt`. |
| AC-006 | PASS | `SELECT count(*) FROM video WHERE source_video_id LIKE 'mock-pqa-accept-1-%'` = **5**. Flyway `public` at v4. |
| AC-007 | PASS | Second job `c0e17549-7d41-4a0f-a2e4-54adc72095f0` → `COMPLETED` `persisted=0` `duplicates=5`. Video count stayed 5. No duplicate `(source, source_video_id)` groups. |
| AC-008 | PASS | `uk_video_source_source_video_id UNIQUE (source, source_video_id)` present. Insert uses `ON CONFLICT DO NOTHING`. TASK-003-run-1: raw JDBC duplicate raises `DuplicateKeyException`. |
| AC-009 | PASS | Job `25c26ad3-…` `discovered=5`. |
| AC-010 | PASS | Same job `persisted=5`. |
| AC-011 | PASS | Job `c0e17549-…` `duplicates=5`. Logs: `crawl item DUPLICATE` for `mock-pqa-accept-1-1`..`-5`. |
| AC-012 | PASS | Live mock emits no item failures (`failed=0`). Isolation + failed counter: `tests/TASK-006-run-1.md` (PARTIAL `failed=1`, remaining items persisted). `ExecuteCrawlJobService` increments `failed` per item and continues. |
| AC-013 | PASS | Same TASK-006-run-1 + `processDiscoveredVideo` catch → `FAILED` then next item. One failure does not abort the job. |
| AC-014 | PASS | `application.yaml`: `crawler.retry.max-attempts=3`, backoff 1s ×2. `DiscoveryHttpGuard` retries timeout / 429 / 5xx. `tests/TASK-007-run-1.md` PASS (WireMock; no live Douyin). |
| AC-015 | PASS | 401/403/captcha-like HTML are permanent; not retried. TASK-007-run-1 PASS. |
| AC-016 | PASS | Live defaults: `crawler.rate.requests-per-second=1`, `crawler.concurrency=4`, `crawler.http.timeout=10s`. TASK-007-run-1 PASS. |
| AC-017 | PASS | `GET /api/v1/crawl-jobs/25c26ad3-…` HTTP **200** with status + counters. |
| AC-018 | PASS | `GET /api/v1/videos?limit=100` → 5 items. GET by id returns latest snapshot fields. |
| AC-019 | PASS | `limit=2` page1 `mock-pqa-accept-1-5`, `-4` + opaque `nextCursor`; page2 `-3`, `-2` + another cursor. Keys only `items`, `nextCursor`. |
| AC-020 | PASS | List JSON has no `total`. `JpaVideoRepository.LIST_AFTER` is keyset `ORDER BY crawled_at DESC, id DESC LIMIT :limit`. No `COUNT(*)` under `src/main`. `limit=101` → 400 `limit must be between 1 and 100`. |
| AC-021 | PASS | After two crawls, each `mock-pqa-accept-1-*` has **2** `video_metric` rows (insert-only). |
| AC-022 | PASS | ECS JSON logs. Sample: `{"message":"crawl item PERSISTED","jobId":"25c26ad3-deb9-4167-b39e-2075f234da18","outcome":"PERSISTED","sourceVideoId":"mock-pqa-accept-1-1","ecs":{"version":"8.11"}}`. No tokens/cookies. |
| AC-023 | PASS | `GET /actuator/prometheus` 200. After two jobs: `crawler_jobs_total{status="COMPLETED"} 2.0`, `crawler_videos_discovered_total 10.0`, `persisted 5.0`, `duplicates 5.0`, `failed 0.0`, `crawler_job_duration_seconds_count 2`. |
| AC-024 | PASS | `GET /actuator/health` 200 `status=UP`. |
| AC-025 | PASS | `GET /v3/api-docs` 200 OpenAPI **3.1.0**. Paths `/api/v1/crawl-jobs`, `/api/v1/crawl-jobs/{jobId}`, `/api/v1/videos`, `/api/v1/videos/{id}`; `operationId` `listVideos` / `getVideo`. |
| AC-026 | PASS | Unit suites on HEAD: TASK-008-run-1 `./mvnw -q verify` **100** tests, 0 failures (includes domain/application). |
| AC-027 | PASS | Same verify + this accept: crawl then query against Docker PostgreSQL 16. `VideoCrawlQueryIntegrationTest` on HEAD. |
| AC-028 | PASS | Accept used `crawler.provider=mock` only. TASK-004-run-1: mock + WireMock, no Douyin account. |
| AC-029 | PASS | Default `crawler.provider: mock` in `application.yaml`. `MockVideoDiscoveryProvider` bean. |
| AC-030 | PASS | `Dockerfile` + `ops/compose/dev.yml` (API + postgres:16). This accept ran DB in Docker. TASK-001 DEVOPS `MERGED` (skip TEST correct). API image not started (no deploy). |
| AC-031 | PASS | Application depends on `VideoDiscoveryProvider` only. `DiscoveryApplicationIsolationTest` + TASK-004-run-1. |
| AC-032 | PASS | No download / media / AI in `src/main`. TASK-007-run-1 `CrawlerReliabilityBoundsTest` AC-032. |
| AC-033 | PASS | Public unauthenticated GET only; 401/403/captcha → permanent failure; no solver/bypass. TASK-007-run-1. |
| AC-034 | PASS | Stable REST + OpenAPI (`listVideos` / `getVideo` / crawl-jobs). RFC 9457: unknown strategy → 400 `Unknown strategy`. Suitable for later n8n. |

| # | Must-fix (FAIL only) | Owner | SA agreement |
|---|----------------------|-------|----------------|
| — | none | — | — |

**Decision:** APPROVED

Side sprint: leftover fix tasks > 5 → Scrum `/scrum sprint`. (none)
