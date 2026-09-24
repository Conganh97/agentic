---
task: TASK-009
round: 1
decision: CHANGES_REQUESTED
branch: feature/TASK-009-cart-checkout-ui
sha: 79a9a63
updated: 2026-09-24 11:32
---

# TASK-009 Review Round 1

Reviewed: `feature/TASK-009-cart-checkout-ui` @ `79a9a63` · Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (48 tests)

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | src/features/cart/CartPage.tsx:83 | MAJOR | `NumberInput` `onChange` clamps empty/NaN to 1 and PATCHes immediately. Editing a line whose quantity is not 1 (clear, then type 3) sends PATCH 1 first. Only PATCH a committed quantity in 1–99 (blur, stepper, or a complete value), not intermediate empty/clamped values. |
| 2 | src/features/cart/CartPage.tsx:151 | MAJOR | `QuantityField` `setValue`s before PATCH. On `mutateAsync` failure the remount key is still `item.quantity` from cache, so the field keeps the failed value while totals stay on the server cart. Reset the input to `item.quantity` when PATCH fails. |
| 3 | src/features/cart/CartCheckout.test.tsx:186 | MAJOR | AC-002 requires on-screen totals to match `totalQuantity` / `totalPriceVnd` after PATCH. The mutation test asserts the fetch and the deleted name, not the updated totals or header indicator. After qty 1→3 on line A, assert totals 5 and 207.000₫ (and header 5). |
