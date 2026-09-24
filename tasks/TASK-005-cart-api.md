---
id: TASK-005
title: Cart APIs and guest merge
type: TASK
priority: CRITICAL
status: BACKLOG
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-002, TASK-004]
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

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
