# ADR-0009: Locked cores, SA-chosen stack, package structure

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Project owner
- **Supersedes:** ADR-0006 (Mantine is no longer the global UI kit). Amends ADR-0003.

## Decision

### Locked (do not change without a new ADR)

| Side | Locked |
|------|--------|
| Backend | Java 21 + Spring (Boot). One Maven module per `*-service`. |
| Frontend | React. One app repo `product/frontend`. |

### SA chooses per requirement

Record the choice in design §5 (Stack table). New technology / data store / kit → ADR.

**Backend examples:** Boot minor, DB, migrations, security (session/JWT), messaging, cache, Spring Cloud, API style extras.

**Frontend examples:** bundler, UI kit (Mantine, shadcn, Ant, Chakra, …), icons, fonts, router, server-state, CSS approach, test runner.

Defaults when the REQ is silent (not locks): Spring Boot 4 + PostgreSQL/Flyway; Vite + TypeScript + Vitest. SA may pick otherwise.

### Structures (required)

BE = **package by feature** (`docs/standards/backend.md`). FE = **app / pages / features / shared** (`docs/standards/frontend.md`). Do not go back to a flat `api/service/repository` or `components/` dump.

## Consequences

- Agents stop assuming Mantine / TanStack / PostgreSQL unless the design says so.
- First FE/BE task of a product installs **the kit SA named**, not a hardcoded list.
- ADR-0006 remains historical; do not follow it for new work.
