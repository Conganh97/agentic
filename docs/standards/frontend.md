# Frontend Standards

Status: baseline only. Detailed stack and rules are defined when Phase 8 (Frontend Agent) starts,
recorded in an ADR.

## Baseline rules

- Components consume backend APIs only through the documented API contract.
- UI requirements and acceptance criteria come from the task; do not invent behavior.
- Every component change ships with tests (unit/component; e2e where the task requires).
- No secrets or environment-specific URLs hardcoded in source.
- Accessibility: semantic HTML, labeled inputs, keyboard navigable.
- FE Agent follows the same boundary as BE Agent: feature branch only, no self-merge, no self-approval.
