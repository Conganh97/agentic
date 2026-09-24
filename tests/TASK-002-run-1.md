---
task: TASK-002
run: 1
verdict: PASS
tested_sha: 37baf91
merge_commit: 37baf91
updated: 2026-09-24 09:54
---

# TASK-002 Test Run 1

- Tested: `main` @ `37baf91` (contains `merge_commit` 37baf91)
- Build/tests: `./mvnw -q verify` PASS (30 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | `curl -s http://localhost:18081/api/v1/categories` → 200 two-level tree. Parents `moi-cau-ca`, `phu-kien-do-cau`. Bait children: `cau-ca-ro-phi`, `cau-ca-chep`, `cau-ca-diec`, `cau-ca-tram-co`, `cau-ca-tram-den`, `huong-lieu-du-ca`, `moi-cau-ca-cac-loai`. Gear children: `can-cau-ca`, `theo-cau-ca`, `truc-cau-ca`, `phao-cau-ca`, `phu-kien-khac`. |
| AC-002 | PASS | `GET /api/v1/products?category=cau-ca-chep` → 200 `items` length 4, all `categorySlug=cau-ca-chep`, each has `name`, `imageUrl=/placeholders/product.svg`, `priceVnd`; `total=4`. `GET /api/v1/products?category=khong-ton-tai` → 404 `{"detail":"Category not found","status":404,"title":"Not Found"}`. |
| AC-003 | PASS | `GET /api/v1/products/vien-moi-chep-ngot` → 200 with `description`, `information`, `usage`, `images` (2 placeholders), `related` length 3 (≤8) all `cau-ca-chep`, none self. `GET /api/v1/products/khong-ton-tai` → 404 `{"detail":"Product not found","status":404}`. |
| AC-004 | PASS | `GET /api/v1/products?q=CHÉP` → 200 `total=4` name matches. `GET /api/v1/products?q=khong-co-san-pham-nao-het` → 200 `{"items":[],"page":1,"size":24,"total":0}`. `q` length 80 → 200; length 81 → 400 `Validation failure`. |
| AC-005 | PASS | `GET /api/v1/products?page=1&size=5&sort=price&order=asc` → 200 5 items, prices 19000..31000, `total=18`. `sort=name&order=desc` → 200 name desc. `featured=true&size=60` → `total=4`. `size=60` → 200; `size=61` → 400; `sort=unknown` → 400. `./mvnw -q verify` CatalogApiTest covers list, detail, empty search, 404. |

Exploratory:
- Blank `q=` treated as no text filter → 200 `total=18` (matches Implementation note).
- Parent `category=moi-cau-ca` → 200 `items: []` `total: 0` (exact category only, not descendants).
- `GET /api/v1/categories/cau-ca-chep` → 200; unknown slug → 404.
- TASK-001 regression: `/actuator/health` 200 `{"status":"UP"}`; `/api/v1/does-not-exist` 404 ProblemDetail, no stack.
- Page 2 `size=5` `sort=price` → next 5 prices 35000..42000.
- Startup Flyway V1/V2/V3. HHH90003004 on detail (known SA MINOR, not AC fail).
- shop-service left clean on `main`; port 18081 free after stop.

Bug (FAIL): n/a
