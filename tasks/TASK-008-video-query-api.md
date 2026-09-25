---
id: TASK-008
title: Video query API, keyset pagination, and crawl integration tests
type: TASK
priority: HIGH
status: BACKLOG
assignee: BE
parent: REQ-001
requirement_revision: 1
repo: douyin-crawler-service
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: [TASK-003, TASK-006]
sprint:
branch:
merge_commit:
release:
review_iteration: 0
uxui_review_iteration: 0
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
updated: 2026-09-25 14:26
---

## Description

Add `GET /api/v1/videos` and `GET /api/v1/videos/{id}` with keyset pagination (no `COUNT(*)` on
`video` for normal paging). Freeze the REST contract for later orchestration. Add Testcontainers
integration tests that run a crawl job (mock provider) and then query persisted videos.

## Acceptance Criteria
- [ ] AC-018 Crawled videos can be queried through an API.
- [ ] AC-019 Video querying supports pagination.
- [ ] AC-020 The implementation does not depend on expensive full-table COUNT queries for normal high-volume pagination.
- [ ] AC-027 Integration tests verify PostgreSQL persistence and crawl-job behaviour.
- [ ] AC-034 The service exposes a stable contract that can later be consumed by an orchestration layer such as n8n.

## Design (SA)

`docs/design/REQ-001-design.md` §6 video endpoints, NFR-3, NFR-10, FR-10. Cursor on
`(crawled_at DESC, id DESC)`. Default limit 20, max 100. OpenAPI must document these paths.
Integration tests: Testcontainers + `crawler.provider=mock` only.

## Implementation (BE/FE)

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
