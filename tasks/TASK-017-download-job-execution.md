---
id: TASK-017
title: Job execution, storage write, metrics, and diagnostics
type: TASK
priority: HIGH
status: BACKLOG
assignee: BE
parent: REQ-002
requirement_revision: 1
repo: video-downloader-service
work_type: BACKEND
requires_uxui: false
uxui_task:
uxui_design:
uxui_review:
figma:
depends_on: [TASK-012, TASK-013, TASK-016]
sprint:
branch:
merge_commit:
release:
review_iteration: 0
uxui_review_iteration: 0
test_iteration: 0
blocked_from:
failed_from:
failure_type:
failure_step:
failure_message:
failure_retry: 0
failure_recoverable:
human_gate:
approved_by:
approved_at:
updated: 2026-09-25 16:33
---

## Description

Wire the async runner: PENDING → RUNNING → provider.download → VideoStorage.put → COMPLETED, or
FAILED with `errorCode` / safe `errorMessage` without crashing the process. GET then returns
metadata including `storageKey`, `fileSize`, `contentType` when COMPLETED. Emit structured log
fields and Prometheus metrics from design §6. Tests use the mock provider.

## Acceptance Criteria
- [ ] AC-016 A successful provider response results in a downloadable video artifact.
- [ ] AC-024 A download failure does not crash the service.
- [ ] AC-036 Download metadata can be queried through an API.
- [ ] AC-037 Provider failures contain sufficient diagnostic information for troubleshooting without logging sensitive information.
- [ ] AC-039 Metrics are available for download jobs, successful downloads, failed downloads, provider latency, and download duration.

## Design (SA)

`docs/design/REQ-002-design.md` §6 metrics and job resource, FR-7, FR-9 (no crash), FR-14, NFR-5
emit `downloadId` / outcome / `errorCode`, NFR-6. Never log cookies, tokens, API keys, or
`cdn_headers`. If status is CANCELLED mid-run, do not mark COMPLETED. Retry policy details are
TASK-018; this task must isolate exceptions.

## Implementation (BE/FE)

## UX/UI Review
PQA writes visual rounds here / `docs/design/ux/reviews/`. UX/UI does not approve its own look.

## Review (SA)
Code only. PQA owns UX_UI merge and FE visual `uxui_review`.

## Test (TEST)

## Deployment (DEVOPS)

## History
| Time | From | To | By | Note |
|------|------|----|----|------|
| 2026-09-25 16:33 | — | BACKLOG | SA | Created from REQ-002 design revision 1 hash b06116020682e658 |
