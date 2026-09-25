---
task: TASK-006
run: 1
verdict: PASS
tested_sha: a79b4957d7a733e65d7c792205b3aecb871c25f6
merge_commit: a79b4957d7a733e65d7c792205b3aecb871c25f6
updated: 2026-09-25 15:50
---

# TASK-006 Test Run 1

- Tested: `main` @ `a79b4957d7a733e65d7c792205b3aecb871c25f6` (contains `merge_commit`; product HEAD)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (`VERIFY_EXIT=0`; 78 tests, Failures: 0, Errors: 0, Skipped: 0). Flyway v3 (`crawl_job_item`) applied in Testcontainers PostgreSQL 16.15.
- Docker: up. Compose `db` only (`postgres:16` on `localhost:15440`, healthy). App: `SERVER_PORT=18081 ./mvnw spring-boot:run --crawler.provider=mock` → `Successfully applied 1 migration … now at version v3`; `Tomcat started on port 18081`; `Started DouyinCrawlerApplication in 4.084 seconds`. Health 200 `{"groups":["liveness","readiness"],"status":"UP"}`. No live Douyin GET.
- Mock provider never emits item failures; AC-012/013 HTTP used a one-row `BEFORE INSERT` fixture on `video` for `mock-task006-iso-2` (dropped after the probe). Process stopped; compose db stopped; product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-009 | PASS | `curl -sS -X POST http://localhost:18081/api/v1/crawl-jobs -H 'Content-Type: application/json' -d '{"strategy":"KEYWORD","keyword":"task006-ac009","limit":3}'` → HTTP **202** `{"jobId":"f082152f-e003-4d11-b727-6ba9e02fa51c","status":"PENDING"}`. `GET /api/v1/crawl-jobs/f082152f-…` → HTTP **200** `status=COMPLETED` `discovered=3` `persisted=3` `duplicates=0` `failed=0`. Verify: `ExecuteCrawlJobServiceTest#ac009_recordsDiscoveredCount` + `CrawlJobExecutionTest#ac009_ac010_jobRecordsDiscoveredAndPersistedVideos`. |
| AC-010 | PASS | Same GET: `persisted=3` for a first-time keyword (3 mock videos written). Prometheus after the run: `crawler_videos_persisted_total 8.0` (includes later jobs). |
| AC-011 | PASS | Second POST same keyword `task006-ac009` limit 3 → job `0204cdc5-5794-457b-9d0f-97000b5b36b0`. GET → `status=COMPLETED` `discovered=3` `persisted=0` `duplicates=3` `failed=0`. Prometheus: `crawler_videos_duplicates_total 3.0`. Verify: `CrawlJobExecutionTest#ac011_jobRecordsDuplicateVideos`. |
| AC-012 | PASS | Isolation POST keyword `task006-iso` limit 3 → job `b2bbba36-c7a7-4aa4-a4b3-51e5f22a5cca`. GET → `failed=1` (and `discovered=3` `persisted=2`). `crawl_job_item` outcomes: `mock-task006-iso-1 PERSISTED`, `mock-task006-iso-2 FAILED` (SQLException wrapping `injected item failure for AC-013`), `mock-task006-iso-3 PERSISTED`. Prometheus: `crawler_videos_failed_total 1.0`. Verify: `ExecuteCrawlJobServiceTest#ac012_recordsFailedCount`. |
| AC-013 | PASS | Same isolation job finished `status=PARTIAL` (not aborted / not FAILED). Videos present: `mock-task006-iso-1` and `mock-task006-iso-3` only (item 2 failed; item 3 still persisted). Verify: `ExecuteCrawlJobServiceTest#ac013_oneItemFailureDoesNotStopRemainingVideos` (`persist` called 3 times; PARTIAL; persisted=2 failed=1). |

Exploratory: RFC 9457 — unknown strategy → 400 `Unknown strategy`; unknown UUID → 404 `Crawl job not found`. Structured crawl logs include `jobId`, `sourceVideoId` (when known), and `outcome` (`PERSISTED` / `DUPLICATE` / `FAILED` / `PARTIAL`). No tokens or cookies. TASK-002/003/004/005/007 suites still pass (78 total). Live Douyin was not called.

Bug (FAIL): none
