---
id: TASK-001
title: Create douyin-crawler-service repo, Docker, GHA, compose
type: TASK
priority: HIGH
status: BACKLOG
assignee: DEVOPS
parent: REQ-001
requirement_revision: 1
repo: douyin-crawler-service
work_type: DEVOPS
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: []
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

Bootstrap the new `douyin-crawler-service` component (ADR-0004, ADR-0011). Create the private
GitHub repo with `python3 scripts/repo.py create douyin-crawler-service --type be`, seed/repair
`Dockerfile` and `.github/workflows/ci.yml`, and wire DEV/STG/PROD compose so this API +
PostgreSQL run **without** a frontend container.

Do not scaffold Spring application code (that is TASK-002). Do not add Redis.

## Acceptance Criteria
- [ ] AC-001 The service can start successfully using the documented local development setup.
- [ ] AC-030 The application can run using Docker.

## Design (SA)

`docs/design/REQ-001-design.md` §5, §8, §12 (TASK-001), FR-1, FR-16. Registry row in `project.md`
after `repo.py create`. Compose: postgres:16 + this API image only. Ports follow `project.md`
(DEV API 18081, DB 15440).

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
