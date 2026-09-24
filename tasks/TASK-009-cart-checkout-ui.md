---
id: TASK-009
title: Cart and checkout UI
type: TASK
priority: CRITICAL
status: CODE_REVIEW
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-005, TASK-006]
sprint:
branch: feature/TASK-009-cart-checkout-ui
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
updated: 2026-09-24 11:29
---

## Description

Cart page with quantity edits, remove (modal confirm), totals, continue shopping, and a checkout
stub that does not take payment.

## Acceptance Criteria
- [ ] AC-001 `/cart` lists lines from `GET /api/v1/cart` with name, image, unit price, quantity,
      line total; header cart indicator shows `totalQuantity`
- [ ] AC-002 Changing `NumberInput` calls PATCH; confirming delete in a `Modal` calls DELETE;
      totals on screen match `totalQuantity` and `totalPriceVnd`
- [ ] AC-003 Empty cart shows §13 empty state and a button to `/products`; “Tiếp tục mua sắm”
      goes to `/products`
- [ ] AC-004 “Thanh toán” navigates to `/checkout`, which shows totals and an `Alert` that
      online payment is not in this version, plus a button to `/contact`
- [ ] AC-005 RTL tests: empty cart, populated totals, delete modal, checkout stub render

## Design (SA)
See `docs/design/REQ-001-design.md` §13 (FR-5, FR-6, FR-13). Repo: frontend (existing).
- Mantine: `Table` (desktop), stacked `Card` below `sm`, `NumberInput`, `Modal`, `Button`,
  `Indicator` on header cart icon, `notifications` on errors.
- `credentials: 'include'` on cart fetch. No payment fields.
- Fetch wrapper already in TASK-006.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-009-cart-checkout-ui` @ 79a9a63
- Changed: `frontend/src/api/cart.ts`, `frontend/src/api/cart.test.ts`, `frontend/src/features/cart/*`, `frontend/src/components/AppShellLayout.tsx`, `frontend/src/app/router.tsx`, `frontend/src/features/catalog/useCatalogQueries.ts`, `frontend/src/features/account/useAuthQueries.ts`, `frontend/src/features/catalog/ProductDetailPage.test.tsx`
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (48 tests)
- Notes: `GET/PATCH/DELETE /api/v1/cart*` with `credentials: 'include'`. Header `Indicator` label = `totalQuantity` (hidden at 0). Empty: `IconBasketOff` + “Giỏ hàng trống” / “Chưa có sản phẩm trong giỏ.” + “Tiếp tục mua sắm” → `/products`. Populated: desktop `Table`, stacked `Card` below `sm` (`useMediaQuery`); `NumberInput` label “Số lượng {name}”; trash `ActionIcon` opens `Modal` “Xóa sản phẩm” / “Xóa {name} khỏi giỏ hàng?”. Totals `Paper` “Tổng số lượng” / “Tổng tiền”. Checkout: reprint totals, teal `Alert` “Thanh toán cổng thanh toán chưa có trong phiên bản này…”, “Liên hệ để hoàn tất” → `/contact`. No payment fields. Add-to-cart writes `CART_QUERY_KEY`; login/register/logout invalidate cart (guest merge). PATCH/DELETE errors toast; delete success “Đã xóa khỏi giỏ”. `PlaceholderPage` left unused. Branch pushed.

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 11:25 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-005, TASK-006] READY_FOR_DEPLOY |
| 2026-09-24 11:27 | READY | IN_PROGRESS | FE | Started on feature/TASK-009-cart-checkout-ui |
| 2026-09-24 11:29 | IN_PROGRESS | CODE_REVIEW | FE | Product 79a9a63; Implementation Iteration 1 |
