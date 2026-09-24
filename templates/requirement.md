---
id: REQ-XXX
title:
status: DRAFT          # DRAFT | APPROVED | ANALYZING | ANALYZED | IN_PROGRESS | TESTING | READY_FOR_RELEASE | RELEASED | BLOCKED | CANCELLED
revision: 1
content_hash:            # python3 scripts/req.py hash requirements/REQ-XXX-*.md
priority: MEDIUM       # LOW | MEDIUM | HIGH | CRITICAL
owner:                 # human name
design:                # docs/design/REQ-XXX-design.md (set by SA)
tasks: []              # [TASK-001, ...] (set by SA)
updated:
---

## Goal
Why this is needed and who benefits.

## Scope
- What must be delivered.

## Out of Scope
- What must not be done.

## User Stories / Behaviour
- As a <user>, I want <capability>, so that <benefit>.

## Acceptance Criteria (business level)
- [ ] AC-001 ...

## Constraints
Technology, performance, security, deadlines, compatibility.

## Notes
Links, mockups, examples.

Bumping `revision` while tasks exist: `/scrum run` must BLOCK those tasks
(`reason: requirement_changed`) until SA re-analyzes. Do not silently continue.
