---
id: TASK-002
title: luma-service members and session
type: TASK
priority: HIGH
status: BACKLOG
assignee: BE
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo: luma-service
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: []
sprint:
branch:
merge_commit:
release:
review_iteration: 0
uxui_review_iteration: 0
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
updated: 2026-09-24 14:44
---

## Description

Create `luma-service` (`/repo create luma-service be` if missing). Implement members and
session-based authentication: sign-up, sign-in, sign-out, `GET /api/v1/auth/me`. Cookie
`LUMA_SESSION` (HttpOnly, SameSite=Lax). CORS for both FE origins. Flyway `members` table.
Package `com.product.luma`. Default port `SERVER_PORT=18081`.

## Acceptance Criteria

- [ ] AC-001 `POST /api/v1/auth/sign-up` with valid email, password (≥8), username creates a
      member, returns 201 without a password field, and sets `LUMA_SESSION`. Duplicate email or
      username returns 409 with a distinct `detail`.
- [ ] AC-002 `POST /api/v1/auth/sign-in` with valid credentials returns 200 + session cookie.
      Unknown email or wrong password returns 401 `Invalid email or password.` and no session.
- [ ] AC-003 `GET /api/v1/auth/me` with the cookie returns the member; after
      `POST /api/v1/auth/sign-out` the cookie is expired and `me` is 401.
- [ ] AC-004 CORS + credentials succeed from `http://localhost:15173` and
      `http://127.0.0.1:15173`. `GET /actuator/health` is 200. Password hashes are BCrypt; passwords
      never appear in JSON.

## Design (SA)

`docs/design/REQ-001-design.md` §5–§7 (stack, auth API, `members`). FR-1, FR-2, FR-3, NFR-1,
NFR-3, NFR-4, NFR-7. `requirement_revision: 3`, `content_hash: 54839e9b074480c8`.

## Implementation (BE/FE)

## UX/UI Review

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001; repo luma-service; human_gate=auth; deps [] |
