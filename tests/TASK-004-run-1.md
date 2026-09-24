---
task: TASK-004
run: 1
verdict: PASS
tested_sha: ed63e6a
merge_commit: ed63e6a
updated: 2026-09-24 11:03
---

# TASK-004 Test Run 1

- Tested: `main` @ `ed63e6a` (contains `merge_commit` ed63e6a)
- Build/tests: `./mvnw -q verify` PASS (71 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | `POST http://localhost:18081/api/v1/auth/register` `{"email":"An@Example.com","password":"password1","displayName":"Tester An"}` → 201 `{"id":"9e1c5141-3504-4213-a8cc-11b996db5d7a","email":"an@example.com","displayName":"Tester An"}` (no `password` / `passwordHash`). `Set-Cookie: shop_session=…` HttpOnly SameSite=Lax Path=/ Max-Age=604800 (128-hex token). DB `users.password_hash` prefix `$2a$10$` len 60, does not contain `password1`. |
| AC-002 | PASS | Invalid email `not-an-email` → 400 `Content-Type: application/problem+json` `{"detail":"Invalid request content.","status":400,"title":"Bad Request"}`. Short password `short` → 400 same ProblemDetail. Duplicate `an@example.com` → 409 `{"detail":"Email already registered","status":409,"title":"Conflict"}`. |
| AC-003 | PASS | `POST /api/v1/auth/login` valid → 200 same user JSON + `Set-Cookie: shop_session` HttpOnly SameSite=Lax. Unknown email and wrong password both 401 identical body `{"detail":"Invalid credentials","instance":"/api/v1/auth/login","status":401,"title":"Unauthorized"}`. `GET /api/v1/auth/me` with login cookie → 200 `{id,email,displayName}`. |
| AC-004 | PASS | `POST /api/v1/auth/logout` with cookie → 204 `Set-Cookie: shop_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax`. Subsequent `GET /auth/me` with prior cookie → 401 `{"detail":"Unauthorized","status":401}`. |
| AC-005 | PASS | `sessions.token_hash` is 64-hex SHA-256 of the raw cookie and ≠ raw 128-hex token. `./mvnw -q verify` AuthApiTest `registerLoginMeLogoutAndRejectsDuplicatesAndBadCredentials`; AuthControllerTest register/duplicate/bad-credentials/me/logout; AuthServiceTest register hash, duplicate, bad credentials, me, logout. |

Exploratory:
- Password len 7 → 400; 8 → 201; 72 → 201; 73 → 400. displayName 81 → 400. `{}` register and empty login password → 400 ProblemDetail.
- `GET /auth/me` without cookie → 401 `Unauthorized`.
- TASK-002/003 regression: `/api/v1/categories` 200 two parents (7+5 children); `/api/v1/products?size=5` 200 `total=18`; `/api/v1/articles` 200 `total=3`.
- TASK-001: `/actuator/health` 200 UP; `/api/v1/does-not-exist` 404 ProblemDetail, no stack.
- Flyway V1–V6 applied (`V6__users_sessions.sql`). App log has no plaintext `password1`.
- shop-service left clean on `main`; port 18081 free after stop. Throwaway PG `:15432` removed (`:5432` is unrelated `task-service-pg`).

Bug (FAIL): n/a
