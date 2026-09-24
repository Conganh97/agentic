---
task: TASK-006
run: 1
verdict: PASS
tested_sha: cb0c07f
merge_commit: cb0c07f
updated: 2026-09-24 09:39
---

# TASK-006 Test Run 1

- Tested: `main` @ `cb0c07f` (contains `merge_commit` cb0c07f)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (18 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | `python3 scripts/repo.py status` → `frontend main clean` at `product/frontend`. Did not re-run `create` (already registered). `BACKEND_PORT=18081 npm run dev -- --port 15173 --strictPort` with mock on :18081 → Vite `Local: http://localhost:15173/`. `curl -s -w '\nHTTP %{http_code}' http://localhost:15173/api/shop/settings` → 200 `{"proxied": true, "path": "/api/shop/settings", "via": "mock-18081"}` (Vite proxy, `server: BaseHTTP/0.6`). |
| AC-002 | PASS | Browser `http://localhost:15173/`: `mantine-AppShell-header` + `mantine-AppShell-main`; `--mantine-color-teal-filled` `#12b886`; `font-family: "Inter Variable", Inter, system-ui, sans-serif`; Notifications host present. Header shop name `Mồi Câu Shop`; mobile `Burger` aria-label `Mở menu`; `ActionIcon` links `Tìm kiếm` → `/search`, `Giỏ hàng` → `/cart`. Desktop: nav Trang chủ / Sản phẩm / Tin tức / Liên hệ; hotline `Hotline 0123 456 789 · Miễn phí vận chuyển từ 200.000₫`. Footer columns Liên kết / Hướng dẫn / Hỗ trợ. |
| AC-003 | PASS | Browser routes inside shell (header + footer persist). `/` H1 `Mồi Câu Shop`; `/products` H2 `Sản phẩm`; `/categories/moi-cau` H2 `Danh mục: moi-cau`; `/products/luoi-cau` H2 `Sản phẩm: luoi-cau`; `/search` H2 `Tìm kiếm`; `/cart` H2 `Giỏ hàng`; `/checkout` H2 `Thanh toán`; `/signin` H2 `Đăng nhập`; `/register` H2 `Đăng ký`; `/news` H2 `Tin tức`; `/news/mo-mua` H2 `Tin tức: mo-mua`; `/pages/about` H2 `Trang: about`; `/contact` H2 `Liên hệ`. Search and cart header clicks landed on `/search` and `/cart`. |
| AC-004 | PASS | `src/api/client.ts` `apiUrl` builds `/api…` (`VITE_API_BASE_URL ?? ''`); Vitest `request('/shop/settings')` calls `fetch('/api/shop/settings')`; 404 ProblemDetail throws `ApiError` status 404 title `Not Found`. `rg` of `src/` found no `<input>`/`<button>`/`<textarea>`/`<select>`. Rendered DOM: 0 native inputs; only button is Mantine `Burger` (`mantine-Burger-root`). |
| AC-005 | PASS | `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS. Vitest 3 files, 18 tests. `AppShellLayout.test.tsx` `renders the shop name in the shell` asserts `getAllByText(SHOP_NAME)`. |

Exploratory:
- Mobile burger visible below `sm`; desktop hides burger and shows nav + hotline row.
- `/no-such-route` keeps AppShell, empty main (no catch-all). Not an AC; no BUG.
- Unknown slugs still render placeholder titles (`Danh mục: moi-cau` etc.).
- `product/frontend` left clean on `main`; ports 18081 and 15173 free after stop.

Bug (FAIL): n/a
