# ADR-0008: First-class UX/UI role

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Project owner

## Context

SA + FE produced functional UIs that used the Mantine kit (ADR-0006) but were not good enough to
sell a commercial website: default theme, thin hierarchy, weak states, and FE inventing visuals
from a short SA §13 note. A dedicated design contract is required before FE implementation.

## Decision

Add role `UX/UI` (`/uxui`, `/uxui review`) without new task states.

- SA still owns architecture, API, data, and task breakdown.
- UX/UI owns journeys, IA, design system, page specs, responsive behavior, UI states, and a11y.
- FE implements the markdown contract in `docs/design/ux/`. FE must not silently redefine the look.
- UX/UI and BE may run in parallel when independent. FE `depends_on` the UX/UI task.
- After FE reaches `CODE_REVIEW`, `/uxui review` runs before `/sa review` when `requires_uxui` /
  `work_type: FRONTEND`. UX/UI may set `CHANGES_REQUESTED` (uses `uxui_review_iteration`, not SA
  `review_iteration`).
- Backend-only / infra / DevOps tasks skip UX/UI.
- Visual review is **Figma** via the official remote MCP (`.cursor/mcp.json` → `https://mcp.figma.com/mcp`).
  Markdown remains the machine contract and the status database. If MCP is not connected, UX/UI
  stops with `NEEDS_INPUT` (human Connects once).

## Consequences

- Positive: FE receives an implementable commercial design; `/scrum run` can dispatch UX/UI from
  `next.py`; existing BE/TEST/DEVOPS paths stay unchanged.
- Negative: UI requirements gain one extra task and one extra review hop.
- Follow-up: SA analyze must create a UX/UI task whenever it creates FE implementation tasks.

## Alternatives considered

- **SA §13 only:** Rejected — produced kit-default pages, not sellable design.
- **New task states for “UX_REVIEW”:** Rejected — reuse `CODE_REVIEW` / `CHANGES_REQUESTED`.
- **Figma as workflow state:** Rejected — status stays in markdown; Figma is the visual review surface.
