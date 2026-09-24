---
task: TASK-005
review_round: 1
status: APPROVED
reviewer: UX/UI
updated: 2026-09-24 15:55
---

# TASK-005 UX/UI Review Round 1

Reviewed: `feature/TASK-005-luma-feed-ui` @ `0604394` · Spec: `docs/design/ux/REQ-001-ux.md`  
Figma: Feed `1:18`, Create `1:21`, Profile `1:24` (MCP screenshot rate-limited; compared running UI to the markdown contract + TASK-001 frame notes: photo-first cards, heart like, square tiles, mobile bottom nav, desktop side rail)

Ran FE @ `0604394` + luma-service (seeded 6 posts) at mobile 390×844 and desktop 1280.

| # | Area | Severity | Comment |
|---|------|----------|---------|
| 1 | Navigation / signed-in chrome | MINOR | Mobile/tablet still puts **Sign out** in a page header on `/feed`, `/create`, and `/u/:username`. Spec: profile overflow `⋯` (own profile) or desktop rail footer. Figma Feed `1:18` / Create `1:21` / Profile `1:24` have no header Sign out. Own profile already has the `⋯` menu. |
| 2 | Profile overlay | MINOR | Tile overlay is a Mantine `Modal` whose title repeats the username already on `PhotoCard`. Spec: simple overlay of image + caption + `HeartLike`. Dismiss/`role="dialog"`/Escape are fine. |

Feed PhotoCards are photo-first (4:5 edge-to-edge, author → caption → heart 44×44, `aria-pressed`). Create empty slot is 1:1 dashed + `IconPhoto` + “Add a photo” (markdown contract; Figma `1:21` filled block was already a known spec/Figma MINOR). Profile identity + 3-col 1:1 grid (2px gap), empty “No photos yet”, 404 “This profile doesn’t exist”, and 9-tile loading skeletons match. Desktop rail 244 / content offset 292 / column 630. No kit-default admin chrome.
