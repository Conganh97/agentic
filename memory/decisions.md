# Decisions

Index of architecture decisions and rejected options. Append-only. Details live in `docs/adr/`.

| Date | ADR / Ref | Decision | Rejected alternatives |
|------|-----------|----------|-----------------------|
| 2026-09-23 | ADR-0002 | Markdown-driven, Cursor-native team; no DB, no tracker | Java orchestrator + DB (ADR-0001), Jira |
| 2026-09-23 | ADR-0003 | Product: Java 21 + Spring Boot 4.0 microservices, React + TS (Vite) | Boot 3.5, Boot 4.1 |
| 2026-09-23 | ADR-0004 | One repo per component, private GitHub remote, pushes via `scripts/repo.py` | Monorepo, GitHub PRs |
| 2026-09-23 | ADR-0005 | REQ-001: `task-service` + shared `frontend` repos | Monolith, H2-only, extend greeting-service |
