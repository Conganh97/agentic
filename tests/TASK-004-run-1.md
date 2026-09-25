---
task: TASK-004
run: 1
verdict: PASS
tested_sha: 8088e33e0cfa4c7490c984dd320e058dac58f919
merge_commit: 8088e33e0cfa4c7490c984dd320e058dac58f919
updated: 2026-09-25 15:10
---

# TASK-004 Test Run 1

- Tested: `main` @ `8088e33e0cfa4c7490c984dd320e058dac58f919` (contains `merge_commit`; product HEAD)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (`VERIFY_EXIT=0`; 30 tests, Failures: 0, Errors: 0, Skipped: 0)
- Docker: up (Testcontainers `postgres:16-alpine`, PostgreSQL 16.15) for Spring wiring + TASK-003 regression ITs
- Discovery is a domain port (no REST). No service process started. Tests used mock + WireMock only; no live Douyin GET. Product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-004 | PASS | `./mvnw -q verify` Surefire `DiscoveryRequestTest` Tests run: 2; `MockVideoDiscoveryProviderTest` Tests run: 2; `PublicKeywordDiscoveryProviderTest` Tests run: 4 — all Failures: 0. KEYWORD strategy accepted (`ac004_acceptsKeywordStrategyAndTrimsKeyword`). Mock `discover(KEYWORD, "cats", 2)` returns 2 deterministic `DOUYIN` videos (`mock-cats-1`, `mock-cats-2`). WireMock public GET `/search/cats` (base URL does not contain `douyin.com`) maps `aweme_id=7123456789`. 401 → `http-401` permanent; 403 → `http-403` permanent; captcha-like HTML → `captcha` permanent. Live Douyin captcha is not a product fail. |
| AC-005 | PASS | Same verify. `MockVideoDiscoveryProviderTest#ac005_populatesRequiredMetadataWhenAvailable`: source, sourceVideoId, canonicalUrl, authorId, authorName, title, publishedAt, durationSeconds, coverImageUrl, like/comment/share/collect counts present. `DouyinPublicSearchParserTest` Tests run: 3, Failures: 0: `ac005_mapsRequiredFieldsFromPublicAwemeJson` maps design §6 fields from public JSON (id, URL, author, title, publishedAt, duration 15s, cover, metrics, hashtags, music, location); `ac005_mapsEncodedRenderDataAndLeavesMissingFieldsNull` leaves omitted fields null; missing id+URL → permanent item failure. |
| AC-028 | PASS | Same verify. `DiscoveryProviderWiringTest#ac028_integrationDiscoverDoesNotNeedADouyinAccount` → 2 mock videos, ids start with `mock-`, no provider failure. `PublicKeywordDiscoveryProviderTest#ac004_ac028_discoversFromPublicGetAgainstWireMock` uses WireMock only (`Cookie`/`msToken`/`a_bogus`/`X-Bogus` absent). `src/test/resources/application.properties`: `crawler.provider=mock`. No Douyin account or live host. |
| AC-029 | PASS | Same verify. `DiscoveryProviderWiringTest#ac029_defaultTestProviderIsMock`: `crawler.provider=mock`; injected `VideoDiscoveryProvider` is `MockVideoDiscoveryProvider`; no `PublicKeywordDiscoveryProvider` bean. `MockVideoDiscoveryProviderTest#ac004_ac029_discoversDeterministicKeywordVideos`: two identical `discover` calls return the same list. |
| AC-031 | PASS | Same verify. `DiscoverVideosServiceTest#ac031_delegatesToPortAndDoesNotDependOnHttpClass` Tests run: 1: application ctor takes only `VideoDiscoveryProvider`. `DiscoveryApplicationIsolationTest#ac031_applicationSourcesDoNotImportHttpProvider` Tests run: 1: `discovery/application` sources do not contain `PublicKeywordDiscoveryProvider`, `discovery.infrastructure`, or `RestClient`. |

Exploratory: 401/403/captcha-like HTML are permanent provider failures (no cookie/signature/CAPTCHA bypass). Missing public identifiers become item failures, not invented IDs. TASK-002 `ServiceSkeletonTest` Tests run: 4 and TASK-003 persistence suites (5+2+3+1) still pass. No PII in test logs.

Bug (FAIL): none
