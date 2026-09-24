---
id: TASK-002
title: Catalog and search APIs
type: TASK
priority: CRITICAL
status: BACKLOG
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-001]
sprint:
branch:
merge_commit:
release:
review_iteration: 0
test_iteration: 0
blocked_from:
failed_from:
failure_type:
failure_step:
failure_message:
failure_retry: 0
failure_recoverable:
human_gate:
approved_by:
approved_at:
updated: 2026-09-24 09:15
---

## Description

Persist categories, products, and product images; seed the tree and ≥16 synthetic products; expose
list/detail/search as specified in the design. Placeholder image URLs only.

## Acceptance Criteria
- [ ] AC-001 `GET /api/v1/categories` returns the two-level tree (bait + gear parents and children)
      with slugs from design §7
- [ ] AC-002 `GET /api/v1/products?category=cau-ca-chep` returns only products in that category;
      each item has `name`, `imageUrl`, `priceVnd`; unknown category → 404
- [ ] AC-003 `GET /api/v1/products/{slug}` returns description, information, usage, images, and
      up to 8 related products in the same category excluding self; missing slug → 404
- [ ] AC-004 `GET /api/v1/products?q=` (case-insensitive name/description contains, `q` max 80)
      returns matches; a `q` with no rows returns `items: []` and `total: 0` (200)
- [ ] AC-005 Pagination (`page`,`size` max 60) and `sort=name|price` + `order` work; seed has
      ≥4 `featured=true`; tests cover list, detail, empty search, and 404

## Design (SA)
See `docs/design/REQ-001-design.md` §6–§7 (FR-2, FR-3, FR-4). Repo: shop-service (existing after TASK-001).
- Flyway `V1`/`V2` tables `categories`, `products`, `product_images` + seed; integer VND; no scraped photos.
- DTOs are records; controllers do not call repositories; `@Size` on `q`.
- Search is SQL contains, not an external search engine.
- `featured=true` query used later by home.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
