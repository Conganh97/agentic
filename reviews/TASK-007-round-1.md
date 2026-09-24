---
task: TASK-007
round: 1
decision: APPROVED
branch: feature/TASK-007-home-catalog-search-ui
sha: ddc0147
updated: 2026-09-24 10:06
---

# TASK-007 Review Round 1

Reviewed: `feature/TASK-007-home-catalog-search-ui` @ `ddc0147` · Build/tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` PASS (23 tests)

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | src/components/CategoryNav.tsx:3 | MINOR | `components/` imports `useCategoriesQuery` from `features/catalog`. Keep shell presentational: pass the tree in or colocate the nav under the feature (`app → features → components/api`). |
| 2 | src/features/catalog/HomePage.tsx:817 | MINOR | Bait/gear sections use `categories.data?.[0]` / `[1]`. Prefer parent slugs (`moi-cau-ca`, `phu-kien-do-cau`) so section titles do not depend on API order. |
| 3 | src/components/HeaderSearch.tsx:368 | MINOR | Visible `TextInput` label in the 64px header row will crowd mobile. Use a visually hidden label (or the §13 `ActionIcon` overlay) and keep `aria-label` / `useId`. |

Merged `4aa99e5`.
Pushed main.
