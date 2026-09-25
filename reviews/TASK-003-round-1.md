---
task: TASK-003
round: 1
decision: APPROVED
branch: feature/TASK-003-video-persistence
sha: f442c78e7259fe645bb5e9dd0faa19a7d2434110
updated: 2026-09-25 14:56
---

# TASK-003 Review Round 1

Reviewed: `feature/TASK-003-video-persistence` @ `f442c78e7259fe645bb5e9dd0faa19a7d2434110` · Build/tests: `./mvnw -q verify` PASS (15)

`project.md` verify: registry row `douyin-crawler-service` · type BE · path `product/services/douyin-crawler-service` · remote `https://github.com/Conganh97/product-douyin-crawler-service`. Stack Java 21 + Boot 4 + PostgreSQL 16 + Flyway + JPA + `ddl-auto=validate` matches design §5. Package-by-feature `video/{application,domain,infrastructure}`.

Schema vs §7: Flyway `V1__video_and_video_metric.sql` creates only `video` and `video_metric`. Columns match FR-6 / FR-11 (`UNIQUE (source, source_video_id)`, insert-only metrics, FK `video_id`). No `crawl_job` / `crawl_job_item`. Missing `source_video_id` → SHA-256 of canonical URL (`SourceVideoIds`). Persist uses `INSERT … ON CONFLICT (source, source_video_id) DO NOTHING`.

Contract-vs-API: no `/api/v1/videos` or other query controllers (TASK-008). Ops paths from TASK-002 unchanged (`GET /actuator/health`, `GET /v3/api-docs`). Repositories are the increment contract.

Implementation-level AC coverage on the branch: AC-006/007/008/021 (Testcontainers) and AC-026 (id derivation + snapshot-append + service).

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | video/infrastructure/JpaVideoRepository.java | MINOR | Class name says JPA; writes use `NamedParameterJdbcTemplate` for `ON CONFLICT DO NOTHING` (correct for FR-6) |
| 2 | video/domain/VideoMetricSnapshots.java | MINOR | `historyWith` is unit-test only; persist path inserts a new row and never mutates prior snapshots |

Merged `677bedb02fc9bedfa0e96fa46cf21ba1fcfeebe2`.
