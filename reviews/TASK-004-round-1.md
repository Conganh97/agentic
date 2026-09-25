---
task: TASK-004
round: 1
decision: APPROVED
branch: feature/TASK-004-discovery-provider
sha: 710f929e83d16570f25ee23f73bd9f2f2999c979
updated: 2026-09-25 15:08
---

# TASK-004 Review Round 1

Reviewed: `feature/TASK-004-discovery-provider` @ `710f929e83d16570f25ee23f73bd9f2f2999c979` · Build/tests: `./mvnw -q verify` PASS (30)

`project.md` verify: registry row `douyin-crawler-service` · type BE · path `product/services/douyin-crawler-service` · remote `https://github.com/Conganh97/product-douyin-crawler-service`. Stack Java 21 + Boot 4.0.8 + `RestClient` matches design §5. Package-by-feature `discovery/{application,domain,infrastructure}`.

Port vs §6: `VideoDiscoveryProvider.discover(DiscoveryRequest)` → `DiscoveryResult` (videos + item failures + optional provider failure). Strategy v1 `KEYWORD` only. `DiscoveredVideo` carries FR-5 / §6 required fields (nullable when the public source omits them) plus optional hashtags/music/location/engagement.

FR-12/13: `crawler.provider=mock` in `src/test/resources/application.properties` and yaml; `DiscoveryConfiguration` wires mock by default (`matchIfMissing=true`). Application (`DiscoverVideosService`) depends on the port only. HTTP impl is unauthenticated public GET via `RestClient`; 401/403/captcha-like HTML → permanent provider failure; tests assert no Cookie / `msToken` / `a_bogus` / `X-Bogus`. Tests use mock + WireMock; they do not call Douyin.

Implementation-level AC coverage on the branch: AC-004 (KEYWORD + WireMock GET), AC-005 (parser maps available fields, nulls missing), AC-028/029 (mock default, no Douyin account), AC-031 (port + application source isolation).

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | DiscoverVideosServiceTest.java | MINOR | `getPackageName().doesNotContain(PublicKeyword…)` is tautological; `DiscoveryApplicationIsolationTest` is the real FR-13 check |
| 2 | DiscoveryProviderWiringTest.java | MINOR | `getBeansOfType(PublicKeywordDiscoveryProvider)` is empty because the `@Bean` return type is the port; `instanceof MockVideoDiscoveryProvider` is the real default-provider assertion |

Merged `8088e33e0cfa4c7490c984dd320e058dac58f919`.
