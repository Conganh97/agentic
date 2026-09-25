# Product QA

Skill: `.cursor/skills/product-qa/SKILL.md`. Role id in History: `PQA`. No new task states (ADR-0010).

TEST = per-task AC black-box. **PQA** = plan quality, UX quality, increment accept.

## When

| Command | When |
|---------|------|
| `/pqa plan REQ-###` | REQ `ANALYZING`, design exists, plan not APPROVED |
| `/pqa review TASK-###` | `CODE_REVIEW` on `UX_UI` or FE with `requires_uxui` |
| `/pqa accept REQ-###` | Every **direct** child (`parent` = REQ id) `READY_FOR_DEPLOY` or UX_UI / DEVOPS `MERGED` |

SA reviews **code** only. PQA reviews **UX and the plan**. They loop until the design is `FINAL`
and the REQ is `ANALYZED`. After all tasks pass TEST, PQA accepts the increment; FAIL → SA adds
fix tasks (optional side sprint).

## Artifacts

| Kind | Path |
|------|------|
| Plan review | `docs/design/reviews/REQ-###-plan-N.md` |
| Increment accept | `docs/design/reviews/REQ-###-accept-N.md` |
| UX / FE visual | `docs/design/ux/reviews/TASK-###-review-NN.md` (`uxui_review`) |

`pqa_accept` authorizes DEVOPS to deploy. PQA does not deploy or set task `RELEASED`.
On PASS, PQA may set REQ `READY_FOR_RELEASE`.

## Density

Always MAJOR: chrome + unused canvas, or an admin blank page.

- FEED / LIST / GRID / DASHBOARD: fewer than two content units above the fold (390 and 1280).
- AUTH / FORM / SYSTEM: do not fail only for fewer than two units; still fail empty-canvas chrome.
- DETAIL / LANDING: unused canvas beside a thin column unless it is a designed split.
