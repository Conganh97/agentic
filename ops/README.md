# Ops

Local stack. No remote app host (ADR-0011). DevOps owns this folder.

```
python3 scripts/deploy.py --env DEV        # build, push GHCR, compose up
python3 scripts/deploy.py --env STG --component frontend
```

| Env | Compose | Web | API | DB |
|-----|---------|-----|-----|-----|
| DEV | `compose/dev.yml` | 15173 | 18081 | 15440 |
| STG | `compose/stg.yml` | 25173 | 28081 | 25440 |
| PROD | `compose/prod.yml` | 80 | 8080 | 5432 |

Copy `compose/.env.example` → `compose/.env.dev` (gitignored). Images:

`ghcr.io/<owner>/product-<component>:<env>-<sha>`

Optional: install a GitHub **self-hosted** runner on this Mac so product `.github/workflows/ci.yml`
pushes the same tags on `main`.
