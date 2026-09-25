# Agentic Engineering Team

Cursor-native team (Scrum, SA, PQA, UX/UI, BE, FE, TEST, DevOps). **Markdown + git only.**

- **State** = `status:` on `tasks/TASK-###-*.md`
- **Rules** = `AGENTS.md` + `.cursor/rules/workflow.mdc`
- **Product** = one GitHub repo per component under `product/` (git-ignored here)

```
HUMAN REQ APPROVED
  → /scrum run REQ-###
      SA ⇄ PQA plan → ANALYZED
      DEVOPS repos + Docker/CI (if new components)
      UX/UI ∥ BE → PQA UX → FE → PQA visual → SA merge
      TEST → PQA accept → DEVOPS deploy DEV/STG/PROD
```

## Once per machine

1. `git config core.hooksPath .githooks`
2. `brew install gh && gh auth login && gh auth refresh -s write:packages`
3. Owner / `product-<component>` / visibility in `project.md`
4. JDK 21+, Node, **Docker Desktop**. `JAVA_HOME` + ports: `project.md`
5. Figma MCP: Settings → Tools & MCP → Connect (`https://mcp.figma.com/mcp`)
6. Optional: self-hosted Actions runner on this Mac. Else `/devops deploy` is CI.

Do not clone `product/` by hand — `/repo create`.

## Deliver a requirement

1. Copy `templates/requirement.md` → `requirements/REQ-###-<slug>.md` (see `requirements/README.md`).
   Hash: `python3 scripts/req.py hash …`. Body edit → bump `revision` + re-hash.
2. You set `status: APPROVED`.
3. `/scrum run REQ-###` (main chat = SCRUM). Or call a role (`/backend TASK-###`, …).
4. You: approve DRAFT REQ, set `approved_by` on gates/PROD, unblock `BLOCKED`. Keep Docker up.

Shell: `python3 scripts/next.py` · `scrum_report.py` · `deps.py` · `req.py check` ·
`deploy.py --env DEV`.

## Commands

| Command | Role | Does |
|---------|------|------|
| `/scrum run\|next\|ready\|sprint\|report` | Scrum | State machine / DoR / increment |
| `/sa analyze REQ-###` · `/sa review TASK-###` | SA | Design+tasks · code merge (`--no-ff`) |
| `/pqa plan\|review\|accept` | PQA | Plan gate · UX · increment |
| `/uxui TASK-###` | UX/UI | `docs/design/ux/` + Figma |
| `/backend TASK-###` | BE | `product/services/<name>-service` |
| `/frontend TASK-###` | FE | `product/frontend` |
| `/tester TASK-###` | TEST | Black-box after MERGED |
| `/devops TASK-###` · `/devops deploy TASK ENV` | DevOps | Repos/Docker/GHA · GHCR + compose |
| `/repo create\|push\|status` | Repo | `repo.py` (DevOps preferred creator) |

One chat = one role except `/scrum run`. Skills do not auto-invoke.

## Layout

```
AGENTS.md  project.md  requirements/  tasks/  sprints/  bugs/
reviews/  tests/  runs/  releases/  ops/  docs/  memory/  templates/
scripts/  .cursor/  .githooks/  product/   ← ignored, one repo per component
```

| Path | Keywords |
|------|----------|
| `project.md` | registry, Java 21 + Spring, React, `./mvnw`, npm, ports 15173/18081, GHCR |
| `ops/compose/{dev,stg,prod}.yml` | local stack; images `ghcr.io/Conganh97/product-<c>:<env>-<sha>` |
| `docs/design/REQ-###-design.md` | SA §5 stack, API, data, tasks |
| `docs/design/ux/` | UX contract + Figma URL |
| `docs/standards/` | BE package-by-feature · FE `app/pages/features/shared` · density · DevOps |
| `docs/adr/` | 0004 repos · 0008 UX · 0009 stack · 0010 PQA · 0011 CI/CD |
| `templates/` | copy these (`requirement`, `task`, `design`, `ux-*`, `ops/`, …) |

Product after create: `product/services/<name>-service/` (pom.xml, package-by-feature) ·
`product/frontend/` (Vite React, `src/{app,pages,features,shared}`). Dockerfile +
`.github/workflows/ci.yml` seeded. `main` only after SA `--no-ff` + `merge_commit`.

## Roles / workflow

| Role | Owns |
|------|------|
| HUMAN | REQ, `approved_by`, unblock |
| SCRUM | board, READY, `/scrum run` |
| SA | design, tasks, **code** merge |
| PQA | plan, UX review, increment accept |
| UX/UI | markdown + Figma (PQA approves look) |
| BE / FE | feature branches |
| TEST | AC vs `main` |
| DEVOPS | repos, Docker, GHA, compose, deploy |

`BACKLOG → READY → IN_PROGRESS → CODE_REVIEW → MERGED → TESTING → READY_FOR_DEPLOY → DEPLOYING → RELEASED`
(+ `CHANGES_REQUESTED` / `BUG` / `FAILED` / `BLOCKED`). Max 3 review/test loops. DoR: `parent`,
`assignee`, `AC-###`, `depends_on`, Design. Locked stack: Java 21 + Spring, React (ADR-0009).
