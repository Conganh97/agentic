---

id: REQ-002

title: Video Downloader Service

status: IN_PROGRESS

revision: 1

content_hash: b06116020682e658

priority: HIGH

owner: anhbc

design: docs/design/REQ-002-design.md

pqa_plan: docs/design/reviews/REQ-002-plan-1.md

pqa_accept:        

tasks: [TASK-009, TASK-010, TASK-011, TASK-012, TASK-013, TASK-014, TASK-015, TASK-016, TASK-017, TASK-018, TASK-019, TASK-020]

updated: 2026-09-25 16:37

---

## Goal

Build an independent Video Downloader Service responsible for downloading public videos discovered by the Douyin Crawler Service.

The first implementation should use **SnapTik at `montague.ie` as the default external download provider**.

The service must NOT tightly couple the business logic to SnapTik.

The external downloader provider must be configurable so that the implementation can be replaced with another provider without changing the core application logic.

The service will consume video URLs produced by `REQ-001 — Douyin Video Crawler Service` and produce downloadable video files that can later be consumed by the video-processing pipeline.

Expected flow:

```text
REQ-001
Douyin Crawler
      |
      | video URL
      v
REQ-002
Video Downloader
      |
      | downloaded video
      v
Object Storage
      |
      v
Future Video Processing Service
```

---

## Scope

* Create an independent Video Downloader Service.
* Accept a public video URL as download input.
* Support Douyin URLs.
* Use `montague.ie` / SnapTik as the default downloader provider.
* Investigate the actual HTTP/API/browser flow used by `montague.ie`.
* Do NOT assume an undocumented API endpoint without verifying it.
* Document the discovered request/response flow in the SA design.
* Implement the SnapTik integration behind a provider abstraction.
* Make the downloader provider configurable.
* Allow the provider implementation to be changed through configuration.
* Support asynchronous download jobs.
* Persist download job status.
* Persist download metadata.
* Download the resulting video file to configured object storage or local storage.
* Provide download job status API.
* Provide retry handling.
* Provide timeout handling.
* Provide rate limiting.
* Provide failure handling.
* Support idempotent download requests.
* Validate downloaded file type.
* Validate downloaded file size.
* Store the original source URL.
* Store provider information.
* Store provider response/download URL metadata where appropriate.
* Provide structured logging.
* Provide metrics.
* Provide health checks.
* Provide OpenAPI documentation.
* Provide unit tests.
* Provide integration tests.
* Provide a mock downloader provider for automated tests.
* Provide Docker support.

The provider abstraction should conceptually look like:

```java
public interface VideoDownloadProvider {

    DownloadResult download(DownloadRequest request);

}
```

The exact interface and domain model must be defined by SA.

---

## Out of Scope

* Douyin crawling.
* Trending discovery.
* Video transcription.
* Speech-to-text.
* Translation.
* Vietsub generation.
* OCR.
* AI content generation.
* AI voice generation.
* Video editing.
* Video transcoding.
* Video publishing.
* TikTok publishing.
* YouTube publishing.
* Facebook publishing.
* n8n workflow implementation.
* Recommendation algorithms.
* Trending-score calculation.
* Copyright ownership verification.
* CAPTCHA bypass.
* Authentication bypass.
* Private content extraction.
* Platform security bypass.
* Building or maintaining a custom Douyin scraping engine in this requirement unless required by the selected downloader provider.

---

## User Stories / Behaviour

* As a content-processing system, I want to submit a public Douyin video URL, so that the video can be downloaded for subsequent processing.

* As a system operator, I want to create a download job, so that downloading can happen asynchronously.

* As a system operator, I want to query download job status, so that I know whether a video has been downloaded successfully.

* As a system operator, I want the downloader provider to be configurable, so that I can replace SnapTik when it becomes unavailable or unsuitable.

* As a developer, I want the downloader provider to be abstracted behind an interface, so that provider-specific implementation does not leak into the application layer.

* As a developer, I want a mock downloader provider, so that the service can be tested without accessing an external downloader.

* As a system operator, I want failed downloads to be retried when the failure is transient, so that temporary provider/network problems do not immediately fail the job.

* As a system operator, I want failed downloads to be recorded, so that failures can be investigated.

* As a downstream video-processing service, I want a stable reference to the downloaded video, so that I can process it without knowing which downloader provider was used.

* As a system operator, I want downloaded files to be stored outside the application container, so that files survive application restarts and can be processed by other services.

---

## Acceptance Criteria (business level)

* [ ] AC-001 The service can start successfully using the documented local development setup.

* [ ] AC-002 The service exposes an API for creating a video download job.

* [ ] AC-003 Download jobs execute asynchronously.

* [ ] AC-004 A valid public Douyin video URL can be submitted for downloading.

* [ ] AC-005 SnapTik at `montague.ie` is implemented as the default provider.

* [ ] AC-006 The implementation verifies the actual `montague.ie` request/response flow before integrating it.

* [ ] AC-007 The actual provider endpoint, HTTP method, required headers, request parameters, request body, and response parsing logic are documented in `docs/design/REQ-002-design.md`.

* [ ] AC-008 Provider-specific implementation is isolated from the application/domain layer.

* [ ] AC-009 The provider can be changed through configuration without changing application business logic.

* [ ] AC-010 The provider base URL is configurable.

* [ ] AC-011 Provider-specific endpoint/path configuration is configurable where technically appropriate.

* [ ] AC-012 Provider-specific timeout is configurable.

* [ ] AC-013 Provider-specific retry configuration is configurable.

* [ ] AC-014 Provider-specific request headers are configurable where appropriate.

* [ ] AC-015 The system does not hard-code the SnapTik provider URL throughout the source code.

* [ ] AC-016 A successful provider response results in a downloadable video artifact.

* [ ] AC-017 The downloaded file is persisted to configured storage.

* [ ] AC-018 The system stores a stable reference to the downloaded file.

* [ ] AC-019 The system stores the original source URL.

* [ ] AC-020 The system stores the downloader provider used.

* [ ] AC-021 The system stores download start time and completion time.

* [ ] AC-022 The system stores download status.

* [ ] AC-023 The system can distinguish successful, failed, cancelled, and in-progress downloads.

* [ ] AC-024 A download failure does not crash the service.

* [ ] AC-025 Transient provider/network failures are retried according to configuration.

* [ ] AC-026 Permanent failures are not retried indefinitely.

* [ ] AC-027 Download timeout is configurable.

* [ ] AC-028 Download concurrency is configurable.

* [ ] AC-029 Provider request rate is configurable.

* [ ] AC-030 The system validates that the downloaded response is a supported video file.

* [ ] AC-031 The system rejects unexpected content types where validation is possible.

* [ ] AC-032 The system supports a configurable maximum file size.

* [ ] AC-033 Duplicate download requests can be detected.

* [ ] AC-034 Repeated requests for the same source video do not unnecessarily create duplicate downloaded files.

* [ ] AC-035 Download job status can be queried through an API.

* [ ] AC-036 Download metadata can be queried through an API.

* [ ] AC-037 Provider failures contain sufficient diagnostic information for troubleshooting without logging sensitive information.

* [ ] AC-038 Structured logs are available.

* [ ] AC-039 Metrics are available for download jobs, successful downloads, failed downloads, provider latency, and download duration.

* [ ] AC-040 Health checks are available.

* [ ] AC-041 OpenAPI documentation is available.

* [ ] AC-042 Unit tests cover provider selection, job lifecycle, retry behaviour, validation, and idempotency.

* [ ] AC-043 Integration tests cover persistence and download job lifecycle.

* [ ] AC-044 Integration tests do not require the real SnapTik service.

* [ ] AC-045 A mock downloader provider is available for automated tests.

* [ ] AC-046 Docker support is provided.

* [ ] AC-047 The implementation does not contain CAPTCHA bypass, authentication bypass, or private-content access mechanisms.

* [ ] AC-048 The service exposes a stable contract that can later be consumed by n8n or another orchestration service.

---

## Constraints

### Technology

Preferred technology:

* Java 21.
* Spring Boot 4.x.
* Maven.
* PostgreSQL.
* Docker.
* JUnit 5.
* Testcontainers.
* OpenAPI.
* Prometheus-compatible metrics.

Object storage should preferably be abstracted.

Possible implementation:

```text
S3-compatible storage
MinIO
AWS S3
Local filesystem for development
```

The exact storage implementation is subject to SA analysis.

---

### Provider Architecture

The application MUST NOT directly depend on SnapTik.

Recommended architecture:

```text
                    Application
                         |
                         v
              VideoDownloadProvider
                         |
              +----------+----------+
              |                     |
              v                     v
      SnapTikProvider        FutureProvider
              |
              v
         montague.ie
```

Example:

```java
public interface VideoDownloadProvider {

    DownloadResult submit(DownloadRequest request);

    DownloadStatus getStatus(String providerJobId);

}
```

The exact interface is determined by SA after investigating the provider flow.

---

### Provider Configuration

The downloader provider MUST be configurable.

Example configuration:

```yaml
downloader:
  provider: snaptik

  providers:
    snaptik:
      base-url: https://montague.ie
      api-path: <DISCOVERED_BY_AGENT>
      timeout: 30s
      max-retries: 3
      rate-limit:
        requests-per-second: 2

    alternative:
      enabled: false
      base-url: ${ALTERNATIVE_DOWNLOADER_BASE_URL:}
      api-path: ${ALTERNATIVE_DOWNLOADER_API_PATH:}
      timeout: 30s
```

The `<DISCOVERED_BY_AGENT>` value MUST NOT be invented.

SA/Backend must investigate the actual provider flow and replace it with the verified configuration.

Secrets, API keys, tokens, or provider credentials MUST NOT be committed to Git.

Use environment variables or secret management:

```yaml
api-key: ${SNAPTIK_API_KEY:}
```

If SnapTik does not require an API key, the implementation must not invent one.

---

### Provider Discovery / Investigation

SA MUST investigate `https://montague.ie/` before implementation.

The investigation should determine:

* Actual download request.
* HTTP method.
* Request URL.
* Required query parameters.
* Required form fields.
* Required JSON fields.
* Required headers.
* Cookies if required.
* CSRF tokens if required.
* Response format.
* Download URL extraction.
* Whether the response is synchronous or asynchronous.
* Whether an intermediate job ID exists.
* Whether the download URL expires.
* Whether the provider has an official public API.
* Whether API authentication is required.
* Rate-limit behaviour.
* Relevant failure responses.

The investigation must use the actual website behaviour rather than assumptions.

If an official API is publicly documented and usable, prefer it over reverse-engineering internal browser endpoints.

If no official API exists, SA must explicitly document that the integration relies on the website's publicly observable request flow.

---

### Provider Switching

The application should allow:

```yaml
downloader:
  provider: snaptik
```

to be changed to:

```yaml
downloader:
  provider: another-provider
```

without changing application/domain code.

Provider selection should be handled through configuration/factory/strategy pattern.

---

### Download Storage

The application must not assume that the provider's temporary download URL is permanent.

If the provider returns:

```text
temporary download URL
```

the service must download the file into configured storage before marking the job as:

```text
COMPLETED
```

The downstream system should consume the application's stable storage reference rather than the provider's temporary URL.

---

### Reliability

The downloader must handle:

```text
connection timeout
connection reset
HTTP 429
HTTP 5xx
provider temporary failure
invalid provider response
expired download URL
invalid video response
file download interruption
storage failure
```

Retry policy must be configurable.

Do not retry permanent failures indefinitely.

---

### Idempotency

The service should use a deterministic source identity.

Example:

```text
source + canonicalSourceUrl
```

or, when integrated with REQ-001:

```text
source + videoId
```

SA must determine the final identity strategy.

---

### Security

* Never log provider API keys.
* Never log authentication tokens.
* Never log cookies.
* Never store secrets in source code.
* Do not accept arbitrary local filesystem paths from API clients.
* Validate source URLs.
* Restrict allowed source domains where appropriate.
* Validate downloaded content.
* Prevent path traversal when generating storage paths.

---

### Compliance

The service is intended to download publicly accessible content.

It must not implement mechanisms intended to:

* bypass authentication;
* bypass CAPTCHA;
* bypass access controls;
* access private content;
* circumvent platform security controls.

The user of the system remains responsible for having appropriate rights to use downloaded content.

---

## Notes

### External Provider

Default provider:

```text
SnapTik
https://montague.ie/
```

The website states that it supports TikTok and Douyin URLs and provides downloadable video results through its web interface.

The website also states that users should respect copyright and only use downloaded content where they have appropriate rights.

No verified official public API endpoint should be assumed at requirement-writing time.

The implementation agent must investigate the website flow and record the verified technical details in:

```text
docs/design/REQ-002-design.md
```

### Suggested API

```text
POST /api/v1/downloads
GET  /api/v1/downloads/{downloadId}
POST /api/v1/downloads/{downloadId}/cancel
```

Example request:

```json
{
  "source": "DOUYIN",
  "videoUrl": "https://www.douyin.com/video/..."
}
```

Example response:

```json
{
  "downloadId": "uuid",
  "status": "PENDING"
}
```

Example completed response:

```json
{
  "downloadId": "uuid",
  "status": "COMPLETED",
  "source": "DOUYIN",
  "provider": "SNAPTIK",
  "storageKey": "videos/2026/09/uuid.mp4",
  "completedAt": "2026-09-25T12:00:00Z"
}
```

Exact API contracts are subject to SA analysis.

---

### Suggested Domain Model

```text
DownloadJob
    |
    +--- source
    +--- sourceVideoId
    +--- sourceUrl
    +--- provider
    +--- status
    +--- providerJobId
    +--- storageKey
    +--- fileSize
    +--- contentType
    +--- createdAt
    +--- startedAt
    +--- completedAt
    +--- failedAt
    +--- retryCount
    +--- errorCode
```

The final model is subject to SA analysis.

---

### Future Pipeline

This service will become:

```text
REQ-001
Douyin Crawler
      |
      | videoId + videoUrl
      v
REQ-002
Video Downloader
      |
      | storageKey
      v
REQ-003
Video Processor
      |
      v
REQ-004
Speech-to-Text
      |
      v
REQ-005
Translation / Vietsub
      |
      v
REQ-006
AI Content Generator
      |
      v
REQ-007
Video Editor
      |
      v
REQ-008
Social Publisher
      |
      v
REQ-009
n8n Orchestration
```

---

### Agentic Engineering Workflow

SA must:

1. Analyze this requirement.
2. Investigate `montague.ie`.
3. Determine whether an official API exists.
4. If no official API exists, document the observed web request flow.
5. Define provider abstraction.
6. Define domain model.
7. Define persistence model.
8. Define API contract.
9. Define storage abstraction.
10. Define provider configuration.
11. Create implementation tasks.

Backend must implement the tasks created by SA.

Test Agent must validate:

* provider selection;
* mocked provider integration;
* job lifecycle;
* retry behaviour;
* idempotency;
* invalid provider response;
* storage failure;
* timeout;
* rate limiting.

DevOps must validate:

* Docker;
* configuration through environment variables;
* secret injection;
* health checks;
* metrics.

---

### Requirement Change Rule

Bumping `revision` while tasks exist: `/scrum run` must BLOCK those tasks

(`reason: requirement_changed`) until SA re-analyzes.

Do not silently continue.

---
