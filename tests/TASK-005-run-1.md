---
task: TASK-005
run: 1
verdict: PASS
tested_sha: ecee1ef0ed1dc917c4e57691b469c2ba3a084844
merge_commit: ecee1ef0ed1dc917c4e57691b469c2ba3a084844
updated: 2026-09-25 15:28
---

# TASK-005 Test Run 1

- Tested: `main` @ `ecee1ef0ed1dc917c4e57691b469c2ba3a084844` (contains `merge_commit`; product HEAD)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (`VERIFY_EXIT=0`; 51 tests, Failures: 0, Errors: 0, Skipped: 0)
- Docker: up. Compose `db` only (`postgres:16` on `localhost:15440`, healthy). App: `SERVER_PORT=18081 ./mvnw spring-boot:run` → Flyway applied v1+v2 (`Successfully applied 2 migrations … now at version v2`); `Tomcat started on port 18081`; `Started DouyinCrawlerApplication in 4.216 seconds`
- Stub runner in scope (PENDING→RUNNING→COMPLETED); full crawl is TASK-006. Process stopped; compose db stopped; product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-002 | PASS | `curl -sS -D - -X POST http://localhost:18081/api/v1/crawl-jobs -H 'Content-Type: application/json' -d '{"strategy":"KEYWORD","keyword":"cats","limit":5}'` → HTTP **202** `{"jobId":"559f14b3-7bd3-4d22-8100-7cc39c0ba595","status":"PENDING"}`. Job row created and returned immediately. |
| AC-003 | PASS | Same POST timed with `/usr/bin/time -p` → `real 0.22` (220 ms, under NFR-2 500 ms). Response status is `PENDING` (request did not wait for crawl finish). Immediate GET on the same `jobId` already `COMPLETED` with `startedAt`/`finishedAt` set (~50 ms later), showing after-commit stub dispatch (`PENDING`→`RUNNING`→`COMPLETED`) not request-held execution. |
| AC-017 | PASS | `GET http://localhost:18081/api/v1/crawl-jobs/559f14b3-7bd3-4d22-8100-7cc39c0ba595` → HTTP **200** `{"jobId":"559f14b3-7bd3-4d22-8100-7cc39c0ba595","status":"COMPLETED","strategy":"KEYWORD","keyword":"cats","limit":5,"discovered":0,"persisted":0,"duplicates":0,"failed":0,"errorMessage":null,"createdAt":"2026-09-25T08:28:32.121699Z","startedAt":"2026-09-25T08:28:32.170945Z","finishedAt":"2026-09-25T08:28:32.171995Z"}`. Counters present; video counts 0 as stub (TASK-006). |
| AC-023 | PASS | `GET http://localhost:18081/actuator/prometheus` → HTTP **200** `text/plain;version=0.0.4`. Meters present: `crawler_jobs_total{status="PENDING"} 1.0`, `{status="RUNNING"} 1.0`, `{status="COMPLETED"} 1.0`, `{status="FAILED"} 0.0`, `{status="PARTIAL"} 0.0`; `crawler_videos_discovered_total 0.0`; `crawler_videos_persisted_total 0.0`; `crawler_videos_duplicates_total 0.0`; `crawler_videos_failed_total 0.0`; `crawler_job_duration_seconds_count 1` / `sum 0.00105`. Video meter values may stay 0 until TASK-006. |

Exploratory: RFC 9457 `application/problem+json` — unknown strategy → 400 `Unknown strategy`; blank keyword → 400 `keyword must not be blank`; `limit: 99` → 400 `limit must be between 1 and 50`; unknown UUID → 404 `Crawl job not found`. Health still 200 `{"groups":["liveness","readiness"],"status":"UP"}`. OpenAPI 3.1.0 paths `/api/v1/crawl-jobs` and `/api/v1/crawl-jobs/{jobId}`. NFR-5 stale RUNNING (30m) not exercised in this run (would need a planted stale row). No PII in logs.

Bug (FAIL): none
