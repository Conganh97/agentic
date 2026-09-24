# Decisions

Index of architecture decisions and rejected options. Append-only. Details live in `docs/adr/`.

| Date | ADR / Ref | Decision | Rejected alternatives |
|------|-----------|----------|-----------------------|
| 2026-09-23 | ADR-0002 | Markdown-driven, Cursor-native team; no DB, no tracker | Java orchestrator + DB (ADR-0001), Jira |
| 2026-09-23 | ADR-0003 | Product: Java 21 + Spring Boot 4.0 microservices, React + TS (Vite) | Boot 3.5, Boot 4.1 |
| 2026-09-23 | ADR-0004 | One repo per component, private GitHub remote, pushes via `scripts/repo.py` | Monorepo, GitHub PRs |
| 2026-09-23 | ADR-0005 | REQ-001: `task-service` + shared `frontend` repos | Monolith, H2-only, extend greeting-service |
| 2026-09-24 | ADR-0006 | FE UI kit: Mantine + Tabler Icons + Inter | Plain CSS, shadcn/Tailwind, Ant Design, Chakra |
| 2026-09-24 | workflow | `FAILED` ≠ `BUG`; deps graph (`deps.py`); merge/AC evidence in pre-commit | Outcome FAILED with no status change; prompt-only retry limits |
| 2026-09-24 | artifacts | Handoffs: `reviews/` `tests/` `runs/`; `req.py` hash/revision; `next.py` resume; human gates | Chat-only handoff; silent REQ edits |
| 2026-09-24 | ADR-0007 | REQ-001 storefront: `shop-service` + `frontend` (supersedes ADR-0005 `task-service`) | Split catalog/user/cart services, reuse task-service, H2 |
