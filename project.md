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

## Local environment notes

- JDK 25 (Homebrew) is installed; services compile with `--release 21`. `/usr/bin/java` finds no runtime,
  so export it before `./mvnw`:
  `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home`
- Every service reads its port from `SERVER_PORT` (`server.port: ${SERVER_PORT:<default>}`). Port 8081 is
  held by a system agent (`macmnsvc`) on this machine: for local runs pick a free port, e.g.
  `SERVER_PORT=18081 ./mvnw -q spring-boot:run`. Check a port with `nc -z localhost <port>` (`lsof` cannot
  see root-owned listeners).
- Maven writes to `~/.m2` and downloads from Maven Central: in Cursor, run `mvn`/`./mvnw` outside the
  sandbox (full permissions), not only with network access. Same for `npm` (cache in `~/.npm`).
- Node 25 / npm 11 are installed.
- Open the FE as `http://localhost:15173` **or** `http://127.0.0.1:15173`. CORS on the API must allow
  both origins (`docs/standards/backend.md`). A localhost-only allowlist returns 403 on credentialed
  POSTs when the page is opened via `127.0.0.1`.
- Docker is required for Testcontainers. If Docker is not running, repository integration tests cannot
  run: say so in the Implementation notes instead of skipping them silently.

## Environments

| Env | How to deploy | Approval |
|-----|---------------|----------|
| DEV | TODO (Phase 9) | none |
| STG | TODO (Phase 9) | none |
| UAT | TODO (Phase 9) | none |
| PROD | TODO (Phase 9) | human `approved_by` required |
