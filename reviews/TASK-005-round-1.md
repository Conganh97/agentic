---
task: TASK-005
round: 1
decision: APPROVED
branch: feature/TASK-005-crawl-job-api
sha: 0c24091821bdfa4fad83f4ff9e5105a7b19a8ea0
updated: 2026-09-25 15:24
---

# TASK-005 Review Round 1

Reviewed: `feature/TASK-005-crawl-job-api` @ `0c24091821bdfa4fad83f4ff9e5105a7b19a8ea0` · Build/tests: `./mvnw -q verify` PASS (51)

`project.md` verify: registry row `douyin-crawler-service` · type BE · path `product/services/douyin-crawler-service` · remote `https://github.com/Conganh97/product-douyin-crawler-service`. Stack Java 21 + Boot 4 + PostgreSQL 16 + Flyway + JPA + `ddl-auto=validate` + `TaskExecutor` (virtual threads) + Micrometer Prometheus matches design §5. Package-by-feature `crawljob/{api,application,domain,infrastructure}`.

Contract vs §6: `POST /api/v1/crawl-jobs` returns **202** `{ jobId, status: PENDING }` without waiting for the run (FR-2 / NFR-2). `GET /api/v1/crawl-jobs/{jobId}` returns the job resource (counters, timestamps, `errorMessage`). 400/404 use RFC 9457 `ProblemDetail` (`application/problem+json`). Flyway `V2__crawl_job.sql` owns `crawl_job` only (no `crawl_job_item`). Stub runner PENDING→RUNNING→COMPLETED is in scope; discover/persist stays TASK-006. Video meters registered at 0.

NFR-5: stale `RUNNING` (`started_at` or null-`started_at` via `created_at` older than `crawler.job.stale-after` default 30m) marked `FAILED` on create and status read; optional 5m `@Scheduled` sweep. NFR-7: `/actuator/prometheus` exposes `crawler.jobs` (tag `status`), `crawler.videos.{discovered,persisted,duplicates,failed}`, `crawler.job.duration`.

Implementation-level AC coverage on the branch: AC-002 (202 + row), AC-003 (dispatch on `crawlJobTaskExecutor` after `insertPending` commits; not inline), AC-017 (GET resource + 404), AC-023 (prometheus meter names).

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | JpaCrawlJobRepository.java | MINOR | Insert path constructs a new entity then immediately `copyFrom` (harmless duplication) |
| 2 | CreateCrawlJobService.java | MINOR | After-commit dispatch relies on `insertPending` being the `@Transactional` boundary; wrapping `create()` later would race the runner |

Merged `ecee1ef0ed1dc917c4e57691b469c2ba3a084844`.
