---
id: TASK-004
title: Frontend shell and authentication screens
type: TASK
priority: HIGH
status: CODE_REVIEW
assignee: FE
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo: frontend
work_type: FRONTEND
requires_uxui: true
uxui_task: TASK-001
uxui_design: docs/design/ux/REQ-001-ux.md
uxui_review: docs/design/ux/reviews/TASK-004-review-2.md
figma: https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma?node-id=1-15
depends_on: [TASK-001, TASK-002]
sprint:
branch: feature/TASK-004-luma-auth-ui
merge_commit:
release:
review_iteration: 0
uxui_review_iteration: 1
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
updated: 2026-09-24 15:29
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

### Iteration 1 (2026-09-24 15:18)
- Branch: `feature/TASK-004-luma-auth-ui` @ c78d7d5
- Changed: `src/app`, `src/pages`, `src/features/auth`, `src/features/shell`, `src/shared`
- Tests: FE verify → pass (11)
- Notes: registered `product-frontend` (GitHub name already existed); Mantine tokens + session `credentials: 'include'`; pushed origin

### Iteration 2 (2026-09-24 15:26)
- Branch: `feature/TASK-004-luma-auth-ui` @ 1561b12
- Changed: `src/pages/EntryPage.tsx`, `src/index.css`, `src/pages/AuthStates.test.tsx`, `public/entry-atmosphere.svg`
- Tests: FE verify → pass (11)
- Notes: MAJOR #1 — grain on `::before` so Mantine `bg` cannot clear it; `/` image slot + 60% canvas scrim; desktop full-bleed + 400px left copy; pushed origin

## UX/UI Review

### Iteration 1 (2026-09-24 15:22)
- Review: `docs/design/ux/reviews/TASK-004-review-1.md` CHANGES_REQUESTED
- Compared: spec + running UI on `feature/TASK-004-luma-auth-ui` @ c78d7d5 (Figma MCP rate-limited)

### Iteration 2 (2026-09-24 15:29)
- Review: `docs/design/ux/reviews/TASK-004-review-2.md` APPROVED
- Compared: spec + running `/` on `feature/TASK-004-luma-auth-ui` @ 1561b12 (tablet 844 + desktop 1280); MAJOR #1 closed (Figma MCP still rate-limited)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001; repo frontend; requires_uxui; human_gate=auth; deps TASK-001, TASK-002 |
| 2026-09-24 14:53 | BACKLOG | BACKLOG | HUMAN (os_anhbc) | approved_by set; auth gate for REQ-001 run |
| 2026-09-24 15:08 | BACKLOG | READY | SCRUM | DoR met; deps TASK-001 MERGED, TASK-002 READY_FOR_DEPLOY |
| 2026-09-24 15:11 | READY | IN_PROGRESS | FE | branch feature/TASK-004-luma-auth-ui |
| 2026-09-24 15:18 | IN_PROGRESS | CODE_REVIEW | FE | product c78d7d5; FE verify pass (11); Implementation iteration 1 |
| 2026-09-24 15:22 | CODE_REVIEW | CHANGES_REQUESTED | UX/UI | review 1 CHANGES_REQUESTED; docs/design/ux/reviews/TASK-004-review-1.md; MAJOR `/` grain/image slot; uxui_review_iteration 1 |
| 2026-09-24 15:24 | CHANGES_REQUESTED | IN_PROGRESS | FE | branch feature/TASK-004-luma-auth-ui |
| 2026-09-24 15:26 | IN_PROGRESS | CODE_REVIEW | FE | product 1561b12; FE verify pass (11); Implementation iteration 2 |

