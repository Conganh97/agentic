---
id: TASK-004
title: Customer account APIs
type: TASK
priority: CRITICAL
status: BACKLOG
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-001]
sprint:
branch:
merge_commit:
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
approved_by:
approved_at:
updated: 2026-09-24 09:15
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

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
