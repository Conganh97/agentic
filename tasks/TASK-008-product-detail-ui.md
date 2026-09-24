---
id: TASK-008
title: Product detail UI
type: TASK
priority: CRITICAL
status: READY
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-002, TASK-006]
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
updated: 2026-09-24 10:15
---

## Description

Product detail page from `GET /api/v1/products/{slug}`: gallery, price, tabs for copy, quantity,
add-to-cart button (POST can land in TASK-009; this task must still render the control and call the
API if `/cart/items` exists, otherwise show the button and keep qty in component state with a
disabled note only if the cart API is absent — prefer depending on mocked fetch). Related products
grid.

## Acceptance Criteria
- [ ] AC-001 `/products/:slug` shows name, price (VND), at least one image, category breadcrumb,
      description, and information; usage section when `usage` is non-empty
- [ ] AC-002 `NumberInput` “Số lượng” is 1–99; `Button` “Thêm vào giỏ” is a Mantine button
- [ ] AC-003 Related products render as cards linking to their slugs when `related` is non-empty
- [ ] AC-004 Unknown slug shows `Alert` (404); loading uses `Skeleton`; add-to-cart success uses
      `notifications.show` when the POST is mocked or available
- [ ] AC-005 RTL tests: renders detail from mock JSON; changing quantity updates the input;
      404 mock shows the alert. No `dangerouslySetInnerHTML`

## Design (SA)
See `docs/design/REQ-001-design.md` §13 (FR-3). Repo: frontend (existing).
- Mantine: `Grid`, `Carousel` or image `SimpleGrid`, `Tabs`, `NumberInput`, `Button`, `Breadcrumbs`,
  `notifications`, related `Card` grid.
- POST `/api/v1/cart/items` with `credentials: 'include'` when implementing the click; if cart
  backend is not merged yet, mock fetch in tests and still implement the client function.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 10:15 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002, TASK-006] READY_FOR_DEPLOY |
