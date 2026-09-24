# Frontend Standards — React + TypeScript

Applies to everything in `product/frontend/`. Stack: `project.md`, ADR-0003, ADR-0006, ADR-0008.
Visual contract: `docs/design/ux/` and `docs/standards/ux-ui.md`. Implement the spec; do not invent
a second look.

## App layout

```
frontend/
├── package.json, package-lock.json, vite.config.ts, tsconfig*.json, .oxlintrc.json, .prettierrc
├── index.html
└── src/
    ├── main.tsx            # renders <App/> with providers
    ├── app/                # App.tsx, router, theme.ts, providers
    ├── api/                # client.ts (fetch wrapper), DTO types per backend service
    ├── features/<feature>/ # components, hooks (useXxxQuery), feature tests
    ├── components/         # AppShellLayout + shared presentational components
    └── test/setup.ts       # jest-dom matchers, cleanup
```

Dependencies point inward: `app → features → components/api`. Components never call `fetch` directly.

## Creating the app (first FE task only)

- The repo `product/frontend` already exists (repo skill) with `README.md` and `.gitignore`. Scaffold into a
  temporary folder and copy in (create-vite refuses a non-empty folder):
  `d=$(mktemp -d) && npm create vite@latest "$d/app" -- --template react-ts --no-interactive && cp -R "$d/app/." product/frontend/`,
  then in `product/frontend/`:
  `npm install @tanstack/react-query @mantine/core @mantine/hooks @mantine/notifications @tabler/icons-react @fontsource-variable/inter`
  and
  `npm install -D vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event prettier`.
  Add `react-router` only when the app has more than one route.
- Delete the create-vite demo (`App.css`, `assets/`, demo markup in `App.tsx`).
- Keep the tooling and versions `create-vite` generates (currently TypeScript 6, Vite 8, **oxlint** as
  linter); add libraries with `npm install` (lockfile committed). Do not pin versions by hand, swap the
  linter, or upgrade majors inside a feature task.
- Set `"strict": true` in `tsconfig.app.json` (not generated).
- `package.json` scripts: `dev`, `build`, `lint`, `test` (`vitest`), `format:check` (`prettier --check .`), `preview`.
- Vitest in `vite.config.ts` (import `defineConfig` from `vitest/config`):
  `test: { environment: 'jsdom', setupFiles: './src/test/setup.ts' }`; without globals the setup file must
  import `@testing-library/jest-dom/vitest` and call `cleanup()` in `afterEach`.
- Dev proxy: `server.proxy['/api']` → `http://localhost:${BACKEND_PORT ?? 18081}` so the app calls
  relative `/api/...` URLs.
- Then add the UI kit files in **UI kit (required)** below. An app that only has create-vite + a raw
  form is not done.

If the repo already has `package.json` but is missing the kit, install the same UI packages on the
current branch and migrate the page — do not add a second library. Map UX/UI tokens into
`src/app/theme.ts` (do not leave the default teal unless the spec says so).

## UI kit (required) — ADR-0006

The product must look like a finished app, not a browser-default form. Use **Mantine** for every
visible control and layout. Do not introduce Tailwind, shadcn, Ant Design, Chakra, or another kit.

### Packages

`@mantine/core`, `@mantine/hooks`, `@mantine/notifications`, `@tabler/icons-react`,
`@fontsource-variable/inter`.

### Boot

`src/index.css` only loads the font and a page background. No feature layout in this file.

```css
@import "@fontsource-variable/inter";
```

`src/main.tsx` (or `src/app/providers.tsx`) imports package CSS **before** the app and wraps providers:

```tsx
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";
import "@fontsource-variable/inter";

import { MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { theme } from "./app/theme";

<MantineProvider theme={theme}>
  <Notifications position="top-right" />
  <App />
</MantineProvider>
```

`src/app/theme.ts` — copy this theme (do not leave Mantine’s default blue):

```ts
import { createTheme } from "@mantine/core";

export const theme = createTheme({
  primaryColor: "teal",
  defaultRadius: "md",
  fontFamily: "Inter Variable, Inter, system-ui, sans-serif",
  headings: { fontFamily: "Inter Variable, Inter, system-ui, sans-serif", fontWeight: "650" },
});
```

`src/components/AppShellLayout.tsx` — one shared shell for every route:

- `AppShell` with a header (product name + short context) and a padded `main`.
- Content in a centered container (`maw={720}` unless the design specifies a wider layout).
- Page background via `AppShell` `padding` and theme `gray.0` / white papers — not a raw white body.

`App.tsx` renders `<AppShellLayout><…pages…></AppShellLayout>`.

### Which component to use

| Need | Use |
|------|-----|
| Page / section title | `Title`, `Text` (`c="dimmed"` for subtitles) |
| Surface | `Card` or `Paper` with `withBorder` + `shadow="sm"` + `p="md"` |
| Text field | `TextInput` (`label` prop, unique `id` via `useId()`) |
| Long text | `Textarea` |
| Primary / secondary action | `Button` (`variant="filled"` / `"light"` / `"default"` / `"subtle"`) |
| Icon-only action | `ActionIcon` + Tabler icon (`aria-label` required) |
| Status | `Badge` (TODO = `gray`/`yellow`, COMPLETED = `teal`) |
| Filter ALL / TODO / COMPLETED | `SegmentedControl` |
| Loading | `Skeleton` (list) or `Loader` (inline) — never a lone “Loading…” paragraph as the page |
| Query / mutation error | `Alert` `color="red"` with `role="alert"` |
| Empty list | Centered `ThemeIcon` + `Title` order={4} + dimmed `Text` + optional CTA |
| Destroy confirm | `Modal` (never `window.confirm`) |
| Success / mutation feedback | `notifications.show` (title + message) |
| Stack / gap | `Stack`, `Group`, `SimpleGrid` — not margin-soup in CSS |

Icons from `@tabler/icons-react` only (`IconPlus`, `IconTrash`, `IconChecklist`, `IconPencil`, …).

### Visual quality bar (SA rejects below this)

A page is **not** ready for CODE_REVIEW if any of these are true:

- Visible native `<input>`, `<textarea>`, `<button>`, or `<select>` used as the product control
- No `AppShell` / no page header — just a heading on a blank page
- Loading / empty / error are unstyled raw `<p>` only
- Delete has no confirm; success has no toast
- Feature-local CSS re-implements buttons, fields, or cards
- Duplicate `id` on labels (use `useId()` per form instance)
- Catalog/home product cards all share one blank or near-blank placeholder (same teal block / missing
  file). Seed **distinct visible** images per product (unique SVG or photo in `public/placeholders/`).
  A 404 image URL or `ThemeIcon` for every card is not a storefront.
- Design §13 or the UX/UI page spec calls for hero `Image`s / `Carousel` and the page ships text-only `Card`s instead
- A UX/UI spec exists and the page ignores tokens, layout, or states in `docs/design/ux/`

Missing copy or spacing in the design is **not** permission to ship unstyled controls. Compose the
kit; record the wording in Implementation Notes.

### Forbidden

- A second UI library or utility-CSS framework
- Ad-hoc hex colors in feature files (use theme tokens: `teal`, `gray`, `red`, `dimmed`)
- `dangerouslySetInnerHTML`
- `console.log` in committed code

## API access

- One wrapper `src/api/client.ts`: base URL `import.meta.env.VITE_API_BASE_URL ?? ''`, JSON in/out,
  non-2xx → throws `ApiError` carrying the RFC 9457 `ProblemDetail` (`title`, `detail`, `status`).
- DTO types mirror the backend contract in the design; never invent fields.
- Server state via TanStack Query hooks in `features/<feature>/` (`queryKey: ['<resource>', params]`).
  No global store unless an ADR says so. Do not retry 4xx responses (`retry` returns false for `ApiError`
  with status < 500).
- Encode user input in URLs (`encodeURIComponent`).

## Code rules

- TypeScript strict; no `any`, no `@ts-ignore`; function components and hooks only.
- Semantic HTML and accessible forms: every field has a label (`TextInput` `label` or `<label htmlFor>`),
  actions are real buttons, errors use `role="alert"`. Unique ids per instance (`useId()`).
- Render loading, error and empty states for every query — using the kit components above.
- No secrets in `VITE_*` variables (they are public in the bundle).

## Testing

- Every AC has at least one test; name tests after behaviour (`shows Vietnamese greeting when vi is selected`).
- Vitest + React Testing Library; query by role/label/text (not CSS classes or test ids unless unavoidable);
  interact with `userEvent`.
- Mock the network at the boundary: `vi.spyOn(globalThis, 'fetch')` returning `new Response(...)`;
  cover success, loading and error (`ProblemDetail`) paths.
- Wrap components in a fresh `QueryClient` per test (`retry: false`) **and** `MantineProvider`
  (theme optional). Without the provider, Mantine hooks throw.
- Verify before CODE_REVIEW: `npm run lint && npm run format:check && npm test -- --run && npm run build`
  must all pass.
