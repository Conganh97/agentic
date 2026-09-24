---
id: TASK-013
title: Playwright critical customer flows
type: TASK
priority: CRITICAL
status: MERGED
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-007, TASK-008, TASK-009, TASK-010]
sprint:
branch: feature/TASK-013-playwright-critical-flows
merge_commit: 1a1a6f2
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
updated: 2026-09-24 11:57
---

## Description

Add Playwright and specs for the critical customer paths: browse catalog, open detail, cart
quantity, and account register/sign-in/sign-out. `human_gate: auth` because the suite includes
account flows.

## Acceptance Criteria
- [ ] AC-001 `npx playwright test` is scripted; specs run against the Vite app (webServer or
      documented BASE_URL) with API either live or mocked at the network layer
- [ ] AC-002 A spec visits `/`, opens a product from a card, and asserts the detail `Title` matches
- [ ] AC-003 A spec adds a product to the cart (or seeds cart via API) and asserts `/cart` shows
      quantity ≥ 1 and a non-zero total
- [ ] AC-004 A spec registers a unique user (or uses a test account), signs in, sees the header
      display name, signs out, and sees “Đăng nhập” again
- [ ] AC-005 CI-local command is documented; tests are not `test.skip` / `fixme`; no secrets in spec files

## Design (SA)
See `docs/design/REQ-001-design.md` NFR-7. Repo: frontend (existing).
- Playwright as in `project.md` E2E row. Do not add a second UI kit.
- Prefer `page.getByRole` over test ids. Account routes: `/signin`, `/register`.
- `human_gate: auth`.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-013-playwright-critical-flows` @ 6c81b4c
- Changed: `frontend/playwright.config.ts`, `frontend/e2e/browse-detail.spec.ts`, `frontend/e2e/cart.spec.ts`, `frontend/e2e/account.spec.ts`, `frontend/e2e/fixtures/shopApi.ts`, `frontend/package.json`, `frontend/vite.config.ts`, `frontend/README.md`
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (49 tests); `npx playwright test` → pass (3)
- Notes: Playwright `webServer` starts Vite on `http://127.0.0.1:15173` (`--host 127.0.0.1`); `BASE_URL` skips webServer. Specs mock `/api/v1/*` via `context.route` (no shop-service). `getByRole` / `getByLabel` only. Account: unique `e2e-${Date.now()}@example.com`, dummy password `password1` (same as RTL). Copy unchanged. Branch pushed.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-013-playwright-critical-flows @ 6c81b4c · Build/tests: npm run lint && npm run format:check && npm test -- --run && npm run build PASS (49); npx playwright test PASS (3)
No comments.

Merged 1a1a6f2.
Push failed: git fetch origin — Failed to connect to github.com port 443.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 10:48 | BACKLOG | BACKLOG | HUMAN (os_anhbc) | approved auth gate; run remaining REQ-001 tasks |
| 2026-09-24 11:45 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-007, TASK-008, TASK-009, TASK-010] READY_FOR_DEPLOY; auth approved |
| 2026-09-24 11:46 | READY | IN_PROGRESS | FE | Started on feature/TASK-013-playwright-critical-flows |
| 2026-09-24 11:53 | IN_PROGRESS | CODE_REVIEW | FE | Product 6c81b4c; Iteration 1; lint/format/vitest/build + 3 Playwright specs pass |
| 2026-09-24 11:57 | CODE_REVIEW | MERGED | SA | Approved round 1; merge_commit=1a1a6f2 |
