---
id: TASK-002
title: Catalog and search APIs
type: TASK
priority: CRITICAL
status: MERGED
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-001]
sprint:
branch: feature/TASK-002-catalog-search-api
merge_commit: 37baf91
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
updated: 2026-09-24 09:50
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
### Iteration 1 (initial)
- Branch: `feature/TASK-002-catalog-search-api` @ bf747cb
- Changed: `services/shop-service/src/main/resources/db/migration/V2__catalog.sql`, `V3__catalog_seed.sql`, `api/CategoryController.java`, `api/ProductController.java`, `api/*Response.java`, `service/CatalogService.java`, `service/ProductSpecifications.java`, `domain/{Category,Product,ProductImage}.java`, `repository/{Category,Product}Repository.java`, `CatalogApiTest.java`, `CategoryControllerTest.java`, `ProductControllerTest.java`, `CatalogServiceTest.java`, `ProductRepositoryTest.java`, `ShopApplicationTests.java`
- Tests: `./mvnw -q verify` in `services/shop-service` → pass (30 tests)
- Notes: TASK-001 already used Flyway V1 baseline, so tables are V2 and seed is V3. Blank `q` is treated as no text filter; unknown `category` is 404 per AC-002. Search is SQL contains with `\`-escaped `%`/`_`. Parent slug filters that exact category only (not descendants). `GET /categories/{slug}` added from design §6. Seed: 18 products, 4 featured, `/placeholders/product.svg` only. Boot 4 `@DataJpaTest` needs `spring-boot-data-jpa-test` (not on classpath); seed/repo check uses `@SpringBootTest` + Testcontainers. Branch pushed.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-002-catalog-search-api @ bf747cb · Build/tests: ./mvnw -q verify PASS (30 tests)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | api/CatalogApiTest.java:38 | MINOR | AC-001 test samples a few slugs; assert the full design §7 parent+child set so a dropped seed category fails CI. |
| 2 | repository/ProductRepository.java:16 | MINOR | `@EntityGraph` on `findTop8…` includes `images` and logs HHH90003004 (limit applied in memory). Fetch related without the collection graph, or load images in a second query. |
| 3 | service/CatalogService.java:47 | MINOR | `listProducts` Specification has no entity graph; `toCard` lazy-loads `category` and `images` (N+1). Add a fetch graph or join on the page query. |

Merged 37baf91.
Pushed main.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:39 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-001] READY_FOR_DEPLOY |
| 2026-09-24 09:41 | READY | IN_PROGRESS | BE | branch feature/TASK-002-catalog-search-api |
| 2026-09-24 09:47 | IN_PROGRESS | CODE_REVIEW | BE | product commit bf747cb; Implementation Iteration 1 |
| 2026-09-24 09:50 | CODE_REVIEW | MERGED | SA | merge_commit=37baf91; reviews/TASK-002-round-1.md APPROVED; --no-ff on main |
