# UX/UI Standards

Applies to `docs/design/ux/` (UX/UI role) and every FE task that implements those artifacts.
Kit: ADR-0006. Role: ADR-0008. Skill: `.cursor/skills/ux-ui/SKILL.md`.

## Purpose

UX/UI produces an **implementable design contract**. Frontend implements it. Neither role invents
the other’s work. The contract must be good enough to sell a commercial website — not a wireframe
that “uses Mantine”.

## When UX/UI is required

Required when `work_type: FRONTEND` or `requires_uxui: true`.

Not required for backend-only, database-only, infrastructure-only, or DevOps-only tasks. An FE
task that is tests-only (e.g. Playwright) sets `requires_uxui: false`.

## Artifact locations

```text
docs/design/ux/
├── REQ-###-ux.md
├── design-system.md
├── design-tokens.md
├── components.md
├── responsive.md
├── user-flows.md
├── pages/<page>.md
└── reviews/TASK-###-review-NN.md
```

Templates: `templates/ux-spec.md`, `templates/ux-page.md`, `templates/ux-review.md`.
Small requirements may use a single `REQ-###-ux.md` plus tokens.

## Design contract (UX/UI must define)

| Topic | Expected |
|-------|----------|
| Brand / tokens | Color, type, spacing, radius, shadow, breakpoints — not “use default Mantine teal” |
| Components | Reusable: button, input, card, nav, modal, toast, tabs, dropdown, loading, empty, error |
| Flows | Named user journeys with entry, steps, success, failure |
| Pages | Purpose, hierarchy, layout, interactions, four UI states, responsive layout change |
| Responsive | Desktop / tablet / mobile described as structure (e.g. 4-col → 2-col → 1-col), not only px |
| Accessibility | Labels, focus, contrast, keyboard, semantics |
| Imagery | Distinct, real slots (hero, product, empty). “Placeholder later” is not done |

## Frontend rules

- Read REQ, SA design, **and** the UX/UI artifacts before coding.
- Map tokens to `src/app/theme.ts`; do not hard-code a second palette in feature files.
- Compose ADR-0006 components as the spec says. Do not ship native inputs/buttons as product UI.
- If the spec is ambiguous: `BLOCKED` for UX/UI. Do not invent a brand, layout, or flow.
- A kit-correct page that ignores the spec is a **MAJOR** miss (SA and UX/UI review).

## Review

`/uxui review TASK-###` runs after FE reaches `CODE_REVIEW` and before `/sa review`, when UX/UI is
required. Results: `APPROVED` | `CHANGES_REQUESTED` | `BLOCKED`.
SA must not merge a UI task until `uxui_review` points at an APPROVED file.

## Figma

Optional. Markdown is the workflow contract. Do not block because Figma is unavailable unless the
requirement explicitly requires a Figma artifact. Task state never lives in Figma.
