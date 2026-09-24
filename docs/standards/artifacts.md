# Artifact contracts — role handoffs

Agents communicate through **files in this repo**, not chat memory. `/scrum run` accepts a step
only after the artifacts below exist on disk.

| From → To | Required artifacts |
|-----------|-------------------|
| HUMAN → SA | `requirements/REQ-###-*.md` (`status: APPROVED`, `revision`, `content_hash`) |
| SA → BE / FE | Design `docs/design/REQ-###-design.md` §5–§7 + §13 · task file (AC `AC-###`, `depends_on`, `repo`, `requirement_revision`) |
| BE / FE → SA | Task `## Implementation` iteration · product branch + commit · `branch` set |
| SA → TEST | Latest `reviews/TASK-###-round-N.md` **APPROVED** · `merge_commit` on `main` |
| TEST → Scrum | `tests/TASK-###-run-N.md` · AC results · `bugs/BUG-###-*.md` on FAIL |
| Scrum (each dispatch) | Append `runs/journal.md` · current `runs/RUN-###.md` |

Commands: `python3 scripts/scrum_report.py` · `python3 scripts/next.py` · `python3 scripts/req.py check`.
