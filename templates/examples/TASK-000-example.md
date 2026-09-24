---
id: TASK-000
title: Health check endpoint
type: TASK
priority: MEDIUM
status: RELEASED
assignee: BE
parent: REQ-000
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
depends_on: []
sprint: SPRINT-00
branch: feature/TASK-000-health-check
merge_commit: 3f2a9c1
release: REL-000
review_iteration: 1
uxui_review_iteration: 0
test_iteration: 1
blocked_from:
approved_by: HUMAN (Anh)
updated: 2026-09-23 16:40
---

## Description
Expose `GET /health` returning service status for load balancer checks.

## Acceptance Criteria
- [x] AC-1 `GET /health` returns 200 with `{"status":"UP"}` when the service is healthy
- [x] AC-2 Endpoint requires no authentication
- [x] AC-3 Response time under 100 ms

## Design (SA)
See `docs/design/REQ-000-design.md` §2. Add a controller in the web layer; no database call.

## Implementation (BE/FE)
### Iteration 1
- Branch: `feature/TASK-000-health-check`
- Changed: `src/web/HealthController.*`, `test/web/HealthControllerTest.*`
- Tests: unit tests pass (`<test command from project.md>`)

### Iteration 2 (review round 1)
- Removed logging of request headers; added test for unauthenticated access.

### Iteration 3 (bug fix, test run 1)
- Endpoint was behind auth filter; excluded `/health` from the filter; added regression test.

## UX/UI Review

## Review (SA)
### Round 1 — CHANGES_REQUESTED
Reviewed: feature/TASK-000-health-check @ `9c41e07` · Build/tests: PASS (3 tests)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | src/web/HealthController | BLOCKER | Request headers are logged (may contain tokens) |
| 2 | test/web/HealthControllerTest | MAJOR | No test for AC-2 (no auth) |

### Round 2 — APPROVED
Reviewed: feature/TASK-000-health-check @ `b82d5f0` · Build/tests: PASS (4 tests)
Previous round: #1 resolved, #2 resolved.
No comments.
Merged `1a7b2d4`.

### Round 3 — APPROVED
Reviewed: feature/TASK-000-health-check @ `e07a3c9` · Build/tests: PASS (5 tests)
No comments. Bug fix for test run 1 reviewed; regression test present.
Merged `3f2a9c1`.

## Test (TEST)
### Run 1 — FAIL
- Scope: AC-1..AC-3 against DEV build of `merge 1a7b2d4`
- AC-2 failed: `curl -i /health` without token → 401
- Expected 200, actual 401. Repro: `curl -i http://localhost:8080/health`

### Run 2 — PASS
- All AC pass on merge `3f2a9c1`; p95 = 12 ms.

## Deployment (DEVOPS)
### STG — 2026-09-23 16:20 — OK
Version `1.4.0`, smoke `GET /health` → 200.

### PROD — 2026-09-23 16:35 — OK
Approved by HUMAN (Anh). Version `1.4.0`, smoke OK. Rollback: redeploy `1.3.2`.

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-23 09:00 | — | BACKLOG | SA | Created from REQ-000 design |
| 2026-09-23 09:10 | BACKLOG | READY | SCRUM | DoR satisfied |
| 2026-09-23 09:15 | READY | IN_PROGRESS | BE | Started on feature/TASK-000-health-check |
| 2026-09-23 10:00 | IN_PROGRESS | CODE_REVIEW | BE | Implementation done, tests pass |
| 2026-09-23 10:30 | CODE_REVIEW | CHANGES_REQUESTED | SA | Round 1: 1 BLOCKER, 1 MAJOR |
| 2026-09-23 10:35 | CHANGES_REQUESTED | IN_PROGRESS | BE | Fixing review round 1 |
| 2026-09-23 11:00 | IN_PROGRESS | CODE_REVIEW | BE | Review comments addressed |
| 2026-09-23 11:20 | CODE_REVIEW | MERGED | SA | Round 2 approved, merged 1a7b2d4 |
| 2026-09-23 11:30 | MERGED | TESTING | TEST | Test run 1 started |
| 2026-09-23 12:00 | TESTING | BUG | TEST | Run 1 FAIL: AC-2 returns 401 |
| 2026-09-23 13:00 | BUG | IN_PROGRESS | BE | Fixing auth filter |
| 2026-09-23 13:40 | IN_PROGRESS | CODE_REVIEW | BE | Bug fixed with regression test |
| 2026-09-23 14:00 | CODE_REVIEW | MERGED | SA | Round 3 approved, merged 3f2a9c1 |
| 2026-09-23 14:10 | MERGED | TESTING | TEST | Test run 2 started |
| 2026-09-23 15:00 | TESTING | READY_FOR_DEPLOY | TEST | Run 2 PASS, all AC checked |
| 2026-09-23 16:00 | READY_FOR_DEPLOY | DEPLOYING | DEVOPS | Targets STG, PROD; PROD approved by HUMAN (Anh) |
| 2026-09-23 16:40 | DEPLOYING | RELEASED | DEVOPS | STG + PROD OK, REL-000 |
