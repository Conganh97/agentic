---
requirement: REQ-001
status: DRAFT
adrs: [ADR-0003, ADR-0004, ADR-0009, ADR-0011, ADR-0012]
updated: 2026-09-25 14:26
---

# REQ-001 Design — Douyin Video Crawler Service

## 1. Summary

Build `douyin-crawler-service`, an independently deployable Spring Boot 4 service that discovers
public Douyin videos by **keyword**, stores metadata and metric snapshots in PostgreSQL, and
exposes REST APIs for crawl jobs and video queries. Crawl execution is asynchronous. The Douyin
access mechanism sits behind `VideoDiscoveryProvider` so tests use a mock and the HTTP adapter can
be replaced later. There is **no user-facing UI** and **no frontend component** in this increment.

## 2. Scope

- In scope:
  - New product component `douyin-crawler-service` (own GitHub repo, Docker, GHA, compose).
  - Keyword discovery of publicly reachable Douyin video metadata.
  - Persist videos with DB uniqueness on `(source, source_video_id)`.
  - Append-only metric snapshots.
  - Crawl jobs with PENDING / RUNNING / COMPLETED / PARTIAL / FAILED.
  - REST: create job, get job, list/get videos (keyset pagination).
  - Structured logs, Prometheus metrics, health, OpenAPI, unit + Testcontainers tests.
- Out of scope:
  - Video file download, transcoding, editing, subtitles, translation, TTS, LLM, publishing.
  - n8n workflows, trending-score engine, AI selection, copyright automation.
  - CAPTCHA solving, credential collection, private content, platform-security bypass.
  - Redis, messaging brokers, and any operator/web UI.

## 3. Functional Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| FR-1 | Operators can start the service from the documented local setup (compose + `SERVER_PORT`). | REQ AC-001 |
| FR-2 | `POST /api/v1/crawl-jobs` creates a job and returns **202** with `jobId` + `PENDING` without waiting for the crawl. | REQ AC-002, AC-003 |
| FR-3 | `GET /api/v1/crawl-jobs/{jobId}` returns status and counters (discovered, persisted, duplicates, failed). | REQ AC-009–AC-012, AC-017 |
| FR-4 | A running job calls `VideoDiscoveryProvider.discover` with strategy `KEYWORD` and persists new videos. | REQ AC-004, AC-006 |
| FR-5 | Each discovered item includes required metadata fields when the public source provides them. | REQ AC-005 |
| FR-6 | The same Douyin video is stored once; uniqueness is a unique index on `(source, source_video_id)`. | REQ AC-007, AC-008 |
| FR-7 | One item failure increments `failed` and does not stop remaining items. | REQ AC-013 |
| FR-8 | Transient provider/HTTP errors retry up to `crawler.retry.max-attempts`; permanent errors are not retried. | REQ AC-014, AC-015 |
| FR-9 | Rate (requests/second) and concurrency are configuration properties. | REQ AC-016 |
| FR-10 | `GET /api/v1/videos` lists videos with keyset pagination; `GET /api/v1/videos/{id}` returns one. | REQ AC-018–AC-020, AC-034 |
| FR-11 | Each crawl that sees engagement numbers inserts a new `video_metric` row; previous rows stay. | REQ AC-021 |
| FR-12 | A `MockVideoDiscoveryProvider` is the default in `test` and is selectable via `crawler.provider=mock`. | REQ AC-028, AC-029 |
| FR-13 | Application code depends on `VideoDiscoveryProvider` only; HTTP Douyin access is one infrastructure impl. | REQ AC-031 |
| FR-14 | The service does not download video bytes or implement downstream media/AI features. | REQ AC-032 |
| FR-15 | The HTTP provider sends only unauthenticated public GETs; on 401/403/captcha-like HTML it records a permanent failure. | REQ AC-033 |
| FR-16 | Docker image for this service runs with the compose file for the target env. | REQ AC-030 |

## 4. Non-functional Requirements

| ID | Category | Requirement (measurable) |
|----|----------|--------------------------|
| NFR-1 | Performance | Default crawl rate **1 req/s**, max concurrency **4**, HTTP timeout **10s**. A 20-video keyword job finishes in **≤ 5 minutes** when the provider responds within timeout. |
| NFR-2 | Performance | `POST /api/v1/crawl-jobs` returns 202 in **≤ 500 ms** (p95, local) and does not hold the request for the crawl. |
| NFR-3 | Performance | Video list uses keyset (`crawled_at`, `id`); list handlers must not run `COUNT(*)` on `video`. Default page size 20, max 100. |
| NFR-4 | Reliability | Retry only on timeout, 429, and 5xx; default max **3** attempts, exponential backoff 1s / 2s / 4s. |
| NFR-5 | Reliability | Stale `RUNNING` jobs older than `crawler.job.stale-after` (default 30m) are marked `FAILED` on the next create/status read or a scheduled sweep. |
| NFR-6 | Observability | JSON structured console logs (Boot structured logging) include `jobId`, `sourceVideoId` (when known), and outcome. No tokens or cookies in logs. |
| NFR-7 | Observability | Prometheus scrape at `/actuator/prometheus` exposes counters/timers in §6. |
| NFR-8 | Operability | `/actuator/health` is 200 when the process and PostgreSQL are up. |
| NFR-9 | Contract | OpenAPI at `/v3/api-docs` matches the controllers (ADR-0012). |
| NFR-10 | Testability | `./mvnw -q verify` uses Testcontainers PostgreSQL; tests never call real Douyin. |
| NFR-11 | Security / compliance | Public metadata only. No credential collection, no CAPTCHA solver, no signature/cookie forging. |
| NFR-12 | Extensibility | Adding a second `VideoDiscoveryProvider` impl does not change `api` or `application` packages. |

## 5. Architecture

```text
REST API                Application                 Domain
crawl-jobs, videos  →   create/run/query use cases  →  Video, CrawlJob, ports
                                                          │
                    ┌─────────────────────────────────────┤
                    ▼                                     ▼
           VideoDiscoveryProvider              VideoRepository / JobRepository
           (port)                              (ports)
                    │                                     │
         ┌──────────┴──────────┐                          ▼
         ▼                     ▼                   Flyway + JPA + PostgreSQL
   Mock impl            PublicKeyword impl
                        (RestClient + limiter)
```

Package-by-feature (`com.product.douyincrawler`):

| Feature | Responsibility |
|---------|----------------|
| `shared` | Boot config, ProblemDetail advice, properties, logging/metrics wiring |
| `discovery` | `VideoDiscoveryProvider`, mock + public-keyword infrastructure |
| `crawljob` | Job API, async executor, counters, item isolation |
| `video` | Video + metric persistence, query API |

**UI:** none. No `product/frontend` work and no UX/UI task.

### Stack (ADR-0009)

Locked: Java 21 + Spring · React. React is **unused** here (no UI).

| Layer | Choice | Why |
|-------|--------|-----|
| BE runtime | Java 21 + Spring Boot 4.0.x, Maven wrapper | locked core; REQ + ADR-0003 |
| BE web | `spring-boot-starter-webmvc`, `RestClient` | Boot 4 MVC + outbound HTTP |
| BE data | PostgreSQL 16, Spring Data JPA, Flyway, `ddl-auto=validate` | REQ DB; default migrator |
| BE observability | Actuator + `micrometer-registry-prometheus` + Boot structured JSON logs | REQ metrics/logs/health |
| BE API docs | springdoc-openapi webmvc UI (ADR-0012) | REQ OpenAPI |
| BE tests | JUnit 5, `webmvc-test`, Testcontainers PostgreSQL | REQ |
| BE resilience | In-process token bucket + semaphore + retry policy (no extra library, no Redis) | single-instance v1; REQ forbids unused infra |
| BE async | `TaskExecutor` (Java 21 virtual threads allowed) + job row | 202-on-create |
| FE runtime | **none** | no user-facing UI |
| FE UI kit / data / router | **none** | no user-facing UI |

Redis is **not** introduced. Horizontal rate limiting is a later REQ if more than one replica must share a budget.

## 6. API Changes

Base path `/api/v1`. JSON. RFC 9457 `ProblemDetail` for 400 / 404 / 409 / 422. No operator identity
in v1; APIs are reachable on the compose network only.

| Method | Path / Interface | Request | Response | Errors |
|--------|------------------|---------|----------|--------|
| POST | `/api/v1/crawl-jobs` | `{ "strategy": "KEYWORD", "keyword": "string", "limit": 20 }` `limit` default 20, min 1, max 50. | **202** `{ "jobId": "uuid", "status": "PENDING" }` | 400 unknown strategy / blank keyword / limit out of range |
| GET | `/api/v1/crawl-jobs/{jobId}` | path UUID | **200** job resource (below) | 404 unknown id |
| GET | `/api/v1/videos` | `source` optional, `keyword` unused, `after` cursor optional, `limit` default 20 max 100 | **200** `{ "items": [video], "nextCursor": "opaque" \| null }` | 400 bad cursor/limit |
| GET | `/api/v1/videos/{id}` | path UUID (internal id) | **200** video + latest snapshot fields | 404 |

Job resource:

```json
{
  "jobId": "uuid",
  "status": "PENDING|RUNNING|COMPLETED|PARTIAL|FAILED",
  "strategy": "KEYWORD",
  "keyword": "string",
  "limit": 20,
  "discovered": 0,
  "persisted": 0,
  "duplicates": 0,
  "failed": 0,
  "errorMessage": null,
  "createdAt": "iso-8601",
  "startedAt": null,
  "finishedAt": null
}
```

Video resource (required fields null when the public source omitted them):

`id`, `source` (`DOUYIN`), `sourceVideoId`, `canonicalUrl`, `authorId`, `authorName`, `title`,
`publishedAt`, `durationSeconds`, `coverImageUrl`, `crawledAt`, plus latest snapshot:
`likeCount`, `commentCount`, `shareCount`, `collectCount`, optional `viewCount`.

Optional video fields when present: `hashtags`, `musicId`, `musicName`, `location`,
`authorFollowerCount`, `width`, `height`, `resolution`.

**Final job status:** `COMPLETED` if the run finished and `failed == 0`; `PARTIAL` if the run
finished and `failed > 0` but work was attempted; `FAILED` if the provider cannot start, every
item fails, or the job is marked stale.

**Metrics (NFR-7):** `crawler.jobs` (counter, tag `status`), `crawler.videos.discovered`,
`crawler.videos.persisted`, `crawler.videos.duplicates`, `crawler.videos.failed`,
`crawler.job.duration` (timer).

**Ops (not versioned as product API):** `GET /actuator/health`, `GET /actuator/prometheus`,
`GET /v3/api-docs`.

Domain port (not HTTP):

```java
public interface VideoDiscoveryProvider {
    DiscoveryResult discover(DiscoveryRequest request);
}
```

`DiscoveryRequest`: `strategy`, `keyword`, `limit`.  
`DiscoveryResult`: list of `DiscoveredVideo` + per-item failures.  
`DiscoveredVideo` carries the metadata fields in FR-5.

## 7. Data Model Changes

New schema (Flyway `V1__crawler.sql`). One database per service.

**`crawl_job`**

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| status | VARCHAR(16) | enum above |
| strategy | VARCHAR(32) | `KEYWORD` |
| keyword | VARCHAR(200) | |
| requested_limit | INT | |
| discovered_count | INT | default 0 |
| persisted_count | INT | default 0 |
| duplicate_count | INT | default 0 |
| failed_count | INT | default 0 |
| error_message | TEXT | nullable |
| created_at | TIMESTAMPTZ | |
| started_at | TIMESTAMPTZ | nullable |
| finished_at | TIMESTAMPTZ | nullable |

**`crawl_job_item`**

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| job_id | UUID FK | |
| source | VARCHAR(16) | |
| source_video_id | VARCHAR(128) | nullable if parse failed |
| outcome | VARCHAR(16) | `PERSISTED` \| `DUPLICATE` \| `FAILED` |
| error_message | TEXT | nullable |

**`video`** (logical name; table `video`)

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | internal id for APIs |
| source | VARCHAR(16) | `DOUYIN` |
| source_video_id | VARCHAR(128) | Douyin video id, or SHA-256 of canonical URL if id missing |
| canonical_url | TEXT | |
| author_id, author_name, title | VARCHAR/TEXT | nullable |
| published_at | TIMESTAMPTZ | nullable |
| duration_seconds | INT | nullable |
| cover_image_url | TEXT | nullable |
| hashtags | TEXT | nullable, comma-separated or JSON array |
| music_id, music_name, location | VARCHAR | nullable |
| author_follower_count | BIGINT | nullable |
| width, height | INT | nullable |
| resolution | VARCHAR(32) | nullable |
| crawled_at | TIMESTAMPTZ | last successful persist/update of metadata (not metrics) |
| UNIQUE (source, source_video_id) | | **required** |

**`video_metric`**

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| video_id | UUID FK | |
| captured_at | TIMESTAMPTZ | insert-only |
| like_count, comment_count, share_count, collect_count | BIGINT | nullable |
| view_count | BIGINT | nullable |

No updates to existing `video_metric` rows. Re-crawling the same video inserts a new snapshot.
`INSERT … ON CONFLICT (source, source_video_id) DO NOTHING` (or catch unique violation) counts as
duplicate; metadata refresh of non-metric columns is allowed on a later increment, not required now.

Backward compatibility: first schema, no existing clients.

## 8. Dependencies

- Internal: TASK-001 creates the repo and compose; BE tasks depend on it as listed in §12.
- External:
  - PostgreSQL 16 (compose).
  - Public Douyin HTTP pages/feeds as reached by unauthenticated GET (unstable; see §10).
  - Libraries: Boot 4 webmvc, JPA, Flyway, Actuator, Micrometer Prometheus, springdoc (ADR-0012),
    Testcontainers. No Redis. No Resilience4j.

## 9. Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Douyin public GET is blocked, signed, or captcha-gated | Real provider returns no videos | High | Mock for tests/local; HTTP impl fails permanently on 401/403/captcha HTML; no bypass. Operator uses `crawler.provider=mock` until a later approved source exists. |
| Douyin HTML/JSON shape changes | Parse failures | High | Isolated parser behind the provider; job items fail individually. |
| Platform terms / copyright | Legal/compliance | Medium | Public metadata only; NFR-11; no media download. |
| Single-instance limiter | Two replicas double request rate | Low in v1 | One replica per env; document; Redis only in a later REQ. |
| Process crash leaves job RUNNING | Stuck jobs | Medium | NFR-5 stale sweep. |

## 10. Assumptions

- Human-approved REQ-001 allows collecting **public** metadata only; v1 does not need official
  Douyin partner credentials.
- First discovery strategy is **keyword** (not a separate trending feed).
- v1 runs **one** service replica per environment.
- Internal video `id` is a UUID; Douyin’s id is `sourceVideoId`.
- Path style follows backend standards (`/api/v1/crawl-jobs`), not the REQ sketch `/api/v1/crawl/jobs`.
- No browser UI; n8n (future) calls REST.

## 11. Open Questions

| # | Question | Blocking? | Answer |
|---|----------|-----------|--------|
| 1 | If public Douyin GETs stay blocked, is mock-only local/demo acceptable for v1 until a later REQ adds an approved source? | No | Assumed yes (§10). Revisit only if HUMAN forbids any real HTTP adapter. |
| 2 | Should v1 add operator identity later? | No | Out of this increment; APIs stay on the compose network. |

## 12. Task Breakdown

| Task | Title | Assignee | Covers | Depends on |
|------|-------|----------|--------|------------|
| TASK-001 | Create douyin-crawler-service repo, Docker, GHA, compose | DEVOPS | FR-1, FR-16, AC-001, AC-030 | — |
| TASK-002 | Service skeleton: health, structured logs, OpenAPI | BE | FR-1 (app process), NFR-6, NFR-8, NFR-9, AC-022, AC-024, AC-025 | TASK-001 |
| TASK-003 | Video + metric persistence and uniqueness | BE | FR-5–FR-6, FR-11, AC-006, AC-007, AC-008, AC-021, AC-026 | TASK-002 |
| TASK-004 | Discovery port, mock, public keyword provider | BE | FR-4, FR-5, FR-12, FR-13, AC-004, AC-005, AC-028, AC-029, AC-031 | TASK-002 |
| TASK-005 | Crawl job API and async dispatch | BE | FR-2, FR-3 (status), NFR-2, NFR-7, AC-002, AC-003, AC-017, AC-023 | TASK-003 |
| TASK-006 | Job execution, stats, item isolation | BE | FR-3, FR-4, FR-7, AC-009–AC-013 | TASK-004, TASK-005, TASK-007 |
| TASK-007 | Retry, rate, concurrency; public-only / no-download | BE | FR-8, FR-9, FR-14, FR-15, AC-014, AC-015, AC-016, AC-032, AC-033 | TASK-004 |
| TASK-008 | Video query API, keyset pagination, crawl integration tests | BE | FR-10, NFR-3, NFR-10, AC-018, AC-019, AC-020, AC-027, AC-034 | TASK-003, TASK-006 |

All product work is `repo: douyin-crawler-service`. No FE / UX/UI tasks.

## 13. UI / UX

**none** — REQ-001 has no user-facing web UI, no screens, and no Figma. Do not create a frontend
app, UX/UI task, or `docs/design/ux/` contract for this requirement. Operators and future
orchestration (n8n) use REST only.
