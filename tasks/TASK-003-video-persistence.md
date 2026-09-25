---
id: TASK-003
title: Video and metric persistence with uniqueness
type: TASK
priority: HIGH
status: MERGED
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
depends_on: [TASK-002]
sprint: SPRINT-03
branch: feature/TASK-003-video-persistence
merge_commit: 677bedb02fc9bedfa0e96fa46cf21ba1fcfeebe2
release:
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
updated: 2026-09-25 14:56
---

## Description

Add Flyway schema for `video` / `video_metric` and the `video` feature: persist discovered
video metadata in PostgreSQL, enforce uniqueness on `(source, source_video_id)` in the
database, and insert metric snapshots without overwriting previous rows. Provide repositories
usable by later crawl tasks. No REST query API yet (TASK-008). Do not create `crawl_job` or
`crawl_job_item` here (TASK-005 / TASK-006).

## Acceptance Criteria
- [ ] AC-006 Successfully discovered videos are persisted in PostgreSQL.
- [ ] AC-007 The same Douyin video cannot be persisted multiple times.
- [ ] AC-008 Video uniqueness is enforced at the persistence layer and is not dependent only on application-level checks.
- [ ] AC-021 Historical video metrics can be stored as separate snapshots without overwriting previous snapshots.
- [ ] AC-026 Unit tests cover the core application and domain behaviour.

## Design (SA)

`docs/design/REQ-001-design.md` §7 tables `video` and `video_metric`, FR-5, FR-6, FR-11.
Flyway ownership: this task owns `video` and `video_metric` only. If `source_video_id` is
missing, derive a stable id as SHA-256 of the canonical URL. Unique constraint is required.
Domain unit tests for id derivation and snapshot-append rules.

## Implementation (BE/FE)

### Iteration 1 (video persistence)
- Branch: `feature/TASK-003-video-persistence` @ f442c78
- Changed: `video/{domain,application,infrastructure}`, `db/migration/V1__video_and_video_metric.sql`, JPA + Flyway wiring
- Tests: `./mvnw -q verify` → pass (15)
- Notes: Flyway owns `video` / `video_metric` only. UNIQUE (source, source_video_id). Missing `source_video_id` → SHA-256 of canonical URL. Metric snapshots insert-only. No REST query API; no crawl_job tables. Testcontainers PostgreSQL 16.

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

### Round 1 — APPROVED
Reviewed: feature/TASK-003-video-persistence @ `f442c78e7259fe645bb5e9dd0faa19a7d2434110` · Build/tests: `./mvnw -q verify` PASS (15)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | JpaVideoRepository.java | MINOR | Name says JPA; writes use JDBC `ON CONFLICT DO NOTHING` (correct for FR-6) |
| 2 | VideoMetricSnapshots.java | MINOR | `historyWith` is unit-test only; persist inserts new rows |

Merged `677bedb02fc9bedfa0e96fa46cf21ba1fcfeebe2`.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 14:49 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002] MERGED |
| 2026-09-25 14:51 | READY | IN_PROGRESS | BE | branch feature/TASK-003-video-persistence |
| 2026-09-25 14:53 | IN_PROGRESS | CODE_REVIEW | BE | product sha f442c78; Implementation iteration 1; ./mvnw -q verify pass (15) |
| 2026-09-25 14:56 | CODE_REVIEW | MERGED | SA | review round 1 APPROVED; merge_commit=677bedb02fc9bedfa0e96fa46cf21ba1fcfeebe2 --no-ff parents 9d951ba + f442c78; reviews/TASK-003-round-1.md |
