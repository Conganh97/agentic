---
id: TASK-001
title: Create douyin-crawler-service repo, Docker, GHA, compose
type: TASK
priority: HIGH
status: CODE_REVIEW
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
sprint: SPRINT-01
branch: ops/TASK-001-douyin-crawler-repo-bootstrap
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
updated: 2026-09-25 14:37
---

## Description

Bootstrap the new `douyin-crawler-service` component (ADR-0004, ADR-0011). Create the private
GitHub repo with `python3 scripts/repo.py create douyin-crawler-service --type be`, seed/repair
`Dockerfile` and `.github/workflows/ci.yml`, and wire DEV/STG/PROD compose so this API +
PostgreSQL run **without** a frontend container.

Do not scaffold Spring application code (that is TASK-002). Do not add Redis. AC-001 (service
can start) is owned by TASK-002.

## Acceptance Criteria
- [ ] AC-030 The application can run using Docker.

## Design (SA)

`docs/design/REQ-001-design.md` §5, §8, §12 (TASK-001), FR-16, AC-030. Registry row in
`project.md` after `repo.py create`. Compose: postgres:16 + this API image only. Ports follow
`project.md` (DEV API 18081, DB 15440). Docker/GHA/compose only; the process-start AC is TASK-002.

## Implementation (BE/FE)

### Iteration 1
- Branch: `ops/TASK-001-douyin-crawler-repo-bootstrap` @ `ffacbe111746b644e1f68b47d4df1726e604c38e` (product repo `douyin-crawler-service`)
- Remote: https://github.com/Conganh97/product-douyin-crawler-service (private)
- Registry: `project.md` row `douyin-crawler-service` → `product/services/douyin-crawler-service`
- Docker/GHA: repaired `Dockerfile` (non-plain Boot jar), added `.dockerignore`, GHA verify + GHCR push skip until `pom.xml`/`mvnw` exist (TASK-002)
- Team stack: `ops/compose/{dev,stg,prod}.yml` + `.env.example` — `postgres:16` + this API image only; no frontend container; DEV API 18081 / DB 15440
- AC-030 evidence (unchecked; TEST owns the box): compose + Dockerfile + GHA paths above; `docker build` skipped — Docker daemon down and Spring app not scaffolded
- Verify: `./mvnw verify` skipped (no Maven wrapper/app). GHCR push skipped (no image to build)

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
| 2026-09-25 14:35 | BACKLOG | READY | SCRUM | DoR met; deps [] |
| 2026-09-25 14:36 | READY | IN_PROGRESS | DEVOPS | branch ops/TASK-001-douyin-crawler-repo-bootstrap |
| 2026-09-25 14:37 | IN_PROGRESS | CODE_REVIEW | DEVOPS | product sha ffacbe1; compose ops/compose/{dev,stg,prod}.yml; docker build skipped (daemon down, no scaffold) |
