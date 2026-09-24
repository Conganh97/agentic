---
id: TASK-010
title: Account sign-in and register UI
type: TASK
priority: CRITICAL
status: READY_FOR_DEPLOY
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-004, TASK-006]
sprint:
branch: feature/TASK-010-account-ui
merge_commit: f4b6275
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
updated: 2026-09-24 11:24
---

## Description

Customer register, sign-in, sign-out, and header account cluster. Session cookie via
`credentials: 'include'`. `human_gate: auth`.

## Acceptance Criteria
- [x] AC-001 `/register` `Paper` form: `TextInput` email, `PasswordInput` password, `TextInput`
      displayName; valid submit calls `POST /api/v1/auth/register` and then shows the signed-in header
- [x] AC-002 `/signin` form calls `POST /api/v1/auth/login`; 401 shows `Alert` role="alert";
      validation errors map to field messages
- [x] AC-003 Signed-out header shows “Đăng nhập” and “Đăng ký”; after session, header shows
      `displayName` and “Đăng xuất”
- [x] AC-004 “Đăng xuất” calls `POST /api/v1/auth/logout` and returns header to the signed-out cluster
- [x] AC-005 RTL tests: register success mock, 401 on sign-in, sign-out restores guest nav;
      no native inputs

## Design (SA)
See `docs/design/REQ-001-design.md` §13 (FR-7, FR-8, FR-9). Repo: frontend (existing).
- Routes `/signin` and `/register` (not a third-party hosted page).
- Mantine `Paper maw={420}`, `TextInput`, `PasswordInput`, `Button`, `Alert`, `Anchor` between pages.
- `GET /api/v1/auth/me` on app load to restore session. `human_gate: auth`.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-010-account-ui` @ db64a0b
- Changed: `frontend/src/api/auth.ts`, `frontend/src/api/client.ts`, `frontend/src/features/account/*`, `frontend/src/components/AppShellLayout.tsx`, `frontend/src/app/router.tsx`, `frontend/src/app/router.test.tsx`
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (40 tests)
- Notes: Session via `credentials: 'include'` on `/auth/me|register|login|logout`. `GET /auth/me` on shell load; 4xx → guest (401 is the contract). After register/login the header updates from the mutation cache (stay on the form page). Copy: “Email”, “Mật khẩu”, “Tên hiển thị”; submit “Đăng nhập” / “Đăng ký”; anchors “Đã có tài khoản? Đăng nhập” / “Chưa có tài khoản? Đăng ký”; toasts “Đăng ký thành công” / “Đăng nhập thành công”; 401/409 `Alert` “Không đăng nhập được” / “Không đăng ký được”. Client-side field messages in Vietnamese; 400 `ProblemDetail.errors` mapped onto fields. Header account cluster always visible (not `visibleFrom="sm"`). Branch pushed.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-010-account-ui @ db64a0b · Build/tests: npm run lint && npm run format:check && npm test -- --run && npm run build PASS (40 tests)
No comments.

Merged f4b6275.
Pushed main.

## Test (TEST)
### Run 1 — PASS
- Tested: main @ f4b6275 (contains merge `f4b6275`), service on port 15173 (shop-service 18081)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (40 tests)
- AC-001 pass — `/register` Paper 420px Mantine Email/Password/Tên hiển thị; POST `/api/v1/auth/register` 201; header `Tester 010` + `Đăng xuất`
- AC-002 pass — `/signin` POST `/api/v1/auth/login`; empty → field messages; 401 Alert `Không đăng nhập được`; 400 mapped in RTL
- AC-003 pass — guest header `Đăng nhập`/`Đăng ký`; after session `Tester 010` + `Đăng xuất` (also after reload `/auth/me`)
- AC-004 pass — `Đăng xuất` POST `/api/v1/auth/logout` 204; header back to guest cluster
- AC-005 pass — 40 Vitest tests; AccountUi register mock / 401 / sign-out; no native inputs
- Exploratory: teal/Inter AppShell; 409 Alert; catalog 18 products; cluster clipped at 611px (burger still has links); product repo left clean
- Bug (FAIL only): n/a

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 10:48 | BACKLOG | BACKLOG | HUMAN (os_anhbc) | approved auth gate; run remaining REQ-001 tasks |
| 2026-09-24 11:04 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-004, TASK-006] READY_FOR_DEPLOY; auth approved |
| 2026-09-24 11:06 | READY | IN_PROGRESS | FE | branch feature/TASK-010-account-ui |
| 2026-09-24 11:10 | IN_PROGRESS | CODE_REVIEW | FE | product db64a0b; Implementation Iteration 1 |
| 2026-09-24 11:16 | CODE_REVIEW | MERGED | SA | reviews/TASK-010-round-1.md APPROVED; merge_commit=f4b6275 (--no-ff, two parents) |
| 2026-09-24 11:21 | MERGED | TESTING | TEST | run 1; tested sha f4b6275 is ancestor of main containing merge_commit f4b6275 |
| 2026-09-24 11:24 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-010-run-1.md PASS; every AC-001..AC-005 checked; tested sha f4b6275 |
