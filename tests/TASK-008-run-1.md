---
task: TASK-008
run: 1
verdict: PASS
tested_sha: 607c9c1d8cd7a795c8913d77aeb36fdeaec74261
merge_commit: 607c9c1d8cd7a795c8913d77aeb36fdeaec74261
updated: 2026-09-25 16:03
---

# TASK-008 Test Run 1

- Tested: `main` @ `607c9c1d8cd7a795c8913d77aeb36fdeaec74261` (contains `merge_commit`; product HEAD)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (`VERIFY_EXIT=0`; 100 tests, Failures: 0, Errors: 0, Skipped: 0). Flyway v4 (`video keyset index`) applied in Testcontainers PostgreSQL 16.15.
- Docker: up. Compose `db` only (`postgres:16` on `localhost:15440`, healthy). App: `SERVER_PORT=18081 ./mvnw spring-boot:run -Dspring-boot.run.arguments=--crawler.provider=mock` → schema already at v4 after first start applied `V4__video_keyset_index`; `Tomcat started on port 18081`; `Started DouyinCrawlerApplication in 3.813 seconds`. Health 200 `{"groups":["liveness","readiness"],"status":"UP"}`. No live Douyin GET.
- Black-box: mock crawl keyword `task008-ac018` limit 5 → GET `/api/v1/videos` keyset pages + GET `/api/v1/videos/{id}`. Process stopped; compose db stopped; product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-018 | PASS | `curl -sS -X POST http://localhost:18081/api/v1/crawl-jobs -H 'Content-Type: application/json' -d '{"strategy":"KEYWORD","keyword":"task008-ac018","limit":5}'` → HTTP **202** `{"jobId":"ccdc72e3-dd37-490c-a52b-b1d72c5ffdb7","status":"PENDING"}`. GET job → `COMPLETED` `discovered=5` `persisted=5`. Logs: five `crawl item PERSISTED` (`mock-task008-ac018-1`..`-5`). `GET /api/v1/videos?limit=100` → 5 items with that prefix. `GET /api/v1/videos/79f7bc19-d1db-4c0d-be38-83fb4ba502e9` → HTTP **200** `sourceVideoId=mock-task008-ac018-5` `likeCount=500` `viewCount=5000` `authorName=Mock Author task008-ac018`. Verify: `VideoQueryApiTest#ac018_getReturnsLatestSnapshotFields` + `VideoCrawlQueryIntegrationTest#ac018_ac027_crawlJobThenQueryPersistedVideos`. |
| AC-019 | PASS | `GET /api/v1/videos?source=DOUYIN&limit=2` → HTTP **200** `items.length=2` (`mock-task008-ac018-5`, `mock-task008-ac018-4`) + opaque `nextCursor=MjAyNi0wOS0yNVQwOTowMjo1NS42Mzc2MzdafGU0YTA5NzdkLTRhNzAtNDRmNy1hZTJmLThhYTk5OGJhZmQ0MA`. Same URL with `after=` that cursor → `mock-task008-ac018-3`, `mock-task008-ac018-2` + another `nextCursor`. Keys are only `items` and `nextCursor`. Verify: `VideoQueryApiTest#ac018_ac019_listsVideosWithKeysetPagination` + `ListVideosServiceTest#ac019_nextCursorIsOpaqueAndResumesAfterLastItem`. |
| AC-020 | PASS | List JSON has no `total`. JDBC DEBUG on each list GET executed `SELECT … FROM video … ORDER BY crawled_at DESC, id DESC LIMIT ?` only — no `COUNT(` in the app log. `VideoKeysetSqlTest#ac020_listAfterDoesNotCountVideoRows`. Flyway v4 index `idx_video_crawled_at_id` on `(crawled_at DESC, id DESC)`. Limit 101 → 400 `limit must be between 1 and 100`. |
| AC-027 | PASS | Same verify. `VideoCrawlQueryIntegrationTest` Tests run: 2, Failures: 0 (Testcontainers PostgreSQL 16.15, Flyway v1–v4). Method `ac018_ac027_crawlJobThenQueryPersistedVideos` POST mock keyword `query-int` limit 3 → job `COMPLETED` `persisted=3` then list/get those `mock-query-int-*` rows. Black-box job `ccdc72e3-…` persisted 5 rows in compose Postgres (`select count(*) from video where source_video_id like 'mock-task008-ac018-%'` = 5). `crawler.provider=mock` only. |
| AC-034 | PASS | `GET /v3/api-docs` → HTTP **200** OpenAPI **3.1.0**. Paths `/api/v1/videos` GET `operationId=listVideos` and `/api/v1/videos/{id}` GET `operationId=getVideo`. Document body contains `nextCursor`, `listVideos`, `getVideo`. Verify: `VideoCrawlQueryIntegrationTest#ac034_openApiDocumentsVideoPaths`. |

Exploratory: RFC 9457 — `limit=101` → 400 `limit must be between 1 and 100`; `after=bad` → 400 `Invalid cursor`; unknown UUID → 404 `Video not found`. Unused `keyword` does not hide crawled items. TASK-002..007 suites still pass (100 total). Live Douyin was not called.

Bug (FAIL): none
