# ADR-0003: Product tech stack — Java Spring microservices + React

- **Status:** Accepted
- **Date:** 2026-09-23
- **Deciders:** Project owner

## Context

Agents need a fixed, documented stack for the product in `product/` so that designs, code, tests and
reviews are consistent.

## Decision

- **Backend:** Java 21, Spring Boot 4.0.x (Maven, one Maven project per service with its own wrapper),
  Spring Cloud 2025.1.x only when a cross-service feature needs it.
- **Architecture:** microservices in one product repo (`services/<name>-service/`), database per service
  (PostgreSQL + Flyway), synchronous REST (`/api/v1/...`) between services; messaging only via a new ADR.
- **Frontend:** React + TypeScript (Vite), TanStack Query, React Router (when there is more than one
  route), Vitest + React Testing Library, oxlint + Prettier. Lives in `frontend/`.
  *Amended 2026-09-23 (Phase 8):* linter changed from ESLint to oxlint, which `create-vite` 9 generates;
  the project keeps the scaffolder's tooling instead of swapping it.
- **Testing:** JUnit 5, AssertJ, Mockito, Spring slice tests; Testcontainers for PostgreSQL when Docker
  is available; Playwright for end-to-end tests (TEST role).

## Consequences

- One repo keeps branching and review simple for agents; services stay independently buildable.
- Spring Boot 4 uses modular starters and moved test annotations; standards document the exact names.
- Docker is required for repository integration tests (Testcontainers).

## Alternatives considered

- Repo per service — rejected for now: more coordination for agents, no benefit at current size.
- Spring Boot 3.5 — rejected: open-source support ends mid-2026.
- Spring Boot 4.1 — deferred: no GA Spring Cloud release train compatible yet.
