---
id: TASK-011
title: News, policy pages and contact UI
type: TASK
priority: CRITICAL
status: TESTING
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-003, TASK-006]
sprint:
branch: feature/TASK-011-news-pages-contact-ui
merge_commit: 580b15c
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
updated: 2026-09-24 10:37
---

## Description

News listing and article detail, seven information pages, and the contact page (settings + form).
Footer and nav must reach every page slug.

## Acceptance Criteria
- [ ] AC-001 `/news` lists articles (title, excerpt, optional image) from `GET /api/v1/articles`;
      a row opens `/news/:slug`
- [ ] AC-002 `/news/:slug` shows title and content; prev/next or back-to-list anchors work;
      missing slug shows `Alert`
- [ ] AC-003 `/pages/about`, `/pages/shipping`, `/pages/privacy`, `/pages/warranty`,
      `/pages/terms`, `/pages/shopping-guide` each render `title` + body from the API (plain text
      `Text` paragraphs; no `dangerouslySetInnerHTML`)
- [ ] AC-004 `/contact` shows hotline, email, Zalo from `/shop/settings` and a Mantine form
      (name, email, phone, message) that POSTs `/api/v1/contact` and toasts on 202
- [ ] AC-005 RTL tests for news list, article detail, one policy page, and contact validation
      error; footer links include all of the above

## Design (SA)
See `docs/design/REQ-001-design.md` §13 (FR-10, FR-11, FR-12). Repo: frontend (existing).
- Mantine: `SimpleGrid`/`Card` news, `Title`, `Image`, `Stack` form, `TextInput`, `Textarea`,
  `Anchor` tel/Zalo, `notifications`.
- Home news teaser may be completed here if TASK-007 left a placeholder.
- Original seed copy only.

## Implementation (BE/FE)
### Iteration 1 (initial)
- Branch: `feature/TASK-011-news-pages-contact-ui` @ 49a6757
- Changed: `frontend/src/api/content.ts`, `frontend/src/features/content/*`, `frontend/src/app/router.tsx`, `frontend/src/features/catalog/HomePage.tsx`
- Tests: `npm run lint && npm run format:check && npm test -- --run && npm run build` → pass (37 tests)
- Notes: List cards use `ThemeIcon` `IconPhoto` because `GET /articles` cards have no `imageUrl` (detail still shows `Image` when present). Home news teaser added (TASK-007 had none); `Badge` “Tin tức”. Copy: “Tin tức”, “Về danh sách tin”, “Bài trước” / “Bài sau”, “Không tìm thấy bài viết”, “Chưa có bài viết”; form “Họ tên”, “Email”, “Số điện thoại”, “Nội dung”, “Gửi”; toast “Đã nhận liên hệ” (does not claim email was sent). `/pages/:slug` covers AC-003 slugs; API also has `/pages/contact` but the form lives at `/contact`. Branch pushed.

## Review (SA)
### Round 1 — APPROVED
Reviewed: feature/TASK-011-news-pages-contact-ui @ 49a6757 · Build/tests: npm run lint && npm run format:check && npm test -- --run && npm run build PASS (37 tests)
No comments.

Merged 580b15c.
Pushed main.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 10:15 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-003, TASK-006] READY_FOR_DEPLOY |
| 2026-09-24 10:28 | READY | IN_PROGRESS | FE | branch feature/TASK-011-news-pages-contact-ui |
| 2026-09-24 10:31 | IN_PROGRESS | CODE_REVIEW | FE | product 49a6757; Implementation Iteration 1 |
| 2026-09-24 10:35 | CODE_REVIEW | MERGED | SA | approved round 1; merge_commit=580b15c |
| 2026-09-24 10:37 | MERGED | TESTING | TEST | run 1; tested sha 580b15c is ancestor of main containing merge_commit 580b15c |
