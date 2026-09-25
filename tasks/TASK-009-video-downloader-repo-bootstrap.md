---
id: TASK-009
title: Create video-downloader-service repo, Docker, GHA, compose
type: TASK
priority: HIGH
status: BACKLOG
assignee: DEVOPS
parent: REQ-002
requirement_revision: 1
repo: video-downloader-service
work_type: DEVOPS
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: []
sprint: SPRINT-04
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
updated: 2026-09-25 16:37
---

## Description

Bootstrap the new `video-downloader-service` component (ADR-0004, ADR-0011). Create the private
GitHub repo with `python3 scripts/repo.py create video-downloader-service --type be`, seed/repair
`Dockerfile` and `.github/workflows/ci.yml`, and wire DEV/STG/PROD compose so this API + its own
PostgreSQL + a video volume run **beside** `douyin-crawler-service`, not as a replacement of
`API_IMAGE`.

Do not scaffold Spring application code (that is TASK-010). Do not add Redis or MinIO. AC-001
(service can start) is owned by TASK-010.

## Acceptance Criteria
- [ ] AC-046 Docker support is provided.

## Design (SA)

`docs/design/REQ-002-design.md` §5 ports, §8, §12 (TASK-009), FR-16, AC-046. Registry row in
`project.md` after `repo.py create`. Compose: dedicated `postgres:16` + this API image + bind/volume
for `DOWNLOADER_STORAGE_ROOT`. Ports: DEV API 18082 / DB 15441; STG 28082 / 25441; PROD 8082 / 5433.
Update `deploy.py` / env files so `--component video-downloader-service` does not overwrite the
crawler `API_IMAGE`. Docker/GHA/compose only.

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
| 2026-09-25 16:33 | — | BACKLOG | SA | Created from REQ-002 design revision 1 hash b06116020682e658 |
