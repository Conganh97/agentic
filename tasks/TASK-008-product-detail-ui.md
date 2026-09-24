---
id: TASK-008
title: Product detail UI
type: TASK
priority: CRITICAL
status: CODE_REVIEW
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-002, TASK-006]
sprint:
branch: feature/TASK-008-product-detail-ui
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
updated: 2026-09-24 10:19
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
### Iteration 1 (initial)
- Branch: `feature/TASK-008-product-detail-ui` @ 4d73acf
- Changed: `frontend/src/api/{catalog,cart}.ts`, `frontend/src/features/catalog/{ProductDetailPage,useCatalogQueries,catalogFixtures}.*`, `frontend/src/app/router.tsx`
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (29 tests)
- Notes: Gallery is `Paper` + `Image` + thumbnail `SimpleGrid` (no `@mantine/carousel`). Tabs: “Mô tả” / “Thông tin” / “Hướng dẫn sử dụng” (usage tab omitted when empty). Related heading “Sản phẩm liên quan”. Success toast “Đã thêm vào giỏ”. 404 Alert “Không tìm thấy sản phẩm”. `addCartItem` POSTs `/api/v1/cart/items` with `credentials: 'include'`; cart backend not merged (TASK-005), so POST is mocked in tests and still called on click. Copy rendered as `Text` paragraphs (newline split). Branch pushed.

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 10:15 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002, TASK-006] READY_FOR_DEPLOY |
| 2026-09-24 10:17 | READY | IN_PROGRESS | FE | branch feature/TASK-008-product-detail-ui |
| 2026-09-24 10:19 | IN_PROGRESS | CODE_REVIEW | FE | product 4d73acf feat(TASK-008): product detail page with qty and add-to-cart |
