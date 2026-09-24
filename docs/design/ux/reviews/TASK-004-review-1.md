---
task: TASK-004
review_round: 1
status: CHANGES_REQUESTED
reviewer: UX/UI
updated: 2026-09-24 15:22
---

# TASK-004 UX/UI Review Round 1

Reviewed: `feature/TASK-004-luma-auth-ui` @ `c78d7d5` · Spec: `docs/design/ux/REQ-001-ux.md`  
Figma: Sign-in `1:15` (MCP screenshot rate-limited; compared running UI to the markdown contract)

| # | Area | Severity | Comment |
|---|------|----------|---------|
| 1 | Visual / `/` Entry | MAJOR | `/` has no photo atmosphere and no warm grain. `.luma-grain` computes `background-image: none` because Mantine `bg` / inline `background` shorthand overrides the class. Desktop is left-aligned type on flat `#0C0C0E` with no image slot. Mobile/tablet slot is a flat `#141417` block. Spec: optional seed photo behind a 60% canvas scrim *or* warm grain; empty state is “solid canvas + grain”; hierarchy starts with photo atmosphere; desktop is full-bleed slot + 400px left copy. Expected: visible grain or a real image slot so `/` reads as a photo community in one glance. |
| 2 | Visual / AuthPanel | MINOR | AuthPanel anatomy says underline-style fields. Implementation uses 48px filled `surface.raised` + 1px `border` (matches the Field token table). Recheck against Figma `1:15` when MCP is available. |
| 3 | Visual / `/sign-in` | MINOR | Demo hint uses `type.meta` (12/16), not `type.caption` (13/18). |
| 4 | Navigation | MINOR | Mobile/tablet chrome puts Sign out in a page header. Spec: profile overflow `⋯` (mobile) or rail footer (desktop). Desktop rail footer is correct. |
| 5 | A11y | MINOR | Password inner input does not set `aria-invalid` when its error is shown (username/email do). |
