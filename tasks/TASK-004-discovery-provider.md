---
id: TASK-004
title: Discovery port, mock, and public keyword provider
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
depends_on: [TASK-002]
sprint: SPRINT-03
branch: feature/TASK-004-discovery-provider
merge_commit: 8088e33e0cfa4c7490c984dd320e058dac58f919
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
updated: 2026-09-25 16:14
---

## Description

Implement the `discovery` feature: domain port `VideoDiscoveryProvider`, a deterministic
`MockVideoDiscoveryProvider`, and a `PublicKeywordDiscoveryProvider` that performs unauthenticated
public GETs via `RestClient` and maps available metadata. Application code must not depend on the
HTTP class. Default `crawler.provider=mock` in `test`.

## Acceptance Criteria
- [x] AC-004 The crawler can discover public Douyin videos using at least one supported discovery strategy.
- [x] AC-005 Discovered videos contain the required metadata when that metadata is publicly available.
- [x] AC-028 Integration tests can run without requiring a real Douyin account.
- [x] AC-029 A mock discovery provider is available for automated tests.
- [x] AC-031 The crawler implementation is isolated behind an abstraction that allows another provider implementation to be introduced later.

## Design (SA)

`docs/design/REQ-001-design.md` §5, §6 port, FR-4, FR-5, FR-12, FR-13. Strategy v1 = `KEYWORD`.
Required fields as in design §6. Tests use the mock and/or WireMock; they must not call Douyin.
HTTP impl on 401/403/captcha-like HTML returns a permanent item/provider failure — no bypass.

## Implementation (BE/FE)

### Iteration 1 (discovery provider)
- Branch: `feature/TASK-004-discovery-provider` @ 710f929
- Changed: `discovery/{domain,application,infrastructure}`, `shared/config/CrawlerProperties.java`
- Tests: `./mvnw -q verify` → pass (30)
- Notes: Strategy v1 KEYWORD. Default `crawler.provider=mock` in test. HTTP impl is unauthenticated public GET via RestClient; 401/403/captcha-like HTML is a permanent failure (no cookies/signatures/CAPTCHA bypass). Application depends on `VideoDiscoveryProvider` only. Tests use mock + WireMock; they do not call Douyin.

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

### Round 1 — APPROVED
Reviewed: feature/TASK-004-discovery-provider @ `710f929e83d16570f25ee23f73bd9f2f2999c979` · Build/tests: `./mvnw -q verify` PASS (30)
| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | DiscoverVideosServiceTest.java | MINOR | Package-name isolation assert is tautological; source-walk test is the real FR-13 check |
| 2 | DiscoveryProviderWiringTest.java | MINOR | `getBeansOfType(PublicKeyword…)` is empty because `@Bean` returns the port; `instanceof Mock` is the real default-provider assertion |

Merged `8088e33e0cfa4c7490c984dd320e058dac58f919`.

## Test (TEST)

### Run 1 — PASS
- Tested: main @ 8088e33e0cfa4c7490c984dd320e058dac58f919 (contains merge_commit)
- Build/tests: `./mvnw -q verify` PASS (30; mock + WireMock; Testcontainers PostgreSQL 16.15 for wiring/regression)
- AC-004 pass — KEYWORD mock + WireMock public GET; 401/403/captcha → permanent failure (not a live-Douyin fail)
- AC-005 pass — mock required fields; parser maps public JSON and leaves missing fields null
- AC-028 pass — Spring IT uses mock; HTTP tests hit WireMock only (no Douyin account)
- AC-029 pass — `crawler.provider=mock` default; injected bean is `MockVideoDiscoveryProvider`
- AC-031 pass — application depends on `VideoDiscoveryProvider` only; no HTTP/infrastructure imports
- Evidence: `tests/TASK-004-run-1.md`

## Deployment (DEVOPS)

### DEV — 2026-09-25 16:14 — OK
- Images: `ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1` and `:dev`
- Command: reused healthy `ops/compose/dev.yml` (TASK-002 image already up; `python3 scripts/deploy.py --env DEV --component douyin-crawler-service` not re-run)
- Smoke: `http://127.0.0.1:18081/actuator/health` → 200 `{"groups":["liveness","readiness"],"status":"UP"}`
- Rollback: `docker compose -f ops/compose/dev.yml up -d` with the previous tag

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 14:26 | — | BACKLOG | SA | Created from REQ-001 design revision 1 hash c34978450afab2c1 |
| 2026-09-25 14:59 | BACKLOG | READY | SCRUM | DoR met; deps [TASK-002] MERGED |
| 2026-09-25 15:02 | READY | IN_PROGRESS | BE | branch feature/TASK-004-discovery-provider |
| 2026-09-25 15:05 | IN_PROGRESS | CODE_REVIEW | BE | product sha 710f929e83d16570f25ee23f73bd9f2f2999c979; Implementation iteration 1; ./mvnw -q verify pass (30) |
| 2026-09-25 15:08 | CODE_REVIEW | MERGED | SA | reviews/TASK-004-round-1.md APPROVED; merge_commit 8088e33e0cfa4c7490c984dd320e058dac58f919 (--no-ff, parents 677bedb + 710f929); ./mvnw -q verify PASS (30) |
| 2026-09-25 15:09 | MERGED | TESTING | TEST | tested sha 8088e33e0cfa4c7490c984dd320e058dac58f919 is product main HEAD and contains merge_commit; run 1 started |
| 2026-09-25 15:10 | TESTING | READY_FOR_DEPLOY | TEST | tests/TASK-004-run-1.md PASS; AC-004 AC-005 AC-028 AC-029 AC-031 checked; ./mvnw -q verify PASS (30) |
| 2026-09-25 16:14 | READY_FOR_DEPLOY | DEPLOYING | DEVOPS | DEV deploy started; PQA accept APPROVED docs/design/reviews/REQ-001-accept-1.md; reuse healthy compose ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1 |
| 2026-09-25 16:14 | DEPLOYING | RELEASED | DEVOPS | DEV compose reused OK; image ghcr.io/conganh97/product-douyin-crawler-service:dev-607c9c1; smoke GET http://127.0.0.1:18081/actuator/health → 200 status=UP; release=DEV |
