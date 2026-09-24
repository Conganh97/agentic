---
task: TASK-005
run: 1
verdict: PASS
tested_sha: ab07b1702e6d70511ba29bf003513c495dda3213
merge_commit: ab07b1702e6d70511ba29bf003513c495dda3213
updated: 2026-09-24 16:04
---

# TASK-005 Test Run 1

- Tested: `main` @ `ab07b1702e6d70511ba29bf003513c495dda3213` (contains `merge_commit`)
- Build/tests: `cd product/frontend && npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (8 files / 23 tests)
- Runtime: `18081` busy (leftover `shop-service`). luma-service on `SERVER_PORT=18085` against ephemeral `postgres:16-alpine` `luma-task005-pg` `:15437` (`localhost:5432` is `task-service-pg`). `LUMA_MEDIA_DIR=/tmp/luma-task005-media`. FE: `BACKEND_PORT=18085 npm run dev -- --port 15173 --host 0.0.0.0` (leftover Vite on `15173`/`127.0.0.1` stopped so this run could bind both origins). Stopped after the run; container removed. Product trees left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Browser `/feed` 6 seeded `article`s newest-first (noah Neon… → luna Sunrise…); each image 800×800 loaded; caption, author, avatar, `Like, 0 likes` `aria-pressed=false`. Not empty. |
| AC-002 | PASS | Signed-out `/create` → `/sign-in`. luna / `demo-pass-8` publishes HTTPS URL + caption; toast “Shared”; new card first on `/feed` (7 cards). |
| AC-003 | PASS | Like 0→1 `aria-pressed=true` then unlike 1→0; same `performance` navigation entry + in-page marker (no reload). Repeat like on `127.0.0.1`. |
| AC-004 | PASS | `/u/luna` identity + 3-col 630 grid + overlay dialog. `/u/empty005` designed empty. Loading: 9 tile skeletons. 404 + network EmptyStates, not blank. |

## Build

```
cd product/frontend && npm run lint && npm run format:check && npm test -- --run && npm run build
```

Exit 0. oxlint clean; Prettier check clean; Vitest 23 passed; `tsc -b && vite build` wrote `dist/`.

## Health

```
curl -sS -D - http://localhost:18085/actuator/health
```

```
HTTP/1.1 200
Content-Type: application/vnd.spring-boot.actuator.v3+json
{"groups":["liveness","readiness"],"status":"UP"}
```

```
curl -sS http://localhost:18085/api/v1/posts
```

6 seed items newest-first (`Neon after midnight.` / noah … `Sunrise over the ridge.` / luna). Distinct HTTPS `imageUrl`s.

```
curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:15173/
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:15173/
```

`200` / `200`.

## AC-001

Browser `http://localhost:15173/feed` (anonymous). After settle:

- 6 `article` PhotoCards, photo-first dusk column, desktop side nav Home / Create / Profile
- Captions newest-first: Neon after midnight. → Trail after rain. → Window light still life. → Fog on the water. → Blue hour downtown. → Sunrise over the ridge.
- Authors `noah` / `luna` alternating; avatars `i.pravatar.cc` 150×150 complete
- Feed photos `picsum` 800×800 `complete` + `naturalWidth=800` (not one blank/404)
- Hearts `Like, 0 likes` `aria-pressed=false`

## AC-002

Signed-out Create nav: `/create` then `/sign-in` (“Welcome back”).

Sign-in `luna@luma.test` / `demo-pass-8` → `/feed` + Sign out.

`/create`: empty slot “Add a photo”, File / Link, caption “Write a caption…”. Link + `https://picsum.photos/id/237/800/800` + `TASK-005 black-box new post`. CTA `Sharing…` then toast “Shared” and `/feed`.

First card: `luna TASK-005 black-box new post 0`, image 237; 7 articles total.

## AC-003

On `/feed` after create: `window.__likeMarker` set; first heart click → `Like, 1 likes` `aria-pressed=true`; second click → `Like, 0 likes` `aria-pressed=false`. `performance.getEntriesByType('navigation').length` stayed `1`; marker still present (no full reload).

Anonymous heart is specified to route `/sign-in` (not re-run after sign-in).

## AC-004

`/u/luna` (session owner): `h1` luna, avatar, `4 photos`, bio `Film and morning light.`, 3-column `630px` grid `gap 2px` (`208px` squares), tiles load. Tile opens `role="dialog"` with PhotoCard + HeartLike.

`/u/empty005` (`postCount=0`): initials `EM`, `0 photos`, EmptyState title “No photos yet”, body “When empty005 shares, they will show up here.” No Share CTA (viewer ≠ owner). Empty photo frame. Not blank.

Loading (profile API delayed on client nav to `/u/luna`): `data-testid=profile-loading`, **9** `skeleton-tile`, 12 pulses, canvas `#0C0C0E`. Not a spinner-only blank page.

Error: `/u/doesnotexist005` → “This profile doesn’t exist” + Home. Fetch reject on `/u/noah` → “Couldn’t load this profile” / “Check your connection.” / Try again. Not raw 404 JSON.

## Exploratory

- UX contract vs `docs/design/ux/REQ-001-ux.md` (Figma MCP not re-fetched; UX review 1 already APPROVED). Photo-first feed; create File/Link; profile 3-col squares.
- CORS credentialed `POST /api/v1/auth/sign-in` to `18085`:
  - `Origin: http://localhost:15173` → `200` + `Allow-Origin` echo + `Allow-Credentials: true` + `LUMA_SESSION`
  - `Origin: http://127.0.0.1:15173` → same (not 403)
- Browser `http://127.0.0.1:15173/sign-in` as luna → `/feed` 7 cards, all feed images `naturalWidth>0`; like 0→1 (no CORS fail).
- Leftover `shop-service` on `18081` and `luma-review-pg` left untouched.

## Bug (FAIL)

none
