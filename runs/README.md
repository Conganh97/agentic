# Execution history

- `runs/journal.md` — append-only row per orchestrator step (`python3 scripts/run_log.py`).
- `runs/RUN-###.md` — one file per `/scrum run` (copy `templates/run.md`).

Resume: `/scrum run` reads current task status + the latest RUN file; it does not restart finished work.
