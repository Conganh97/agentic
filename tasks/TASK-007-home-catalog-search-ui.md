---
id: TASK-007
title: Home, catalog, category and search UI
type: TASK
priority: CRITICAL
status: IN_PROGRESS
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
updated: 2026-09-24 09:57
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

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:55 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002, TASK-006] READY_FOR_DEPLOY |
| 2026-09-24 09:57 | READY | IN_PROGRESS | FE | branch feature/TASK-007-home-catalog-search-ui |
