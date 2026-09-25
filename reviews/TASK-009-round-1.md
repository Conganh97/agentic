---
task: TASK-009
round: 1
decision: APPROVED
branch: ops/TASK-009-video-downloader-repo-bootstrap
sha: 0e80f738cc098868dc32755a21d0950d770af592
updated: 2026-09-25 16:50
---

# TASK-009 Review Round 1

Reviewed: `ops/TASK-009-video-downloader-repo-bootstrap` @ `0e80f738cc098868dc32755a21d0950d770af592` · Build/tests: SKIP (docker daemon down; `./mvnw verify` not expected — no Spring scaffold, TASK-010)

`project.md` verify: registry row `video-downloader-service` · type BE · path `product/services/video-downloader-service` · remote `https://github.com/Conganh97/product-video-downloader-service`. Compose is sibling `downloader_db` (`postgres:16`) + `downloader_api` (`DOWNLOADER_API_IMAGE`) + `downloader_videos_*` volume (profile `downloader`). Crawler `api`/`db`/`API_IMAGE` unchanged. Ports match design §5 (DEV 18082/15441, STG 28082/25441, PROD 8082/5433). `deploy.py --component video-downloader-service` writes `DOWNLOADER_API_IMAGE` only.

Scope: Docker, GHA, `ops/compose`, `deploy.py` only. Missing Spring app is TASK-010, not a fail.

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | ops/compose/.env.example | MINOR | Example pins DEV ports only; a STG/PROD copy would override compose defaults |
| 2 | .github/workflows/ci.yml | MINOR | GHCR login still runs when verify/build are skipped (harmless) |
| 3 | scripts/deploy.py | MINOR | `docker build` is not gated on `pom.xml`/`mvnw`; will fail until TASK-010 scaffolds the app |

Merged `679d92cc29157282db2e90645202dd3320435e66`.
