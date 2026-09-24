# ADR-0007: REQ-001 shop storefront components

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** SA (REQ-001 analysis)

## Context

REQ-001 (revision 1) is a customer-facing e-commerce storefront cloned in spirit from the public
site https://bietdoisanhang.vn/ (fishing bait and equipment). The product registry is empty
(greenfield). ADR-0003/0004/0006 still apply. ADR-0005 described a previous, replaced REQ-001
(`task-service` + task UI) and must not be reused for this product.

The requirement forbids unnecessary infrastructure (no payment, shipping, ERP, or CMS) while still
requiring REST APIs, PostgreSQL, a multi-page React UI, and Docker.

## Decision

Add two product components for REQ-001. Repos are created only via `scripts/repo.py` during the
implementing tasks.

1. **`shop-service`** — one Spring Boot 4 service at `product/services/shop-service`, package
   `com.product.shop`, PostgreSQL + Flyway, default port `18081` (`SERVER_PORT` override). It owns
   catalog, search, news, static pages, customer accounts, and cart. No second backend service in v1.
2. **`frontend`** — React + TypeScript Vite app at `product/frontend` with Mantine (ADR-0006).
   Storefront shell, catalog, cart, account, news, and policy pages.

DEVOPS adds a Dockerfile in each repo and a Compose file in `shop-service` that builds
`shop-service` plus `../../frontend` and runs PostgreSQL. That path is valid only when both
repos are cloned under `product/` as the registry expects.

ADR-0005 is superseded by this ADR for product components.

## Consequences

- Positive: one BE repo and one FE repo; no Spring Cloud; matches “do not introduce unnecessary
  infrastructure”; clear BE/FE/DEVOPS task split.
- Negative: catalog, accounts, and cart share one database (acceptable for a single shop).
- Follow-up: payment, admin CMS, or a split `user-service` need a new ADR.

## Alternatives considered

- **Reuse ADR-0005 `task-service`:** Rejected — different domain; that REQ-001 was replaced.
- **Split catalog / user / cart / content services:** Rejected for v1 — extra repos and network hops
  without a requirement to scale them independently.
- **H2 instead of PostgreSQL:** Rejected (stack and requirement).
- **Copy reference assets or Haravan auth:** Rejected (legal / out of scope).
