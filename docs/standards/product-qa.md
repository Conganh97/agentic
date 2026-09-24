# Product QA

Skill: `.cursor/skills/product-qa/SKILL.md`. Role id in History: `PQA`. No new task states (ADR-0010).

TEST = per-task AC black-box. **PQA** = plan quality, UX quality, increment accept.

## When

| Command | When |
|---------|------|
| `/pqa plan REQ-###` | REQ `ANALYZING`, design exists, plan not APPROVED |
| `/pqa review TASK-###` | `CODE_REVIEW` on `UX_UI` or FE with `requires_uxui` |
| `/pqa accept REQ-###` | Every child `READY_FOR_DEPLOY` or UX_UI `MERGED` |

SA reviews **code** only. PQA reviews **UX and the plan**. They loop until the design is `FINAL`
and the REQ is `ANALYZED`. After all tasks pass TEST, PQA accepts the increment; FAIL → SA adds
fix tasks (optional side sprint).

## Artifacts

| Kind | Path |
|------|------|
| Plan review | `docs/design/reviews/REQ-###-plan-N.md` |
| Increment accept | `docs/design/reviews/REQ-###-accept-N.md` |
| UX / FE visual | `docs/design/ux/reviews/TASK-###-review-NN.md` (`uxui_review`) |

## Density

MAJOR if a primary screen is chrome + empty void, a lonely centered form, or a feed/list with
fewer than two content units above the fold (390 and 1280).
