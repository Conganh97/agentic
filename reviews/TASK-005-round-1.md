---
task: TASK-005
round: 1
decision: APPROVED
branch: feature/TASK-005-luma-feed-ui
sha: 0604394
updated: 2026-09-24 15:57
---

# TASK-005 Review Round 1

Reviewed: `feature/TASK-005-luma-feed-ui` @ `0604394` · Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (23)

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | ProfileView.tsx | MINOR | Overlay is a Mantine `Modal` whose title repeats the author already on `PhotoCard`. UX asked for a simple image+caption+heart overlay; UX/UI review already logged this as MINOR. |
| 2 | useFeed.ts | MINOR | `useCreatePost` prepends the new card then `invalidateQueries(feedQueryKey)`, so the optimistic first row can refetch immediately. Harmless if the API returns the same post first. |

AC-001..AC-004 met against design §6/§13 and UX spec: `/feed` PhotoCards newest-first (image, caption, author avatar/name, like count, `likedByMe`); `/create` file or HTTPS URL + caption 1–2200, signed-out → `/sign-in`, success prepends then `/feed`; HeartLike optimistic PUT/DELETE changes count by one without reload; `/u/:username` identity + 3-col square grid, empty “No photos yet”, 404/error/loading states (not blank). Mantine + Tabler + Inter + TanStack Query + React Router; tokens (no ad-hoc hex in feature files); pages compose only; `encodeURIComponent` on ids/usernames; FormData create omits JSON Content-Type; no 4xx retry. Hidden file input only. UX/UI review 1 APPROVED. ≥1 test per AC.

Merged `ab07b1702e6d70511ba29bf003513c495dda3213`.
