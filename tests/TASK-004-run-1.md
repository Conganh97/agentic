---
task: TASK-004
run: 1
verdict: PASS
tested_sha: 154bf4f19514e9fde423eff32eb900247263e787
merge_commit: 154bf4f19514e9fde423eff32eb900247263e787
updated: 2026-09-24 15:40
---

# TASK-004 Test Run 1

- Tested: `main` @ `154bf4f19514e9fde423eff32eb900247263e787` (contains `merge_commit`)
- Build/tests: `cd product/frontend && npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (5 files / 11 tests)
- Runtime: `18081` busy (leftover `shop-service` from Trash — left running). luma-service on `SERVER_PORT=18084` against ephemeral `postgres:16-alpine` `luma-task004-pg` `:15435` (`localhost:5432` is `task-service-pg`). `LUMA_MEDIA_DIR=/tmp/luma-task004-media`. FE: `BACKEND_PORT=18084 npm run dev -- --port 15173 --host 0.0.0.0` (default Vite `localhost` bind did not accept `127.0.0.1`). Stopped after the run; container removed. Product trees left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Browser `POST /api/v1/auth/sign-up` `tester004a` → `/feed` + member chrome; duplicate email stays on `/sign-up` with API `detail` `Email is already taken.` |
| AC-002 | PASS | Invalid stay on `/sign-in` `role=alert` `Invalid email or password.`; valid `tester004a` → `/feed`. Same valid path on `http://127.0.0.1:15173` as `luna` / `demo-pass-8` |
| AC-003 | PASS | Reload `/` while signed in redirects to `/feed` with Sign out / Home / Create / Profile. Sign out → `/` splash. Repeat reload on `127.0.0.1` still shows Sign out after `GET /me` |
| AC-004 | PASS | UX contract on `/` `/sign-up` `/sign-in` (loading / empty / error / success). No native unthemed inputs. CORS + session from both origins |

## Build

```
cd product/frontend && npm run lint && npm run format:check && npm test -- --run && npm run build
```

Exit 0. oxlint clean; Prettier check clean; Vitest 11 passed; `tsc -b && vite build` wrote `dist/`.

## Health

```
curl -sS -D - http://localhost:18084/actuator/health
```

```
HTTP/1.1 200
Content-Type: application/vnd.spring-boot.actuator.v3+json
{"groups":["liveness","readiness"],"status":"UP"}
```

```
curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:15173/
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:15173/
curl -sS -o /dev/null -w '%{http_code} %{content_type}\n' http://localhost:15173/entry-atmosphere.svg
```

`200` / `200` / `200 image/svg+xml`.

## AC-001

Browser `http://localhost:15173/sign-up` (themed AuthPanel: gold wordmark, “Create your account”, 48px raised fields, pill “Join Luma”).

Submit username `tester004a` / email `tester004a@example.com` / password `testpass8`:

- Loading: fields disabled, CTA `Joining…`
- Success: URL `http://localhost:15173/feed`, side nav Home / Create / Profile, Sign out, empty feed copy “Nothing here yet” (feed cards are TASK-005)

Sign out, then sign-up again with username `tester004b` and the same email:

- Stayed on `/sign-up`
- Email field `invalid`, copy `Email is already taken.` (API `detail`, not a blank or raw JSON dump)

## AC-002

Browser `http://localhost:15173/sign-in` (“Welcome back”, demo hint `demo-pass-8`).

Invalid `nobody@example.com` / `wrongpass`:

- Loading: fields disabled, CTA `Signing in…`
- Stayed on `/sign-in`
- `role="alert"` `Invalid email or password.`

Valid `tester004a@example.com` / `testpass8` → `/feed` + member chrome.

`http://127.0.0.1:15173/sign-in` as `luna@luma.test` / `demo-pass-8` → `/feed` (session cookie via Vite proxy; no CORS 403).

## AC-003

While signed in on `localhost`, navigate `/` → pulse wordmark skeleton → hard redirect `/feed` with Sign out still present (`GET /api/v1/auth/me`).

Sign out: button disabled while pending, then URL `http://localhost:15173/` splash (“Photos, in their own light.”, Create account, Sign in).

Reload `/feed` on `127.0.0.1` after luna sign-in: Sign out returns after `me` settles.

## AC-004

Compared running UI to `docs/design/ux/REQ-001-ux.md` (Figma MCP not re-fetched; UX review 2 already APPROVED).

| Route | Loading | Empty | Error | Success |
|-------|---------|-------|-------|---------|
| `/` | Full-canvas pulse wordmark while `me` in flight | Signed-out splash + atmosphere slot + grain + two pill CTAs | Backend down: stay on splash, `Couldn’t check session.`, CTAs still there | Signed-out splash; signed-in → `/feed` |
| `/sign-up` | `Joining…` + disabled fields | Pristine form, username/password hints | 409 `Email is already taken.` under email | Redirect `/feed` |
| `/sign-in` | `Signing in…` + disabled fields | Pristine form + demo caption | 401 fixed copy; network `Couldn’t reach Luma. Try again.` | Redirect `/feed` |

CDP on `/sign-in` and `/feed`: every visible `input`/`button` has a `mantine-*` class; `nativeVisible: []`.

OPTIONS + credentialed `POST /api/v1/auth/sign-in` to `18084`:

- `Origin: http://localhost:15173` → `200` `Access-Control-Allow-Origin: http://localhost:15173` + `Allow-Credentials: true` + `LUMA_SESSION` + luna member JSON
- `Origin: http://127.0.0.1:15173` → same with origin echoed (not 403)

## Exploratory

- Leftover Trash Vite on `15173` and `shop-service` on `18081` were occupying the usual ports; only the Trash Vite was stopped so this run could bind `15173`. shop-service left untouched.
- Vite default host did not accept `127.0.0.1`; `--host 0.0.0.0` used for the dual-origin check. Not a product AC miss.
- Feed empty state is expected on TASK-004 (no feed cards yet).

## Bug (FAIL)

none
