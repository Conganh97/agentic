# ADR-0005: REQ-001 task management components

- **Status:** Superseded by ADR-0007
- **Date:** 2026-09-23
- **Deciders:** SA (REQ-001 analysis)

## Context

REQ-001 requires a full-stack task management application with PostgreSQL persistence, REST APIs, a web UI,
and Docker-based runtimes. The product registry has no components yet. ADR-0003 defines the stack; ADR-0004
requires one git repo per component.

## Decision

Add two new product components for REQ-001:

1. **`task-service`** — Spring Boot microservice at `product/services/task-service`, package
   `com.product.task`, PostgreSQL + Flyway, default port 18082 (`SERVER_PORT` override).
2. **`frontend`** — React + TypeScript Vite app at `product/frontend` (shared shell for future features;
   REQ-001 implements the tasks feature only).

DEVOPS delivers root-level (or `deploy/`) Docker Compose binding PostgreSQL, `task-service`, and `frontend`
build contexts. Repos are created and registered only via `scripts/repo.py` during implementation tasks.

## Consequences

- Positive: Clear separation BE/FE/DEVOPS tasks; aligns with existing standards and greeting-service patterns.
- Negative: Two repos to bootstrap; FE repo scaffolding is non-trivial first-time work (documented in frontend standards).
- Follow-up: Future authentication likely adds `user-service` or auth filter + `user_id` column migration.

## Alternatives considered

- **Monolithic single repo for BE+FE:** Rejected (ADR-0004 repo-per-component).
- **Embed H2 for v1 instead of PostgreSQL:** Rejected (requirement and stack mandate PostgreSQL).
- **Extend `greeting-service` for tasks:** Rejected (unrelated domain; REQ-001 is greenfield task app).
