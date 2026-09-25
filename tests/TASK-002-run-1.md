---
task: TASK-002
run: 1
verdict: PASS
tested_sha: 9d951ba14568ca1c6fa5eaf84c7317407b47c178
merge_commit: 9d951ba14568ca1c6fa5eaf84c7317407b47c178
updated: 2026-09-25 14:48
---

# TASK-002 Test Run 1

- Tested: `main` @ `9d951ba14568ca1c6fa5eaf84c7317407b47c178` (contains `merge_commit`)
- Build/tests: `export JAVA_HOME=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home && ./mvnw -q verify` PASS
- Docker: down; used documented `SERVER_PORT=18081 ./mvnw spring-boot:run` (not compose)
- Process stopped after probes; product tree clean

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | Documented README/`project.md` setup: `JAVA_HOME=…/openjdk…/Home` `SERVER_PORT=18081 ./mvnw spring-boot:run` → ECS log `Started DouyinCrawlerApplication in 1.244 seconds`; `Tomcat started on port 18081`; `nc -z localhost 18081` succeeded |
| AC-022 | PASS | Console logs are ECS JSON (`logging.structured.format.console: ecs`). Sample: `{"@timestamp":"2026-09-25T07:48:04.622199Z","log":{"level":"INFO","logger":"com.product.douyincrawler.DouyinCrawlerApplication"},"process":{"pid":31985,"thread":{"name":"main"}},"service":{"name":"douyin-crawler-service","node":{}},"message":"Started DouyinCrawlerApplication in 1.244 seconds (process running for 1.409)","tags":["COMMONS-LOGGING"],"ecs":{"version":"8.11"}}`. Crawl fields `jobId` / `sourceVideoId` / outcome are TASK-006 |
| AC-024 | PASS | `curl -sS -D - http://localhost:18081/actuator/health` → HTTP 200 `{"groups":["liveness","readiness"],"status":"UP"}` |
| AC-025 | PASS | `curl -sS -D - http://localhost:18081/v3/api-docs` → HTTP 200 `{"openapi":"3.1.0","info":{"title":"douyin-crawler-service","description":"Public Douyin video metadata crawler","version":"0.0.1"},"servers":[{"url":"http://localhost:18081","description":"Generated server url"}],"paths":{},"components":{}}` (empty paths acceptable per design) |

Exploratory: no crawl/video routes; `/actuator/health` and `/v3/api-docs` only as scoped. No PII in startup logs.

Bug (FAIL): none
