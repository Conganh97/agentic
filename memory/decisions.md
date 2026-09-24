# Decisions

Index of architecture decisions and rejected options. Append-only. Details live in `docs/adr/`.

| Date | ADR / Ref | Decision | Rejected alternatives |
|------|-----------|----------|-----------------------|
| 2026-09-23 | ADR-0002 | Markdown-driven, Cursor-native team; no DB, no tracker | Java orchestrator + DB (ADR-0001), Jira |
| 2026-09-23 | ADR-0003 | Product: Java 21 + Spring Boot 4.0 microservices, React + TS (Vite) | Boot 3.5, Boot 4.1 |
| 2026-09-23 | ADR-0004 | One repo per component, private GitHub remote, pushes via `scripts/repo.py` | Monorepo, GitHub PRs |
| 2026-09-24 | ADR-0006 | *(superseded)* Mantine as global kit | — |
| 2026-09-24 | workflow | `FAILED` ≠ `BUG`; deps graph (`deps.py`); merge/AC evidence in pre-commit | Outcome FAILED with no status change; prompt-only retry limits |
| 2026-09-24 | artifacts | Handoffs: `reviews/` `tests/` `runs/`; `req.py` hash/revision; `next.py` resume; human gates | Chat-only handoff; silent REQ edits |
| 2026-09-24 | ADR-0008 | First-class UX/UI role; markdown contract + Figma MCP for visual review | FE invents UI; Figma as workflow state |
| 2026-09-24 | ADR-0009 | Locked: Java 21 + Spring, React. SA chooses kit/DB/etc. Package-by-feature FE/BE layouts | Global Mantine lock (ADR-0006) |
