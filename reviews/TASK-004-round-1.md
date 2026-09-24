---
task: TASK-004
round: 1
decision: APPROVED
branch: feature/TASK-004-luma-auth-ui
sha: 1561b12
updated: 2026-09-24 15:31
---

# TASK-004 Review Round 1

Reviewed: `feature/TASK-004-luma-auth-ui` @ `1561b12` · Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (11)

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | fieldErrors.ts | MINOR | 400 maps the same `detail` onto username, email, and password; UX asks for the invalid field only. Harmless until a 400 names one field. |
| 2 | AuthPanel.tsx | MINOR | Demo hint uses `type.meta` rather than the spec’s `type.caption`. |

AC-001..AC-004 met against design §5/§13 and UX spec: credentialed `POST /api/v1/auth/sign-up` → `/feed` with 409 `detail` on the email field; sign-in 200 → `/feed`, 401 fixed copy stay on `/sign-in`; `GET /me` member chrome + `POST /sign-out` → `/`; `/`, `/sign-up`, `/sign-in` loading/empty/error/success; Mantine + Tabler + Inter + TanStack Query + React Router; tokens on `MantineProvider`; `credentials: 'include'`. UX/UI review 2 APPROVED. ≥1 test per AC.

Merged `154bf4f19514e9fde423eff32eb900247263e787`.
