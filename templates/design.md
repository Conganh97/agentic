---
requirement: REQ-XXX
status: DRAFT          # DRAFT | FINAL
adrs: []               # [ADR-0003, ...]
updated:
---

# REQ-XXX Design — <title>

## 1. Summary
2–5 lines: what will be built and how.

## 2. Scope
- In scope:
- Out of scope:

## 3. Functional Requirements
| ID | Requirement | Source |
|----|-------------|--------|
| FR-1 | | REQ-XXX Scope / story |

## 4. Non-functional Requirements
| ID | Category | Requirement (measurable) |
|----|----------|--------------------------|
| NFR-1 | Performance / Security / Reliability / ... | |

## 5. Architecture
Components involved or added, responsibilities, interactions (optional mermaid diagram).

## 6. API Changes
| Method | Path / Interface | Request | Response | Errors |
|--------|------------------|---------|----------|--------|

## 7. Data Model Changes
Entities/tables/fields added or changed, migrations, backward compatibility.

## 8. Dependencies
- Internal: other tasks, modules
- External: services, libraries (new ones need an ADR)

## 9. Risks
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|

## 10. Assumptions
- 

## 11. Open Questions
| # | Question | Blocking? | Answer |
|---|----------|-----------|--------|

## 12. Task Breakdown
| Task | Title | Assignee | Covers | Depends on |
|------|-------|----------|--------|------------|
| TASK-XXX | | BE / FE / DEVOPS / TEST | FR-1, NFR-1 | — |

## 13. UI / UX
Required when any task is assigned to FE. Kit: ADR-0006 (Mantine + Tabler Icons). Write "none" only if there is no web UI.

- **Screens:** one row per view (route, purpose, primary actions).
- **Shell:** AppShell header title, nav (if any), content width.
- **Per screen:** Mantine components (Card, TextInput, SegmentedControl, Badge, …), empty / loading / error treatment, confirmations, toasts.
- **Do not** specify “a form on a blank page” or leave layout to FE improvisation.
