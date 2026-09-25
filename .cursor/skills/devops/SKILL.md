---
name: devops
description: DevOps. Creates product repos if missing, writes or repairs Docker and GitHub Actions, deploys DEV/STG/PROD on this machine via GHCR images + compose. Use when invoked as /devops, e.g. "/devops TASK-006" or "/devops deploy TASK-003 DEV".
disable-model-invocation: true
---

# DevOps

Role: `DEVOPS`. `AGENTS.md` + `.cursor/rules/workflow.mdc`. Standards: `docs/standards/devops.md`.
ADR-0011. **Writes:** product Docker/CI on `ops/TASK-###-<slug>`; team `ops/compose/`; Deployment
section; `release`; parent REQ `RELEASED` when every direct child is `RELEASED`.
**Forbidden:** app features; merge; `approved_by`; secrets in markdown; checking task AC boxes.

**Transition discipline:** workflow §5. Role + guard + §8 evidence. Never `--no-verify`. `NEEDS_INPUT` is an outcome, not a status.

### FAILED recovery

`FAILED` is recovery, not a restart. Read `failed_from`, fix the tooling/env issue, then
`FAILED → failed_from`. Do not force `FAILED → IN_PROGRESS` unless `failed_from` is `IN_PROGRESS`.
Product AC misses are `BUG`, not `FAILED`.

## `/devops TASK-###` — bootstrap or repair

Assignee `DEVOPS`. READY / CHANGES_REQUESTED / BUG / IN_PROGRESS / FAILED.

1. Re-read the task + design §5. Create every **named** component that is missing:
   `python3 scripts/repo.py create <name>-service --type be` or `frontend --type fe`.
   You own create (BE/FE only as fallback when no DEVOPS bootstrap is READY/IN_PROGRESS).
   Never create an unapproved component.
2. READY → IN_PROGRESS. `branch: ops/TASK-###-<slug>` **in each product repo you touch**.
3. If Docker/GHA **missing**: copy `templates/ops/` (`Dockerfile.be` / `Dockerfile.fe`, `ci.yml`,
   FE `nginx.conf`). If **present**: fix so verify + `docker build` + push to GHCR work.
4. Team stack: `ops/compose/{dev,stg,prod}.yml` + `.env.example` (never commit `.env.*`).
   Default compose has one `api` + one `web`. More than one `*-service` → update compose first;
   do not silently overwrite `API_IMAGE`.
5. Verify: `docker build` for each component (skip if the app is not scaffolded yet — note it).
6. Push product branches via `repo.py`. Implementation iteration. CODE_REVIEW. Next: `/sa review`.
   Skip TEST after MERGED (`work_type: DEVOPS`).

## `/devops deploy TASK-### <ENV>`

`READY_FOR_DEPLOY` or `DEPLOYING`. `<ENV>` is `DEV` | `STG` | `PROD` (default `DEV`).

A compose up may start multiple compatible images, but **every affected task** must get its own
`## Deployment` evidence and its own authorized transition. Do not change sibling `status`
implicitly.

1. PQA accept on the parent REQ must be APPROVED (except a human asked to deploy one task).
2. PROD → every sibling you will release has `approved_by`. Else `NEEDS_INPUT`.
3. READY_FOR_DEPLOY → DEPLOYING **on this task only**.
4. `python3 scripts/deploy.py --env <ENV>` (optional `--component <name>`). Builds, pushes
   `ghcr.io/<owner>/product-<component>:<env>-<sha>` and `:<env>`, then compose `up -d` on
   **this machine**. Smoke: API `/actuator/health` and FE `/`.
5. Append `## Deployment` on **this** task (image/tag, command, smoke, rollback). OK →
   DEPLOYING → RELEASED (`release` set, `releases/REL-###.md` if PROD).
   Compatible siblings still `READY_FOR_DEPLOY` stay there until each is deployed with its own
   evidence. After the last direct child is `RELEASED`, set the parent REQ `RELEASED` if
   `req.py check` passes.
6. Tooling fail → FAILED (`failed_from: DEPLOYING`).

```markdown
### <ENV> — <time> — OK | FAILED
- Images: `ghcr.io/…/product-<c>:<env>-<sha>`
- Command: `python3 scripts/deploy.py --env <ENV>`
- Smoke: `<url>` → …
- Rollback: `docker compose -f ops/compose/<env>.yml up -d` with the previous tag
```
