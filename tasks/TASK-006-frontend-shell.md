---
id: TASK-006
title: Frontend scaffold and AppShell
type: TASK
priority: CRITICAL
status: READY_FOR_DEPLOY
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: []
sprint:
branch: feature/TASK-006-frontend-shell
merge_commit: cb0c07f
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
human_gate:
approved_by:
approved_at:
updated: 2026-09-24 09:39
---

## Description

Create the `frontend` repo, Vite React-TS scaffold, ADR-0006 kit, shared `AppShellLayout`, router
placeholders, API client, and Vite `/api` proxy. No feature pages beyond a themed home placeholder.

## Acceptance Criteria
- [x] AC-001 `python3 scripts/repo.py create frontend` registers `product/frontend`; `npm run dev`
      on port 15173 with `BACKEND_PORT=18081` proxies `/api`
- [x] AC-002 App boots with `MantineProvider` (teal/Inter theme), `Notifications`, and
      `AppShellLayout` (header shop name, burger, search and cart `ActionIcon`s, footer columns)
- [x] AC-003 Routes exist for `/`, `/products`, `/categories/:slug`, `/products/:slug`, `/search`,
      `/cart`, `/checkout`, `/signin`, `/register`, `/news`, `/news/:slug`, `/pages/:slug`, `/contact`
      and render inside the shell (placeholder `Title` is enough except `/` shows the shop name)
- [x] AC-004 `src/api/client.ts` uses relative `/api` and throws `ApiError` from ProblemDetail;
      no native `<input>`/`<button>` as product controls
- [x] AC-005 `npm run lint && npm run format:check && npm test -- --run && npm run build` passes
      with at least one RTL test that the shell renders the shop name

## Design (SA)
See `docs/design/REQ-001-design.md` §13 and NFR-1. Repo: frontend (new, ADR-0007).
- Follow `docs/standards/frontend.md` create-app + UI kit steps; `maw={1280}`.
- Tabler icons: `IconSearch`, `IconShoppingCart`, `IconMenu2`. Vietnamese labels.
- Do not implement catalog or account forms in this task.
- Create the GitHub repo only via `scripts/repo.py`.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-006-frontend-shell` @ 1a1957a
- Changed: `frontend/src/main.tsx`, `frontend/src/app/*`, `frontend/src/components/AppShellLayout.tsx`, `frontend/src/api/client.ts`, `frontend/src/features/placeholders/*`, `frontend/vite.config.ts`, `frontend/package.json`
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (18 tests)
- Notes: shop name/hotline/email/Zalo from design defaults (`Mồi Câu Shop`); header second row is static (no `/shop/settings` fetch yet); Sản phẩm mega is a stub `Menu` (Tất cả sản phẩm); account signed-out buttons only; no catalog/account forms; `IconMenu2` used as mobile navbar heading beside Mantine `Burger`; leftover workspace `var/` from create-vite path resolution was not deleted (`rm -rf` blocked by guard-shell)

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-006-frontend-shell @ 1a1957a · Build/tests: npm run lint && npm run format:check && npm test -- --run && npm run build PASS (18 tests)
No comments.

Merged cb0c07f.
Pushed main.

## Test (TEST)
### Run 1 — PASS
- Tested: main @ cb0c07f (contains merge `cb0c07f`), service on port 15173 (mock API 18081)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (18 tests)
- AC-001 pass — `python3 scripts/repo.py status` → frontend registered `product/frontend` clean; `BACKEND_PORT=18081 npm run dev -- --port 15173`; `curl -s localhost:15173/api/shop/settings` → 200 `{"proxied": true, "path": "/api/shop/settings", "via": "mock-18081"}`
- AC-002 pass — browser `/`: Mantine AppShell teal `#12b886` / Inter Variable; Notifications host; header shop name, burger `Mở menu`, search/cart ActionIcons; footer Liên kết / Hướng dẫn / Hỗ trợ
- AC-003 pass — all 13 routes render placeholder Title inside the shell; `/` H1 `Mồi Câu Shop`
- AC-004 pass — `client.ts` fetch `/api/…`; Vitest ApiError from ProblemDetail; no native product `<input>`/`<button>`
- AC-005 pass — verify command PASS (18 tests) including RTL shell shop name
- Exploratory: `/no-such-route` keeps shell with empty main (no catch-all); search/cart icon clicks work; product repo left clean
- Bug (FAIL only): n/a

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:20 | BACKLOG | READY | SCRUM | DoR met; deps [] |
| 2026-09-24 09:21 | READY | IN_PROGRESS | FE | branch feature/TASK-006-frontend-shell |
| 2026-09-24 09:25 | IN_PROGRESS | CODE_REVIEW | FE | product 1a1957a; Iteration 1; 18 tests pass |
| 2026-09-24 09:31 | CODE_REVIEW | MERGED | SA | merge_commit=cb0c07f; reviews/TASK-006-round-1.md APPROVED; --no-ff on main |
| 2026-09-24 09:36 | MERGED | TESTING | TEST | run 1; tested sha cb0c07f is ancestor of main containing merge_commit cb0c07f |
| 2026-09-24 09:39 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-006-run-1.md PASS; every AC-001..AC-005 checked; tested sha cb0c07f |
