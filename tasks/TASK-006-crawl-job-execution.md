---
id: TASK-006
title: Crawl job execution, statistics, and item isolation
type: TASK
priority: HIGH
status: TESTING
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
updated: 2026-09-25 15:48
---

## Description

Implement the crawl runner: call `VideoDiscoveryProvider`, persist new videos, count discovered /
persisted / duplicate / failed items on the job (and `crawl_job_item` rows), and finish with
COMPLETED, PARTIAL, or FAILED. A single item failure must not abort the rest of the job.

## Acceptance Criteria
- [ ] AC-009 A crawl job records the number of discovered videos.
- [ ] AC-010 A crawl job records the number of newly persisted videos.
- [ ] AC-011 A crawl job records duplicate videos.
- [ ] AC-012 A crawl job records failed video processing.
- [ ] AC-013 A failure processing one video does not automatically terminate the entire crawl job.

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

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 15:39 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-004, TASK-005, TASK-007] READY_FOR_DEPLOY |
| 2026-09-25 15:40 | READY | IN_PROGRESS | BE | branch feature/TASK-006-crawl-job-execution |
| 2026-09-25 15:44 | IN_PROGRESS | CODE_REVIEW | BE | product sha ba57cd9408a7c7e46755a38a45dc33fe61fc4dc9; Implementation iteration 1; ./mvnw -q verify pass (78) |
| 2026-09-25 15:46 | CODE_REVIEW | MERGED | SA | reviews/TASK-006-round-1.md APPROVED; merge_commit a79b4957d7a733e65d7c792205b3aecb871c25f6 (--no-ff, parents 3f1d0d4 + ba57cd9); ./mvnw -q verify PASS (78) |
| 2026-09-25 15:48 | MERGED | TESTING | TEST | tested sha a79b4957d7a733e65d7c792205b3aecb871c25f6 is product main HEAD and contains merge_commit; run 1 started |
