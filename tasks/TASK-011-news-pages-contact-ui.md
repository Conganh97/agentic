---
id: TASK-011
title: News, policy pages and contact UI
type: TASK
priority: CRITICAL
status: IN_PROGRESS
assignee: FE
parent: REQ-001
requirement_revision: 1
repo: frontend
depends_on: [TASK-003, TASK-006]
sprint:
branch: feature/TASK-011-news-pages-contact-ui
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
updated: 2026-09-24 10:28
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

## Review (SA)

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-24 09:15 | — | BACKLOG | SA | Created from REQ-001 design |
| 2026-09-24 10:15 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-003, TASK-006] READY_FOR_DEPLOY |
| 2026-09-24 10:28 | READY | IN_PROGRESS | FE | branch feature/TASK-011-news-pages-contact-ui |
