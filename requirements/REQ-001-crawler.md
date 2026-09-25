---

id: REQ-001

title: Douyin Video Crawler Service

status: APPROVED

revision: 1

content_hash: c34978450afab2c1

priority: HIGH

owner: anhbc

design:               

pqa_plan:            

pqa_accept:        

tasks: []

updated: 2026-09-25 14:23

---

## Goal

Build the first independent service in the content-repurposing pipeline.

The service is responsible for discovering public/trending Douyin videos and storing their metadata so that downstream services can later process, download, translate, edit, and publish the content.

The first phase must focus only on **reliable video discovery and metadata collection**.

The service must be independently deployable, testable, and usable by future orchestration systems such as n8n.

The service should be implemented using **Java 21 and Spring Boot** unless SA identifies a concrete technical reason to use another technology for a specific crawler component.

---

## Scope

* Create an independent Douyin Crawler Service.
* Support discovering public Douyin videos.
* Support at least one discovery strategy in the first implementation:

  * trending videos, or
  * keyword/topic-based discovery.
* Extract available public video metadata.
* Store discovered video metadata in PostgreSQL.
* Prevent duplicate video records.
* Support crawl jobs.
* Support asynchronous crawl execution.
* Provide APIs to:

  * create a crawl job;
  * query crawl job status;
  * query crawled videos.
* Store crawl statistics.
* Support configurable crawler concurrency.
* Support configurable request timeout.
* Support configurable retry policy.
* Support configurable rate limiting.
* Handle individual video failures without necessarily failing the entire crawl job.
* Support historical metric snapshots where available.
* Provide structured logging.
* Provide application metrics suitable for Prometheus.
* Provide health checks.
* Provide OpenAPI documentation.
* Provide unit tests.
* Provide integration tests using Testcontainers.
* Provide Docker support for local development.
* Keep the crawler implementation behind an abstraction so the underlying Douyin access mechanism can be replaced later.
* Keep crawler logic independent from persistence and API layers.

Minimum video metadata should include, where publicly available:

* source
* videoId
* canonical video URL
* authorId
* authorName
* title/caption
* publish time
* duration
* cover image URL
* like count
* comment count
* share count
* collect/favorite count
* crawl time

Optional metadata may include:

* hashtags
* music ID
* music name
* location
* view count
* author follower count
* video width
* video height
* video resolution

The service should support the following conceptual flow:

```text
Douyin
   |
   v
Discovery Provider
   |
   v
Crawl Job
   |
   v
Video Metadata
   |
   v
Deduplication
   |
   v
PostgreSQL
```

The crawler should expose a provider abstraction similar to:

```java
interface VideoDiscoveryProvider {
    DiscoveryResult discover(DiscoveryRequest request);
}
```

The exact interfaces and architecture are to be defined by SA during analysis.

---

## Out of Scope

* Downloading video files.
* Video transcoding.
* Video cutting.
* Video editing.
* Subtitle generation.
* Vietsub generation.
* Speech-to-text.
* OCR.
* Translation.
* LLM-based content generation.
* AI voice generation.
* Text-to-speech.
* TikTok publishing.
* YouTube publishing.
* Facebook publishing.
* Other social media publishing.
* n8n workflow implementation.
* Trending-score/recommendation engine.
* Automated content selection based on AI.
* Copyright decision automation.
* Bypassing CAPTCHA.
* Bypassing authentication.
* Accessing private Douyin content.
* Circumventing platform security mechanisms.

The crawler only handles publicly accessible content and metadata.

---

## User Stories / Behaviour

* As a content automation system, I want to discover public Douyin videos, so that downstream services can process them.

* As a content automation system, I want video metadata to be persisted, so that discovered videos can be processed asynchronously later.

* As a system operator, I want to trigger a crawl job, so that I can manually start content discovery.

* As a system operator, I want to query crawl job status, so that I can monitor whether a crawl completed successfully.

* As a system operator, I want crawl statistics, so that I can understand how many videos were discovered, persisted, duplicated, or failed.

* As a system operator, I want configurable rate limiting, so that the crawler does not continuously send requests to Douyin.

* As a system operator, I want configurable retries, so that transient failures can be recovered automatically.

* As a downstream service, I want a stable video query API, so that I can retrieve videos discovered by the crawler.

* As a downstream service, I want every video to have a stable unique identifier, so that the same video is not processed multiple times.

* As a system operator, I want historical metric snapshots, so that a future service can calculate engagement growth and trending velocity.

* As a developer, I want the Douyin access mechanism to be abstracted, so that the crawler can be replaced or extended without changing the application layer.

* As a developer, I want a mock discovery provider, so that the system can be tested without depending on Douyin.

---

## Acceptance Criteria (business level)

* [ ] AC-001 The service can start successfully using the documented local development setup.

* [ ] AC-002 The service can create a crawl job through an API.

* [ ] AC-003 A crawl job executes asynchronously and does not require the API request to remain open until crawling finishes.

* [ ] AC-004 The crawler can discover public Douyin videos using at least one supported discovery strategy.

* [ ] AC-005 Discovered videos contain the required metadata when that metadata is publicly available.

* [ ] AC-006 Successfully discovered videos are persisted in PostgreSQL.

* [ ] AC-007 The same Douyin video cannot be persisted multiple times.

* [ ] AC-008 Video uniqueness is enforced at the persistence layer and is not dependent only on application-level checks.

* [ ] AC-009 A crawl job records the number of discovered videos.

* [ ] AC-010 A crawl job records the number of newly persisted videos.

* [ ] AC-011 A crawl job records duplicate videos.

* [ ] AC-012 A crawl job records failed video processing.

* [ ] AC-013 A failure processing one video does not automatically terminate the entire crawl job.

* [ ] AC-014 Transient crawler failures are retried according to configurable retry settings.

* [ ] AC-015 Permanent failures are not endlessly retried.

* [ ] AC-016 Crawler request rate and concurrency are configurable.

* [ ] AC-017 Crawl job status can be queried through an API.

* [ ] AC-018 Crawled videos can be queried through an API.

* [ ] AC-019 Video querying supports pagination.

* [ ] AC-020 The implementation does not depend on expensive full-table COUNT queries for normal high-volume pagination.

* [ ] AC-021 Historical video metrics can be stored as separate snapshots without overwriting previous snapshots.

* [ ] AC-022 Application logs are structured and contain sufficient information to investigate crawl failures.

* [ ] AC-023 Application metrics are exposed for crawler jobs, discovered videos, persisted videos, duplicates, failures, and crawl duration.

* [ ] AC-024 Application health checks are available.

* [ ] AC-025 APIs are documented through OpenAPI.

* [ ] AC-026 Unit tests cover the core application and domain behaviour.

* [ ] AC-027 Integration tests verify PostgreSQL persistence and crawl-job behaviour.

* [ ] AC-028 Integration tests can run without requiring a real Douyin account.

* [ ] AC-029 A mock discovery provider is available for automated tests.

* [ ] AC-030 The application can run using Docker.

* [ ] AC-031 The crawler implementation is isolated behind an abstraction that allows another provider implementation to be introduced later.

* [ ] AC-032 The implementation does not include video downloading or any downstream AI/video-processing functionality.

* [ ] AC-033 The crawler only accesses publicly available content and does not implement authentication, CAPTCHA, or platform-security bypass mechanisms.

* [ ] AC-034 The service exposes a stable contract that can later be consumed by an orchestration layer such as n8n.

---

## Constraints

### Technology

* Java 21.
* Spring Boot 4.x.
* Maven.
* PostgreSQL.
* Docker.
* JUnit 5.
* Testcontainers.
* OpenAPI.
* Prometheus-compatible metrics.

Redis may be introduced if SA determines that it is necessary for distributed rate limiting, caching, or coordination.

Do not introduce infrastructure without a concrete requirement.

### Architecture

The service must maintain clear separation between:

```text
API
Application
Domain
Infrastructure
Crawler Provider
Persistence
```

The application/domain layer must not directly depend on a specific Douyin crawler implementation.

SA must define the final architecture in:

```text
docs/design/REQ-001-design.md
```

### Reliability

* Individual video failures must be isolated.
* Transient failures should be retried.
* Retry count must be configurable.
* Requests must have timeouts.
* Crawler concurrency must be configurable.
* Rate limiting must be configurable.
* Crawl jobs must provide deterministic final states.

Expected crawl states:

```text
PENDING
RUNNING
COMPLETED
PARTIAL
FAILED
```

### Persistence

Primary video uniqueness:

```text
source + videoId
```

If a stable video ID cannot be obtained, the implementation may use a deterministic identifier derived from the canonical video URL.

Database constraints must enforce uniqueness.

Historical metrics must not overwrite previous snapshots.

### Security / Compliance

* Only public content may be collected.
* Do not bypass authentication.
* Do not bypass CAPTCHA.
* Do not bypass access-control mechanisms.
* Do not implement techniques intended to circumvent platform security.
* The implementation must consider applicable Douyin terms and copyright requirements.

### Performance

The first implementation should be designed for moderate crawler throughput and horizontal extensibility.

The requirement does not mandate a specific videos-per-second target.

SA must identify reasonable performance targets during analysis based on the selected crawling mechanism.

### Compatibility

The service must expose REST APIs suitable for future integration with:

```text
n8n
other backend services
future content-processing services
```

The crawler must not directly depend on n8n.

---

## Notes

### Expected future pipeline

This requirement is Phase 1 of a larger system:

```text
REQ-001
Douyin Crawler
      |
      v
REQ-002
Video Downloader
      |
      v
REQ-003
Video/Audio Processor
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
Social Media Publisher
      |
      v
REQ-009
n8n E2E Orchestration
```

These future requirements must remain independently deployable and testable.

### Suggested initial service name

```text
douyin-crawler-service
```

### Suggested API

```text
POST /api/v1/crawl/jobs
GET  /api/v1/crawl/jobs/{jobId}
GET  /api/v1/videos
GET  /api/v1/videos/{videoId}
```

The exact API contract is subject to SA analysis.

### Suggested persistence model

The implementation may use a structure similar to:

```text
crawl_job
    |
    +--- crawl_job_item
    |
    +--- douyin_video
              |
              +--- douyin_video_metric
```

The exact schema is subject to SA analysis.

### Agentic Engineering Workflow

SA must first analyze this requirement and produce the design before Backend implementation begins.

Expected sequence:

```text
HUMAN
  |
  v
REQ-001 DRAFT
  |
  v
HUMAN APPROVE
  |
  v
SA ANALYZING
  |
  v
SA Design
  |
  v
SA creates TASKs
  |
  v
PQA ANALYZED
  |
  v
SCRUM IN_PROGRESS
  |
  +------> Backend
  |
  +------> Test
  |
  +------> DevOps
  |
  v
PQA READY_FOR_RELEASE
  |
  v
DEVOPS RELEASED
```

SA must break this requirement into small, independently executable tasks.

No agent should implement the entire requirement as one large task.

### Requirement Change Rule

Bumping `revision` while tasks exist: `/scrum run` must BLOCK those tasks

(`reason: requirement_changed`) until SA re-analyzes.

Do not silently continue.

---
