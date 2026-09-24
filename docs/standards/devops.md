# DevOps

Skill: `.cursor/skills/devops/SKILL.md`. ADR-0011. Envs: **DEV · STG · PROD**.

## Owns

| Item | Where |
|------|--------|
| Create product repos if missing | `scripts/repo.py` |
| Dockerfile + GHA | each `product/<component>/` |
| Stack compose | `ops/compose/<env>.yml` |
| Build / push / run | `python3 scripts/deploy.py --env <ENV>` |

## Images

`ghcr.io/<GitHub owner>/product-<component>:<env>-<sha7>` and `:<env>`.

Compose **pulls** those tags. Do not run unpacked jars/dist as the deploy.

## Local pipeline

No remote app host. DevOps (or a self-hosted Actions runner on this Mac) builds and pushes here,
then `docker compose up` on this Mac. Ports: `project.md` → Environments.

## PROD

Human `approved_by` on every task being released. Never set it yourself.

## Forbidden

Application feature code. Merging. Force-push. Secrets in markdown. Destructive compose (`down -v`)
without the human asking.
