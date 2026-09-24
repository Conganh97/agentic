---
task: TASK-010
run: 1
verdict: PASS
tested_sha: f4b6275
merge_commit: f4b6275
updated: 2026-09-24 11:24
---

# TASK-010 Test Run 1

- Tested: `main` @ `f4b6275` (contains `merge_commit` f4b6275)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (40 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Browser `http://localhost:15173/register`: Mantine `AppShell` + `Paper` `max-width: 420px`; H1 `Đăng ký`; `TextInput` Email, `PasswordInput` Mật khẩu (toggle), `TextInput` Tên hiển thị (classes `mantine-TextInput-input` / `mantine-PasswordInput-innerInput`). Empty submit → `Vui lòng nhập email` / `Vui lòng nhập mật khẩu` / `Vui lòng nhập tên hiển thị`. Valid tester010@example.com / password1 / Tester 010 → hooked `POST /api/v1/auth/register` `credentials: include` body `{"email":"tester010@example.com","password":"password1","displayName":"Tester 010"}` → 201 `{"id":"26832e30-da2c-40c9-8e75-ced4b6c522fb","email":"tester010@example.com","displayName":"Tester 010"}`. Header `Tài khoản` → `Tester 010` + `Đăng xuất`. Toast `Đăng ký thành công` / `Xin chào Tester 010`. |
| AC-002 | PASS | `/signin` `Paper maw=420` H1 `Đăng nhập`. Empty submit → `Vui lòng nhập email` / `Vui lòng nhập mật khẩu`. Wrong password → `POST /api/v1/auth/login` `credentials: include` `{"email":"tester010@example.com","password":"wrongpass"}` → 401 `{"detail":"Invalid credentials",...}`; `role=alert` Mantine Alert `Không đăng nhập được` / `Invalid credentials`. RTL `maps login validation errors from ProblemDetail onto fields` maps 400 `must be a well-formed email address` without the 401 alert. Valid login → `POST /api/v1/auth/login` 200 same user JSON; toast `Đăng nhập thành công`. |
| AC-003 | PASS | Signed-out header `nav[aria-label=Tài khoản]` text `Đăng nhập` + `Đăng ký` (Mantine `Button` links `/signin` `/register`), visible at 1280. After register/login: `Tester 010` + `Đăng xuất`. Reload `/` restores session via `GET /api/v1/auth/me` (cookie); header still `Tester 010` + `Đăng xuất`. |
| AC-004 | PASS | Header `Đăng xuất` → hooked `POST /api/v1/auth/logout` `credentials: include` → 204 empty body. Header returns to `Đăng nhập` + `Đăng ký`. |
| AC-005 | PASS | `npm test -- --run` 13 files / 40 tests. `AccountUi.test.tsx`: register mock then signed-in header; 401 Alert + 400 field mapping; sign-out restores guest nav; inputs `className` match `/mantine/i`. Live register/signin: 0 non-Mantine buttons; all form inputs have Mantine classes. |

Exploratory:
- Themed Mantine AppShell (teal `#12b886`, Inter Variable); not a raw HTML form.
- Duplicate register → 409 `Email already registered`; Alert `Không đăng ký được`.
- Home still `Bán chạy` / `Mồi câu cá` / `Phụ kiện đồ câu` / `Tin tức`; product links e.g. `/products/vien-moi-chep-ngot`. API `GET /api/v1/products?size=1` 200 `total=18`. `/actuator/health` 200 UP.
- At 611px the header cluster is in the DOM but clipped; burger `AccountMobileNav` still has the same labels. Not an AC miss.
- Default `:5432` is unrelated `task-service-pg`; run used throwaway shop PG `:15432`.
- `product/frontend` left clean on `main`; ports 18081 and 15173 free after stop.

Bug (FAIL): n/a
