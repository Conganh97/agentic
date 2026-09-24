---
task: TASK-011
run: 1
verdict: PASS
tested_sha: 580b15c
merge_commit: 580b15c
updated: 2026-09-24 10:40
---

# TASK-011 Test Run 1

- Tested: `main` @ `580b15c` (contains `merge_commit` 580b15c)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (37 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Browser `http://localhost:15173/news`: AppShell H1 `Tin tức`; 3 cards from `GET /api/v1/articles` (proxy 200 `total=3`) — `Chuẩn bị cần câu buổi sớm`, `Bảo quản mồi câu sau khi mở bao`, `Chọn mồi câu chép mùa lạnh` with excerpts. Cards are `link` to `/news/:slug`. Click first card → `/news/chuan-bi-can-cau-buoi-som`. List uses `ThemeIcon` `IconPhoto` (API cards have no `imageUrl`). |
| AC-002 | PASS | `/news/bao-quan-moi-cau-sau-khi-mo-bao` H1 title + `Text` body + `img` `/placeholders/article.svg`; anchors `Bài trước` `/news/chon-moi-cau-chep-mua-lanh`, `Bài sau` `/news/chuan-bi-can-cau-buoi-som`, `Về danh sách tin` `/news`. Newest article has only prev + back. `/news/khong-ton-tai` `role=alert` `Không tìm thấy bài viết` / `Article not found`. No `dangerouslySetInnerHTML`. |
| AC-003 | PASS | Each slug H1 + `P.mantine-Text-root` body, `hasDsih=false`: `/pages/about` `Giới thiệu`; `/pages/shipping` `Chính sách vận chuyển và kiểm hàng`; `/pages/privacy` `Chính sách bảo mật`; `/pages/warranty` `Chính sách bảo hành và đổi trả`; `/pages/terms` `Điều khoản dịch vụ`; `/pages/shopping-guide` `Hướng dẫn mua hàng`. Bodies match `GET /api/v1/pages/{slug}` 200. |
| AC-004 | PASS | `/contact` H1 `Liên hệ`; hotline `tel:0123456789` `0123 456 789`, `mailto:shop@example.com`, Zalo `https://zalo.me/0123456789` from `GET /api/v1/shop/settings` 200. Mantine `TextInput`/`Textarea`/`Button` (no bare native controls). Empty Gửi → `Vui lòng nhập họ tên/email/số điện thoại/nội dung`. Filled An / an@example.com / 0900000001 / Hỏi hàng → `POST /api/v1/contact` 202 `{"accepted":true}`; toast `Đã nhận liên hệ` (does not claim email sent); form cleared. |
| AC-005 | PASS | `npm test -- --run` 12 files / 37 tests. `NewsListPage.test` list + `FOOTER_PATHS`; `ArticleDetailPage.test` title/content/prev-next + missing Alert; `PolicyPage.test` about paragraphs; `ContactPage.test` empty-form validation. Live footer hrefs: `/`, `/pages/about`, `/products`, `/news`, `/contact`, `/pages/shopping-guide`, `/pages/shipping`, `/pages/privacy`, `/pages/warranty`, `/pages/terms`. |

Exploratory:
- AppShell teal `#12b886`, Inter Variable; themed Mantine (not a raw form).
- Home `/` H2 `Tin tức` teaser 3 cards with Badge `TIN TỨC`; catalog still `Bán chạy` / `Mồi câu cá` / `Phụ kiện đồ câu` (17 product links on home).
- `/products` H2 `Sản phẩm`, 18 cards, first A–Z `Bột câu rô phi 36.000₫` (TASK-007).
- `/pages/khong-ton-tai` Alert `Không tìm thấy trang` / `Page not found`.
- Vite proxy `GET /api/v1/articles` and `POST /api/v1/contact` both work.
- Default `:5432` is unrelated `task-service-pg`; run used throwaway shop PG `:15432`.
- `product/frontend` left clean on `main`; ports 18081 and 15173 free after stop.

Bug (FAIL): n/a
