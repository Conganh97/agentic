---
id: TASK-006
title: Crawl job execution, statistics, and item isolation
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
depends_on: [TASK-004, TASK-005, TASK-007]
sprint:
branch: feature/TASK-006-crawl-job-execution
merge_commit: a79b4957d7a733e65d7c792205b3aecb871c25f6
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
updated: 2026-09-25 16:17
---

## Description

Implement the crawl runner: call `VideoDiscoveryProvider`, persist new videos, count discovered /
persisted / duplicate / failed items on the job (and `crawl_job_item` rows), and finish with
COMPLETED, PARTIAL, or FAILED. A single item failure must not abort the rest of the job.

## Acceptance Criteria
- [x] AC-009 A crawl job records the number of discovered videos.
- [x] AC-010 A crawl job records the number of newly persisted videos.
- [x] AC-011 A crawl job records duplicate videos.
- [x] AC-012 A crawl job records failed video processing.
- [x] AC-013 A failure processing one video does not automatically terminate the entire crawl job.

## Design (SA)

`docs/design/REQ-001-design.md` §6 job resource + final status rules, §7 `crawl_job` /
`crawl_job_item`, FR-3, FR-4, FR-7. Flyway ownership: this task owns `crawl_job_item`
(TASK-005 owns `crawl_job`). Use the mock provider in tests. Increment TASK-005 meters.

NFR-6 / AC-022 crawl fields: structured logs from the runner must include `jobId`,
`sourceVideoId` (when known), and item/job `outcome`. Do not log tokens or cookies.
TASK-002 provides the JSON logging stack; this task emits the crawl-specific fields.

## Implementation (BE/FE)

### Iteration 1 (crawl job execution)
- Branch: `feature/TASK-006-crawl-job-execution` @ ba57cd9
- Changed: `crawljob/{application,domain,infrastructure}`, `V3__crawl_job_item.sql`; replaced `StubCrawlJobRunner` with `ExecuteCrawlJobService`
- Tests: `./mvnw -q verify` → pass (78)
- Notes: Runner calls `VideoDiscoveryProvider`, persists via `PersistVideoService`, writes `crawl_job_item` (PERSISTED/DUPLICATE/FAILED). One item exception does not abort remaining items. Final status COMPLETED / PARTIAL / FAILED per design §6. Increments TASK-005 meters. Structured logs include `jobId`, `sourceVideoId` (when known), and item/job `outcome`. Tests use `crawler.provider=mock`.

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

### Round 1 — APPROVED
Reviewed: feature/TASK-006-crawl-job-execution @ `ba57cd9408a7c7e46755a38a45dc33fe61fc4dc9` · Build/tests: `./mvnw -q verify` PASS (78)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | ExecuteCrawlJobService.java | MINOR | Uncaught exception in `processItems` calls `finishFailed` with the pre-loop `job` snapshot and can overwrite in-progress counters |
| 2 | ExecuteCrawlJobService.java | MINOR | `recordItem` swallows `crawl_job_item` persist failures, so item rows and job counters can diverge |

## Test (TEST)

### Run 1 — PASS
- Tested: main @ a79b4957d7a733e65d7c792205b3aecb871c25f6 (contains merge_commit)
- Build/tests: `./mvnw -q verify` PASS (78; Testcontainers PostgreSQL 16.15; Flyway v3)
- AC-009 pass — POST `/api/v1/crawl-jobs` keyword `task006-ac009` limit 3 → GET `discovered=3` COMPLETED
- AC-010 pass — same GET `persisted=3`
- AC-011 pass — second POST same keyword → GET `duplicates=3` `persisted=0`
- AC-012 pass — isolation POST `task006-iso` → GET `failed=1`; item `mock-task006-iso-2` FAILED
- AC-013 pass — same job `status=PARTIAL`; items 1 and 3 PERSISTED (job not aborted)
- Evidence: `tests/TASK-006-run-1.md`

## Deployment (DEVOPS)

### DEV — 2026-09-25 16:17 — OK
- Images: `ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1` and `:dev`
- Command: reused healthy `ops/compose/dev.yml` (TASK-002 image already up; `python3 scripts/deploy.py --env DEV --component douyin-crawler-service` not re-run)
- Smoke: `http://127.0.0.1:18081/actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}`; POST `/api/v1/crawl-jobs` keyword `task006-dev-smoke` limit 3 → 202 `{"jobId":"2e957c97-…","status":"PENDING"}`; GET same job → 200 `COMPLETED` `discovered=3` `persisted=3`
- Rollback: `docker compose -f ops/compose/dev.yml up -d` with the previous tag

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 15:39 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-004, TASK-005, TASK-007] READY_FOR_DEPLOY |
| 2026-09-25 15:40 | READY | IN_PROGRESS | BE | branch feature/TASK-006-crawl-job-execution |
| 2026-09-25 15:44 | IN_PROGRESS | CODE_REVIEW | BE | product sha ba57cd9408a7c7e46755a38a45dc33fe61fc4dc9; Implementation iteration 1; ./mvnw -q verify pass (78) |
| 2026-09-25 15:46 | CODE_REVIEW | MERGED | SA | reviews/TASK-006-round-1.md APPROVED; merge_commit a79b4957d7a733e65d7c792205b3aecb871c25f6 (--no-ff, parents 3f1d0d4 + ba57cd9); ./mvnw -q verify PASS (78) |
| 2026-09-25 15:48 | MERGED | TESTING | TEST | tested sha a79b4957d7a733e65d7c792205b3aecb871c25f6 is product main HEAD and contains merge_commit; run 1 started |
| 2026-09-25 15:50 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-006-run-1.md PASS; AC-009 AC-010 AC-011 AC-012 AC-013 checked; ./mvnw -q verify PASS (78); POST 202 + GET counters + PARTIAL isolation |
| 2026-09-25 16:17 | READY_FOR_DEPLOY | DEPLOYING | DEVOPS | DEV deploy started; PQA accept APPROVED docs/design/reviews/REQ-001-accept-1.md; reuse healthy compose ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1 |
| 2026-09-25 16:17 | DEPLOYING | RELEASED | DEVOPS | DEV compose reused OK; image ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1; smoke GET http://127.0.0.1:18081/actuator/health → 200 status=UP; POST /api/v1/crawl-jobs → 202 PENDING; GET COMPLETED discovered=3 persisted=3; release=DEV |
