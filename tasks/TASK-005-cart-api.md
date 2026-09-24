---
id: TASK-005
title: Cart APIs and guest merge
type: TASK
priority: CRITICAL
status: MERGED
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-002, TASK-004]
sprint:
branch: feature/TASK-005-cart-api
merge_commit: ded64f8
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
updated: 2026-09-24 11:13
---

## Description

Server-side cart for guests (`cart_token` cookie) and for a signed-in user. Support add, change
quantity, remove, and correct totals. When the customer signs in, merge guest lines into the user
cart by `product_id` (sum quantity, cap 99).

## Acceptance Criteria
- [ ] AC-001 `POST /api/v1/cart/items` with a valid `productId` and quantity 1–99 returns 200
      `Cart` with that line and may `Set-Cookie: cart_token` for a guest; unknown product → 404;
      quantity 0 or 100 → 400
- [ ] AC-002 `GET /api/v1/cart` returns items with `unitPriceVnd`, `quantity`, `lineTotalVnd`,
      `totalQuantity` (sum of qty), `totalPriceVnd` (sum of line totals); empty cart is 200 with zeros
- [ ] AC-003 `PATCH /api/v1/cart/items/{productId}` updates quantity; `DELETE` removes the line;
      missing line → 404
- [ ] AC-004 After a successful sign-in while a guest `cart_token` is present, guest lines merge
      into the user cart (same product: quantities added, max 99); later GET uses the user cart
- [ ] AC-005 Tests cover add, update, delete, totals, empty cart, and merge-on-sign-in

## Design (SA)
See `docs/design/REQ-001-design.md` §6–§7 (FR-5, FR-6). Repo: shop-service (existing).
- Tables `carts`, `cart_items`; prices copied from current `products.price_vnd` at add/update.
- Guest cookie UUID; user cart unique on `user_id`. Do not add payment or orders.
- Avoid new public routes beyond `/api/v1/cart*`.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-005-cart-api` @ ac3c4f2
- Changed: `services/shop-service/src/main/resources/db/migration/V7__carts.sql`, `api/CartController.java`, `api/{AddCartItem,UpdateCartItem}Request.java`, `api/{Cart,CartItem}Response.java`, `service/CartService.java`, `domain/{Cart,CartItem}.java`, `repository/CartRepository.java`, `api/AuthController.java`, `service/AuthService.java`, `CartControllerTest.java`, `CartServiceTest.java`, `CartApiTest.java`, `AuthControllerTest.java`, `AuthServiceTest.java`, `ShopApplicationTests.java`
- Tests: `./mvnw -q verify` in `services/shop-service` → pass (88 tests)
- Notes: Flyway V7 (V1–V6 already used). `cart_items.unit_price_vnd` stores the product price copied at add/update (column not listed in design §7). Guest `cart_token` is httpOnly SameSite=Lax Path=/ 30 days; issued only when a new guest cart is created. POST add increments an existing line and caps at 99, then refreshes unit price. Merge runs on login and register; same `product_id` sums qty (max 99) and keeps the user line’s unit price; guest-only lines keep the stored guest price; guest cart row is deleted. Invalid/expired session falls back to guest/empty cart (no 401). Invalid `cart_token` is ignored. Branch pushed.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-005-cart-api @ ac3c4f2 · Build/tests: ./mvnw -q verify PASS (88 tests)
No comments.

Merged ded64f8.
Pushed main.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 11:04 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002, TASK-004] READY_FOR_DEPLOY |
| 2026-09-24 11:05 | READY | IN_PROGRESS | BE | branch feature/TASK-005-cart-api |
| 2026-09-24 11:09 | IN_PROGRESS | CODE_REVIEW | BE | product ac3c4f2; Implementation Iteration 1; ./mvnw -q verify pass (88 tests) |
| 2026-09-24 11:13 | CODE_REVIEW | MERGED | SA | review round 1 APPROVED; merge_commit=ded64f8 (--no-ff); ./mvnw -q verify PASS (88 tests) |
