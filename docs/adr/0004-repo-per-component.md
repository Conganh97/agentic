# ADR-0004: One repository per product component, pushed to GitHub

- **Status:** Accepted
- **Date:** 2026-09-23
- **Deciders:** HUMAN (anh), SA

## Context

ADR-0003 kept all services and the frontend in one local product repo. The human wants each service and
the frontend to be deployable on its own (CI/CD with GitHub Actions, Docker Compose, later Kubernetes),
which works best with one repository per deployable unit, and wants code pushed automatically.

## Decision

- Every backend service (`product/services/<name>-service/`) and the frontend (`product/frontend/`) is its
  own git repository with a private GitHub remote `Conganh97/product-<component>`. `product/` is only a
  folder, git-ignored by the team repo.
- Repositories are created and pushed only through `scripts/repo.py` (skill `repo`), which records them in
  the `project.md` registry.
- Push policy: task branches are pushed by BE/FE after each product commit; `main` is pushed by SA right
  after the local `--no-ff` merge, and the script refuses any `main` commit that is not a merge recorded
  as a task's `merge_commit`. Raw pushes to `main`, force pushes and repo deletion are blocked by the shell
  guard.
- Review and merge stay local and markdown-based (no pull requests), as in ADR-0002.

## Consequences

- Each component has its own CI/CD (Dockerfile + GHA) from `repo.py create`; DevOps owns create and
  repairs (ADR-0011). Stack compose lives in the team `ops/` folder.
- Agents must use the component path (`<repo>`) instead of a single `product/` repo; a task touches one
  component, so one task = one repo.
- Needs the GitHub CLI logged in once by a human; without it, creation stops with `NEEDS_INPUT`.
- Cross-component changes (API + UI) are already split into separate tasks, so no atomic multi-repo commit
  is needed.

## Alternatives considered

- Keep the monorepo (ADR-0003) with one GitHub remote — rejected: the human wants per-component deployment.
- Pull requests on GitHub for review — rejected: ADR-0002, review and approval live in task files.
