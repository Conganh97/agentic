# Artifact contracts — role handoffs

Agents communicate through **files in this repo**, not chat memory. `/scrum run` accepts a step
only after the artifacts below exist on disk.

| From → To | Required artifacts |
|-----------|-------------------|
| HUMAN → SA | `requirements/REQ-###-*.md` (`status: APPROVED`, `revision`, `content_hash`) |
| SA → UX/UI / BE / FE | Design `docs/design/REQ-###-design.md` §5–§7 + §13 · task file (AC `AC-###`, `depends_on`, `repo`, `work_type`, `requirement_revision`) |
| UX/UI → FE | `docs/design/ux/REQ-###-ux.md` · page specs · tokens · Figma URL (`figma:`) · `uxui_design` |
| FE → UX/UI | Task `## Implementation` iteration · product branch + commit · `branch` set (when `requires_uxui`) |
| UX/UI → SA | `docs/design/ux/reviews/TASK-###-review-N.md` **APPROVED** · `uxui_review` set |
| BE / FE → SA | Task `## Implementation` iteration · product branch + commit · `branch` set |
| UX/UI → SA (design task) | `docs/design/ux/**` · Implementation iteration · team sha as `merge_commit` |
| SA → TEST | Latest `reviews/TASK-###-round-N.md` **APPROVED** · `merge_commit` on `main` (skip TEST for `work_type: UX_UI`) |
| TEST → Scrum | `tests/TASK-###-run-N.md` · AC results · `bugs/BUG-###-*.md` on FAIL |
| Scrum (each dispatch) | Append `runs/journal.md` · current `runs/RUN-###.md` |
| Scrum (large work) | ACTIVE `sprints/SPRINT-##.md` · tasks stamped `sprint:` (`scripts/sprint.py`) |

Commands: `python3 scripts/scrum_report.py` · `python3 scripts/next.py` · `python3 scripts/sprint.py` · `python3 scripts/req.py check`.
