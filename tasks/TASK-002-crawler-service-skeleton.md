---
id: TASK-002
title: Service skeleton with health, logs, and OpenAPI
type: TASK
priority: HIGH
status: RELEASED
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
branch: feature/TASK-002-crawler-service-skeleton
merge_commit: 9d951ba14568ca1c6fa5eaf84c7317407b47c178
release: DEV
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
updated: 2026-09-25 16:11
---

## Description

Scaffold `product/services/douyin-crawler-service` as a Java 21 Spring Boot 4 Maven app
(`com.product.douyincrawler`), package-by-feature with `shared` only. Enable Actuator health,
structured JSON logs, and springdoc OpenAPI. `server.port: ${SERVER_PORT:18081}`. The process
must start from the documented local setup (compose + `SERVER_PORT`). No crawl or video
features yet.

## Acceptance Criteria
- [x] AC-001 The service can start successfully using the documented local development setup.
- [x] AC-022 Application logs are structured and contain sufficient information to investigate crawl failures.
- [x] AC-024 Application health checks are available.
- [x] AC-025 APIs are documented through OpenAPI.

## Design (SA)

`docs/design/REQ-001-design.md` §5 Stack, §6 ops paths, FR-1, NFR-6, NFR-8, NFR-9, ADR-0012.
`GET /actuator/health`, `GET /v3/api-docs`. Structured logging via Boot (no PII). Empty OpenAPI
until later controllers appear is acceptable if the endpoint is live. AC-001 is demonstrated
here (this task scaffolds the app), not on TASK-001. Crawl-specific log fields (`jobId`,
`sourceVideoId`, outcome) are emitted by TASK-006; this task provides the JSON logging stack.

## Implementation (BE/FE)

### Iteration 1 (skeleton)
- Branch: `feature/TASK-002-crawler-service-skeleton` @ 523e282
- Changed: `pom.xml`, `src/main/java/com/product/douyincrawler/`, `shared/config/OpenApiConfiguration.java`, `application.yaml`, `ServiceSkeletonTest.java`, `README.md`
- Tests: `./mvnw -q verify` → pass (4)
- Notes: Java 21 / Boot 4.0.8 / springdoc 3.0.3. Actuator health + ECS JSON console logs + `/v3/api-docs`. No crawl/video, no datasource (db health comes with TASK-003). Crawl log fields stay TASK-006.

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

### Round 1 — APPROVED
Reviewed: feature/TASK-002-crawler-service-skeleton @ `523e282b4fddd27778e9bf9e1a8a084834f9282e` · Build/tests: `./mvnw -q verify` PASS (4)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | ServiceSkeletonTest.java | MINOR | AC-001 asserts context + yaml port, not a bound HTTP port |
| 2 | application.yaml | MINOR | springdoc UI/docs on in all profiles; ADR-0012 says non-prod |

Merged `9d951ba14568ca1c6fa5eaf84c7317407b47c178`.

## Test (TEST)

### Run 1 — PASS
- Tested: main @ 9d951ba14568ca1c6fa5eaf84c7317407b47c178 (contains merge_commit)
- Build/tests: `./mvnw -q verify` PASS
- AC-001 pass — `SERVER_PORT=18081 ./mvnw spring-boot:run` → Started DouyinCrawlerApplication; Tomcat 18081
- AC-022 pass — ECS JSON console (`ecs.version=8.11`, `@timestamp`, `log.level`, `service.name`); crawl fields TASK-006
- AC-024 pass — `GET /actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}`
- AC-025 pass — `GET /v3/api-docs` → 200 OpenAPI 3.1.0 empty `paths`
- Evidence: `tests/TASK-002-run-1.md`

## Deployment (DEVOPS)

### DEV — 2026-09-25 16:11 — OK
- Images: `ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1` and `:dev`
- Command: `python3 scripts/deploy.py --env DEV --component douyin-crawler-service`
- Smoke: `http://127.0.0.1:18081/actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}`
- Rollback: `docker compose -f ops/compose/dev.yml up -d` with the previous tag

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 14:40 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-001] MERGED |
| 2026-09-25 14:42 | READY | IN_PROGRESS | BE | branch feature/TASK-002-crawler-service-skeleton |
| 2026-09-25 14:44 | IN_PROGRESS | CODE_REVIEW | BE | product sha 523e282; Implementation iteration 1; ./mvnw -q verify pass (4) |
| 2026-09-25 14:46 | CODE_REVIEW | MERGED | SA | review round 1 APPROVED; merge_commit=9d951ba14568ca1c6fa5eaf84c7317407b47c178 --no-ff parents 70231b2 + 523e282; reviews/TASK-002-round-1.md |
| 2026-09-25 14:47 | MERGED | TESTING | TEST | tested sha 9d951ba14568ca1c6fa5eaf84c7317407b47c178 is main HEAD and contains merge_commit; run 1 started |
| 2026-09-25 14:48 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-002-run-1.md PASS; AC-001 AC-022 AC-024 AC-025 checked; ./mvnw -q verify PASS; health+openapi 200 |
| 2026-09-25 16:07 | READY_FOR_DEPLOY | DEPLOYING | DEVOPS | DEV deploy started; PQA accept APPROVED docs/design/reviews/REQ-001-accept-1.md; python3 scripts/deploy.py --env DEV --component douyin-crawler-service |
| 2026-09-25 16:11 | DEPLOYING | RELEASED | DEVOPS | DEV compose up OK; image ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1; smoke GET http://127.0.0.1:18081/actuator/health → 200 status=UP; release=DEV |
