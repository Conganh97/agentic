---
task: TASK-008
run: 1
verdict: PASS
tested_sha: 4d7cf8d
merge_commit: 4d7cf8d
updated: 2026-09-24 10:26
---

# TASK-008 Test Run 1

- Tested: `main` @ `4d7cf8d` (contains `merge_commit` 4d7cf8d)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (29 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Browser `http://localhost:15173/products/vien-moi-chep-ngot`: Mantine `AppShell` teal `#12b886` / Inter Variable. Breadcrumb Trang chủ / Sản phẩm / `Câu cá chép` → `/categories/cau-ca-chep` / Viên mồi chép ngọt. H2 `Viên mồi chép ngọt`, price `45.000₫`, ≥1 `img` `/placeholders/product.svg`. Tabs Mô tả `Viên mồi vị ngọt dịu, tan chậm dưới đáy hồ.`; Thông tin `Gói 200g, viên 8mm, hương bắp sữa.`; Hướng dẫn sử dụng `Thả từng viên quanh phao, bổ sung sau 15 phút.` Vite proxy `GET /api/v1/products/vien-moi-chep-ngot` → 200. |
| AC-002 | PASS | `NumberInput` label `Số lượng` class `mantine-NumberInput-input`, value 1 then typed 5. Type `100` clamped to `99`. `Button` `Thêm vào giỏ` class `mantine-Button-root`. |
| AC-003 | PASS | Related heading `Sản phẩm liên quan`; cards `Bột thơm dụ chép 52.000₫` / `Combo hồ chép 89.000₫` / `Hạt ngô ủ chép 38.000₫`. Click first → `/products/bot-thom-du-chep` H2 `Bột thơm dụ chép`. |
| AC-004 | PASS | `/products/khong-ton-tai` `role=alert` `Không tìm thấy sản phẩm` / `Product not found` (API 404). RTL `ProductDetailPage.test` hang → `aria-label` `Đang tải sản phẩm` skeletons; mocked POST → `Đã thêm vào giỏ`. Live click POSTs `/api/v1/cart/items` (TASK-005 not merged) → notification `Không thêm được vào giỏ` / `No static resource api/v1/cart/items.` |
| AC-005 | PASS | `npm test -- --run` 8 files / 29 tests. ProductDetailPage.test: mock JSON name/price/image/breadcrumb/copy/related; qty input 1→3; 404 alert; no `dangerouslySetInnerHTML`. |

Exploratory:
- `/products/hop-phu-kien-nho` (related empty) has no `Sản phẩm liên quan` heading; usage tab still present (all seed products have usage; empty-usage hide covered by RTL).
- `/news` still H2 `Tin tức` inside AppShell (TASK-006). Catalog proxy `GET /api/v1/products?size=5` → 200 `total=18`.
- Default `:5432` is unrelated `task-service-pg`; run used throwaway shop PG `:15432`.
- Live add-to-cart error toast is expected until TASK-005; success path is mocked per design.
- `product/frontend` left clean on `main`; ports 18081 and 15173 free after stop.

Bug (FAIL): n/a
