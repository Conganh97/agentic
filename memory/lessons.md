# Lessons Learned

Recurring review findings, bugs and failed approaches. Append-only. Read by SA (review) and TEST.

| Date | Source | Lesson | Applies to |
|------|--------|--------|------------|
| 2026-09-23 | TASK-001 review round 1 | When an AC specifies an exact JSON body, assert it with `isStrictlyEqualTo`, not `isLenientlyEqualTo` (lenient ignores extra fields) | BE |
| 2026-09-24 | ADR-0006 | FE must ship Mantine AppShell + kit controls (ADR-0006). Browser-default inputs/buttons or a CSS-only white form is a MAJOR standards miss, even if ACs pass | FE / SA |
| 2026-09-24 | TASK-002 review round 1 | Do not put `@EntityGraph` collection paths (`images`) on `findTopN` / paginated queries — Hibernate logs HHH90003004 and applies the limit in memory. Fetch the collection in a second query. | BE |
