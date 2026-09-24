---
requirement: REQ-001
status: FINAL
figma: https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma
updated: 2026-09-24 14:50
---

# REQ-001 UX — Luma

Machine contract for FE. Visual review is the Figma file (ADR-0008). Stack: Mantine + Tabler Icons + Inter (`docs/design/REQ-001-design.md` §5). Do not change API or business AC.

## Brand

**Luma** is an Instagram-class photo-first consumer app. Quiet, warm, analog-dusk. Photos are the product; chrome recedes.

| Attribute | Rule |
|-----------|------|
| Name | **Luma** (legally fixed). Wordmark is title-case Inter 700, tracking −0.02em. No logo mark required this REQ. |
| Voice | Short, human, present tense. “Share a photo.” never “Submit record.” |
| Density | Feed image dominates the viewport. Caption + like sit *below* the photo, never beside it on mobile. |
| Forbidden chrome | Kit-default Mantine AppShell gray, default blue `Button`, stacked `Paper`/`Card` CRUD, `Table`/`DataTable`, “Dashboard / Settings / Admin” nav, boxed admin forms, generic empty “No data”. |

**Avatar fallback (SA §10):** when `avatarUrl` is empty or missing, FE draws a 1:1 circle on `color.surface.raised` with Inter 600 initials from the first 1–2 letters of `username` in `color.text.secondary`. No third-party avatar CDN.

## Tokens

Map onto `MantineProvider` theme. Values are the contract; Mantine defaults are not.

### Color

| Token | Hex | Use |
|-------|-----|-----|
| `color.canvas` | `#0C0C0E` | App background. Not Mantine gray. |
| `color.surface` | `#141417` | Chrome (nav, auth panel). |
| `color.surface.raised` | `#1C1C21` | Skeleton blocks, avatar fallback, input fill. |
| `color.text.primary` | `#F5F2EC` | Headings, captions, primary labels. |
| `color.text.secondary` | `#A8A39A` | Meta (time, like count, bio). |
| `color.text.muted` | `#6F6B64` | Placeholders, disabled. |
| `color.accent` | `#E8C39A` | Wordmark, primary CTA, focus ring. Warm gold — not Mantine blue. |
| `color.like` | `#F43F5E` | Heart (liked + count bump). |
| `color.border` | `#2A2A30` | Hairline only (0.5–1px). No card drop-shadow. |
| `color.danger` | `#F87171` | Field + page errors. |
| `color.success` | `#34D399` | Toast after publish. |
| `color.focus` | `#E8C39A` | 2px focus ring, offset 2px. |

Light mode is out of this REQ. Theme is dusk only.

### Type (Inter Variable via `@fontsource-variable/inter`)

| Token | Size / line | Weight | Use |
|-------|-------------|--------|-----|
| `type.display` | 32 / 38 | 700 | Entry wordmark, splash headline |
| `type.title` | 22 / 28 | 600 | Screen titles, profile username |
| `type.body` | 15 / 22 | 400 | Captions, form values |
| `type.caption` | 13 / 18 | 400 | Bio, helper, empty-state body |
| `type.meta` | 12 / 16 | 500 | Like count, timestamps, nav labels |

Tabular figures for like counts. Never wrap a username mid-word; truncate with ellipsis.

### Space, radius, elevation

| Token | Value | Use |
|-------|-------|-----|
| `space.gutter` | 16 | Mobile page inset |
| `space.feed` | 24 | Vertical gap between `PhotoCard`s |
| `space.nav` | 56 | Mobile bottom nav height; desktop rail item hit area |
| `size.feed` | 630 | Desktop/tablet feed column max-width |
| `size.rail` | 244 | Desktop side nav width |
| `radius.photo` | 4 | Feed photo + profile tiles (not 12px admin cards) |
| `radius.pill` | 999 | Primary CTA, nav create + |
| `radius.avatar` | 999 | Circles only |
| `elevation` | none | No default Mantine shadow. Hairline `color.border` only. |

### Motion

150–220 ms ease-out on like scale (1 → 1.12 → 1) and toast. No page-wide fade that hides content.

## UX Goals

1. A visitor understands Luma is a photo community in one glance on `/`.
2. Sign-up / sign-in feel like joining an app, not filling a back-office form.
3. The home feed is a vertical film strip: photo first, then author, caption, heart.
4. Empty, loading, and error states look finished (NFR-6). Empty profile is designed, not blank.

## Target Users

New visitors creating a first account; returning members browsing and posting; anyone opening a public profile. English copy only.

## User Flows

1. **Join:** `/` → `/sign-up` → session cookie → `/feed`.
2. **Return:** `/` → `/sign-in` → `/feed`. Invalid credentials stay on `/sign-in` with `Invalid email or password.`
3. **Browse:** `/feed` scroll; tap author → `/u/:username`; heart toggles like (signed-in) or routes to `/sign-in` (anonymous).
4. **Publish:** `/create` (signed-in) → image + caption → success toast → `/feed` with new post first. Anonymous hitting `/create` redirects to `/sign-in`.
5. **Leave:** Profile overflow or desktop rail footer → sign out → `/`.

## Information Architecture

```
/                 public entry (signed-in → /feed)
/sign-up          create account
/sign-in          return
/feed             home (public read; like/create need session)
/create           compose (session)
/u/:username      public profile
```

No settings, explore, DMs, or notifications in this REQ. Sign-out is an action, not a route.

## Navigation

Persistent **app chrome** on `/feed`, `/create`, `/u/:username`. Auth routes (`/`, `/sign-up`, `/sign-in`) have **no** bottom/side nav — only wordmark + a text link to the other auth page.

| Viewport | Layout change |
|----------|----------------|
| Mobile `<768` | **Bottom nav** 56px, three equal targets: Home (`/feed`), Create (`/create`, center + in a 40px accent circle), Profile (`/u/{me}` or `/sign-in` if anonymous). Icons Tabler `IconHome` / `IconPlus` / `IconUser`. Active item uses `color.accent`. Safe-area inset on iOS. |
| Tablet `768–1023` | Same **bottom nav**. Content column centered at `size.feed`. |
| Desktop `≥1024` | **Side nav** left, `size.rail` wide, full viewport height. Wordmark top; same three items as stacked icon+label rows; Sign out at the bottom when signed in. Content starts at `244 + 48` gutter. |

Nav never includes Dashboard, Users, or Settings.

## Reusable components

| Component | Anatomy | Forbidden |
|-----------|---------|-----------|
| `Wordmark` | “Luma” `type.display` or `type.title` in `color.accent`. | Generic Mantine `Title` in default blue. |
| `AppChrome` | Bottom or side nav per viewport. | Default `AppShell` gray bar. |
| `PhotoCard` | Full-width **image slot** (4:5 preferred, 1:1 accepted) → row: `Avatar` 32 + username (`type.meta`) → caption (`type.body`, 3-line clamp + “more”) → `HeartLike`. | Image in a 160px thumbnail next to a form. |
| `HeartLike` | Tabler `IconHeart` (outline, 24) / `IconHeartFilled` when `likedByMe`. Count to the right in `type.meta`. Liked: `color.like`. Hit area ≥44×44. Anonymous tap → `/sign-in`. | Star, thumbs-up, Mantine `ActionIcon` default, or a “Like” text button. |
| `ProfileTile` | Square **image slot**, `object-fit: cover`, `radius.photo`, 2px gap. Opens that post (same `/feed` card in a simple overlay or in-place expand — no new route this REQ). | Portrait list rows, rectangular admin thumbs. |
| `Avatar` | 32 (feed) / 88 (profile) circle. Image slot or initials fallback. | Rounded-square user icon. |
| `AuthPanel` | Centered 360px column: wordmark, 1–2 sentences, underline-style fields, one accent pill CTA. | `Paper` card with default shadow and stacked `TextInput` in a 480 gray box. |
| `Field` | Label `type.meta` above; 48px height; fill `color.surface.raised`; 1px `color.border`; focus `color.focus`. Error text `color.danger` under the field. | Default Mantine input chrome. |
| `PrimaryButton` | Full-width (auth/create) or hug (entry), height 48, `radius.pill`, fill `color.accent`, label `color.canvas` Inter 600. Disabled 40% opacity. | Default filled blue button. |
| `EmptyState` | 120px illustrated photo frame (empty slot) + title `type.title` + body `type.caption` + optional CTA. | “No data available.” |
| `SkeletonPhoto` | Pulsing `color.surface.raised` block matching the image slot aspect. | Spinner-only page. |
| `Toast` | Mantine notifications restyled: `color.surface`, `color.success` or `color.danger` left bar, Inter. | Default blue toast. |

## Page Structure

Six routes from design §13. Page specs below (small REQ: one file).

---

# `/` — Entry

## Page purpose

Public splash. Signed-in visitors redirect to `/feed` after `GET /auth/me`.

## User goal

Choose join or return in one glance.

## Layout

Full-bleed `color.canvas`. Center column. Optional **image slot** behind a 60% canvas scrim (seed photo or warm grain — never a stock illustration of a dashboard). Wordmark. Line: “Photos, in their own light.” Two `PrimaryButton`s: “Create account” → `/sign-up`, outline twin “Sign in” → `/sign-in`. No app chrome.

## Components

`Wordmark`, `PrimaryButton` ×2, background image slot.

## Content hierarchy

1. Photo atmosphere 2. Wordmark 3. Line 4. CTAs.

## Interactions

Clicks only. `me` 200 → hard redirect `/feed`.

## Loading state

Full-screen `color.canvas` + pulsing wordmark skeleton (no spinner logo dump). `me` in flight.

## Empty state

No session and no background image: solid canvas + grain. CTAs still present. Not a blank page.

## Error state

`me` network fail: stay on splash (treat as signed-out). Do not show a raw error dump. Optional quiet caption “Couldn’t check session.” + CTAs.

## Success state

Signed-out: splash as specified. Signed-in: no flash of splash longer than the skeleton; land on `/feed`.

## Responsive behavior

| Viewport | Layout change |
|----------|----------------|
| Desktop | Background image slot full-bleed; copy column 400px left-third. |
| Tablet | Image slot top 45vh, copy below centered. |
| Mobile | Image slot top 38vh, copy stacked, buttons full-width in `space.gutter`. |

## Accessibility

H1 is “Luma”. Buttons are real `<button>`/`<a>`. Contrast CTAs ≥ 4.5:1 (`color.canvas` on `color.accent`). Focus visible.

---

# `/sign-up` — Create account

## Page purpose

Create a member (email, password ≥8, username 3–30 `[a-zA-Z0-9_]`).

## User goal

Join and land on `/feed` with a session.

## Layout

`AuthPanel` centered. Fields: Username, Email, Password (show/hide). CTA “Join Luma”. Footer link “Already on Luma? Sign in”. No app chrome.

## Components

`Wordmark`, `Field` ×3, `PrimaryButton`, text link.

## Content hierarchy

Wordmark → “Create your account” (`type.title`) → fields → CTA → link.

## Interactions

Submit `POST /auth/sign-up`. 201 → `/feed`. 409 maps `email_taken` / `username_taken` onto the matching field. 400 under the invalid field.

## Loading state

Fields disabled; CTA shows “Joining…” and is non-interactive. No full-page blank.

## Empty state

Pristine form (designed default). Password hint: “At least 8 characters.” Not an empty-data illustration.

## Error state

409/400: inline field errors. Network: banner under wordmark “Couldn’t reach Luma. Try again.” 401 not used here.

## Success state

Redirect `/feed`. Do not stay on a “Success” admin page.

## Responsive behavior

| Viewport | Layout change |
|----------|----------------|
| Desktop | Panel 360px, vertically centered, no card shadow. |
| Tablet | Same panel, more vertical padding. |
| Mobile | Panel full width minus `space.gutter`; fields 48px; CTA full-width. |

## Accessibility

Labels associated with inputs. Password `type="password"`. Error text referenced by `aria-describedby`. Username pattern announced.

---

# `/sign-in` — Return

## Page purpose

Return with email + password.

## User goal

Open the home feed.

## Layout

`AuthPanel`. Fields: Email, Password. CTA “Sign in”. Link “New here? Create an account”. Demo hint allowed as `type.caption` muted: “Demo: seeded members, password `demo-pass-8`.” — fixture, not a secret.

## Components

Same as sign-up minus username.

## Content hierarchy

Wordmark → “Welcome back” → fields → CTA → link.

## Interactions

`POST /auth/sign-in`. 200 → `/feed`. 401: single generic message **`Invalid email or password.`** (legally fixed) under the form — never say which field failed.

## Loading state

Fields disabled; CTA “Signing in…”.

## Empty state

Pristine form.

## Error state

401: fixed copy. Network: same reachability banner as sign-up.

## Success state

Redirect `/feed`.

## Responsive behavior

Same breakpoints as `/sign-up` (panel 360 → full-width mobile).

## Accessibility

One `role="alert"` for the 401 line. Autocomplete `username` / `current-password`.

---

# `/feed` — Home

## Page purpose

Newest-first photo stream (`GET /posts`). Default after sign-in; public read.

## User goal

Browse, like, open a profile, reach create.

## Layout

`AppChrome` + single column of `PhotoCard`s. **Image slot is the largest element** in each card (min height 320 mobile, up to 4:5). No multi-column masonry this REQ.

## Components

`AppChrome`, `PhotoCard`, `HeartLike`, `Avatar`, `SkeletonPhoto`, `EmptyState`.

## Content hierarchy

Photo → author → caption → heart + count.

## Interactions

Infinite scroll via `before` cursor when `nextBefore` present. Like: optimistic `PUT`/`DELETE`; rollback on error. Username → `/u/:username`. Create nav → `/create`.

## Loading state

Three `SkeletonPhoto` cards (4:5, 32px avatar pulse, two caption lines). No table skeleton.

## Empty state

`EmptyState`: empty photo frame, title “Nothing here yet”, body “When someone shares a photo, it will land here.” Signed-in CTA “Share a photo” → `/create`. (Seed makes this rare on first run; still required.)

## Error state

`EmptyState` variant: title “Couldn’t load the feed”, body from `ProblemDetail.detail` or “Check your connection.”, CTA “Try again” refetches.

## Success state

Cards as specified; like count live. Seeded ≥6 posts on first local run.

## Responsive behavior

| Viewport | Layout change |
|----------|----------------|
| Desktop | Side nav + centered 630 column. Photos full column width. |
| Tablet | Bottom nav + centered 630. |
| Mobile | Bottom nav; photos edge-to-edge (0 horizontal gutter on the image slot; 16px on caption/like). |

## Accessibility

Each card is an article. Image `alt` = caption (truncated 120) or “Photo by {username}”. Heart button `aria-pressed` + `aria-label="Like, {n} likes"`. Keyboard: tab to like and username.

---

# `/create` — Compose

## Page purpose

Publish image + caption (signed-in). Else redirect `/sign-in`.

## User goal

Share a photo that appears first on `/feed`.

## Layout

`AppChrome`. Column `size.feed`. Top: large **image slot** (1:1 square, tap to pick file *or* paste HTTPS URL in a text field under the slot). Below: caption textarea (1–2200). CTA “Share” pinned above nav / in column footer.

## Components

`AppChrome`, image slot (drop + file + URL), `Field` textarea, `PrimaryButton`.

## Content hierarchy

Preview slot → source (File / Link toggle) → caption → Share.

## Interactions

XOR file vs `https://` URL (SA FR-5). Client reject: empty caption, caption >2200, non-https URL, file not jpeg/png/webp or >8 MiB — inline, no API call. 201 → toast “Shared” + `/feed`.

## Loading state

Preview shows selected image (or URL thumbnail if browser can). Share disabled with “Sharing…”. Slot not replaced by a blank page.

## Empty state

Slot shows dashed `color.border` frame + Tabler `IconPhoto` + “Add a photo”. Caption placeholder “Write a caption…”. Designed, not a naked file input.

## Error state

400/401/network: toast or banner `color.danger` with `detail`. 401 mid-submit → `/sign-in`. Keep the draft (image + caption) in memory.

## Success state

Toast + navigate `/feed` (new card first). Do not show an admin “created id=…” page.

## Responsive behavior

| Viewport | Layout change |
|----------|----------------|
| Desktop | Side nav; 630 column; slot 630×630. |
| Tablet | Bottom nav; slot 100% of column. |
| Mobile | Bottom nav; slot full viewport width 1:1; Share full-width above nav. |

## Accessibility

File input visually hidden, triggered by slot button `aria-label="Add a photo"`. Caption labelled. Character count `aria-live="polite"` after 2000.

---

# `/u/:username` — Profile

## Page purpose

Public identity + that author’s posts.

## User goal

See who they are and their photos.

## Layout

`AppChrome`. Identity row: `Avatar` 88, username `type.title`, post count `type.meta` (“{n} photos”), bio `type.caption` (up to 160). Then **3-column square `ProfileTile` grid**, 2px gap, no outer radius on the grid. Own profile (session username matches): overflow `⋯` with Sign out.

## Components

`AppChrome`, `Avatar`, `ProfileTile`, `EmptyState`.

## Content hierarchy

Avatar → username → count → bio → grid.

## Interactions

Tile opens the post image + caption + `HeartLike` in a simple overlay (no `/posts/:id` route this REQ). Back / overlay dismiss returns to the grid. Unknown user: error state.

## Loading state

Avatar circle pulse, 2 text lines pulse, **9 square tile skeletons**. Never an empty white page.

## Empty state (required — not blank)

Identity still renders (avatar fallback, username, “0 photos”). Grid replaced by `EmptyState`: empty square frame, title “No photos yet”, body “When {username} shares, they will show up here.” If `me.username === :username`, CTA “Share a photo” → `/create`. Otherwise no CTA.

## Error state

404: `EmptyState` “This profile doesn’t exist” + link Home. Network: “Couldn’t load this profile” + Try again. Do not show a raw 404 JSON page.

## Success state

Identity + grid of square/portrait-cropped tiles (always 1:1 cover). Seed users have posts.

## Responsive behavior

| Viewport | Layout change |
|----------|----------------|
| Desktop | Side nav; identity + 3-col grid in 630 column. |
| Tablet | Bottom nav; same 3-col in 630. |
| Mobile | Bottom nav; identity padded 16; grid edge-to-edge 3-col, 2px gap. |

## Accessibility

Username is `h1`. Grid is a list. Each tile button: `aria-label` caption or “Photo {n}”. Overlay `role="dialog"` + Escape closes. Sign out is a real button.

---

## Interaction Rules

- Session cookie only (`LUMA_SESSION`); never tokens in `localStorage`.
- Optimistic like; count changes by exactly one; floor 0.
- Anonymous like or Create → `/sign-in` (preserve `from` query optional; default `/feed` or `/create`).
- English only.
- Image slots always have an aspect box *before* bytes load (no layout jump).

## Loading States

Per-page above. Global rule: skeleton mimics the photo geometry (4:5 cards, 1:1 tiles), not a centered Mantine `Loader` on a blank canvas.

## Empty States

Per-page above. Empty profile is a designed identity + message, not a blank main.

## Error States

Use `ProblemDetail.detail` when present. 401 on write → sign-in. Never stack traces or unthemed forms.

## Success States

Redirects and toasts as specified. Feed and profile success show **real image slots** filled with `imageUrl` (`object-fit: cover`).

## Responsive Behavior

| Viewport | Layout change |
|----------|----------------|
| Desktop (≥1024) | Side nav `244`; content offset; feed/profile column 630. Entry uses left copy + full-bleed photo. |
| Tablet (768–1023) | Bottom nav; content centered 630. Entry stacks photo then copy. |
| Mobile (`<768`) | Bottom nav; feed images edge-to-edge; profile 3-col edge-to-edge; auth full-width gutters. |

## Accessibility

- Contrast: primary text on canvas ≥ 7:1; secondary ≥ 4.5:1; accent-on-canvas CTA ≥ 4.5:1.
- Hit targets ≥ 44×44 (heart, nav, tiles).
- Visible focus `color.focus`.
- Images: meaningful `alt`; decorative grain `alt=""`.
- Reduced motion: skip like bounce.
- Auth errors are text, not color-only.

## Figma

File: [https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma](https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma)  
Key: `2e7pwemMZdOQ2CX7eYvHoB` · page `Screens`.

| Frame | Node id | URL |
|-------|---------|-----|
| Feed | `1:18` | [node](https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma?node-id=1-18) |
| Create | `1:21` | [node](https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma?node-id=1-21) |
| Profile | `1:24` | [node](https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma?node-id=1-24) |
| Sign-in | `1:15` | [node](https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma?node-id=1-15) |
| Feed desktop (side nav) | `1:155` | [node](https://www.figma.com/design/2e7pwemMZdOQ2CX7eYvHoB/Luma?node-id=1-155) |

## Open Questions

| # | Question | Blocking? | Answer |
|---|----------|-----------|--------|
| 1 | Member edit of avatar/bio? | No | Out of REQ (SA §11). Seed + empty fields only. |
| 2 | Post detail route? | No | Overlay on profile tiles; no extra route. |
