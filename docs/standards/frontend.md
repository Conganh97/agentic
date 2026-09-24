# Frontend Standards

`product/frontend/`. Cores: React (ADR-0009). Kit, data, router, bundler: **SA design §5**.
Visual contract: `docs/design/ux/` (+ Figma URL). Do not invent a second look.

## Layout

```
src/
  app/                 # bootstrap only: providers, router, theme (map UX tokens → chosen kit)
  pages/               # route composition; no fetch
  features/<name>/
    api/               # hooks + DTOs
    model/             # types, mappers
    ui/
    index.ts
  shared/
    api/client.ts      # one HTTP wrapper
    ui/                # kit wrappers, AppShell/layout
    lib/
    config/
  assets/
  test/setup.ts
```

Import rule: `app → pages → features → shared`. `shared` never imports `features` or `pages`.
Pages do not call `fetch`. Feature `ui` does not talk HTTP; hooks live in `features/*/api`.

## First app

Scaffold `react-ts` (create-vite into a temp dir, copy into the repo). Then install **only** what
the design names. Keep the scaffolder’s linter. `"strict": true`. Scripts: `dev`, `build`, `lint`,
`test`, `format:check`, `preview`. Proxy `/api` → `http://localhost:${BACKEND_PORT ?? 18081}`.

## Quality bar (CODE_REVIEW fails if)

- Native `<input>`/`<button>`/`<select>` as the product UI (hidden file input OK)
- No shared layout / heading-on-blank-page / chrome + empty canvas
- Fewer than two content units above the fold on a feed, list, or grid (390 and 1280)
- Loading / empty / error are raw `<p>` only or a one-line void
- Ignores `docs/design/ux/` or the Figma frames linked on the task
- A second UI kit besides the one SA chose
- Ad-hoc hex in feature files (use tokens)
- `dangerouslySetInnerHTML`, `console.log`, secrets in `VITE_*`

## API

One client; non-2xx → `ApiError` with RFC 9457 fields. DTOs match the design. Server state via
whatever SA chose (e.g. TanStack Query). No retry on 4xx. `encodeURIComponent` user input.

## Tests

≥1 per AC; RTL by role/label; wrap the **chosen** provider(s). Verify =
`npm run lint && npm run format:check && npm test -- --run && npm run build`.
