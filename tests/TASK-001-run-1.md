---
task: TASK-001
run: 1
verdict: PASS
tested_sha: 48801b6
merge_commit: 48801b6
updated: 2026-09-24 09:34
---

# TASK-001 Test Run 1

- Tested: `main` @ `48801b6` (contains `merge_commit` 48801b6)
- Build/tests: `./mvnw -q verify` PASS (6 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | `python3 scripts/repo.py status` → `shop-service main clean` at `product/services/shop-service`. Did not re-run `create` (already registered). `SERVER_PORT=18081 ./mvnw spring-boot:run` with shop PostgreSQL on localhost:15432 → process listening, `/actuator/health` UP. |
| AC-002 | PASS | `curl -s -w '\n%{http_code}' http://localhost:18081/actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}` |
| AC-003 | PASS | Startup: Flyway applied `V1__baseline` (`Migrating schema "public" to version "1 - baseline"`). `flyway_schema_history`: version=1, script=`V1__baseline.sql`, success=t. `application.yml`: `ddl-auto: validate`, `flyway.enabled: true`. |
| AC-004 | PASS | `curl -s -D - http://localhost:18081/api/v1/does-not-exist` → 404 `Content-Type: application/problem+json` body `{"detail":"No static resource api/v1/does-not-exist.","instance":"/api/v1/does-not-exist","status":404,"title":"Not Found"}`. No `trace` / stack / `at com.product`. |
| AC-005 | PASS | `cd product/services/shop-service && ./mvnw -q verify` PASS (ShopApplicationTests 3, ApiExceptionHandlerTest 2, CorsConfigTest 1). |

Exploratory:
- OPTIONS `/api/v1/does-not-exist` Origin `http://localhost:15173` → 200 `Access-Control-Allow-Origin: http://localhost:15173`, `Allow-Credentials: true`.
- OPTIONS same path Origin `http://evil.example` → 403, no allow-origin.
- POST `/actuator/health` → 405 ProblemDetail (`Method 'POST' is not supported.`).
- GET `/actuator/env` → 404 (endpoint not exposed).
- GET `/` → 404 ProblemDetail, no stack trace.

Bug (FAIL): n/a
