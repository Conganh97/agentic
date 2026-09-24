---
task: TASK-002
run: 1
verdict: PASS
tested_sha: b110ab945924d95a525c6ae5ce652ab8ff8aa17a
merge_commit: b110ab945924d95a525c6ae5ce652ab8ff8aa17a
updated: 2026-09-24 15:07
---

# TASK-002 Test Run 1

- Tested: `main` @ `b110ab945924d95a525c6ae5ce652ab8ff8aa17a` (contains `merge_commit`)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (Testcontainers PostgreSQL)
- Runtime: `18081` busy (`nc -z`); service on `SERVER_PORT=18082` against ephemeral `postgres:16-alpine` `luma-task002-pg` `:15433` (`localhost:5432` is `task-service-pg`). Stopped after the run; container removed. Product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | sign-up 201 + `LUMA_SESSION` HttpOnly SameSite=Lax, no password in JSON; duplicate email/username 409 with distinct `detail` |
| AC-002 | PASS | sign-in 200 + cookie; unknown email and wrong password 401 `Invalid email or password.` and empty cookie jars |
| AC-003 | PASS | `GET /me` 200 member; sign-out 204 expires cookie (`Max-Age=0`); later `me` 401 |
| AC-004 | PASS | OPTIONS + credentialed POST from both origins; health 200 `UP`; hashes `$2a$10$` / 60 chars; no password in JSON |

## Build

```
export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home
cd product/services/luma-service && ./mvnw -q verify
```

Exit 0. AuthControllerTest + AuthApiTest started; Testcontainers `postgres:16-alpine`; Flyway `V1 - members`.

## Health

```
curl -sS -D - http://localhost:18082/actuator/health
```

```
HTTP/1.1 200
Content-Type: application/vnd.spring-boot.actuator.v3+json
{"groups":["liveness","readiness"],"status":"UP"}
```

## AC-001

```
curl -sS -D - -c $COOKIE_A -X POST http://localhost:18082/api/v1/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{"email":"tester002.1790237211@example.com","password":"testpass8","username":"tester0021790237211"}'
```

```
HTTP/1.1 201
Set-Cookie: LUMA_SESSION=25B6821145E63306D511C7EE3A1F5882; Path=/; HttpOnly; SameSite=Lax
Set-Cookie: LUMA_SESSION=25B6821145E63306D511C7EE3A1F5882; Path=/; HttpOnly; SameSite=Lax
{"id":"77f10b10-e0bf-49cb-9d20-b49d467673ee","email":"tester002.1790237211@example.com","username":"tester0021790237211","avatarUrl":null,"bio":null}
```

No `password` field. Duplicate email → `409` `{"detail":"Email is already taken.","type":"urn:luma:problem:email_taken",...}`. Duplicate username → `409` `{"detail":"Username is already taken.","type":"urn:luma:problem:username_taken",...}`.

## AC-002

```
curl -sS -D - -c $COOKIE_B -X POST http://localhost:18082/api/v1/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{"email":"tester002.1790237211@example.com","password":"testpass8"}'
```

```
HTTP/1.1 200
Set-Cookie: LUMA_SESSION=76A4BE4EE6600D4DB6034E2AC06A794C; Path=/; HttpOnly; SameSite=Lax
{"id":"77f10b10-e0bf-49cb-9d20-b49d467673ee","email":"tester002.1790237211@example.com","username":"tester0021790237211","avatarUrl":null,"bio":null}
```

Unknown email / wrong password:

```
HTTP/1.1 401
{"detail":"Invalid email or password.","instance":"/api/v1/auth/sign-in","status":401,"title":"Unauthorized","type":"urn:luma:problem:invalid_credentials"}
```

Cookie jars for both 401s empty (no `LUMA_SESSION`).

## AC-003

```
curl -sS -D - -b $COOKIE_B http://localhost:18082/api/v1/auth/me
```

```
HTTP/1.1 200
{"id":"77f10b10-e0bf-49cb-9d20-b49d467673ee","email":"tester002.1790237211@example.com","username":"tester0021790237211","avatarUrl":null,"bio":null}
```

```
curl -sS -D - -b $COOKIE_B -c $COOKIE_B -X POST http://localhost:18082/api/v1/auth/sign-out
```

```
HTTP/1.1 204
Set-Cookie: LUMA_SESSION=; Path=/; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; SameSite=Lax
```

```
curl -sS -D - -b $COOKIE_B http://localhost:18082/api/v1/auth/me
```

```
HTTP/1.1 401
{"type":"about:blank","title":"Unauthorized","status":401,"detail":"Authentication required."}
```

## AC-004

OPTIONS `POST /api/v1/auth/sign-in` from `http://localhost:15173` → `200` `Access-Control-Allow-Origin: http://localhost:15173` + `Access-Control-Allow-Credentials: true`. Same from `http://127.0.0.1:15173` (origin echoed).

Credentialed `POST /sign-up` with `Origin: http://localhost:15173` → `201` + ACAO + credentials + `LUMA_SESSION`. Credentialed `POST /sign-in` with `Origin: http://127.0.0.1:15173` → `200` + ACAO + credentials + `LUMA_SESSION`.

```
docker exec luma-task002-pg psql -U luma -d luma \
  -c "SELECT username, left(password_hash,7) AS hash_prefix, length(password_hash) FROM members;"
```

```
 tester0021790237211  | $2a$10$     |     60
 tester002b1790237211 | $2a$10$     |     60
```

Member JSON never included a password field.

## Exploratory

- Password `short` (len 5) → `400` `urn:luma:problem:validation` `Validation failed.`
- `GET /me` without cookie → `401` `Authentication required.`
- OPTIONS from `http://evil.example` → `403` (allowlist held)

## Bug (FAIL)

none
