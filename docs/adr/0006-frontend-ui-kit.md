# ADR-0006: Frontend UI kit — Mantine + Tabler Icons

- **Status:** Superseded by ADR-0009
- **Date:** 2026-09-24
- **Deciders:** Project owner

## Context

ADR-0003 and `docs/standards/frontend.md` specified React + TypeScript with **plain CSS / CSS modules**
and forbade a UI library unless a new ADR approved it. The FE skill also told agents to pick the
“simplest accessible option” when the design omitted layout.

An early FE task produced a functional but unfinished UI: browser-default inputs, unstyled
buttons, a bare `<h1>` page, no app shell, no icons, no themed empty/loading states. Functional ACs
passed; the product did not look complete.

Agents will keep shipping that baseline unless the stack **requires** a component kit and SA/TEST
reject unthemed pages.

Do **not** use this ADR for new work. UI kit is chosen by SA per requirement (ADR-0009).

## Decision (historical)

The `product/frontend` app uses this UI kit (install latest compatible majors with `npm install`;
do not pin versions by hand):

| Package | Role |
|---------|------|
| `@mantine/core` | Themed, accessible components (inputs, buttons, cards, badges, modal, alert, skeleton, AppShell) |
| `@mantine/hooks` | Required peer of `@mantine/core` |
| `@mantine/notifications` | Toast feedback for create / update / delete / API errors |
| `@tabler/icons-react` | Icons (Mantine’s documented companion) |
| `@fontsource-variable/inter` | Product typeface |

Rules:

- Wrap the tree in `MantineProvider` + `Notifications` (see `docs/standards/frontend.md`).
- Product controls are Mantine primitives (or thin wrappers). Native `<input>` / `<button>` /
  `<select>` are not the visible product UI (hidden file inputs are the exception).
- Every screen sits in the shared `AppShell` layout (`src/components/AppShellLayout.tsx`).
- Feature CSS is not a substitute for the kit. No second component library (no shadcn, Ant Design,
  Chakra, or ad-hoc Tailwind) without a new ADR.

ADR-0003 is amended: Frontend = React + TypeScript (Vite) + this kit + TanStack Query.

## Consequences

- Positive: default look is a finished product (spacing, radius, typography, states); FE tasks stay
  small because agents compose kit components; accessibility comes from Mantine, not hand-rolled CSS.
- Negative: the first FE task must add the packages, theme, and AppShell; tests must wrap
  `MantineProvider`.
- Follow-up: UX/UI (ADR-0008) specifies tokens and page composition; FE maps them onto this kit.

## Alternatives considered

- **Keep plain CSS:** Rejected — agents consistently produce browser-default forms.
- **shadcn/ui + Tailwind CSS:** Rejected for this team — copy-paste primitives inflate diffs and the
  scaffold is easy to skip; Mantine is one provider + imports.
- **Ant Design / Chakra / HeroUI:** Rejected — heavier or less aligned with Vite + React 19 defaults;
  Mantine covers AppShell, forms, notifications, and overlays in one system.
