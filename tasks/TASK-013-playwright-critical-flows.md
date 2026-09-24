---
id: TASK-013
title: Playwright critical customer flows
type: TASK
priority: CRITICAL
status: READY_FOR_DEPLOY
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
updated: 2026-09-24 11:59
---

## Description

Add Playwright and specs for the critical customer paths: browse catalog, open detail, cart
quantity, and account register/sign-in/sign-out. `human_gate: auth` because the suite includes
account flows.

## Acceptance Criteria
- [x] AC-001 `npx playwright test` is scripted; specs run against the Vite app (webServer or
      documented BASE_URL) with API either live or mocked at the network layer
- [x] AC-002 A spec visits `/`, opens a product from a card, and asserts the detail `Title` matches
- [x] AC-003 A spec adds a product to the cart (or seeds cart via API) and asserts `/cart` shows
      quantity ≥ 1 and a non-zero total
- [x] AC-004 A spec registers a unique user (or uses a test account), signs in, sees the header
      display name, signs out, and sees “Đăng nhập” again
- [x] AC-005 CI-local command is documented; tests are not `test.skip` / `fixme`; no secrets in spec files

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
### Run 1 — PASS
- Tested: main @ 1a1a6f2 (contains merge `1a1a6f2`), service on port 15173 (Playwright webServer; no shop-service)
- Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (49 tests); `npx playwright test` PASS (3)
- AC-001 pass — `package.json` script `e2e`; `playwright.config.ts` webServer Vite `http://127.0.0.1:15173` (skipped if `BASE_URL`); `e2e/fixtures/shopApi.ts` `context.route(/\/api\/v1\//)`; `npx playwright test` started Vite and ran 3 specs
- AC-002 pass — `e2e/browse-detail.spec.ts` ✓ visits home, opens a product card, and shows the matching detail title (1.3s)
- AC-003 pass — `e2e/cart.spec.ts` ✓ adds a product and shows cart quantity and a non-zero total (1.6s)
- AC-004 pass — `e2e/account.spec.ts` ✓ registers, signs in, sees the header name, then signs out (10.7s)
- AC-005 pass — README documents `npx playwright test` / `npm run e2e`; no `test.skip` / `fixme` / `only`; dummy `password1` only (same as RTL)
- Exploratory: no skip/fixme; Vite logged ECONNREFUSED on `/api/v1/*` (shop-service not running) while Playwright mocks still satisfied specs; 15173 free after stop; `product/frontend` porcelain empty (`test-results/.last-run.json` gitignored)
- Bug (FAIL only): n/a

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
| 2026-09-24 11:58 | MERGED | TESTING | TEST | run 1; tested sha 1a1a6f2 is ancestor of main containing merge_commit 1a1a6f2 |
| 2026-09-24 11:59 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-013-run-1.md PASS; every AC-001..AC-005 checked; tested sha 1a1a6f2 |
