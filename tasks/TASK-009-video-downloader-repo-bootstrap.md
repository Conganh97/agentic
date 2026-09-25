---
id: TASK-009
title: Create video-downloader-service repo, Docker, GHA, compose
type: TASK
priority: HIGH
status: MERGED
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
branch: ops/TASK-009-video-downloader-repo-bootstrap
merge_commit: 679d92cc29157282db2e90645202dd3320435e66
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
updated: 2026-09-25 16:50
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

### Iteration 1
- Branch: `ops/TASK-009-video-downloader-repo-bootstrap` @ `0e80f738cc098868dc32755a21d0950d770af592` (product repo `video-downloader-service`)
- Remote: https://github.com/Conganh97/product-video-downloader-service (private)
- Registry: `project.md` row `video-downloader-service` → `product/services/video-downloader-service`
- Docker/GHA: repaired `Dockerfile` (non-plain Boot jar), added `.dockerignore`, GHA verify + GHCR push skip until `pom.xml`/`mvnw` exist (TASK-010)
- Team stack: `ops/compose/{dev,stg,prod}.yml` + `.env.example` — sibling `downloader_db` + `downloader_api` + `downloader_videos_*` volume (profile `downloader`); crawler `api`/`db`/`API_IMAGE` unchanged. Ports DEV 18082/15441, STG 28082/25441, PROD 8082/5433
- `deploy.py`: `--component video-downloader-service` writes `DOWNLOADER_API_IMAGE` only (does not overwrite crawler `API_IMAGE`)
- AC-046 evidence (unchecked; TEST owns the box): compose + Dockerfile + GHA paths above; `docker build` skipped — Docker daemon down and Spring app not scaffolded (TASK-010)
- Verify: `./mvnw verify` skipped (no Maven wrapper/app). GHCR push skipped (no image to build)
- Skip TEST after MERGED (`work_type: DEVOPS`)

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

### Round 1 — APPROVED
Reviewed: ops/TASK-009-video-downloader-repo-bootstrap @ `0e80f738cc098868dc32755a21d0950d770af592` · Build/tests: SKIP (docker daemon down; no Spring scaffold — TASK-010)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | ops/compose/.env.example | MINOR | Example pins DEV ports only; a STG/PROD copy would override compose defaults |
| 2 | .github/workflows/ci.yml | MINOR | GHCR login still runs when verify/build are skipped (harmless) |
| 3 | scripts/deploy.py | MINOR | `docker build` is not gated on `pom.xml`/`mvnw`; will fail until TASK-010 scaffolds the app |

Merged `679d92cc29157282db2e90645202dd3320435e66`.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 16:33 | — | BACKLOG | SA | Created from REQ-002 design revision 1 hash b06116020682e658 |
| 2026-09-25 16:37 | BACKLOG | READY | SCRUM | DoR met; deps [] |
| 2026-09-25 16:38 | READY | IN_PROGRESS | DEVOPS | branch ops/TASK-009-video-downloader-repo-bootstrap |
| 2026-09-25 16:42 | IN_PROGRESS | CODE_REVIEW | DEVOPS | product sha 0e80f73; compose ops/compose/{dev,stg,prod}.yml; deploy.py DOWNLOADER_API_IMAGE; docker build skipped (daemon down, no scaffold) |
| 2026-09-25 16:50 | CODE_REVIEW | MERGED | SA | review round 1 APPROVED; merge_commit=679d92cc29157282db2e90645202dd3320435e66 --no-ff parents 83785c4 + 0e80f73; reviews/TASK-009-round-1.md |
