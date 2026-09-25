---
requirement: REQ-001
round: 1
status: CHANGES_REQUESTED
reviewer: PQA
updated: 2026-09-25 14:30
---

# REQ-001 plan review 1

Read: `docs/design/REQ-001-design.md` + proposed tasks TASK-001..TASK-008.

API-only increment. §13 is correctly **none**. No frontend or UX/UI task requested.

| # | Area | Severity | Comment |
|---|------|----------|---------|
| 1 | Scope / FR / NFR | MAJOR | NFR-5 (stale `RUNNING` jobs older than `crawler.job.stale-after`, default 30m, marked `FAILED` on the next create/status read or a scheduled sweep) is in design §4, §6 final-status rules, and §9 risk mitigation, but is **not** in any task `Covers` list or Design section. Assign it to TASK-005 and/or TASK-006 (recommended: TASK-005 status/create path + optional sweep), or remove NFR-5 from the design. Do not leave an orphaned NFR. |
| 2 | §13 screens + density | — | Correctly **none**. REQ and design exclude user-facing UI. No UX/UI task. Density bar N/A. |
| 3 | Task graph / roles | MAJOR | AC-001 lives on TASK-001, which forbids Spring scaffolding (`repo.py create` seeds README + Dockerfile/GHA only). After TASK-001 the API image has no application, so “the service can start” cannot be demonstrated. Move **AC-001** to TASK-002 (the task that actually starts the process). Keep **AC-030** on TASK-001 (Docker/compose/GHA). Graph has no cycles; roles, `depends_on`, and DoR fields are otherwise complete. No FE/UX_UI task (correct). |
| 4 | AC mapping | MINOR | All 34 REQ ACs appear on exactly one task. AC-022 / NFR-6 crawl fields (`jobId`, `sourceVideoId`, outcome) are tasked only on the skeleton (TASK-002) before crawl exists — add a Design note on TASK-006 to emit those fields. `crawl_job` / `crawl_job_item` Flyway ownership is implicit; state it on TASK-005 / TASK-006. |

Density bar: feed/list has ≥2 content units above the fold; no chrome+void; no lonely centered form.

**Decision:** CHANGES_REQUESTED

Must-fix before plan APPROVED:

1. Own **NFR-5** on a BE task (or drop it from the design).
2. Move **AC-001** from TASK-001 → TASK-002 so the start AC is on the task that scaffolds the app. Leave AC-030 on TASK-001.

Next: `/sa analyze REQ-001` (revise design/tasks, stay ANALYZING).
