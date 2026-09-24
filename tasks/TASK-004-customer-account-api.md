---
id: TASK-004
title: Customer account APIs
type: TASK
priority: CRITICAL
status: TESTING
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-001]
sprint:
branch: feature/TASK-004-customer-account-api
merge_commit: ed63e6a
release:
review_iteration: 0
test_iteration: 0
blocked_from:
failed_from:
failure_type:
failure_step:
failure_message:
failure_retry: 0
failure_recoverable:
human_gate: auth
approved_by: HUMAN (os_anhbc)
approved_at: 2026-09-24 10:48
updated: 2026-09-24 11:00
---

## Description

Customer registration, sign-in, sign-out, and current-user using opaque httpOnly session cookies
and BCrypt password hashes. No OAuth. Cart merge is TASK-005.

## Acceptance Criteria
- [ ] AC-001 `POST /api/v1/auth/register` with valid email, password (≥8, ≤72), displayName
      returns 201 `{ id, email, displayName }` and `Set-Cookie: shop_session`; password is BCrypt
      in `users.password_hash` and never appears in the response
- [ ] AC-002 Register with invalid email/short password → 400 ProblemDetail; existing email → 409
- [ ] AC-003 `POST /api/v1/auth/login` with a registered user returns 200 and the session cookie;
      wrong password or unknown email → 401 (same message); `GET /api/v1/auth/me` with cookie → 200
- [ ] AC-004 `POST /api/v1/auth/logout` returns 204 and clears the cookie; subsequent `/auth/me` → 401
- [ ] AC-005 Session token is stored as a hash only; tests cover register, duplicate, bad credentials, me, logout

## Design (SA)
See `docs/design/REQ-001-design.md` §5–§7 (FR-7, FR-8, NFR-3). Repo: shop-service (existing).
- Tables `users`, `sessions`; cookie httpOnly SameSite=Lax; 7-day expiry.
- Opaque token (not JWT). Jakarta Validation on bodies. `human_gate: auth`.
- Do not implement cart merge here.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-004-customer-account-api` @ a7a64d9
- Changed: `services/shop-service/src/main/resources/db/migration/V6__users_sessions.sql`, `api/AuthController.java`, `api/{Register,Login}Request.java`, `api/UserResponse.java`, `api/ApiExceptionHandler.java`, `service/AuthService.java`, `service/{DuplicateEmail,Unauthorized}Exception.java`, `domain/{User,Session}.java`, `repository/{User,Session}Repository.java`, `config/AuthConfig.java`, `pom.xml`, `AuthControllerTest.java`, `AuthServiceTest.java`, `AuthApiTest.java`, `ShopApplicationTests.java`
- Tests: `./mvnw -q verify` in `services/shop-service` → pass (71 tests)
- Notes: Flyway V6 because V1–V5 already used. Email stored trimmed+lowercase. displayName max 80. Login does not merge guest cart (TASK-005). `spring-security-crypto` only (no security filter). Cookie `shop_session` httpOnly SameSite=Lax Path=/ 7 days; token is 64-byte hex, SHA-256 stored. Login 401 detail is `Invalid credentials` for unknown email and wrong password. Branch pushed. `git pull` on shop-service main hung; created branch from already-up-to-date local main.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-004-customer-account-api @ a7a64d9 · Build/tests: ./mvnw -q verify PASS (71 tests)
No comments.

Merged ed63e6a.
Pushed main.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 10:15 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-001] READY_FOR_DEPLOY; waiting approved_by (human_gate: auth) |
| 2026-09-24 10:48 | READY | READY | HUMAN (os_anhbc) | approved auth gate; run remaining REQ-001 tasks |
| 2026-09-24 10:53 | READY | IN_PROGRESS | BE | branch feature/TASK-004-customer-account-api |
| 2026-09-24 10:56 | IN_PROGRESS | CODE_REVIEW | BE | product a7a64d9; Implementation Iteration 1 |
| 2026-09-24 10:59 | CODE_REVIEW | MERGED | SA | reviews/TASK-004-round-1.md APPROVED; merge_commit=ed63e6a --no-ff |
| 2026-09-24 11:00 | MERGED | TESTING | TEST | run 1; tested sha ed63e6a is ancestor of main containing merge_commit ed63e6a |
