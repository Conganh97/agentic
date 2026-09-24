# Update — Add UX/UI Agent

## Objective

Add a dedicated `UX/UI` role to the existing Cursor-native Agentic Engineering Team.

Current roles:

```text
Scrum
SA
Backend
Frontend
Test
DevOps
```

Add:

```text
UX/UI
```

Do not recreate the project. Do not remove existing roles. Reuse existing conventions, workflow states, task formats, skills and artifact patterns.

---

# 1. New Role

Create:

```text
.cursor/skills/ux-ui/SKILL.md
```

Recommended command:

```text
/uxui TASK-###
```

Optional review command:

```text
/uxui review TASK-###
```

The UX/UI role is responsible for turning requirements and SA architecture into an implementable UX/UI design contract for Frontend.

---

# 2. UX/UI Responsibilities

The agent must handle:

### UX

- User journeys.
- Information architecture.
- Navigation.
- Page hierarchy.
- User flows.
- Loading states.
- Empty states.
- Error states.
- Success states.
- Responsive behavior.

### UI

- Layout.
- Visual hierarchy.
- Typography.
- Colors.
- Spacing.
- Components.
- Interaction states.
- Responsive layouts.
- Accessibility.

### Design System

Define reusable:

```text
Colors
Typography
Spacing
Grid
Breakpoints
Buttons
Inputs
Forms
Cards
Navigation
Modal
Toast
Tabs
Dropdown
Loading
Empty State
Error State
```

Prefer reusable components over page-specific duplication.

---

# 3. UX/UI Inputs

Before designing, the agent must read:

```text
Requirement
SA Design
User Stories
Acceptance Criteria
Relevant TASK
Existing frontend standards
Existing design system, if available
```

For website-cloning tasks, inspect the reference website when accessible.

Analyze:

- Page structure.
- Navigation.
- User flows.
- Components.
- Responsive behavior.
- Interaction patterns.
- Content hierarchy.
- Forms.
- Search.
- Product cards.
- Product detail.
- Cart.
- Loading/empty/error states.

---

# 4. UX/UI Outputs

Create artifacts under:

```text
docs/design/ux/
```

Recommended:

```text
docs/design/ux/
├── REQ-###-ux.md
├── design-system.md
├── design-tokens.md
├── components.md
├── responsive.md
├── user-flows.md
├── pages/
│   ├── home.md
│   ├── product-list.md
│   ├── product-detail.md
│   ├── cart.md
│   └── login.md
└── reviews/
```

Simplify the structure for small requirements.

---

# 5. UX Specification

`REQ-###-ux.md` should contain:

```text
## UX Goals
## Target Users
## User Flows
## Information Architecture
## Navigation
## Page Structure
## Interaction Rules
## Loading States
## Empty States
## Error States
## Success States
## Responsive Behavior
## Accessibility
## Open Questions
```

---

# 6. Design System

If no existing design system exists, create:

```text
docs/design/ux/design-system.md
docs/design/ux/design-tokens.md
```

Define:

```text
Colors
Typography
Spacing
Border Radius
Shadows
Breakpoints
Grid
Icons
Buttons
Inputs
Cards
Navigation
Feedback Components
```

Use design tokens where practical.

---

# 7. Page-Level Design

For every UI page define:

```text
Page purpose
User goal
Layout
Components
Content hierarchy
Interactions
Loading state
Empty state
Error state
Success state
Responsive behavior
Accessibility
```

The UX/UI output is a specification, not frontend implementation code.

---

# 8. Responsive Design

Explicitly define:

```text
Desktop
Tablet
Mobile
```

Describe how the layout changes, not just screen widths.

Example:

```text
Desktop: 4-column product grid
Tablet: 2-column product grid
Mobile: 1-column product grid
```

---

# 9. Figma Boundary

Figma is an optional design artifact.

If a supported Figma integration/tool is available:

```text
UX/UI
 ↓
Markdown Design Specification
 ↓
Figma Design
 ↓
Frontend
```

If no Figma integration is available:

```text
UX/UI
 ↓
Markdown Design Specification
 ↓
Frontend
```

Do not block the engineering workflow merely because Figma is unavailable unless the requirement explicitly requires a Figma artifact.

When Figma is available, the UX/UI agent may create/update:

```text
Pages / Frames
Components
Variants
Auto Layout
Responsive layouts
Design tokens
Typography styles
Color styles
Prototype flows
```

Important:

```text
Markdown = machine-readable design contract
Figma    = visual design artifact
```

Do not make Figma the workflow state database.

---

# 10. UX/UI → Frontend Handoff

Frontend must read:

```text
REQ
SA Design
UX/UI Design
Design System
Relevant Page Specification
```

FE must not silently redefine the visual design.

If FE finds an ambiguity:

```text
FE
 ↓
clarification / BLOCKED
 ↓
UX/UI
```

Do not invent UX decisions silently.

---

# 11. UX/UI Review

Add:

```text
/uxui review TASK-###
```

Review:

### Visual

- Layout consistency.
- Typography.
- Spacing.
- Colors.
- Components.
- Visual hierarchy.

### UX

- User flow.
- Navigation.
- Interaction.
- Loading.
- Empty.
- Error.
- Success states.

### Responsive

- Desktop.
- Tablet.
- Mobile.

### Accessibility

- Keyboard interaction where applicable.
- Focus states.
- Form labels.
- Contrast.
- Semantic structure.
- Accessible interactive elements.

Create:

```text
docs/design/ux/reviews/TASK-###-review-01.md
```

Example:

```yaml
---
task: TASK-###
review_round: 1
status: APPROVED
reviewer: UX/UI
---
```

Allowed results:

```text
APPROVED
CHANGES_REQUESTED
BLOCKED
```

Reuse existing workflow/change mechanisms instead of inventing unnecessary new task states.

---

# 12. Updated Workflow

For UI requirements:

```text
                    SA
                     │
              Design + Tasks
                     │
            ┌────────┴────────┐
            ▼                 ▼
          UX/UI              BE
            │                 │
            ▼                 │
       UX/UI Design           │
            │                 │
            └──────┬──────────┘
                   ▼
                   FE
                   │
                   ▼
              UX/UI Review
                   │
             ┌─────┴─────┐
             ▼           ▼
          CHANGES      APPROVED
             │           │
             └─────┐     ▼
                   │  SA Review
                   │     │
                   └─────┘
                         ▼
                        TEST
```

For backend-only requirements:

```text
SA
 ↓
BE
 ↓
SA Review
 ↓
TEST
```

Do not invoke UX/UI unnecessarily.

---

# 13. Dependency Rules

UX/UI is a normal task dependency.

Example:

```text
TASK-001 SA Design
       │
       ├──────────────┐
       ▼              ▼
TASK-002 UX/UI     TASK-003 BE
       │
       ▼
TASK-004 FE
       │
       ▼
TASK-005 UX/UI Review
       │
       ▼
TASK-006 SA Review
       │
       ▼
TASK-007 Test
```

If FE depends on UX/UI:

```yaml
depends_on:
  - TASK-002
```

The orchestrator must not start FE before the dependency is satisfied.

UX/UI and BE may run in parallel when they are independent.

---

# 14. Task Metadata

Add optional fields:

```yaml
work_type:
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
```

Example:

```yaml
---
id: TASK-004
title: Implement Product Detail Page
status: READY
work_type: FRONTEND
requires_uxui: true
depends_on:
  - TASK-002
uxui_design: docs/design/ux/pages/product-detail.md
uxui_review:
---
```

Do not make these fields mandatory for non-UI tasks.

---

# 15. Role Registry

Add UX/UI to the existing role registry:

```text
Role        Command          Responsibility
------------------------------------------------
Scrum       /scrum           Orchestration
SA          /sa              Architecture
UX/UI       /uxui            UX/UI Design
Backend     /backend         Backend implementation
Frontend    /frontend        Frontend implementation
Test        /tester          Testing
DevOps      /devops          Deployment
```

---

# 16. `/scrum run` Integration

The orchestrator must determine whether UX/UI is required.

UX/UI is required when:

```text
task.work_type = FRONTEND
```

or the requirement contains meaningful UI/UX work.

UX/UI is not required for:

```text
BACKEND-only
DATABASE-only
INFRASTRUCTURE-only
DEVOPS-only
```

Recommended:

```yaml
work_type:
  - FRONTEND
  - UX_UI
  - BACKEND
  - TEST
  - DEVOPS
```

A frontend task may use:

```yaml
requires_uxui: true
```

The orchestrator should automatically dispatch UX/UI when required.

---

# 17. UX/UI Role Contract

The SKILL must explicitly define:

```text
Mission:
Turn requirements and SA architecture into a clear, reusable and implementable UX/UI design.

Inputs:
REQ
SA Design
User Stories
Acceptance Criteria
Existing design system
Reference website when applicable

Outputs:
UX specification
Design system
Page specifications
User flows
Responsive rules
Optional Figma design
UX/UI review

Must:
- Follow requirement scope.
- Follow SA architecture.
- Use reusable patterns.
- Define responsive behavior.
- Define important UI states.
- Provide FE with an implementable design contract.

Must not:
- Implement backend code.
- Change backend architecture.
- Invent product requirements.
- Change business acceptance criteria.
- Silently resolve ambiguous requirements.
- Block execution only because Figma is unavailable.

Escalate when:
- Requirement is ambiguous.
- UX conflicts with business requirements.
- SA architecture prevents required UX.
- Figma is explicitly required but unavailable.
```

---

# 18. Acceptance Criteria

- [ ] UX/UI skill exists.
- [ ] `/uxui TASK-###` works.
- [ ] UX/UI consumes REQ + SA Design.
- [ ] UX/UI produces Markdown design artifacts.
- [ ] UX/UI defines user flows.
- [ ] UX/UI defines page structure.
- [ ] UX/UI defines reusable components.
- [ ] UX/UI defines responsive behavior.
- [ ] UX/UI defines loading/empty/error/success states.
- [ ] UX/UI defines accessibility requirements.
- [ ] FE can consume UX/UI artifacts.
- [ ] UX/UI review exists.
- [ ] UX/UI review can request FE changes.
- [ ] UX/UI and BE can run in parallel when independent.
- [ ] `/scrum run` automatically includes UX/UI when required.
- [ ] Backend-only requirements skip UX/UI.
- [ ] Figma is optional unless explicitly required.
- [ ] Existing Scrum, SA, BE, FE, Test and DevOps workflows continue to work.

---

# 19. Definition of Done

The UX/UI role is integrated when:

```text
REQ
 ↓
SA
 ↓
Design + Tasks
 ↓
UX/UI
 ↓
UX/UI Design Artifact
 ↓
FE
 ↓
UX/UI Review
 ↓
SA Review
 ↓
TEST
```

For a UI-heavy requirement the human should still only need to:

```text
write requirement
      ↓
approve requirement
      ↓
/scrum run REQ-###
```

The orchestrator determines that UX/UI is required and dispatches the UX/UI Agent.

---

# 20. Implementation Instructions

Before changing files, inspect the existing:

```text
.cursor/
templates/
tasks/
requirements/
docs/
project.md
AGENTS.md
```

Reuse existing conventions.

Do not recreate the framework.

Do not remove existing roles.

Do not replace existing workflow rules unless necessary.

Implement the UX/UI role, artifacts, task metadata, review flow and `/scrum run` integration.

Do not implement a Figma integration unless a supported Figma tool/integration is actually available.

If Figma is unavailable, implement the Markdown-based UX/UI workflow and document the Figma integration boundary.

After implementation:

1. Validate UX/UI skill.
2. Validate `/uxui TASK-###`.
3. Validate task metadata.
4. Validate `/scrum run` dispatch.
5. Validate UX/UI → FE handoff.
6. Validate UX/UI review loop.
7. Validate backend-only tasks skip UX/UI.
8. Validate existing workflows.
9. Update documentation.
10. Commit the changes with a clear Git commit.
