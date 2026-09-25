---
id: TASK-002
title: Service skeleton with health, logs, and OpenAPI
type: TASK
priority: HIGH
status: READY
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
depends_on: [TASK-001]
sprint: SPRINT-02
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
updated: 2026-09-25 14:40
---

## Description

Scaffold `product/services/douyin-crawler-service` as a Java 21 Spring Boot 4 Maven app
(`com.product.douyincrawler`), package-by-feature with `shared` only. Enable Actuator health,
structured JSON logs, and springdoc OpenAPI. `server.port: ${SERVER_PORT:18081}`. The process
must start from the documented local setup (compose + `SERVER_PORT`). No crawl or video
features yet.

## Acceptance Criteria
- [ ] AC-001 The service can start successfully using the documented local development setup.
- [ ] AC-022 Application logs are structured and contain sufficient information to investigate crawl failures.
- [ ] AC-024 Application health checks are available.
- [ ] AC-025 APIs are documented through OpenAPI.

## Design (SA)

`docs/design/REQ-001-design.md` §5 Stack, §6 ops paths, FR-1, NFR-6, NFR-8, NFR-9, ADR-0012.
`GET /actuator/health`, `GET /v3/api-docs`. Structured logging via Boot (no PII). Empty OpenAPI
until later controllers appear is acceptable if the endpoint is live. AC-001 is demonstrated
here (this task scaffolds the app), not on TASK-001. Crawl-specific log fields (`jobId`,
`sourceVideoId`, outcome) are emitted by TASK-006; this task provides the JSON logging stack.

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
| 2026-09-25 14:40 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-001] MERGED |
