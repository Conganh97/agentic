---
id: TASK-001
title: Luma UX/UI design contract
type: TASK
priority: HIGH
status: READY
assignee: UX/UI
parent: REQ-001
requirement_revision: 3
content_hash: 54839e9b074480c8
repo:
work_type: UX_UI
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: []
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
human_gate:
approved_by:
approved_at:
updated: 2026-09-24 14:46
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

## UX/UI Review

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 14:44 | — | BACKLOG | SA | Created from REQ-001 design §13; work_type UX_UI; deps [] |
| 2026-09-24 14:46 | BACKLOG | READY | SCRUM | DoR met; deps [] |
