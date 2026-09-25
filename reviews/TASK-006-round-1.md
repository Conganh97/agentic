---
task: TASK-006
round: 1
decision: APPROVED
branch: feature/TASK-006-crawl-job-execution
sha: ba57cd9408a7c7e46755a38a45dc33fe61fc4dc9
updated: 2026-09-25 15:46
---

# TASK-006 Review Round 1

Reviewed: `feature/TASK-006-crawl-job-execution` @ `ba57cd9408a7c7e46755a38a45dc33fe61fc4dc9` · Build/tests: `./mvnw -q verify` PASS (78)

`project.md` verify: registry row `douyin-crawler-service` · type BE · path `product/services/douyin-crawler-service` · remote `https://github.com/Conganh97/product-douyin-crawler-service`. Stack Java 21 + Boot 4 + PostgreSQL 16 + Flyway + JPA + `ddl-auto=validate` matches design §5. Package-by-feature `crawljob/{application,domain,infrastructure}`. Tests use `crawler.provider=mock`.

Contract vs §6 / §7: `StubCrawlJobRunner` replaced by `ExecuteCrawlJobService`. Runner calls `VideoDiscoveryProvider.discover` (KEYWORD) and persists via `PersistVideoService` (FR-4). Job counters `discovered` / `persisted` / `duplicates` / `failed` (FR-3 / AC-009–012). Flyway `V3__crawl_job_item.sql` owns `crawl_job_item` (`PERSISTED` | `DUPLICATE` | `FAILED`). One item exception does not abort remaining items (FR-7 / AC-013). Final status COMPLETED (`failed == 0`) / PARTIAL (`failed > 0` and persist or duplicate work) / FAILED (provider cannot start, every item fails). TASK-005 meters incremented (`crawler.videos.*`, `crawler.jobs` tag `status`, `crawler.job.duration`).

NFR-6: structured logs include `jobId`, `sourceVideoId` (when known), and item/job `outcome`. No tokens or cookies.

Implementation-level AC coverage on the branch: AC-009 (discovered count + meter), AC-010 (persisted + COMPLETED), AC-011 (duplicates), AC-012 (failed from persist exception and provider itemFailures), AC-013 (one item fail → remaining persist, job PARTIAL).

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | ExecuteCrawlJobService.java | MINOR | Uncaught exception in `processItems` calls `finishFailed` with the pre-loop `job` snapshot and can overwrite in-progress counters |
| 2 | ExecuteCrawlJobService.java | MINOR | `recordItem` swallows `crawl_job_item` persist failures, so item rows and job counters can diverge |

Merged `a79b4957d7a733e65d7c792205b3aecb871c25f6`.
