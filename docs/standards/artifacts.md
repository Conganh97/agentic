# Artifact contracts — role handoffs

Agents communicate through **files in this repo**, not chat memory. `/scrum run` accepts a step
only after the artifacts below exist on disk.

| From → To | Required artifacts |
|-----------|-------------------|
| HUMAN → SA | `requirements/REQ-###-*.md` (`status: APPROVED`, `revision`, `content_hash`) |
| SA → PQA (plan) | Design `DRAFT` · REQ `ANALYZING` · proposed tasks |
| PQA → SA (plan) | `docs/design/reviews/REQ-###-plan-N.md` APPROVED → REQ `ANALYZED` · or CHANGES_REQUESTED |
| SA → UX/UI / BE / FE | Design `FINAL` §5–§7 + §13 · task file (AC, `depends_on`, `repo`, `work_type`) after PQA plan APPROVED |
| UX/UI → PQA | `docs/design/ux/` · Figma URL · Implementation iteration (`UX_UI` CODE_REVIEW) |
| PQA → FE | `uxui_review` APPROVED on the UX_UI task (MERGED) |
| FE → PQA | Implementation iteration · product branch (when `requires_uxui`) |
| PQA → SA (FE) | `docs/design/ux/reviews/TASK-###-review-N.md` **APPROVED** · `uxui_review` set |
| BE / FE → SA | Implementation iteration · product branch · `branch` set |
| SA → TEST | `reviews/TASK-###-round-N.md` **APPROVED** · `merge_commit` on `main` (skip TEST for `UX_UI` / `DEVOPS`) |
| TEST → PQA | every child `READY_FOR_DEPLOY` (UX_UI / DEVOPS `MERGED`) |
| PQA → DEVOPS | `pqa_accept` APPROVED · then `/devops deploy TASK-### DEV` |
| DEVOPS → HUMAN | `## Deployment` · GHCR image tags · compose smoke · `release` on RELEASED · `releases/REL-###.md` for PROD |
| PQA → SA (accept fail) | `docs/design/reviews/REQ-###-accept-N.md` CHANGES_REQUESTED + agreed fix list |
| TEST → Scrum | `tests/TASK-###-run-N.md` · AC results · `bugs/BUG-###-*.md` on FAIL |
| Scrum (each dispatch) | Append `runs/journal.md` · current `runs/RUN-###.md` |
| Scrum (large work) | ACTIVE `sprints/SPRINT-##.md` · tasks stamped `sprint:` (`scripts/sprint.py`) |

Commands: `python3 scripts/scrum_report.py` · `python3 scripts/next.py` · `python3 scripts/sprint.py` · `python3 scripts/req.py check` · `python3 scripts/deploy.py --env DEV`.
