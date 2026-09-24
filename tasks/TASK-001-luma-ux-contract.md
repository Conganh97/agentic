---
id: TASK-001
title: Luma UX/UI design contract
type: TASK
priority: HIGH
status: MERGED
assignee: UX/UI
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo:
work_type: UX_UI
requires_uxui: false
uxui_task:
uxui_design: docs/design/ux/REQ-001-ux.md
uxui_review:
figma: "https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma (Feed 1:18, Create 1:21, Profile 1:24, Sign-in 1:15)"
depends_on: []
sprint:
branch: ux/TASK-001-luma-ux-contract
merge_commit: e394833
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
human_gate:
approved_by:
approved_at:
updated: 2026-09-24 14:52
---

## Description

Write the sellable markdown + Figma contract for Luma (REQ-001). Cover every screen in
`docs/design/REQ-001-design.md` §13: entry, sign-up, sign-in, home feed, create post, profile,
plus loading / empty / error / success. Brand must read as a consumer photo app (Instagram-class
density), not an admin or CRUD form. Machine contract lives in `docs/design/ux/`; humans review Figma.

## Acceptance Criteria

- [ ] AC-001 `docs/design/ux/REQ-001-ux.md` (from `templates/ux-spec.md`) names brand, tokens, IA,
      navigation, and the six routes in design §13.
- [ ] AC-002 Each of those screens has page spec content for loading, empty, error, and success
      (four states); empty profile is a designed state, not a blank page.
- [ ] AC-003 Figma file exists; task `figma:` and the UX spec list the file URL plus frame ids for
      feed, create, profile, and sign-in.
- [ ] AC-004 Spec forbids kit-default admin chrome: photo-first feed, square/portrait profile tiles,
      heart like control, mobile bottom nav / desktop side nav.

## Design (SA)

`docs/design/REQ-001-design.md` §5 (Mantine + Tabler + Inter) and §13 (screens + constraints).
Do not change API or AC. `requirement_revision: 3`, `content_hash: 54839e9b074480c8`.

## Implementation (BE/FE)

### Iteration 1
- Wrote: `docs/design/ux/REQ-001-ux.md`
- Figma: https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma (frames: Feed `1:18`, Create `1:21`, Profile `1:24`, Sign-in `1:15`; also Feed desktop `1:155`)

## UX/UI Review

## Review (SA)

### Round 1 — APPROVED
Reviewed: ux/TASK-001-luma-ux-contract @ `e394833` · Build/tests: n/a (UX_UI; Figma MCP screenshots inspected)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | Figma Screens | MINOR | No frames for `/` or `/sign-up`. Markdown covers both; AC-003 only requires four frames. |
| 2 | Figma Screens | MINOR | Loading / error / empty-profile are markdown-only; Figma shows success + create-empty. |
| 3 | Figma Create `1:21` | MINOR | Slot is a filled raised block, not the spec’s 1:1 dashed frame. |

AC-001..AC-004 met. Photo-first feed, heart like, square tiles, mobile bottom nav, desktop side nav. No product merge (`work_type: UX_UI`). Merged `e394833`.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001 design §13; work_type UX_UI; deps [] |
| 2026-09-24 14:46 | BACKLOG | READY | SCRUM | DoR met; deps [] |
| 2026-09-24 14:47 | READY | IN_PROGRESS | UX/UI | branch ux/TASK-001-luma-ux-contract |
| 2026-09-24 14:50 | IN_PROGRESS | CODE_REVIEW | UX/UI | Iteration 1; docs/design/ux/REQ-001-ux.md; Figma https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma frames Feed 1:18 Create 1:21 Profile 1:24 Sign-in 1:15 |
| 2026-09-24 14:52 | CODE_REVIEW | MERGED | SA | Round 1 APPROVED; merge_commit=e394833 (UX artifacts; no product merge); reviews/TASK-001-round-1.md |
