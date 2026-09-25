# Ops

Local stack. No remote app host (ADR-0011). DevOps owns this folder.

```
python3 scripts/deploy.py --env DEV        # build, push GHCR, compose up
python3 scripts/deploy.py --env STG --component frontend
python3 scripts/deploy.py --env DEV --component video-downloader-service
```

| Env | Compose | Web | Crawler API | Crawler DB | Downloader API | Downloader DB |
|-----|---------|-----|-------------|------------|----------------|---------------|
| DEV | `compose/dev.yml` | 15173 | 18081 | 15440 | 18082 | 15441 |
| STG | `compose/stg.yml` | 25173 | 28081 | 25440 | 28082 | 25441 |
| PROD | `compose/prod.yml` | 80 | 8080 | 5432 | 8082 | 5433 |

Downloader services use compose profile `downloader` and `DOWNLOADER_API_IMAGE` (not `API_IMAGE`).
`deploy.py --component video-downloader-service` writes `DOWNLOADER_API_IMAGE` only.

Copy `compose/.env.example` → `compose/.env.dev` (gitignored). Images:

`ghcr.io/<owner>/product-<component>:<env>-<sha>`

Optional: install a GitHub **self-hosted** runner on this Mac so product `.github/workflows/ci.yml`
pushes the same tags on `main`.
