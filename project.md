# Product Configuration

Agents read this file to learn how to work with the product. Stack policy: `docs/adr/0009-stack-policy-and-structure.md`.

## Repositories

One git repository + GitHub remote per component (ADR-0004). `product/` is only a folder holding them and
is git-ignored by the team repo. In skills, `<repo>` means the component's Path from the registry below.

- GitHub owner: `Conganh97`
- Repo name: `product-<component>`
- Visibility: `private`
- Main branch: `main` in every repo. SA merges locally with `git merge --no-ff` after approval in the task
  file (no PR/MR), then pushes `main`.
- Create / push only via `python3 scripts/repo.py` (skill `.cursor/skills/repo/SKILL.md`); raw
  `git push` to `main` in `product/` is blocked by the shell guard.

```
product/
├── services/
│   └── <name>-service/     # own repo: one Spring Boot app (pom.xml, mvnw, src/)
└── frontend/               # own repo: React app (Vite)
```

Registry (written by `scripts/repo.py create`; do not edit by hand):

| Component | Type | Path | Remote |
|-----------|------|------|--------|

## Stack

**Locked:** BE = Java 21 + Spring. FE = React. See ADR-0009.

**SA fills per requirement** (design §5): UI kit, data library, bundler, DB, migrations, security,
messaging. Defaults if the REQ is silent — Boot 4, PostgreSQL/Flyway, Vite + TypeScript + Vitest —
are starting points, not locks.

| Area | Notes |
|------|--------|
| Base package | `com.product.<service>` |
| FE layout | `src/{app,pages,features,shared}` |
| BE layout | package-by-feature (`<feature>/{api,application,domain,infrastructure}`) |
| Commands below | assume Maven wrapper + npm; override in the task if SA chose otherwise |

## Commands

| Purpose | Command |
|---------|---------|
| Build + all tests (one service) | `cd product/services/<svc> && ./mvnw -q verify` |
| Unit tests only (one service) | `cd product/services/<svc> && ./mvnw -q test` |
| Run a service | `cd product/services/<svc> && ./mvnw spring-boot:run` |
| FE install | `cd product/frontend && npm ci` |
| FE tests | `cd product/frontend && npm test -- --run` |
| FE lint / build | `cd product/frontend && npm run lint && npm run build` |
| FE verify (before CODE_REVIEW) | `cd product/frontend && npm run lint && npm run format:check && npm test -- --run && npm run build` |
| FE dev server | `cd product/frontend && BACKEND_PORT=18081 npm run dev -- --port 15173` |
| E2E tests | `cd product/frontend && npx playwright test` |
| Deploy DEV/STG/PROD (this machine) | `python3 scripts/deploy.py --env DEV` |

## Local environment notes

- `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home` before `./mvnw`
  (`--release 21`; `/usr/bin/java` has no runtime). Node 25 / npm 11 installed.
- `server.port: ${SERVER_PORT:<default>}`. 8081 is taken (`macmnsvc`) → `SERVER_PORT=18081`.
  Probe: `nc -z localhost <port>` (`lsof` misses root listeners).
- `./mvnw` / `npm` need full permissions (Maven Central, `~/.m2`, `~/.npm`), not sandbox-only.
- FE: `http://localhost:15173` **and** `http://127.0.0.1:15173`. CORS must allow both or
  credentialed POSTs 403. Docker required for Testcontainers — if down, say so, do not skip silently.

## Environments

No remote app host. DevOps builds images here, pushes GHCR, and `docker compose up` on this Mac
(ADR-0011). Images: `ghcr.io/Conganh97/product-<component>:<env>-<sha>`.

| Env | Compose | Web | API | DB | Approval |
|-----|---------|-----|-----|-----|----------|
| DEV | `ops/compose/dev.yml` | 15173 | 18081 | 15440 | none |
| STG | `ops/compose/stg.yml` | 25173 | 28081 | 25440 | none |
| PROD | `ops/compose/prod.yml` | 80 | 8080 | 5432 | human `approved_by` |

`python3 scripts/deploy.py --env DEV`. Secrets in gitignored `ops/compose/.env.<env>`. Optional
self-hosted GitHub Actions runner on this Mac repeats the image push on `main`.
