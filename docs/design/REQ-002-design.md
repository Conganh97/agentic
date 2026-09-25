---
requirement: REQ-002
status: FINAL
adrs: [ADR-0003, ADR-0004, ADR-0009, ADR-0011, ADR-0012]
updated: 2026-09-25 16:37
---

# REQ-002 Design — Video Downloader Service

## 1. Summary

Build `video-downloader-service`, an independently deployable Spring Boot 4 service that accepts a
public Douyin video URL, runs an asynchronous download job, stores the file on a volume outside the
container, and exposes REST for job create/status/cancel. The default external provider is the
**publicly observed SnapTik / montague.ie flow**, which calls VieSnap HTTP hosts (not a published
partner API). Provider I/O sits behind `VideoDownloadProvider` so tests use a mock. There is **no
user-facing UI** and **no frontend component** in this increment.

## 2. Scope

- In scope:
  - New product component `video-downloader-service` (own GitHub repo, Docker, GHA, compose).
  - Accept public Douyin URLs; create async download jobs; persist status and metadata.
  - SnapTik provider isolated behind a port; default hosts/paths from the 2026-09-25 site investigation.
  - Configurable provider selection, base URLs, paths, timeout, retry, optional extra headers.
  - Filesystem storage behind `VideoStorage` (compose volume). Validate type and max size.
  - Idempotent identity so the same source does not store a second file while a live/completed job exists.
  - Structured logs, Prometheus metrics, health, OpenAPI, unit + Testcontainers tests, mock provider.
- Out of scope:
  - Douyin crawling, trending, transcription, translation, OCR, AI, editing, transcoding, publishing.
  - n8n workflows, copyright ownership checks, MinIO/S3, Redis, messaging.
  - Facebook / Instagram / Pinterest / Xiaohongshu downloads (VieSnap exposes those paths; v1 does not).
  - CAPTCHA solving, credential collection, private-content access, platform-security bypass.
  - Any operator/web UI.

## 3. Functional Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| FR-1 | Operators can start the service from the documented local setup (compose + `SERVER_PORT`). | REQ AC-001 |
| FR-2 | `POST /api/v1/downloads` creates a job and returns **202** with `downloadId` + `PENDING` without waiting for the file. | REQ AC-002, AC-003 |
| FR-3 | A public Douyin URL on an allowed host is accepted; other hosts and unparseable URLs are **400**. | REQ AC-004 |
| FR-4 | Default non-test provider is SnapTik using the documented VieSnap info + byte-fetch flow. | REQ AC-005, AC-006, AC-007 |
| FR-5 | Application/domain depend on `VideoDownloadProvider` only; provider id is a configuration property. | REQ AC-008, AC-009 |
| FR-6 | Provider base URL, paths, timeout, retry, and optional headers are properties; SnapTik hosts are not literals in Java. | REQ AC-010–AC-015 |
| FR-7 | A successful provider artifact is written to configured storage and the job stores a stable `storageKey`. | REQ AC-016, AC-017, AC-018 |
| FR-8 | Each job stores source URL, provider id, start/completion times, and a status in {PENDING, RUNNING, COMPLETED, FAILED, CANCELLED}. | REQ AC-019–AC-023 |
| FR-9 | A failed download does not stop the process. Transient provider/network errors retry; 4xx (except 429) and validation errors do not retry indefinitely. | REQ AC-024, AC-025, AC-026 |
| FR-10 | Download timeout, concurrency, and provider request rate are configuration properties. | REQ AC-027, AC-028, AC-029 |
| FR-11 | Stored bytes must look like a supported video (mp4/webm); unexpected content types and oversize bodies are rejected. | REQ AC-030, AC-031, AC-032 |
| FR-12 | Identity `(source, sourceIdentity)` detects duplicates; a COMPLETED/PENDING/RUNNING hit reuses the job and does not write a second file. | REQ AC-033, AC-034 |
| FR-13 | `GET /api/v1/downloads/{downloadId}` returns status and metadata (including `storageKey` when COMPLETED). | REQ AC-035, AC-036 |
| FR-14 | Failures record `errorCode` + safe `errorMessage`. Logs are JSON. Metrics and health exist. OpenAPI matches controllers. | REQ AC-037–AC-041 |
| FR-15 | Unit tests cover selection, lifecycle, retry, validation, idempotency. Integration tests use mock/WireMock only. | REQ AC-042–AC-045 |
| FR-16 | Docker image for this service runs with the compose file for the target env (own DB + storage volume). | REQ AC-046 |
| FR-17 | The service does not implement CAPTCHA solving, credential/session bypass, or private-content access. | REQ AC-047 |
| FR-18 | REST paths and JSON fields in §6 are the v1 contract for later n8n/orchestrators. | REQ AC-048 |

## 4. Non-functional Requirements

| ID | Category | Requirement (measurable) |
|----|----------|--------------------------|
| NFR-1 | Performance | `POST /api/v1/downloads` returns 202 or idempotent 200 in **≤ 500 ms** (p95, local) and does not hold the request for the file download. |
| NFR-2 | Performance | Defaults: provider rate **2 req/s**, download concurrency **2**, provider HTTP timeout **30s**, full download timeout **120s**. |
| NFR-3 | Reliability | Retry only on timeout, connection reset, 429, and 5xx; default max **3** attempts, exponential backoff 1s / 2s / 4s. |
| NFR-4 | Reliability | Stale `RUNNING` jobs older than `downloader.job.stale-after` (default 30m) are marked `FAILED` on the next create/status read or a scheduled sweep. |
| NFR-5 | Observability | JSON structured console logs include `downloadId`, `source` host (not full query string if it may contain tokens), outcome, `errorCode`. Never log API keys, tokens, cookies, or `cdn_headers`. |
| NFR-6 | Observability | Prometheus scrape at `/actuator/prometheus` exposes counters/timers in §6. |
| NFR-7 | Operability | `/actuator/health` is 200 when the process is up. PostgreSQL health is required after TASK-011. Storage-root writable indicator after TASK-012. |
| NFR-8 | Contract | OpenAPI at `/v3/api-docs` matches the controllers (ADR-0012). |
| NFR-9 | Testability | `./mvnw -q verify` uses Testcontainers PostgreSQL; tests never call `*.viesnap.com` or `montague.ie`. |
| NFR-10 | Security / compliance | Public URLs only. No CAPTCHA solver. No credential collection. No invented SnapTik API key. 401/403/captcha-like HTML from the provider are permanent failures. |
| NFR-11 | Extensibility | Adding a second `VideoDownloadProvider` impl does not change `api` or `application` packages. |
| NFR-12 | Storage | Files live on a compose volume (default max **500 MiB**). Storage keys are server-generated (`videos/{yyyy}/{MM}/{downloadId}.mp4`). Clients cannot pass filesystem paths. |
| NFR-13 | Security | Allowed source hosts: `douyin.com`, `iesdouyin.com`, and their subdomains only (`v.douyin.com` included). |

## 5. Architecture

```text
REST API                         Application                      Domain
downloads create/get/cancel  →   create/run/query/cancel     →  DownloadJob, ports
                                                                   │
                    ┌──────────────────────────────────────────────┤
                    ▼                                              ▼
           VideoDownloadProvider                         VideoStorage / JobRepository
           (port)                                        (ports)
                    │                                              │
         ┌──────────┴──────────┐                    ┌──────────────┴──────────────┐
         ▼                     ▼                    ▼                             ▼
   Mock impl            SnapTik / VieSnap     LocalFilesystemStorage          Flyway + JPA
                        (RestClient)          (volume root)                  + PostgreSQL
```

Package-by-feature (`com.product.videodownloader`):

| Feature | Responsibility |
|---------|----------------|
| `shared` | Boot config, ProblemDetail advice, properties, logging/metrics wiring |
| `provider` | `VideoDownloadProvider`, mock + SnapTik/VieSnap infrastructure |
| `storage` | `VideoStorage` port + filesystem implementation + type/size checks |
| `downloadjob` | Job API, async executor, persistence, idempotency, cancel, stale sweep |

**UI:** none. No `product/frontend` work and no UX/UI task.

### Stack (ADR-0009)

Locked: Java 21 + Spring · React. React is **unused** here (no UI).

| Layer | Choice | Why |
|-------|--------|-----|
| BE runtime | Java 21 + Spring Boot 4.0.x, Maven wrapper | locked core; REQ + ADR-0003 |
| BE web | `spring-boot-starter-webmvc`, `RestClient` | Boot 4 MVC + outbound HTTP |
| BE data | PostgreSQL 16, Spring Data JPA, Flyway, `ddl-auto=validate` | REQ DB; same default as REQ-001 |
| BE storage | Local filesystem via `VideoStorage` + Docker volume | REQ “outside the container”; no MinIO/S3 in v1 |
| BE observability | Actuator + `micrometer-registry-prometheus` + Boot structured JSON logs | REQ metrics/logs/health |
| BE API docs | springdoc-openapi webmvc UI (ADR-0012) | REQ OpenAPI |
| BE tests | JUnit 5, `webmvc-test`, Testcontainers PostgreSQL, WireMock | REQ; no real provider |
| BE resilience | In-process token bucket + semaphore + retry policy (no extra library, no Redis) | single-instance v1 |
| BE async | `TaskExecutor` (Java 21 virtual threads allowed) + job row | 202-on-create |
| FE runtime | **none** | no user-facing UI |
| FE UI kit / data / router | **none** | no user-facing UI |

Redis and MinIO are **not** introduced. S3-compatible storage is a later REQ if more than one host must share files. Horizontal rate limiting is a later REQ if more than one replica must share a budget.

### Ports (this machine)

Crawler (REQ-001) keeps existing ports. Downloader is a sibling stack, not a replacement of `API_IMAGE`.

| Env | Downloader API | Downloader DB | Storage volume |
|-----|----------------|---------------|----------------|
| DEV | 18082 | 15441 | `downloader_videos_dev` |
| STG | 28082 | 25441 | `downloader_videos_stg` |
| PROD | 8082 | 5433 | `downloader_videos_prod` |

`server.port: ${SERVER_PORT:18082}`. `deploy.py` today writes a single `API_IMAGE`; DEVOPS must add downloader-specific compose services and env vars so deploying this component does not clobber `douyin-crawler-service`.

## 6. API Changes

Base path `/api/v1`. JSON. RFC 9457 `ProblemDetail` for 400 / 404 / 409 / 422. No operator identity
in v1; APIs are reachable on the compose network only.

| Method | Path / Interface | Request | Response | Errors |
|--------|------------------|---------|----------|--------|
| POST | `/api/v1/downloads` | `{ "source": "DOUYIN", "videoUrl": "https://…", "sourceVideoId": "optional" }` | **202** new `{ "downloadId", "status": "PENDING" }`. **200** if an existing PENDING/RUNNING/COMPLETED job matches identity (same body shape + current status). | 400 bad source/URL/host; 409 only if a conflicting in-flight rule is violated (should not happen with the lookup rule) |
| GET | `/api/v1/downloads/{downloadId}` | path UUID | **200** job resource (below) | 404 |
| POST | `/api/v1/downloads/{downloadId}/cancel` | none | **200** job resource with `CANCELLED` | 404; 409 if already COMPLETED/FAILED/CANCELLED |

`source` v1 allows only `DOUYIN`. `sourceVideoId` is optional; when omitted the service parses it from the URL or hashes the canonical URL (§7).

Job resource:

```json
{
  "downloadId": "uuid",
  "status": "PENDING|RUNNING|COMPLETED|FAILED|CANCELLED",
  "source": "DOUYIN",
  "sourceVideoId": "string|null",
  "sourceUrl": "https://…",
  "provider": "SNAPTIK|MOCK",
  "storageKey": "videos/2026/09/{downloadId}.mp4",
  "fileSize": 0,
  "contentType": "video/mp4",
  "retryCount": 0,
  "errorCode": null,
  "errorMessage": null,
  "createdAt": "iso-8601",
  "startedAt": null,
  "completedAt": null,
  "failedAt": null,
  "cancelledAt": null
}
```

`storageKey`, `fileSize`, and `contentType` are null until COMPLETED. Cancel is cooperative: a RUNNING worker must stop before writing COMPLETED if it sees CANCELLED.

**Error codes (job):** `INVALID_URL`, `PROVIDER_TIMEOUT`, `PROVIDER_429`, `PROVIDER_5XX`, `PROVIDER_4XX`, `INVALID_CONTENT`, `FILE_TOO_LARGE`, `STORAGE_FAILURE`, `STALE`, `CANCELLED`.

**Metrics (NFR-6):** `downloader.jobs` (counter, tag `status`), `downloader.downloads.success`, `downloader.downloads.failed` (tag `errorCode`), `downloader.provider.latency` (timer), `downloader.download.duration` (timer).

**Ops (not versioned as product API):** `GET /actuator/health`, `GET /actuator/prometheus`, `GET /v3/api-docs`.

Domain ports (not HTTP):

```java
public interface VideoDownloadProvider {
    ProviderDownloadResult download(DownloadRequest request);
}

public interface VideoStorage {
    StoredObject put(StoragePut request); // stream + declared type/size limits
    boolean exists(String storageKey);
}
```

`DownloadRequest`: `source`, `sourceUrl`, `sourceVideoId` (optional).  
`ProviderDownloadResult`: byte stream (or temp channel) + `contentType`, `suggestedExtension`, `providerId`, `providerSource` (e.g. `scrape` / `hybrid`), optional non-secret metadata. The application writes the stream through `VideoStorage` and must not treat any provider URL as the durable reference.

### Provider investigation (AC-006 / AC-007) — 2026-09-25

**Official API:** none found. `https://montague.ie/` is a WordPress marketing/UI site. `rel="https://api.w.org/"` is WordPress JSON, not a download API. Third-party marketplace “SnapTik APIs” (RapidAPI, Zyla, etc.) are **not** affiliated with this site and must not be used.

**Observed browser flow** (Velvet theme `app.js?ver=1787291104`, plus `window.VELVET_DOWNLOADER` injected on the homepage):

1. Operator pastes a URL into `#urlInput`. Client-side checks reject empty input and TikTok non-video pages (profile/live/section). Those checks are UI-only; the service still validates hosts.
2. **Resolve (synchronous JSON).**  
   - Method: `POST`  
   - URL: `{apiBase}{infoPath}`  
   - Injected `apiBase` on montague.ie: `https://api3.viesnap.com` (JS fallback if unset: `https://api.viesnap.com`).  
   - Path for Douyin (`douyin.com` / `iesdouyin.com`): `/douyin/info`. Other site paths (`/info`, `/fb/info`, …) are **out of v1 scope**.  
   - Headers observed: `Content-Type: application/json` only. No API key, no CSRF header, no `credentials: 'include'`.  
   - Body: `{"url":"<cleaned source URL>"}`.  
   - Success: JSON object. Fields the UI reads: `source` (default `'scrape'`), `qualities` (object with `best` and optional `audio`), `images[]`, `thumbnail`, `author`, `description`, `duration`, `view_count`.  
   - `qualities.best` fields the UI uses later: `cdn_url`, optional `ext` (default `mp4`), `filesize`, `cookies`, `cdn_headers`.  
   - Failure: HTTP 400 JSON. Live probe 2026-09-25 with a non-video Douyin path returned `{"detail":"Invalid Douyin URL."}` (no `code`). The UI also maps optional machine `code` values `invalid_url`, `nonvideo_profile`, `nonvideo_live`, `nonvideo_page` to permanent input errors. Non-400 → treat as server/transient per status (429/5xx retry; 401/403 permanent).  
   - CORS on that probe: `access-control-allow-origin: https://montague.ie`. Server-side `RestClient` does not need an Origin header and must not spoof browser headers to evade controls. Exposed rate-limit header names: `Retry-After`, `X-RateLimit-*`.
3. **Fetch bytes (synchronous GET, URL is temporary).**  
   - Injected `dlBase`: `https://dl2.viesnap.com` (JS fallback: `https://dl.viesnap.com`).  
   - If `source === 'hybrid'` and the URL is Douyin: `GET {dlBase}/douyin/redirect?u={base64url(cdn_url)}` with fallback `GET {dlBase}/download?source=scrape&cdn_url=…&filename=…&format=…&dl_id=…&platform_hint=douyin` plus optional `cdn_headers`.  
   - Default (`scrape`, shared TikTok/Douyin): `GET {dlBase}/download?source=scrape&cdn_url=…&filename=…&format=…&dl_id=…&platform_hint=douyin` plus optional `cookies` / `cdn_headers` **only when the info JSON supplied them**.  
   - Other `source` values (`tikwm`, `fb`, …) may use a raw `cdn_url`; v1 still goes through the provider impl and then **our** storage.  
   - The browser streams the GET into a blob (stall 20s, up to 5 stream attempts). The service uses `RestClient` GET with configured timeouts/retries instead of copying that UI loop.  
4. **Telemetry** `POST {apiBase}/stats/download` is browser analytics. **Do not implement** it.  
5. **Affiliate “offer” gate** (client-side ads / cooldown) is not a CAPTCHA and is not part of the HTTP contract. **Do not implement** it and do not add any bypass of CAPTCHA, login, or private videos.

**Configuration mapping (replace `<DISCOVERED_BY_AGENT>`):**

```yaml
downloader:
  provider: snaptik   # test profile: mock
  providers:
    snaptik:
      api-base-url: ${SNAPTIK_API_BASE_URL:https://api3.viesnap.com}
      download-base-url: ${SNAPTIK_DL_BASE_URL:https://dl2.viesnap.com}
      info-path: ${SNAPTIK_INFO_PATH:/douyin/info}
      download-path: ${SNAPTIK_DOWNLOAD_PATH:/download}
      redirect-path: ${SNAPTIK_REDIRECT_PATH:/douyin/redirect}
      timeout: 30s
      max-retries: 3
      headers: {}     # optional extra request headers; do not invent an API key
```

If VieSnap later requires a real key, inject `${SNAPTIK_API_KEY:}` via env — never commit a secret. Today the site does not send one.

The integration **relies on the website’s publicly observable request flow**, not an official documented API. Hosts and paths are configuration so they can change without domain edits.

## 7. Data Model Changes

New schema (Flyway). One database per service. `download_job` = TASK-011. No other tables in v1.

**`download_job`**

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | API `downloadId` |
| source | VARCHAR(16) | `DOUYIN` |
| source_video_id | VARCHAR(128) | nullable if not parseable |
| source_identity | VARCHAR(64) | `source_video_id` or SHA-256 hex of canonical URL |
| source_url | TEXT | original submitted URL |
| canonical_url | TEXT | host lowercased; tracking query params stripped |
| provider | VARCHAR(32) | `SNAPTIK` / `MOCK` |
| status | VARCHAR(16) | enum in FR-8 |
| storage_key | TEXT | nullable until COMPLETED |
| file_size | BIGINT | nullable |
| content_type | VARCHAR(128) | nullable |
| provider_source | VARCHAR(32) | info JSON `source` when present |
| created_at | TIMESTAMPTZ | |
| started_at | TIMESTAMPTZ | nullable |
| completed_at | TIMESTAMPTZ | nullable |
| failed_at | TIMESTAMPTZ | nullable |
| cancelled_at | TIMESTAMPTZ | nullable |
| retry_count | INT | default 0 |
| error_code | VARCHAR(64) | nullable |
| error_message | TEXT | nullable; no secrets |

Partial unique index: `(source, source_identity)` WHERE `status IN ('PENDING','RUNNING','COMPLETED')`.

Identity: if `sourceVideoId` is provided or parsed from `/video/{id}` (or Douyin `modal_id` query), use it; else SHA-256 of `canonical_url`. Short `v.douyin.com/…` links are allowed hosts; if the id cannot be parsed, hash the canonical short URL (do not follow redirects onto sign-in walls).

FAILED/CANCELLED rows do not block a later POST (new id, new storage key). COMPLETED/PENDING/RUNNING return the existing job (FR-12).

Backward compatibility: first schema, no existing clients.

## 8. Dependencies

- Internal: TASK-009 creates the repo and compose; BE tasks depend on it as listed in §12. Does not call REQ-001 APIs in v1 (operator/orchestrator submits URLs).
- External:
  - PostgreSQL 16 (compose, dedicated instance).
  - VieSnap hosts as configured (unstable; mock/WireMock in tests).
  - Libraries: Boot 4 webmvc, JPA, Flyway, Actuator, Micrometer Prometheus, springdoc (ADR-0012), Testcontainers, WireMock. No Redis. No Resilience4j. No AWS SDK. No Jsoup required if JSON is parsed with Jackson.

## 9. Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| VieSnap/montague.ie changes paths or blocks datacenter IPs | Real provider fails | High | All hosts/paths in config; mock for tests/local; permanent fail on 401/403/captcha HTML; no bypass |
| Provider `cdn_url` expires before byte GET | Job FAILED after resolve | Medium | Download immediately after info; retry only transient errors; do not persist provider URL as the product reference |
| Site affiliate/CAPTCHA changes | Confusion vs AC-047 | Medium | Document: ads gate is client-only; we call the same public JSON/GET the page uses; we never solve CAPTCHA |
| Single-instance limiter | Two replicas double request rate | Low in v1 | One replica per env; document |
| Process crash leaves job RUNNING | Stuck jobs | Medium | NFR-4 stale sweep |
| deploy.py single `API_IMAGE` | Deploying downloader replaces crawler | High if ignored | DEVOPS sibling services + separate env vars (TASK-009) |

## 10. Assumptions

- Human-approved REQ-002 allows downloading **public** Douyin URLs the operator is responsible for having rights to use.
- v1 is API-submit only; no automatic consume of REQ-001 video rows.
- v1 runs **one** downloader replica per environment.
- Default provider name in config is `snaptik` even though the HTTP backend is VieSnap (that is what montague.ie uses).
- No browser UI; n8n (future) calls REST.
- Filesystem volume is sufficient durable storage until a later REQ adds S3/MinIO.

## 11. Open Questions

| # | Question | Blocking? | Answer |
|---|----------|-----------|--------|
| 1 | If VieSnap blocks this machine, is mock-only local/demo acceptable until hosts are updated in config? | No | Assumed yes (§10), same pattern as REQ-001. |
| 2 | Should v1 persist provider `cdn_url` for audit? | No | No. Store `provider_source` only; provider URLs are temporary and may include sensitive query data. |
| 3 | Auto-pull URLs from `douyin-crawler-service`? | No | Later REQ; v1 is REST submit. |

## 12. Task Breakdown

| Task | Title | Assignee | Covers | Depends on |
|------|-------|----------|--------|------------|
| TASK-009 | Create video-downloader-service repo, Docker, GHA, compose | DEVOPS | FR-16, AC-046 | — |
| TASK-010 | Service skeleton: health, structured logs, OpenAPI | BE | FR-1, FR-14 (log/health/OpenAPI stack), NFR-5 (stack), NFR-7 (process), NFR-8, AC-001, AC-038, AC-040, AC-041 | TASK-009 |
| TASK-011 | Download job persistence and status model | BE | FR-8, AC-019, AC-020, AC-021, AC-022, AC-023 | TASK-010 |
| TASK-012 | Storage port, volume persist, type/size validation | BE | FR-7 (storage write), FR-11, NFR-12, AC-017, AC-018, AC-030, AC-031, AC-032 | TASK-010 |
| TASK-013 | Provider port, mock, config switch | BE | FR-5, FR-15 (mock/IT isolation), NFR-11, AC-008, AC-009, AC-044, AC-045 | TASK-010 |
| TASK-014 | SnapTik/VieSnap adapter using documented flow | BE | FR-4, FR-6 (base URL + no literals), AC-005, AC-006, AC-007, AC-010, AC-015 | TASK-013 |
| TASK-015 | Provider path, timeout, retry, header properties | BE | FR-6 (remaining knobs), AC-011, AC-012, AC-013, AC-014 | TASK-014 |
| TASK-016 | Download job API, async dispatch, URL rules, cancel | BE | FR-2, FR-3, FR-13 (GET status), FR-18, NFR-1, NFR-4, NFR-13, AC-002, AC-003, AC-004, AC-035, AC-048 | TASK-011 |
| TASK-017 | Job execution: provider → storage, metrics, diagnostics | BE | FR-7 (success path), FR-9 (no crash), FR-13 (metadata), FR-14 (metrics/diag), NFR-5 (emit fields), NFR-6, AC-016, AC-024, AC-036, AC-037, AC-039 | TASK-012, TASK-013, TASK-016 |
| TASK-018 | Retry, timeout, rate, concurrency | BE | FR-9 (retry policy), FR-10, NFR-2, NFR-3, AC-025, AC-026, AC-027, AC-028, AC-029 | TASK-014, TASK-017 |
| TASK-019 | Idempotency and public-only bounds | BE | FR-12, FR-17, NFR-10, AC-033, AC-034, AC-047 | TASK-012, TASK-017 |
| TASK-020 | Unit + integration coverage for lifecycle | BE | FR-15, NFR-9, AC-042, AC-043 | TASK-018, TASK-019 |

All product work is `repo: video-downloader-service`. No FE / UX/UI tasks.

## 13. UI / UX

**none** — REQ-002 has no user-facing web UI, no screens, and no Figma. Do not create a frontend
app, UX/UI task, or `docs/design/ux/` contract for this requirement. Operators and future
orchestration (n8n) use REST only.
