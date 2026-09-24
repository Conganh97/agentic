---
task: TASK-003
run: 1
verdict: PASS
tested_sha: 9113e93db114032c2f90383a76af872709af33f3
merge_commit: 9113e93db114032c2f90383a76af872709af33f3
updated: 2026-09-24 15:25
---

# TASK-003 Test Run 1

- Tested: `main` @ `9113e93db114032c2f90383a76af872709af33f3` (contains `merge_commit`)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (Testcontainers PostgreSQL; Flyway V1+V2+seed)
- Runtime: `18081` busy (`nc -z`); service on `SERVER_PORT=18083` against ephemeral `postgres:16-alpine` `luma-task003-pg` `:15434` (`localhost:5432` is `task-service-pg`). `LUMA_MEDIA_DIR=/tmp/luma-task003-media`. Stopped after the run; container removed. Product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | anonymous `GET /api/v1/posts` 200, 6 items newest-first, all `PostCard` fields, `likedByMe=false`, 6 distinct HTTPS `imageUrl`s |
| AC-002 | PASS | signed-in create 201 and first in feed; no session 401; `http://` / bad MIME / file > 8 MiB each 400 |
| AC-003 | PASS | PUT `likeCount` 0→1 `likedByMe=true`; second PUT stays 1; DELETE 1→0 `likedByMe=false`; no session 401 |
| AC-004 | PASS | `GET /profiles/luna` + `/posts`; unknown username 404; `empty003` `postCount=0` and `items:[]` 200 |

## Build

```
export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home
cd product/services/luma-service && ./mvnw -q verify
```

Exit 0. PostApiTest + AuthApiTest + controller tests; Testcontainers `postgres:16-alpine`; Flyway `V1 - members`, `V2 - posts likes media`, `R__seed_demo`.

## Health

```
curl -sS -D - http://localhost:18083/actuator/health
```

```
HTTP/1.1 200
Content-Type: application/vnd.spring-boot.actuator.v3+json
{"groups":["liveness","readiness"],"status":"UP"}
```

## AC-001

```
curl -sS -D - http://localhost:18083/api/v1/posts
```

```
HTTP/1.1 200
{"items":[{"id":"bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb6","caption":"Neon after midnight.","imageUrl":"https://picsum.photos/id/1043/800/800","createdAt":"2026-01-02T13:00:00Z","author":{"username":"noah","avatarUrl":"https://i.pravatar.cc/150?u=noah"},"likeCount":0,"likedByMe":false}, … 5 more], "nextBefore":null}
```

6 items, newest-first (`bbb6` 13:00Z … `bbb1` 08:00Z). Every card has `imageUrl`, `caption`, `author.username`, `author.avatarUrl`, `likeCount`, `likedByMe`. All `likedByMe=false` without a session. Six distinct HTTPS image URLs. GET of two seed URLs returned `200 image/jpeg` (picsum HEAD is 405; not a product miss).

## AC-002

```
curl -sS -c $COOKIE -X POST http://localhost:18083/api/v1/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{"email":"luna@luma.test","password":"demo-pass-8"}'
```

```
HTTP/1.1 200
Set-Cookie: LUMA_SESSION=…; Path=/; HttpOnly; SameSite=Lax
{"id":"aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1","email":"luna@luma.test","username":"luna","avatarUrl":"https://i.pravatar.cc/150?u=luna","bio":"Film and morning light."}
```

```
curl -sS -b $COOKIE -c $COOKIE -X POST http://localhost:18083/api/v1/posts \
  -F "caption=TEST-003 black-box new post" \
  -F "imageUrl=https://picsum.photos/id/237/800/800"
```

```
HTTP/1.1 201
{"id":"2fda7556-d87e-42ae-be20-2144ddd7c2be","caption":"TEST-003 black-box new post","imageUrl":"https://picsum.photos/id/237/800/800",…,"author":{"username":"luna",…},"likeCount":0,"likedByMe":false}
```

That id was first in the next `GET /api/v1/posts` (7 items).

No session:

```
HTTP/1.1 401
{"type":"about:blank","title":"Unauthorized","status":401,"detail":"Authentication required."}
```

`imageUrl=http://example.com/x.jpg` → `400` `{"detail":"Image URL must be https.","type":"urn:luma:problem:invalid_post"}`.

`image` `text/plain` → `400` `{"detail":"Image must be image/jpeg, image/png, or image/webp."}`.

`image` > 8 MiB `image/jpeg` → `400` `{"detail":"Image file must be 8 MiB or smaller."}`.

## AC-003

Target seed post `bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb6` (`likeCount` 0, `likedByMe` false).

```
curl -sS -b $COOKIE -c $COOKIE -X PUT http://localhost:18083/api/v1/posts/{id}/likes
```

```
HTTP/1.1 200
{"likeCount":1,"likedByMe":true}
```

Second PUT: `200 {"likeCount":1,"likedByMe":true}` (no increment). GET post confirms `likeCount=1`, `likedByMe=true`.

```
curl -sS -b $COOKIE -c $COOKIE -X DELETE http://localhost:18083/api/v1/posts/{id}/likes
```

```
HTTP/1.1 200
{"likeCount":0,"likedByMe":false}
```

No session PUT and DELETE → `401` `Authentication required.`

## AC-004

```
curl -sS http://localhost:18083/api/v1/profiles/luna
```

```
HTTP/1.1 200
{"username":"luna","avatarUrl":"https://i.pravatar.cc/150?u=luna","bio":"Film and morning light.","postCount":4}
```

`GET /api/v1/profiles/luna/posts` → `200`, 4 items, all `author.username=luna`, newest first (created test post then seed).

```
curl -sS http://localhost:18083/api/v1/profiles/doesnotexist999
```

```
HTTP/1.1 404
{"detail":"Profile not found.","type":"urn:luma:problem:not_found",…}
```

Signed up `empty003` (no posts). `GET /profiles/empty003` → `200 {"username":"empty003","avatarUrl":null,"bio":null,"postCount":0}`. `GET .../posts` → `200 {"items":[],"nextBefore":null}` (not 404).

## Exploratory

- `noah@luma.test` / `demo-pass-8` sign-in → 200 member `noah`.
- Empty caption → `400` `Caption must be 1 to 2200 characters.`
- File XOR URL both sent → `400` `Provide either an image file or an imageUrl, not both.`
- Valid `image/jpeg` upload → `201` `imageUrl=/api/v1/media/{id}`; GET media `200 image/jpeg` 138 bytes `\xff\xd8\xff\xe0`.
- Like unknown post id → `404` `Post not found.`
- OPTIONS `POST /api/v1/posts` from `http://localhost:15173` and `http://127.0.0.1:15173` → `200` ACAO echoed + `Access-Control-Allow-Credentials: true`.
- Auth regression: `GET /api/v1/auth/me` with session → 200 luna (no password field).
- Session cookie is rewritten on some requests; callers must keep the jar updated (`-c` + `-b`). Not an AC miss.

## Bug (FAIL)

none
