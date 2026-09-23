# DevOps Standards

Status: baseline only. Detailed pipeline and environment rules are defined when Phase 9
(DevOps Agent) starts, recorded in an ADR.

## Git

- Branch naming: `feature/<task-id>-<short-name>`, `fix/<task-id>-<short-name>`.
- Commit messages: `<type>(<scope>): <summary>` — types: `feat, fix, refactor, test, docs, chore`.
  Reference the task id, e.g. `feat(orchestrator): add state machine [TASK-12]`.
- No direct pushes to `main`. Every change goes through a PR and code review.
- Agents never merge their own PRs.

## Environments and deployment

- Environments: `DEV → STG → UAT → PROD`.
- DEV/STG/UAT deployments follow policy; **PROD requires explicit human approval**.
- Every deployment is traceable to a commit, build, and task; rollback procedure must exist.

## Security

- Secrets come from a secret manager or environment, never from the repository.
- Destructive operations (DB drop/truncate, force push, resource deletion) are blocked for agents
  unless explicitly approved.
- Agents never get unrestricted shell access in production.
