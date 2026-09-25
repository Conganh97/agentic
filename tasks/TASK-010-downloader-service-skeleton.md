---
id: TASK-010
title: Service skeleton with health, logs, and OpenAPI
type: TASK
priority: HIGH
status: CODE_REVIEW
assignee: BE
parent: REQ-002
requirement_revision: 1
repo: video-downloader-service
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: [TASK-009]
sprint: SPRINT-05
branch: feature/TASK-010-downloader-service-skeleton
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
updated: 2026-09-25 16:53
---

## Description

Scaffold `product/services/video-downloader-service` as a Java 21 Spring Boot 4 Maven app
(`com.product.videodownloader`), package-by-feature with `shared` only. Enable Actuator health,
structured JSON logs, and springdoc OpenAPI. `server.port: ${SERVER_PORT:18082}`. The process
must start from the documented local setup (compose + `SERVER_PORT`). No download or storage
features yet.

## Acceptance Criteria
- [ ] AC-001 The service can start successfully using the documented local development setup.
- [ ] AC-038 Structured logs are available.
- [ ] AC-040 Health checks are available.
- [ ] AC-041 OpenAPI documentation is available.

## Design (SA)

`docs/design/REQ-002-design.md` §5 Stack, §6 ops paths, FR-1, FR-14 (stack), NFR-5 (logging stack),
NFR-7 (process), NFR-8, ADR-0012. `GET /actuator/health`, `GET /v3/api-docs`. Structured logging via
Boot (no secrets). Empty OpenAPI until later controllers appear is acceptable if the endpoint is
live. AC-001 is demonstrated here, not on TASK-009. Download-specific log fields are emitted by
TASK-017; this task provides the JSON logging stack. DB health arrives with TASK-011.

## Implementation (BE/FE)

### Iteration 1 (skeleton)
- Branch: `feature/TASK-010-downloader-service-skeleton` @ d77a24778f7674f31425e658eeba28b7ebbdd975
- Changed: `pom.xml`, `src/main/java/com/product/videodownloader/`, `shared/config/OpenApiConfiguration.java`, `shared/config/RestClientConfiguration.java`, `application.yaml`, `ServiceSkeletonTest.java`, `README.md`
- Tests: `./mvnw -q verify` → pass (4)
- Notes: Java 21 / Boot 4.0.8 / springdoc 3.0.3. Actuator health + ECS JSON console logs + `/v3/api-docs`. `spring-boot-starter-restclient` plus `RestClient.Builder` `@ConditionalOnMissingBean` in shared config. No download/storage, no datasource (db health TASK-011). Download log fields stay TASK-017.

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 16:33 | — | BACKLOG | SA | Created from REQ-002 design revision 1 hash b06116020682e658 |
| 2026-09-25 16:51 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-009] MERGED |
| 2026-09-25 16:52 | READY | IN_PROGRESS | BE | branch feature/TASK-010-downloader-service-skeleton |
| 2026-09-25 16:53 | IN_PROGRESS | CODE_REVIEW | BE | product sha d77a24778f7674f31425e658eeba28b7ebbdd975; Implementation iteration 1; ./mvnw -q verify pass (4) |
