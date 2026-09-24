---
task: TASK-XXX
run: 1
verdict: PASS              # PASS | FAIL | INCOMPLETE | NOT_APPLICABLE
tested_sha:
merge_commit:
updated:
---

# TASK-XXX Test Run 1

- Tested: `main` @ `<sha>` (contains `merge_commit`)
- Build/tests: `<command>` PASS | FAIL

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS / FAIL / NOT_APPLICABLE | `curl …` → 200 `…` |

Exploratory:

Bug (FAIL): repro · expected · actual · `bugs/BUG-###-*.md`
