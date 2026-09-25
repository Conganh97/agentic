---
id: TASK-005
title: Crawl job API and async dispatch
type: TASK
priority: HIGH
status: RELEASED
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
depends_on: [TASK-003]
sprint:
branch: feature/TASK-005-crawl-job-api
merge_commit: ecee1ef0ed1dc917c4e57691b469c2ba3a084844
release: DEV
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
updated: 2026-09-25 16:16
---

## Description

Add the `crawljob` API and job row lifecycle: `POST /api/v1/crawl-jobs` returns 202 immediately
and dispatches work on a `TaskExecutor`; `GET /api/v1/crawl-jobs/{jobId}` returns status. Wire
Micrometer job/video counters and `crawler.job.duration`. A no-op or stub runner is enough until
TASK-006 implements full execution.

NFR-5: mark stale `RUNNING` jobs older than `crawler.job.stale-after` (default 30m) as
`FAILED` on the next create or status read. An optional scheduled sweep may use the same rule.

## Acceptance Criteria
- [x] AC-002 The service can create a crawl job through an API.
- [x] AC-003 A crawl job executes asynchronously and does not require the API request to remain open until crawling finishes.
- [x] AC-017 Crawl job status can be queried through an API.
- [x] AC-023 Application metrics are exposed for crawler jobs, discovered videos, persisted videos, duplicates, failures, and crawl duration.

## Design (SA)

`docs/design/REQ-001-design.md` §6 job endpoints, §4 NFR-5, NFR-2, NFR-7, FR-2, FR-3.
Flyway ownership: this task owns `crawl_job` (do not leave it to TASK-003). States: PENDING,
RUNNING, COMPLETED, PARTIAL, FAILED. RFC 9457 errors. `/actuator/prometheus` must include the
named meters (values may stay 0 until TASK-006 increments them).

NFR-5: a `RUNNING` row with `started_at` older than `crawler.job.stale-after` (default 30m),
or `RUNNING` with null `started_at` older than that window from `created_at`, is marked
`FAILED` with an error message on `POST /api/v1/crawl-jobs` and `GET /api/v1/crawl-jobs/{jobId}`.
Optional `@Scheduled` sweep applies the same rule so jobs fail even if no one reads them.

## Implementation (BE/FE)

### Iteration 1 (crawl job API)
- Branch: `feature/TASK-005-crawl-job-api` @ 0c24091
- Changed: `crawljob/{api,application,domain,infrastructure}`, `shared/error/ApiExceptionHandler.java`, `V2__crawl_job.sql`, `CrawlerProperties` job.stale-after, actuator prometheus
- Tests: `./mvnw -q verify` → pass (51)
- Notes: POST `/api/v1/crawl-jobs` returns 202 PENDING and dispatches on `crawlJobTaskExecutor` after commit. GET returns job resource + counters. Stub runner marks RUNNING then COMPLETED (no item work; TASK-006). NFR-5 stale RUNNING marked FAILED on create/status read and optional 5m sweep. RFC 9457 ProblemDetail for 400/404. Meters `crawler.jobs`, `crawler.videos.*`, `crawler.job.duration` registered at `/actuator/prometheus`.

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

### Round 1 — APPROVED
Reviewed: feature/TASK-005-crawl-job-api @ `0c24091821bdfa4fad83f4ff9e5105a7b19a8ea0` · Build/tests: `./mvnw -q verify` PASS (51)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | JpaCrawlJobRepository.java | MINOR | Insert path constructs a new entity then immediately `copyFrom` (harmless duplication) |
| 2 | CreateCrawlJobService.java | MINOR | After-commit dispatch relies on `insertPending` being the `@Transactional` boundary; wrapping `create()` later would race the runner |

## Test (TEST)

### Run 1 — PASS
- Tested: main @ ecee1ef0ed1dc917c4e57691b469c2ba3a084844 (contains merge_commit)
- Build/tests: `./mvnw -q verify` PASS (51; Testcontainers PostgreSQL 16.15; Flyway v2)
- AC-002 pass — POST `/api/v1/crawl-jobs` → 202 `{"jobId":"559f14b3-…","status":"PENDING"}`
- AC-003 pass — POST `real 0.22` (220 ms) returned PENDING; GET immediately COMPLETED (stub after-commit, not request-held)
- AC-017 pass — GET `/api/v1/crawl-jobs/{jobId}` → 200 job resource + counters (videos 0; stub)
- AC-023 pass — GET `/actuator/prometheus` exposes `crawler_jobs_total`, `crawler_videos_*`, `crawler_job_duration_seconds`
- Evidence: `tests/TASK-005-run-1.md`

## Deployment (DEVOPS)

### DEV — 2026-09-25 16:16 — OK
- Images: `ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1` and `:dev`
- Command: reused healthy `ops/compose/dev.yml` (TASK-002 image already up; `python3 scripts/deploy.py --env DEV --component douyin-crawler-service` not re-run)
- Smoke: `http://127.0.0.1:18081/actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}`; optional POST `/api/v1/crawl-jobs` → 202 `{"jobId":"1721bb6f-…","status":"PENDING"}`; GET same job → 200 `COMPLETED`
- Rollback: `docker compose -f ops/compose/dev.yml up -d` with the previous tag

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 15:11 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-003] READY_FOR_DEPLOY |
| 2026-09-25 15:17 | READY | IN_PROGRESS | BE | branch feature/TASK-005-crawl-job-api |
| 2026-09-25 15:22 | IN_PROGRESS | CODE_REVIEW | BE | product sha 0c24091821bdfa4fad83f4ff9e5105a7b19a8ea0; Implementation iteration 1; ./mvnw -q verify pass (51) |
| 2026-09-25 15:25 | CODE_REVIEW | MERGED | SA | reviews/TASK-005-round-1.md APPROVED; merge_commit ecee1ef0ed1dc917c4e57691b469c2ba3a084844 (--no-ff, parents 8088e33 + 0c24091); ./mvnw -q verify PASS (51) |
| 2026-09-25 15:26 | MERGED | TESTING | TEST | tested sha ecee1ef0ed1dc917c4e57691b469c2ba3a084844 is main HEAD and contains merge_commit; run 1 started |
| 2026-09-25 15:28 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-005-run-1.md PASS; AC-002 AC-003 AC-017 AC-023 checked; ./mvnw -q verify PASS (51); POST 202 + GET 200 + prometheus meters |
| 2026-09-25 16:15 | READY_FOR_DEPLOY | DEPLOYING | DEVOPS | DEV deploy started; PQA accept APPROVED docs/design/reviews/REQ-001-accept-1.md; reuse healthy compose ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1 |
| 2026-09-25 16:16 | DEPLOYING | RELEASED | DEVOPS | DEV compose reused OK; image ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1; smoke GET http://127.0.0.1:18081/actuator/health → 200 status=UP; POST /api/v1/crawl-jobs → 202 PENDING; release=DEV |
