---
task: TASK-013
run: 1
verdict: PASS
tested_sha: 1a1a6f2
merge_commit: 1a1a6f2
updated: 2026-09-24 11:59
---

# TASK-013 Test Run 1

- Tested: `main` @ `1a1a6f2` (contains `merge_commit` 1a1a6f2)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (49 tests); `npx playwright test` PASS (3)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | `package.json` has `"e2e": "playwright test"`. `playwright.config.ts` `webServer` runs `npm run dev -- --host 127.0.0.1 --port 15173 --strictPort` at `http://127.0.0.1:15173` unless `BASE_URL` is set (then webServer is omitted). `e2e/fixtures/shopApi.ts` mocks `/api/v1/*` via `context.route`. `npx playwright test` started Vite (`VITE v8.3.0 ready` on 15173) and finished `3 passed (12.4s)`. README documents `BASE_URL` and that shop-service is not required. |
| AC-002 | PASS | `npx playwright test` → `✓ [chromium] › e2e/browse-detail.spec.ts:8:1 › visits home, opens a product card, and shows the matching detail title (1.3s)`. Spec: `page.goto('/')`, click product card link `Viên mồi chép ngọt`, assert URL `/products/vien-moi-chep-ngot` and `heading` level 2 with that title. |
| AC-003 | PASS | `npx playwright test` → `✓ [chromium] › e2e/cart.spec.ts:8:1 › adds a product and shows cart quantity and a non-zero total (1.6s)`. Spec: add from detail (`Thêm vào giỏ`), `goto('/cart')`, `Tổng số lượng` matches `/[1-9]\d*/`, `Tổng tiền` contains `₫` and is not `0₫`. |
| AC-004 | PASS | `npx playwright test` → `✓ [chromium] › e2e/account.spec.ts:8:1 › registers, signs in, sees the header name, then signs out (10.7s)`. Spec: unique `e2e-${Date.now()}@example.com`, register as `Tester 013`, header shows name, sign out → `Đăng nhập`, sign in, name again, sign out → `Đăng nhập`. |
| AC-005 | PASS | README “E2E (Playwright)” documents `npx playwright test` / `npm run e2e` and `BASE_URL`. Grep of `e2e/` + `playwright.config.ts`: no `test.skip` / `fixme` / `only`. Spec files contain no API keys or tokens; only dummy password `password1` (same as RTL, documented in Implementation). |

Exploratory:
- No `test.skip` / `fixme` / `only` in the e2e suite.
- Playwright `webServer` started and stopped Vite; `nc -z localhost 15173` failed after the run (port free). `18081` unused (API mocked).
- Vite logged `http proxy error` / `ECONNREFUSED` for `/api/v1/categories`, `/cart`, `/auth/me`, `/products…` because shop-service was not running. Specs still passed via `context.route` mocks (AC-001 allows mocked API).
- `product/frontend` `git status --porcelain` empty. `test-results/.last-run.json` exists and is ignored by `/test-results/` in `.gitignore` (not untracked). `rm -rf` to delete it was blocked by guard-shell; left in place as ignored.
- Frontend `main` left clean on `1a1a6f2`.

Bug (FAIL): n/a
