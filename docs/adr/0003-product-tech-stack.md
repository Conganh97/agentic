# ADR-0003: Product tech stack — Java Spring microservices + React

- **Status:** Accepted (amended by ADR-0009)
- **Date:** 2026-09-23
- **Deciders:** Project owner

## Context

Agents need a fixed, documented stack for the product in `product/` so that designs, code, tests and
reviews are consistent.

## Decision

**Locked cores** (ADR-0009): Backend = Java 21 + Spring (Boot), Maven wrapper per service.
Frontend = React, one `frontend/` app. One repo per component (ADR-0004).

**SA chooses per requirement** (design §5 + ADR if new): Boot minor, DB, migrations, security,
messaging, FE bundler, UI kit, data library, router, test tooling. Defaults when silent:
Boot 4, PostgreSQL/Flyway, Vite + TypeScript + Vitest — not locks.

REST `/api/v1/...` between services unless the design says otherwise. Messaging / extra kits need an ADR.

## Consequences

- One repo keeps branching and review simple for agents; services stay independently buildable.
- Spring Boot 4 uses modular starters and moved test annotations; standards document the exact names.
- Docker is required for repository integration tests (Testcontainers).

## Alternatives considered

- Repo per service — rejected at first (more coordination); adopted later by ADR-0004.
- Spring Boot 3.5 — rejected: open-source support ends mid-2026.
- Spring Boot 4.1 — deferred: no GA Spring Cloud release train compatible yet.
