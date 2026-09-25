---
id: TASK-005
title: Crawl job API and async dispatch
type: TASK
priority: HIGH
status: CODE_REVIEW
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
merge_commit:
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
updated: 2026-09-25 15:22
---

## Description

Add the `crawljob` API and job row lifecycle: `POST /api/v1/crawl-jobs` returns 202 immediately
and dispatches work on a `TaskExecutor`; `GET /api/v1/crawl-jobs/{jobId}` returns status. Wire
Micrometer job/video counters and `crawler.job.duration`. A no-op or stub runner is enough until
TASK-006 implements full execution.

NFR-5: mark stale `RUNNING` jobs older than `crawler.job.stale-after` (default 30m) as
`FAILED` on the next create or status read. An optional scheduled sweep may use the same rule.

## Acceptance Criteria
- [ ] AC-002 The service can create a crawl job through an API.
- [ ] AC-003 A crawl job executes asynchronously and does not require the API request to remain open until crawling finishes.
- [ ] AC-017 Crawl job status can be queried through an API.
- [ ] AC-023 Application metrics are exposed for crawler jobs, discovered videos, persisted videos, duplicates, failures, and crawl duration.

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

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 15:11 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-003] READY_FOR_DEPLOY |
| 2026-09-25 15:17 | READY | IN_PROGRESS | BE | branch feature/TASK-005-crawl-job-api |
| 2026-09-25 15:22 | IN_PROGRESS | CODE_REVIEW | BE | product sha 0c24091821bdfa4fad83f4ff9e5105a7b19a8ea0; Implementation iteration 1; ./mvnw -q verify pass (51) |
