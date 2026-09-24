# Lessons Learned

Recurring review findings, bugs and failed approaches. Append-only. Read by SA (review), UX/UI and TEST.

| Date | Source | Lesson | Applies to |
|------|--------|--------|------------|
| 2026-09-24 | ADR-0006 | FE must ship Mantine AppShell + kit controls (ADR-0006). Browser-default inputs/buttons or a CSS-only white form is a MAJOR standards miss, even if ACs pass | FE / SA / UX/UI |
| 2026-09-24 | ADR-0008 | FE must implement the UX/UI design contract. A kit-correct but generic page that ignores `docs/design/ux/` is MAJOR. Do not invent visual design when a spec exists | FE / SA / UX/UI |
| 2026-09-24 | browser + Vite | CORS `allowedOrigins` must include both `localhost` and `127.0.0.1` for the Vite port; otherwise credentialed browser POSTs return 403 `Invalid CORS request` | BE / SA / TEST |
| 2026-09-24 | storefront visual bar | Seed images must be distinct and present under `public/`. One shared blank SVG or 404 image reads as unfinished and is not sellable | FE / UX/UI / TEST |
