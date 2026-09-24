---
task: TASK-009
run: 1
verdict: PASS
tested_sha: b4bd0ef
merge_commit: b4bd0ef
updated: 2026-09-24 11:44
---

# TASK-009 Test Run 1

- Tested: `main` @ `b4bd0ef` (contains `merge_commit` b4bd0ef)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (49 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Browser `http://localhost:15173/cart` after add-to-cart (A `Viên mồi chép ngọt` ×1 + B `Bột câu rô phi` ×2): names, `img` `/placeholders/product.svg`, unit `45.000₫` / `36.000₫`, `NumberInput` `Số lượng …`, line `45.000₫` / `72.000₫`. Header `Giỏ hàng` indicator `3`. Totals `Tổng số lượng` `3` / `Tổng tiền` `117.000₫`. Desktop `Table`; stacked `Card` at 687px. AppShell teal `#12b886` / Inter Variable. |
| AC-002 | PASS | Qty A 1→3: `PATCH /api/v1/cart/items/aaaaaaaa-0001-4000-8000-000000000001` body `{"quantity":3}` `credentials: include` → 200. Totals `5` / `207.000₫`, header `5`, line A `135.000₫`. Trash → `Modal` `Xóa sản phẩm` / `Xóa Bột câu rô phi khỏi giỏ hàng?` → confirm `Xóa`: `DELETE /api/v1/cart/items/aaaaaaaa-0001-4000-8000-000000000006` `credentials: include` → 200; toast `Đã xóa khỏi giỏ`; remaining A totals `3` / `135.000₫`, header `3`. |
| AC-003 | PASS | Empty `/cart` H4 `Giỏ hàng trống`, `Chưa có sản phẩm trong giỏ.`, `IconBasketOff`, `Tiếp tục mua sắm` → `/products`. Populated cart same link `href=/products`. |
| AC-004 | PASS | `Thanh toán` → `/checkout` H2 `Thanh toán`; totals `3` / `135.000₫`; teal `Alert` `Thanh toán cổng thanh toán chưa có trong phiên bản này. Liên hệ cửa hàng để hoàn tất đơn.`; `mantine-Button` `Liên hệ để hoàn tất` → `/contact`. No payment fields (only header search). |
| AC-005 | PASS | `npm test -- --run` 14 files / 49 tests. `CartCheckout.test`: empty state + continue; populated lines/totals/header 3; PATCH 1→3 only `{quantity:3}` then totals 5 / 207.000₫; delete modal; failed-PATCH reset; checkout stub + contact, no payment labels. |

Exploratory:
- AppShell teal `#12b886`, Inter Variable; Mantine `Table`/`Card`/`NumberInput`/`Modal`/`Button`/`Indicator` (not a raw form).
- Guest add-to-cart from detail writes cart; header indicator 0 hidden, then 1, 3, 5, 3 after delete.
- Vite proxy `GET /api/v1/cart` empty 200; `GET /api/v1/shop/settings` 200; `GET /api/v1/products?size=5` `total=18`.
- `/products` still H2 `Sản phẩm` sort `Tên A–Z` (TASK-007). `/contact` reachable from checkout.
- Default `:5432` is unrelated `task-service-pg`; run used throwaway shop PG `:15432`.
- `product/frontend` left clean on `main`; ports 18081 and 15173 free after stop.

Bug (FAIL): n/a
