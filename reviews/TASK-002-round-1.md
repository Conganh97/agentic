---
task: TASK-002
round: 1
decision: APPROVED
branch: feature/TASK-002-catalog-search-api
sha: bf747cb
updated: 2026-09-24 09:50
---

# TASK-002 Review Round 1

Reviewed: `feature/TASK-002-catalog-search-api` @ `bf747cb` · Build/tests: `./mvnw -q verify` PASS (30 tests)

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | api/CatalogApiTest.java:38 | MINOR | AC-001 test samples a few slugs; assert the full design §7 parent+child set so a dropped seed category fails CI. |
| 2 | repository/ProductRepository.java:16 | MINOR | `@EntityGraph` on `findTop8…` includes `images` and logs HHH90003004 (limit applied in memory). Fetch related without the collection graph, or load images in a second query. |
| 3 | service/CatalogService.java:47 | MINOR | `listProducts` Specification has no entity graph; `toCard` lazy-loads `category` and `images` (N+1). Add a fetch graph or join on the page query. |

Merged `37baf91`.
Pushed main.
