# ADR-0011: Local CI/CD, GHCR images, DevOps-owned repos

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Project owner
- **Amends:** ADR-0004 (DevOps is the preferred repo creator)

## Context

There is no remote app server yet. Product repos already live on GitHub. The team needs DEV / STG /
PROD, Docker images that can be pulled and run, and one role that owns repos, Docker, compose, and
the pipeline.

## Decision

- **DevOps** creates product repos when they are missing (`/repo create`), then writes or repairs
  `Dockerfile`, GitHub Actions, and compose. BE/FE may create a repo only as a fallback.
- **Environments:** `DEV`, `STG`, `PROD` (no UAT). PROD still needs human `approved_by`.
- **Images:** `ghcr.io/<owner>/product-<component>:<env>-<sha>` and `:<env>`. Push on every deploy
  so anyone (or compose) can `docker pull` and run.
- **Where it runs:** this machine. `python3 scripts/deploy.py --env DEV|STG|PROD` is the pipeline
  (build → push GHCR → `docker compose up`). Optional GitHub Actions on a **self-hosted** runner
  repeats the same on push to `main`.
- **Stack compose** lives in the team repo (`ops/compose/`). Per-component Docker/CI live in the
  product repo. SA creates a `work_type: DEVOPS` bootstrap task per requirement that introduces
  components. That task skips TEST (like UX_UI).

## Consequences

- Deploy does not wait for a cloud host.
- Human installs Docker and `gh` (packages write). A self-hosted Actions runner is optional.
- Secrets stay in gitignored `ops/compose/.env.*`, never in markdown.

## Alternatives considered

- Cloud-only GitHub-hosted runners — rejected: no target server; human asked for this machine.
- Images only on disk, never pushed — rejected: must be pullable.
- BE/FE remain the default repo creators — rejected: DevOps must control the pipeline from day one.
