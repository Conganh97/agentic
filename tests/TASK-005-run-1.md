---
task: TASK-005
run: 1
verdict: PASS
tested_sha: ded64f8
merge_commit: ded64f8
updated: 2026-09-24 11:20
---

# TASK-005 Test Run 1

- Tested: `main` @ `ded64f8` (contains `merge_commit` ded64f8)
- Build/tests: `./mvnw -q verify` PASS (88 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | `POST http://localhost:18081/api/v1/cart/items` `{"productId":"aaaaaaaa-0001-4000-8000-000000000001","quantity":1}` → 200 `{"items":[{"productId":"aaaaaaaa-0001-4000-8000-000000000001","slug":"vien-moi-chep-ngot","name":"Viên mồi chép ngọt","imageUrl":"/placeholders/product.svg","unitPriceVnd":45000,"quantity":1,"lineTotalVnd":45000}],"totalQuantity":1,"totalPriceVnd":45000}` + `Set-Cookie: cart_token=…` HttpOnly SameSite=Lax Path=/ Max-Age=2592000. Unknown `…0099` → 404 ProblemDetail `{"detail":"Product not found","status":404}`. quantity 0 and 100 → 400 `{"detail":"Invalid request content.","status":400}`. |
| AC-002 | PASS | `GET /api/v1/cart` no cookie → 200 `{"items":[],"totalQuantity":0,"totalPriceVnd":0}`. After A×1 + B×2: items include `unitPriceVnd` 45000/52000, `quantity` 1/2, `lineTotalVnd` 45000/104000; `totalQuantity` 3; `totalPriceVnd` 149000. |
| AC-003 | PASS | `PATCH /api/v1/cart/items/aaaaaaaa-…0001` `{"quantity":5}` → 200 A qty 5 `lineTotalVnd` 225000, totals 7 / 329000. `DELETE` B → 200 remaining A qty 5. Repeat DELETE and PATCH missing B → 404 `{"detail":"Cart item not found","status":404}`. |
| AC-004 | PASS | Guest A×5 then login with `cart_token` after user already had A×80 → `GET /api/v1/cart` 200 A qty 85 `totalPriceVnd` 3825000. Cap: guest A×30 + user A×80 → qty 99. Register with guest B×3 → session GET 200 B qty 3 (user cart). |
| AC-005 | PASS | `./mvnw -q verify` 88 tests. CartApiTest `addUpdateDeleteTotalsEmptyCartAndMergeOnSignIn`, `mergeCapsSharedLineAt99`. CartControllerTest add/404/empty/patch/qty 0–100/delete missing. CartServiceTest add, empty, increment+cap, merge sum+cap+delete guest. AuthControllerTest `loginWithGuestCartTokenMergesIntoUserCart`. |

Exploratory:
- POST add increments existing line and caps at 99 (50 then 60 → qty 99). PATCH qty 0/100 → 400; PATCH 99 → 200.
- Invalid `cart_token=not-a-uuid` GET → 200 empty cart. `{}` POST → 400 ProblemDetail, no stack.
- TASK-002/003 regression: `/api/v1/categories` 200 two parents (7+5 children); `/api/v1/products?size=5` 200 `total=18`; `/api/v1/articles` 200 `total=3`.
- TASK-001/004: `/actuator/health` 200 UP; `/api/v1/does-not-exist` 404 ProblemDetail, no stack.
- Flyway V1–V7 applied (`V7__carts.sql`). shop-service left clean on `main`; port 18081 free after stop. Throwaway PG `:15432` removed (`:5432` is unrelated `task-service-pg`).

Bug (FAIL): n/a
