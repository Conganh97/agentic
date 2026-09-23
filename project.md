# Product Configuration

Agents read this file to learn how to work with the product. Stack decision: `docs/adr/0003-product-tech-stack.md`.

## Repository

- Path: `product/` (separate git repo, git-ignored by the team repo)
- Remote: none (local-only; set a git URL here to enable pushing branches as backup)
- Main branch: `main`
- Merge: SA merges locally with `git merge --no-ff` after approval in the task file (no PR/MR)

## Layout

```
product/
├── services/
│   └── <name>-service/     # one Spring Boot app per service: pom.xml, mvnw, src/
├── frontend/               # React app (Vite)
└── README.md
```

## Stack

| Area | Choice |
|------|--------|
| Backend | Java 21, Spring Boot 4.0.8, Maven (wrapper per service) |
| Cross-service | REST `/api/v1/...` via `RestClient`; Spring Cloud 2025.1.3 only when needed (ADR) |
| Database | PostgreSQL, one database per service, Flyway migrations |
| Base package | `com.product.<service>` (e.g. `com.product.user`) |
| Frontend | React + TypeScript, Vite, React Router, TanStack Query |
| Tests (BE) | JUnit 5, AssertJ, Mockito, `@WebMvcTest`, `@DataJpaTest`, Testcontainers |
| Tests (FE) | Vitest + React Testing Library; Playwright for e2e |
| Lint (FE) | ESLint + Prettier |

## Commands

| Purpose | Command |
|---------|---------|
| Build + all tests (one service) | `cd product/services/<svc> && ./mvnw -q verify` |
| Unit tests only (one service) | `cd product/services/<svc> && ./mvnw -q test` |
| Run a service | `cd product/services/<svc> && ./mvnw spring-boot:run` |
| FE install | `cd product/frontend && npm ci` |
| FE tests | `cd product/frontend && npm test -- --run` |
| FE lint / build | `cd product/frontend && npm run lint && npm run build` |
| E2E tests | `cd product/frontend && npx playwright test` |

## Local environment notes

- JDK 25 (Homebrew) is installed; services compile with `--release 21`. `/usr/bin/java` finds no runtime,
  so export it before `./mvnw`:
  `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home`
- Maven writes to `~/.m2` and downloads from Maven Central: in Cursor, run `mvn`/`./mvnw` outside the
  sandbox (full permissions), not only with network access.
- Docker is required for Testcontainers. If Docker is not running, repository integration tests cannot
  run: say so in the Implementation notes instead of skipping them silently.

## Environments

| Env | How to deploy | Approval |
|-----|---------------|----------|
| DEV | TODO (Phase 9) | none |
| STG | TODO (Phase 9) | none |
| UAT | TODO (Phase 9) | none |
| PROD | TODO (Phase 9) | human `approved_by` required |
