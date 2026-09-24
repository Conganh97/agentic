---
task: TASK-007
run: 1
verdict: PASS
tested_sha: 4aa99e5
merge_commit: 4aa99e5
updated: 2026-09-24 10:14
---

# TASK-007 Test Run 1

- Tested: `main` @ `4aa99e5` (contains `merge_commit` 4aa99e5)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (23 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Browser `http://localhost:15173/`: Mantine `AppShell` header + main; teal `#12b886`; Inter Variable. Header shop name, `Sản phẩm` HoverCard (collapsed), search `Tìm`, cart. H1 `Mồi Câu Shop`. Heroes + trust copy. H2 `Bán chạy`, `Mồi câu cá`, `Phụ kiện đồ câu`. Cards e.g. `Viên mồi chép ngọt 45.000₫` → `/products/vien-moi-chep-ngot` with `img` `loading=lazy` `/placeholders/product.svg`. Footer Liên kết / Hướng dẫn / Hỗ trợ. |
| AC-002 | PASS | `/products` H2 `Sản phẩm`, 18 API cards (A–Z first `Bột câu rô phi`). Sort `Select` → `Giá giảm` URL `/products?sort=price-desc`, first card `Cần máy hồ 345.000₫`. Pagination present (`aria-label` Phân trang, page 1 current; next/prev disabled — seed `total=18` `size=24`). Card click → `/products/can-may-ho` H2 `Sản phẩm: can-may-ho`. `/categories/cau-ca-chep` H2 `Câu cá chép`, 4 cards (chép bait). RTL CatalogPage.test page=2 with mocked `total=48`. |
| AC-003 | PASS | Header type `chép` + `Tìm` → `/search?q=ch%C3%A9p` H2 `Tìm kiếm`, 4 match cards. `/search?q=xyzzy` H4 `Không tìm thấy sản phẩm` + `Về trang sản phẩm` → `/products`. Vite proxy `GET /api/v1/products?q=chép` → 200 `total=4`. |
| AC-004 | PASS | RTL HomePage.test: hang → `Đang tải sản phẩm` skeletons; fail → `role=alert` `Catalog down`. Live `/categories/khong-ton-tai` → two `role=alert` `Không tải được dữ liệu Category not found`. Grid `--sg-cols`: 1280→4, 768→3, 375→2. |
| AC-005 | PASS | `npm test -- --run` 6 files / 23 tests. HomePage.test mocked featured + bait/gear; CatalogPage.test category list + sort/page; SearchPage.test empty `Không tìm thấy sản phẩm`. |

Exploratory:
- Parent `/categories/moi-cau-ca` empty copy `Chưa có sản phẩm trong danh mục này` + child category links (TASK-002 exact-slug).
- `/news` still H2 `Tin tức` inside AppShell (TASK-006).
- Default `:5432` is unrelated `task-service-pg`; run used throwaway shop PG `:15432`.
- SA MINOR: `CategoryNav` still imports `features/catalog`; bait/gear use `categories.data[0]/[1]` (live order matched parents); header search label visible. Not AC fails.
- `product/frontend` left clean on `main`; ports 18081 and 15173 free after stop.

Bug (FAIL): n/a
