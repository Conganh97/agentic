---
id: TASK-010
title: Account sign-in and register UI
type: TASK
priority: CRITICAL
status: BACKLOG
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-004, TASK-006]
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

Customer register, sign-in, sign-out, and header account cluster. Session cookie via
`credentials: 'include'`. `human_gate: auth`.

## Acceptance Criteria
- [ ] AC-001 `/register` `Paper` form: `TextInput` email, `PasswordInput` password, `TextInput`
      displayName; valid submit calls `POST /api/v1/auth/register` and then shows the signed-in header
- [ ] AC-002 `/signin` form calls `POST /api/v1/auth/login`; 401 shows `Alert` role="alert";
      validation errors map to field messages
- [ ] AC-003 Signed-out header shows “Đăng nhập” and “Đăng ký”; after session, header shows
      `displayName` and “Đăng xuất”
- [ ] AC-004 “Đăng xuất” calls `POST /api/v1/auth/logout` and returns header to the signed-out cluster
- [ ] AC-005 RTL tests: register success mock, 401 on sign-in, sign-out restores guest nav;
      no native inputs

## Design (SA)
See `docs/design/REQ-001-design.md` §13 (FR-7, FR-8, FR-9). Repo: frontend (existing).
- Routes `/signin` and `/register` (not a third-party hosted page).
- Mantine `Paper maw={420}`, `TextInput`, `PasswordInput`, `Button`, `Alert`, `Anchor` between pages.
- `GET /api/v1/auth/me` on app load to restore session. `human_gate: auth`.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
