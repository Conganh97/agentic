---
id: TASK-006
title: Frontend scaffold and AppShell
type: TASK
priority: CRITICAL
status: BACKLOG
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: []
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
human_gate:
approved_by:
approved_at:
updated: 2026-09-24 09:15
---

## Description

Create the `frontend` repo, Vite React-TS scaffold, ADR-0006 kit, shared `AppShellLayout`, router
placeholders, API client, and Vite `/api` proxy. No feature pages beyond a themed home placeholder.

## Acceptance Criteria
- [ ] AC-001 `python3 scripts/repo.py create frontend` registers `product/frontend`; `npm run dev`
      on port 15173 with `BACKEND_PORT=18081` proxies `/api`
- [ ] AC-002 App boots with `MantineProvider` (teal/Inter theme), `Notifications`, and
      `AppShellLayout` (header shop name, burger, search and cart `ActionIcon`s, footer columns)
- [ ] AC-003 Routes exist for `/`, `/products`, `/categories/:slug`, `/products/:slug`, `/search`,
      `/cart`, `/checkout`, `/signin`, `/register`, `/news`, `/news/:slug`, `/pages/:slug`, `/contact`
      and render inside the shell (placeholder `Title` is enough except `/` shows the shop name)
- [ ] AC-004 `src/api/client.ts` uses relative `/api` and throws `ApiError` from ProblemDetail;
      no native `<input>`/`<button>` as product controls
- [ ] AC-005 `npm run lint && npm run format:check && npm test -- --run && npm run build` passes
      with at least one RTL test that the shell renders the shop name

## Design (SA)
See `docs/design/REQ-001-design.md` §13 and NFR-1. Repo: frontend (new, ADR-0007).
- Follow `docs/standards/frontend.md` create-app + UI kit steps; `maw={1280}`.
- Tabler icons: `IconSearch`, `IconShoppingCart`, `IconMenu2`. Vietnamese labels.
- Do not implement catalog or account forms in this task.
- Create the GitHub repo only via `scripts/repo.py`.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
