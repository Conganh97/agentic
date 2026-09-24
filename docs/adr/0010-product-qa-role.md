# ADR-0010: Product QA role

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Project owner
- **Amends:** ADR-0008 (UX/UI visual sign-off moves from SA / designer self-review to PQA)

## Context

SA + UX/UI + FE shipped functional screens that still looked unfinished: sparse layout, large empty
regions, kit-default chrome. SA was both planning the work and approving the look. There was no
increment-level accept after every task passed TEST.

## Decision

Add role `PQA` (`/pqa plan`, `/pqa review`, `/pqa accept`) **without new task states**.

- SA analyzes (design + tasks) and reviews **code**. SA does not merge `work_type: UX_UI` and does
  not own visual APPROVED.
- PQA and SA **loop** while the REQ is `ANALYZING`. PQA plan APPROVED → design `FINAL`, REQ
  `ANALYZED`. Tasks stay BACKLOG until then.
- PQA reviews the UX/UI contract (`CODE_REVIEW` → `MERGED` for `UX_UI`) and the FE against that
  contract + a **density / sellable** bar, before SA code review.
- After every child is `READY_FOR_DEPLOY` (UX_UI: `MERGED`), PQA **accepts** the increment. FAIL →
  written fix list, SA agrees and creates tasks; Scrum may open a side sprint if leftover > 5.
- TEST remains per-task AC black-box. PQA does not replace TEST.

## Consequences

- Positive: plan is challenged before build; look is challenged by someone who did not draw it;
  sparse UI is a MAJOR, not a taste note.
- Negative: two extra hops on UI work (plan + accept).
- Follow-up: UX/UI skill must specify density; FE quality bar matches.

## Alternatives considered

- **New status `PLAN_REVIEW` / `PQA_ACCEPT`:** Rejected — reuse REQ `ANALYZING`/`ANALYZED` and
  existing task states.
- **UX/UI reviews own FE:** Rejected — designer is not the accept gate.
- **SA keeps UX merge:** Rejected — SA is code + architecture only.
