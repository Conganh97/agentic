# Frontend Standards — React + TypeScript

Applies to everything in `product/frontend/`. Stack: `project.md`, ADR-0003.

## App layout

```
frontend/
├── package.json, package-lock.json, vite.config.ts, tsconfig*.json, .oxlintrc.json, .prettierrc
├── index.html
└── src/
    ├── main.tsx            # renders <App/> with providers
    ├── app/                # App.tsx, router, QueryClient provider
    ├── api/                # client.ts (fetch wrapper), DTO types per backend service
    ├── features/<feature>/ # components, hooks (useXxxQuery), feature tests
    ├── components/         # shared presentational components
    └── test/setup.ts       # jest-dom matchers, cleanup
```

Dependencies point inward: `app → features → components/api`. Components never call `fetch` directly.

## Creating the app (first FE task only)

- Remove the placeholder first (`git -C product rm frontend/.gitkeep`), then
  `cd product && npm create vite@latest frontend -- --template react-ts --no-interactive`, then in `frontend/`:
  `npm install @tanstack/react-query` and
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
- Semantic HTML and accessible forms: every input has a `<label>`, buttons are `<button>`,
  errors use `role="alert"`.
- Render loading, error and empty states for every query.
- No `dangerouslySetInnerHTML`; no secrets in `VITE_*` variables (they are public in the bundle).
- Styling: plain CSS / CSS modules; no UI library without an ADR.
- No `console.log` in committed code.

## Testing

- Every AC has at least one test; name tests after behaviour (`shows Vietnamese greeting when vi is selected`).
- Vitest + React Testing Library; query by role/label/text (not CSS classes or test ids unless unavoidable);
  interact with `userEvent`.
- Mock the network at the boundary: `vi.spyOn(globalThis, 'fetch')` returning `new Response(...)`;
  cover success, loading and error (`ProblemDetail`) paths.
- Wrap components in a fresh `QueryClient` per test (`retry: false`).
- Verify before CODE_REVIEW: `npm run lint && npm run format:check && npm test -- --run && npm run build`
  must all pass.
