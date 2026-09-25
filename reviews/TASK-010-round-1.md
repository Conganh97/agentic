---
task: TASK-010
round: 1
decision: APPROVED
branch: feature/TASK-010-downloader-service-skeleton
sha: d77a24778f7674f31425e658eeba28b7ebbdd975
updated: 2026-09-25 16:55
---

# TASK-010 Review Round 1

Reviewed: `feature/TASK-010-downloader-service-skeleton` @ `d77a24778f7674f31425e658eeba28b7ebbdd975` · Build/tests: `./mvnw -q verify` PASS (4)

`project.md` verify: registry row `video-downloader-service` · type BE · path `product/services/video-downloader-service` · remote `https://github.com/Conganh97/product-video-downloader-service`. Stack Java 21 + Boot 4.0.8 + springdoc 3.0.3 matches design §5 / ADR-0012. Package `com.product.videodownloader` with `shared/config` only.

Contract-vs-API: ops paths `GET /actuator/health` and `GET /v3/api-docs` match design §6. No `/api/v1` download controllers (correct for this increment). Empty OpenAPI is acceptable until later controllers. `server.port: ${SERVER_PORT:18082}` matches compose (`SERVER_PORT=8080` in container, host 18082). JSON ECS console logs wired; download fields (`downloadId`, source host, outcome, `errorCode`) stay TASK-017. DB health stays TASK-011.

| # | File | Severity | Comment |
|---|------|----------|---------|
| 1 | src/test/java/com/product/videodownloader/ServiceSkeletonTest.java | MINOR | AC-001 asserts context load + yaml port default, not a bound HTTP port (Boot 4 MockMvc; compose image start not exercised) |
| 2 | application.yaml | MINOR | springdoc warns `/v3/api-docs` and Swagger UI are on in all profiles; ADR-0012 says non-prod — acceptable while APIs stay compose-network-only |

Merged `8f11a3c29f25f63ef053afcb20fb27ff3f95a26c`.
