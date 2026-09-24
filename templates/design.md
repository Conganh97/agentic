---
requirement: REQ-XXX
status: DRAFT          # DRAFT until PQA plan APPROVED, then FINAL
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
Components, responsibilities, interactions (optional mermaid).

### Stack (ADR-0009)
Locked: Java 21 + Spring · React. SA names everything else.

| Layer | Choice | Why |
|-------|--------|-----|
| BE runtime | Java 21 + Spring Boot <ver> | locked core |
| BE data / security / messaging | | |
| FE runtime | React + <bundler> | locked core |
| FE UI kit / data / router | | |

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
| TASK-XXX | | UX/UI / BE / FE / DEVOPS / TEST | FR-1, NFR-1 | — |

New components: one DEVOPS task (`depends_on: []`) creates the GitHub repos and Docker/CI. BE/FE
that need those repos depend on it. Skip the extra task if every repo already exists and CI is correct.

## 13. UI / UX
Required when any task is assigned to FE. Write "none" only if there is no web UI.
SA lists **constraints** here. The sellable visual contract is the UX/UI task (`docs/design/ux/`, ADR-0008).

- **Screens:** one row per view (route, purpose, primary actions, data/API it needs).
- **Constraints:** auth, i18n, the UI kit named in §5, legally fixed copy, **density**
  (feed/list ≥2 content units above the fold; no chrome+void).
- **UX/UI task:** id that will write `docs/design/ux/REQ-###-ux.md` and page specs. Every FE
  implementation task `depends_on` that UX/UI task and sets `requires_uxui: true`.
- Do **not** write the visual spec here (UX/UI + Figma). A blank-page form is not a design.
