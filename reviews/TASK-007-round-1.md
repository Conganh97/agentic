---
task: TASK-007
round: 1
decision: APPROVED
branch: feature/TASK-007-crawler-reliability
sha: e276e04312887c921aa1d1e6ff28617a0203cecc
updated: 2026-09-25 15:36
---

# TASK-007 Review Round 1

Reviewed: `feature/TASK-007-crawler-reliability` @ `e276e04312887c921aa1d1e6ff28617a0203cecc` · Build/tests: `./mvnw -q verify` PASS (62)

`project.md` verify: registry row `douyin-crawler-service` · type BE · path `product/services/douyin-crawler-service` · remote `https://github.com/Conganh97/product-douyin-crawler-service`. Stack Java 21 + Boot 4 + `RestClient` + in-process token bucket / semaphore / retry (no Redis, no Resilience4j) matches design §5. Package-by-feature `discovery/infrastructure` + `shared/config`.

FR-8 / NFR-4: `DiscoveryHttpGuard` retries timeout / 429 / 5xx only up to `crawler.retry.max-attempts=3` (total attempts) with backoff `1s` × `multiplier=2`. 401/403/captcha-like / other 4xx stay permanent (FR-15). FR-9 / NFR-1: `crawler.rate.requests-per-second=1`, `crawler.concurrency=4`, `crawler.http.timeout=10s` bound RestClient connect/read. FR-14 / NFR-11 / AC-032–033: public GET only; no video-byte download, no media/AI, no Cookie / Authorization / `msToken` / `a_bogus` / CAPTCHA solver. POM unchanged.

Implementation-level AC coverage on the branch: AC-014 (503 then success; timeout/429/5xx retry cap), AC-015 (401/403/captcha/400 and non-timeout I/O not retried), AC-016 (property bind + semaphore + token bucket), AC-032/033 (source bounds + WireMock public GET).

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | CrawlerProperties.java | MINOR | `crawler.discovery.timeout` remains; RestClient now uses `crawler.http.timeout` |
| 2 | DiscoveryHttpGuard.java | MINOR | `max-attempts=3` is total attempts, so the 4s backoff step is never slept |

Merged `3f1d0d4e31239489c3dab81eefe535ce03119a00`.
