---
id: TASK-007
title: Home, catalog, category and search UI
type: TASK
priority: CRITICAL
status: CODE_REVIEW
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-002, TASK-006]
sprint:
branch: feature/TASK-007-home-catalog-search-ui
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
updated: 2026-09-24 10:01
---

## Description

Wire header nav to the category tree; implement home sections, all-products, category listing, and
keyword search using TASK-002 APIs. Responsive card grids.

## Acceptance Criteria
- [ ] AC-001 `/` loads header, category nav, a featured product section, bait and gear sections
      (or equivalent category sections), and footer; product `Card` shows name, image, price
- [ ] AC-002 `/products` and `/categories/:slug` list products from the API; sort `Select` and
      `Pagination` change the query; opening a card goes to `/products/:slug`
- [ ] AC-003 Header search submits to `/search?q=`; matching products render; `q` with zero
      results shows the design §13 empty state (icon + “Không tìm thấy sản phẩm”)
- [ ] AC-004 Loading uses `Skeleton` cards; API failure shows `Alert` role="alert"; layout is
      4/3/2 columns at md/sm/base
- [ ] AC-005 RTL tests cover home render of a mocked featured list, category list, and empty search

## Design (SA)
See `docs/design/REQ-001-design.md` §13 (FR-1, FR-2, FR-4, FR-14). Repo: frontend (existing).
- Mantine: `Card`, `Image`, `SimpleGrid`, `Select`, `Pagination`, `Skeleton`, `Alert`, `Breadcrumbs`,
  `Menu`/`HoverCard` for category tree, `TextInput` search overlay or `/search`.
- TanStack Query keys `['categories']`, `['products', params]`.
- Hero placeholders allowed; no copyrighted banners.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-007-home-catalog-search-ui` @ ddc0147
- Changed: `frontend/src/api/catalog.ts`, `frontend/src/features/catalog/*`, `frontend/src/components/{AppShellLayout,CategoryNav,HeaderSearch}.tsx`, `frontend/src/app/router.tsx`, `frontend/src/test/{render,setup}.tsx`, `frontend/public/placeholders/product.svg`
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (23 tests)
- Notes: header `TextInput` + submit “Tìm” goes to `/search?q=` (not a popover). Hero/trust copy: “Mồi câu cho mọi mặt nước”, “Phụ kiện đủ bộ cho buổi câu”, “Giao nhanh nội thành”; “Tư vấn chọn mồi”, “Đổi trả 7 ngày”, “Giao toàn quốc”, “Giá niêm yết rõ”. Parent category slugs have no products (TASK-002); home bait/gear sections filter `GET /products?size=24` by child slugs and omit featured ids. Home makes 3 catalog GETs (categories, featured, all) — ProductCard has no `featured` flag so NFR-2 ≤2 cannot hold without dropping a section. Empty search: `IconSearchOff` + “Không tìm thấy sản phẩm”. `/products/:slug` stays TASK-008 placeholder. Branch pushed.

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:55 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002, TASK-006] READY_FOR_DEPLOY |
| 2026-09-24 09:57 | READY | IN_PROGRESS | FE | branch feature/TASK-007-home-catalog-search-ui |
| 2026-09-24 10:01 | IN_PROGRESS | CODE_REVIEW | FE | product ddc0147; Iteration 1; 23 tests pass |
