# Lessons Learned

Recurring review findings, bugs and failed approaches. Append-only. Read by SA (review) and TEST.

| Date | Source | Lesson | Applies to |
|------|--------|--------|------------|
| 2026-09-23 | TASK-001 review round 1 | When an AC specifies an exact JSON body, assert it with `isStrictlyEqualTo`, not `isLenientlyEqualTo` (lenient ignores extra fields) | BE |
