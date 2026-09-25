---
task: TASK-007
run: 1
verdict: PASS
tested_sha: 3f1d0d4e31239489c3dab81eefe535ce03119a00
merge_commit: 3f1d0d4e31239489c3dab81eefe535ce03119a00
updated: 2026-09-25 15:38
---

# TASK-007 Test Run 1

- Tested: `main` @ `3f1d0d4e31239489c3dab81eefe535ce03119a00` (contains `merge_commit`; product HEAD)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS (`VERIFY_EXIT=0`; 62 tests, Failures: 0, Errors: 0, Skipped: 0)
- Docker: up (Testcontainers `postgres:16-alpine`, PostgreSQL 16.15) for Spring wiring + TASK-002/003/005 regression ITs
- Discovery HTTP tests used WireMock + in-process unit doubles only; no live Douyin GET. No service process started. Product tree left clean.

| AC | Result | Evidence |
|----|--------|----------|
| AC-014 | PASS | `./mvnw -q verify` Surefire `DiscoveryHttpGuardTest` Tests run: 6, Failures: 0. `ac014_retriesTimeout429And5xxUpToMaxAttempts`: timeout then `http-429` then `http-503` → 3 attempts (`crawler.retry.max-attempts=3`); last result `http-503` transient. `ac014_stopsRetryingAfterTransientSuccess`: `http-500` then success → 2 attempts. `PublicKeywordDiscoveryProviderTest#ac014_retriesTransient500ThenSucceeds`: WireMock scenario 500 then JSON → 2 GETs `/search/cats`, video id `9`. Defaults in `application.yaml`: `crawler.retry.max-attempts: 3`, `initial-backoff: 1s`, `multiplier: 2`. |
| AC-015 | PASS | Same verify. `DiscoveryHttpGuardTest#ac015_doesNotRetryPermanentFailures`: `http-401`, `http-403`, `captcha`, `http-400` each attempted once and `hasPermanentProviderFailure()`. `ac015_doesNotRetryNonTimeoutIo`: `ResourceAccessException("connection refused")` thrown after 1 attempt. `PublicKeywordDiscoveryProviderTest#ac015_doesNotRetry401`: WireMock 401 → 1 GET, permanent. Captcha-like HTML (`id="captcha"` / geetest) → permanent `captcha` (not solved). |
| AC-016 | PASS | Same verify. `DiscoveryHttpGuardTest#ac016_concurrencyLimitsInFlightCalls`: semaphore 1; second call does not enter until first releases. `ac016_rateLimiterIsConfigurable`: `TokenBucketRateLimiter(2.0)` third acquire waits ~500 ms. `application.yaml` + `CrawlerProperties`: `crawler.rate.requests-per-second: 1`, `crawler.concurrency: 4`, `crawler.http.timeout: 10s`. No Redis / Resilience4j in `pom.xml`. |
| AC-032 | PASS | Same verify. `CrawlerReliabilityBoundsTest#ac032_sourcesDoNotDownloadVideoOrAddMediaAi` Tests run: 2 (with AC-033), Failures: 0: every `src/main/java` file lacks `ffmpeg`, `whisper`, `openai`, `langchain`, `downloadVideo`, `video/mp4`, `application/octet-stream`; provider methods exclude `download` / `transcribe` / `embed`. Independent TEST grep of `src/main` found no download/AI tokens; `DouyinPublicSearchParser.decodeEmbedded` is HTML/JSON parse only. |
| AC-033 | PASS | Same verify. `CrawlerReliabilityBoundsTest#ac033_sourcesStayPublicGetWithoutBypass`: `PublicKeywordDiscoveryProvider` contains `.get()`, `status == 401 \|\| status == 403`, `isCaptchaLike`; lacks `.post(`/`.put(`/`.delete(`, `setBearerAuth`, `Authorization`, `Cookie`, `msToken`, `a_bogus`, `X-Bogus`, `2captcha`, `anticaptcha`. `PublicKeywordDiscoveryProviderTest#ac004_ac028_discoversFromPublicGetAgainstWireMock`: Cookie/Authorization/msToken/a_bogus/X-Bogus absent; `wireMock.baseUrl()` does not contain `douyin.com`. `src/test/resources/application.properties`: `crawler.provider=mock`. Captcha regex is detect-and-fail-permanent, not a solver. |

Exploratory: Retry only timeout / 429 / 5xx (NFR-4). Non-timeout IO is not retried. `geetest` appears only in captcha-detection regex. TASK-002/003/004/005 suites still pass (62 total). No PII in test logs. Live Douyin was not called.

Bug (FAIL): none
