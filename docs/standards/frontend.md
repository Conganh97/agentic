# Frontend Standards — React + TypeScript

Applies to everything in `product/frontend/`. Stack: `project.md`, ADR-0003.

## App layout

```
frontend/
├── package.json, package-lock.json, vite.config.ts, tsconfig*.json, eslint.config.js, .prettierrc
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

- `cd product && npm create vite@latest frontend -- --template react-ts`, then in `frontend/`:
  `npm install @tanstack/react-query react-router` and
  `npm install -D vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event prettier`.
- Keep the versions `create-vite` generates; add libraries with `npm install` (lockfile committed). Do not
  pin versions by hand or upgrade majors inside a feature task.
- `package.json` scripts: `dev`, `build`, `lint`, `test` (`vitest`), `preview`.
- Vitest in `vite.config.ts`: `test: { environment: 'jsdom', setupFiles: './src/test/setup.ts' }`.
- Dev proxy: `server.proxy['/api']` → `http://localhost:${BACKEND_PORT ?? 18081}` so the app calls
  relative `/api/...` URLs.

## API access

- One wrapper `src/api/client.ts`: base URL `import.meta.env.VITE_API_BASE_URL ?? ''`, JSON in/out,
  non-2xx → throws `ApiError` carrying the RFC 9457 `ProblemDetail` (`title`, `detail`, `status`).
- DTO types mirror the backend contract in the design; never invent fields.
- Server state via TanStack Query hooks in `features/<feature>/` (`queryKey: ['<resource>', params]`).
  No global store unless an ADR says so.
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
- Verify before CODE_REVIEW: `npm run lint && npm test -- --run && npm run build` must all pass.
