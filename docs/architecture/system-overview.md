# System Overview

Control = workflow rule. State = markdown. Audit = git. No orchestrator service (ADR-0002).

```
HUMAN (REQ, approved_by, unblock)
        → Scrum (/scrum run, next.py)
        → tasks/TASK-###.md  status = truth
             SA  PQA  UX/UI  BE/FE  TEST  DEVOPS
             → product/<component>  ·  ops/compose  ·  GHCR
```

| Piece | Where |
|-------|--------|
| Rules | `AGENTS.md`, `workflow.mdc` |
| Skills | `.cursor/skills/<role>/SKILL.md` |
| State / board | `tasks/*.md`, `sync_board.py` |
| Guards | `.githooks/pre-commit`, `.cursor/hooks.json` |
| Build/run | `project.md` (Java 21, Spring, React, ports) |
| Deploy | `scripts/deploy.py`, `ops/compose/`, ADR-0011 |

Flow: `BACKLOG → READY → IN_PROGRESS → CODE_REVIEW → MERGED → TESTING → READY_FOR_DEPLOY → DEPLOYING → RELEASED`
(+ `CHANGES_REQUESTED` / `BUG` / `FAILED` / `BLOCKED`). Table + evidence: `workflow.mdc` §2 / §8.
REQ status owners: §13. Deps: `scripts/deps.py`. `NEEDS_INPUT` is an outcome, not a task status.
