---
id: TASK-003
title: News and static page APIs
type: TASK
priority: CRITICAL
status: BACKLOG
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-001]
sprint:
branch:
merge_commit:
release:
review_iteration: 0
test_iteration: 0
blocked_from:
failed_from:
failure_type:
failure_step:
failure_message:
failure_retry: 0
failure_recoverable:
human_gate:
approved_by:
approved_at:
updated: 2026-09-24 09:15
---

## Description

Add articles and static pages with original short Vietnamese seed copy (not scraped). Expose list
and detail APIs plus shop settings and a contact accept endpoint.

## Acceptance Criteria
- [ ] AC-001 `GET /api/v1/articles` returns ≥2 seeded articles with `slug`, `title`, `excerpt`,
      `publishedAt`; pagination accepted
- [ ] AC-002 `GET /api/v1/articles/{slug}` returns `title`, `content`, optional `imageUrl`, and
      `prevSlug`/`nextSlug` by `published_at`; missing slug → 404
- [ ] AC-003 `GET /api/v1/pages/{slug}` returns `{ slug, title, body }` for
      about, contact, shipping, privacy, warranty, terms, shopping-guide; other slugs → 404
- [ ] AC-004 `GET /api/v1/shop/settings` returns `shopName`, `hotline`, `email`, `zaloUrl`,
      `freeShipFromVnd` from environment with the design §7 defaults
- [ ] AC-005 `POST /api/v1/contact` with valid fields returns 202 `{ accepted: true }` and does
      not send email; blank/oversized fields → 400 ProblemDetail

## Design (SA)
See `docs/design/REQ-001-design.md` §6–§7 (FR-10, FR-11, FR-12). Repo: shop-service (existing).
- Tables `articles`, `pages`; settings from env only; contact is validate-and-ack.
- Seed original blurbs; placeholder article image; never copy reference articles.
- Keep this task under ~400 lines: no catalog changes.

## Implementation (BE/FE)

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
