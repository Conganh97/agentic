---
task: TASK-003
run: 1
verdict: PASS
tested_sha: 677bedb02fc9bedfa0e96fa46cf21ba1fcfeebe2
merge_commit: 677bedb02fc9bedfa0e96fa46cf21ba1fcfeebe2
updated: 2026-09-25 14:59
---

# TASK-003 Test Run 1

- Tested: `main` @ `677bedb02fc9bedfa0e96fa46cf21ba1fcfeebe2` (contains `merge_commit`)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (`VERIFY_EXIT=0`; 15 tests)
- Docker: up (Testcontainers `postgres:16-alpine`, PostgreSQL 16.15). Flyway: `Successfully applied 1 migration to schema "public", now at version v1`
- Persistence only (no REST query API; TASK-008). No service process started. Product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-006 | PASS | `./mvnw -q -Dtest=VideoPersistenceTest test` → `TARGETED_IT_EXIT=0`. Surefire: `Tests run: 5, Failures: 0, Errors: 0, Skipped: 0 … VideoPersistenceTest`. Method `ac006_persistsDiscoveredVideoInPostgres` persists via `PersistVideoService` then `select count(*) from video where id = ?` = 1 on Testcontainers PostgreSQL. Verify Flyway applied `V1__video_and_video_metric` (`video` table). |
| AC-007 | PASS | Same command. Method `ac007_sameDouyinVideoIsPersistedOnce`: second persist of `ac007-video` returns `duplicate=true` and same id; `select count(*) from video where source = ? and source_video_id = ?` = 1. |
| AC-008 | PASS | Same command. Method `ac008_uniquenessIsEnforcedByDatabaseConstraint`: raw JDBC `insert into video` with a different UUID and the same `(DOUYIN, ac008-video)` throws `DuplicateKeyException`; row count stays 1. Schema: `CONSTRAINT uk_video_source_source_video_id UNIQUE (source, source_video_id)`. Not application-only (`ON CONFLICT DO NOTHING` plus DB unique index). |
| AC-021 | PASS | Same command. Method `ac021_metricSnapshotsAreInsertOnly`: persist likes 10 then 20; `findByVideoIdOrderByCapturedAtAsc` size 2; first `likeCount=10`, second `likeCount=20`, distinct metric ids (insert-only, no overwrite). |
| AC-026 | PASS | `./mvnw -q -Dtest=SourceVideoIdsTest,VideoMetricSnapshotsTest,PersistVideoServiceTest test` → `TARGETED_UNIT_EXIT=0`. Surefire: `SourceVideoIdsTest` Tests run: 3, Failures: 0; `VideoMetricSnapshotsTest` Tests run: 1, Failures: 0; `PersistVideoServiceTest` Tests run: 2, Failures: 0. Plus IT `ac026_missingSourceVideoIdUsesSha256OfCanonicalUrl`. Covers SHA-256 id derivation, insert-only snapshot rules, persist/duplicate-append application behaviour. Full `./mvnw -q verify` also kept TASK-002 `ServiceSkeletonTest` Tests run: 4, Failures: 0. |

Exploratory: no video query routes (in scope of TASK-008). Uniqueness holds at the unique index even when bypassing the service. Metric history appends rows. No PII in test logs.

Bug (FAIL): none
