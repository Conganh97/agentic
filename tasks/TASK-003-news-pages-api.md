---
id: TASK-003
title: News and static page APIs
type: TASK
priority: CRITICAL
status: READY_FOR_DEPLOY
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: shop-service
depends_on: [TASK-001]
sprint:
branch: feature/TASK-003-news-pages-api
merge_commit: a8b6f11
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
updated: 2026-09-24 10:09
---

## Description

Add articles and static pages with original short Vietnamese seed copy (not scraped). Expose list
and detail APIs plus shop settings and a contact accept endpoint.

## Acceptance Criteria
- [x] AC-001 `GET /api/v1/articles` returns ≥2 seeded articles with `slug`, `title`, `excerpt`,
      `publishedAt`; pagination accepted
- [x] AC-002 `GET /api/v1/articles/{slug}` returns `title`, `content`, optional `imageUrl`, and
      `prevSlug`/`nextSlug` by `published_at`; missing slug → 404
- [x] AC-003 `GET /api/v1/pages/{slug}` returns `{ slug, title, body }` for
      about, contact, shipping, privacy, warranty, terms, shopping-guide; other slugs → 404
- [x] AC-004 `GET /api/v1/shop/settings` returns `shopName`, `hotline`, `email`, `zaloUrl`,
      `freeShipFromVnd` from environment with the design §7 defaults
- [x] AC-005 `POST /api/v1/contact` with valid fields returns 202 `{ accepted: true }` and does
      not send email; blank/oversized fields → 400 ProblemDetail

## Design (SA)
See `docs/design/REQ-001-design.md` §6–§7 (FR-10, FR-11, FR-12). Repo: shop-service (existing).
- Tables `articles`, `pages`; settings from env only; contact is validate-and-ack.
- Seed original blurbs; placeholder article image; never copy reference articles.
- Keep this task under ~400 lines: no catalog changes.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-003-news-pages-api` @ 571eb47
- Changed: `services/shop-service/src/main/resources/db/migration/V4__content.sql`, `V5__content_seed.sql`, `api/{Article,Page,Shop,Contact}Controller.java`, `api/*Response.java`, `api/ContactRequest.java`, `service/ContentService.java`, `domain/{Article,StaticPage}.java`, `repository/{Article,StaticPage}Repository.java`, `config/ShopProperties*.java`, `application.yml`, `ArticleControllerTest.java`, `PageControllerTest.java`, `ShopControllerTest.java`, `ContactControllerTest.java`, `ContentApiTest.java`, `ContentServiceTest.java`, `ShopApplicationTests.java`
- Tests: `./mvnw -q verify` in `services/shop-service` → pass (53 tests)
- Notes: Flyway V4/V5 because V1–V3 already used. Seeded 3 original articles (placeholder `/placeholders/article.svg`) and 7 design slugs. List newest-first; `prevSlug`=older, `nextSlug`=newer by `published_at`. Pagination matches catalog (`page` 1, `size` 24 max 60). Contact caps: name 80, email 254, phone 30, message 2000; validate-and-ack only (no persist/send). Settings from `SHOP_*` with design §7 defaults. No catalog changes. Branch pushed.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-003-news-pages-api @ 571eb47 · Build/tests: ./mvnw -q verify PASS (53 tests)
No comments.

Merged a8b6f11.
Pushed main.

## Test (TEST)
### Run 1 — PASS
- Tested: main @ a8b6f11 (contains merge `a8b6f11`), service on port 18081
- Build/tests: `./mvnw -q verify` PASS (53 tests)
- AC-001 pass — `GET /api/v1/articles` → 200 3 items newest-first with `slug`/`title`/`excerpt`/`publishedAt`; `page=1&size=2` → 2 items `total=3`; `page=2&size=2` → remaining 1
- AC-002 pass — `GET /api/v1/articles/bao-quan-moi-cau-sau-khi-mo-bao` → 200 `title`/`content`/`imageUrl` `/placeholders/article.svg` `prevSlug=chon-moi-cau-chep-mua-lanh` `nextSlug=chuan-bi-can-cau-buoi-som`; missing slug → 404 `Article not found`
- AC-003 pass — all 7 design slugs 200 `{slug,title,body}`; `GET /api/v1/pages/khong-ton-tai` → 404 `Page not found`
- AC-004 pass — `GET /api/v1/shop/settings` → 200 `shopName=Mồi Câu Shop` `hotline=0123 456 789` `email=shop@example.com` `zaloUrl=https://zalo.me/0123456789` `freeShipFromVnd=200000`
- AC-005 pass — valid POST → 202 `{"accepted":true}`; blank name / name 81 / phone 31 / message 2001 → 400 ProblemDetail; no mail/smtp in logs
- Exploratory: `size=60` 200; `size=61`/`page=0` 400; catalog `/categories` and `/products?size=5` still 200 `total=18`; unknown path 404 ProblemDetail; health UP; Flyway V1–V5; 3 articles / 7 pages; port 18081 free after stop
- Bug (FAIL only): n/a

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 09:55 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-001] READY_FOR_DEPLOY |
| 2026-09-24 09:57 | READY | IN_PROGRESS | BE | branch feature/TASK-003-news-pages-api |
| 2026-09-24 10:00 | IN_PROGRESS | CODE_REVIEW | BE | product commit 571eb47; Implementation Iteration 1 |
| 2026-09-24 10:03 | CODE_REVIEW | MERGED | SA | merge_commit=a8b6f11; reviews/TASK-003-round-1.md APPROVED; --no-ff on main |
| 2026-09-24 10:07 | MERGED | TESTING | TEST | run 1; tested sha a8b6f11 is ancestor of main containing merge_commit a8b6f11 |
| 2026-09-24 10:09 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-003-run-1.md PASS; every AC-001..AC-005 checked; tested sha a8b6f11 |
