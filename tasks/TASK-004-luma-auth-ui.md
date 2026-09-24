---
id: TASK-004
title: Frontend shell and authentication screens
type: TASK
priority: HIGH
status: READY
assignee: FE
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo: frontend
work_type: FRONTEND
requires_uxui: true
uxui_task: TASK-001
uxui_design:
uxui_review:
figma:
depends_on: [TASK-001, TASK-002]
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
approved_by: os_anhbc
approved_at: 2026-09-24 14:53
updated: 2026-09-24 15:08
---

## Description

Create `product/frontend` (`/repo create frontend fe` if missing). Install the §5 kit (Mantine,
Tabler, Inter, TanStack Query, React Router). Implement app shell plus sign-up, sign-in, and
sign-out against `luma-service` session cookies (`credentials: 'include'`). Map TASK-001 tokens
onto `MantineProvider`. Do not invent a second look.

## Acceptance Criteria

- [ ] AC-001 Sign-up with email, password, username calls `POST /api/v1/auth/sign-up`, then lands
      on `/feed`. Duplicate email shows the API `detail`, not a blank or raw dump.
- [ ] AC-002 Sign-in with valid credentials opens `/feed`. Invalid credentials show
      `Invalid email or password.` and stay on `/sign-in`.
- [ ] AC-003 Reload while signed in still shows the member chrome (`GET /api/v1/auth/me`).
      Sign-out calls `POST /api/v1/auth/sign-out` and returns to `/`.
- [ ] AC-004 Routes `/`, `/sign-up`, `/sign-in` use the UX/UI contract (loading, empty, error,
      success). No native unthemed `<input>`/`<button>` as the visible product UI (hidden file
      input exception does not apply here).

## Design (SA)

`docs/design/REQ-001-design.md` §5, §13 routes `/`, `/sign-up`, `/sign-in`. FR-1..FR-3, NFR-6.
`requires_uxui: true`; `depends_on` TASK-001 (UX) and TASK-002 (API). `requirement_revision: 3`,
`content_hash: 54839e9b074480c8`.

## Implementation (BE/FE)

## UX/UI Review

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001; repo frontend; requires_uxui; human_gate=auth; deps TASK-001, TASK-002 |
| 2026-09-24 14:53 | BACKLOG | BACKLOG | HUMAN (os_anhbc) | approved_by set; auth gate for REQ-001 run |
| 2026-09-24 15:08 | BACKLOG | READY | SCRUM | DoR met; deps TASK-001 MERGED, TASK-002 READY_FOR_DEPLOY |
