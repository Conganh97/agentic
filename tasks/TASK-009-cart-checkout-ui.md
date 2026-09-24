---
id: TASK-009
title: Cart and checkout UI
type: TASK
priority: CRITICAL
status: IN_PROGRESS
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
updated: 2026-09-24 11:27
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

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 11:25 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-005, TASK-006] READY_FOR_DEPLOY |
| 2026-09-24 11:27 | READY | IN_PROGRESS | FE | Started on feature/TASK-009-cart-checkout-ui |
