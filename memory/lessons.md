# Lessons Learned

| Date | Source | Lesson | Applies to |
|------|--------|--------|------------|
| 2026-09-24 | ADR-0009 | Do not assume Mantine / TanStack / PostgreSQL. Use the stack SA wrote in design §5 | SA / BE / FE |
| 2026-09-24 | ADR-0008 | FE implements `docs/design/ux/` + Figma. A kit-correct page that ignores the spec is MAJOR | FE / SA / UX/UI |
| 2026-09-24 | browser + Vite | CORS must allow both `localhost` and `127.0.0.1` for the FE port or credentialed POSTs 403 | BE / SA / TEST |
| 2026-09-24 | storefront | Seed images must be distinct and present; one blank/404 for every card is unfinished | FE / UX/UI / TEST |
