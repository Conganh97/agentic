---
id: REQ-001
title: Luma — Instagram-like photo social
status: ANALYZED
revision: 3
content_hash: 54839e9b074480c8
priority: HIGH
owner: os_anhbc
design: docs/design/REQ-001-design.md
tasks: [TASK-001, TASK-002, TASK-003, TASK-004, TASK-005]
updated: 2026-09-24 14:44
---

## Goal

Ship a **sellable** local Instagram-like photo social called **Luma**. A visitor can create an
account, post photos with captions, scroll a home feed, like posts, and open a profile. This
requirement exists to exercise the full agentic flow (UX/UI → BE → FE → TEST) on a real consumer
product, not a placeholder catalog.

## Scope

- Email + password **sign up** and **sign in**; stay signed in for the browser session; **sign out**.
- Home feed of recent photo posts (newest first): image, caption, author avatar/name, like count,
  whether the current user liked it.
- Create a post: image (file or HTTPS URL) + caption (1–2200 characters).
- Like and unlike a post; count updates immediately.
- Profile: username, avatar, short bio, grid of that user's posts.
- Empty, loading, and error states that look like a consumer app (no blank page, no raw form dump).
- Seeded demo users and posts so the feed is not empty on first run.

## Out of Scope

- Stories, Reels / video, DMs, comments, hashtags, explore ranking, ads.
- Follow / unfollow, notifications, live, shopping.
- Native iOS / Android apps, multi-tenant SaaS, PROD release.

## User Stories / Behaviour

- As a new visitor, I want to create an account, so that I can post and like.
- As a member, I want to sign in and stay signed in, so that I do not re-enter credentials each click.
- As a member, I want a home feed of recent photos, so that I can browse the community.
- As a member, I want to publish a photo with a caption, so that others can see it.
- As a member, I want to like or unlike a post, so that I can react.
- As a visitor or member, I want to open a profile and see that person's posts, so that I can explore them.
- As anyone, I want empty/error/loading states that look finished, so that the product feels sellable.

## Acceptance Criteria (business level)

- [ ] AC-001 Sign up with email + password creates a member; duplicate email is rejected with a clear message.
- [ ] AC-002 Sign in with valid credentials opens the home feed; invalid credentials show a clear error and do not enter the app.
- [ ] AC-003 Signed-in members stay signed in across page reloads in the same browser; sign out returns to the public entry.
- [ ] AC-004 Home feed lists recent posts newest first, each with image, caption, author, like count, and liked state.
- [ ] AC-005 A signed-in member can create a post (image + caption); it appears at the top of the home feed.
- [ ] AC-006 Like and unlike toggle the current user's liked state and change the count by exactly one.
- [ ] AC-007 A profile shows username, avatar, bio, and that user's posts; a user with no posts sees an empty state, not a blank page.
- [ ] AC-008 First local run shows seeded demo posts so the feed is not empty before anyone posts.

## Constraints

- Stack policy ADR-0009: BE Java 21 + Spring; FE React. SA chooses UI kit, DB, session style, and the rest.
- Local only (DEV). No PROD release in this requirement.
- Session-based access is required for post / like; public feed and public profiles may be readable without a session.
- Images: accept an HTTPS URL or a local file that the API stores and serves. No third-party CDN required.
- UX must look like a consumer photo app (Instagram-class density and hierarchy), not an admin CRUD form.

## Notes

Visual reference: Instagram (mobile web / app) — photo-first feed, bottom or side nav, square/portrait
tiles on profile, heart like control. UX/UI produces the Figma file humans review; markdown is the
implementation contract (ADR-0008).
