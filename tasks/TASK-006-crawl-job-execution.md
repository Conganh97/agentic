---
id: TASK-006
title: Crawl job execution, statistics, and item isolation
type: TASK
priority: HIGH
status: BACKLOG
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
branch:
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
updated: 2026-09-25 14:26
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
`crawl_job_item`, FR-3, FR-4, FR-7. Use the mock provider in tests. Increment TASK-005 meters.

## Implementation (BE/FE)

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
