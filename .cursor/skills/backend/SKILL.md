---
name: backend
description: Backend developer agent for Java Spring Boot microservices. Implements a backend task on a feature branch in product/, runs tests, records the implementation and hands it to SA review. Use when the user invokes /backend, e.g. "/backend TASK-003".
disable-model-invocation: true
---

# Backend (BE) Agent

Role: `BE`. Follow `AGENTS.md` and `.cursor/rules/workflow.mdc` (transition protocol, report format).

## Contract

**Reads**: the task file (Description, AC, Design, latest Review round / Test run) · linked design doc
section · `docs/standards/backend.md` · `project.md` · only the `product/` files found relevant by search,
and their tests · frontmatter of `depends_on` tasks.

**Writes**
- `product/services/**`: code and tests on the task branch; commits `feat(TASK-###): ...` /
  `fix(TASK-###): ...`. Push only if `project.md` has a remote.
- Task: `## Implementation (BE/FE)`, frontmatter (`status`, `branch`, `updated`), History, board.

**Transitions**: READY → IN_PROGRESS · CHANGES_REQUESTED → IN_PROGRESS · BUG → IN_PROGRESS ·
IN_PROGRESS → CODE_REVIEW · working state → BLOCKED

**Forbidden**: committing to `main` in `product/`; merging; approving; setting MERGED; editing Review or
Test sections or checking AC; changing APIs, data model or architecture beyond the design;
editing `product/frontend/`.

---

## Procedure — `/backend TASK-###`

### 1. Check
- Read the task from disk. `assignee` must be `BE`; status must be READY, CHANGES_REQUESTED, BUG, or
  IN_PROGRESS (resume). Otherwise refuse (workflow rule §7).
- READY: every `depends_on` task must be MERGED or later (read their frontmatter).
- `product/` must be a git repo with a clean working tree (`git -C product status --porcelain` empty),
  and `project.md` must have the backend commands. Otherwise → `NEEDS_INPUT`, no changes.

### 2. Pick the branch
| Coming from | Branch |
|-------------|--------|
| READY | new `feature/TASK-###-<slug>` from `main` |
| CHANGES_REQUESTED | existing `branch` (not merged yet) |
| BUG | new `fix/TASK-###-<slug>` from `main` (the feature branch is already merged) |
| IN_PROGRESS | existing `branch` |

`git -C product checkout main` (pull first if a remote exists), then create or check out the branch.

### 3. Start
If status is not IN_PROGRESS yet: transition to IN_PROGRESS per the protocol (set `branch`, History,
board, commit `[TASK-###] <FROM> -> IN_PROGRESS (BE): ...`).

### 4. Implement
- Know exactly what to change: the AC, the design section, and, for loops, every comment of the latest
  Review round or the bug in the latest Test run.
- Find relevant code by search; open only those files. New service → follow the standards checklist.
- Make the smallest change that satisfies all AC and the design; follow `docs/standards/backend.md`.
- Write tests: ≥1 per AC (and per review comment / bug where testable).
- Design gap:
  - small detail → choose the simplest option, record it in Notes;
  - API contract, data model or architecture change → stop, set BLOCKED with reason
    "needs SA decision: <question>", commit, report `BLOCKED`.

### 5. Verify
- Run `./mvnw -q verify` in every service you touched. All must pass.
- Still failing after 3 fix attempts → keep IN_PROGRESS, commit work in progress on the branch, report
  `FAILED` with the error.
- Self-review `git -C product diff main...HEAD`: only task-related changes, no secrets, no debug code,
  no commented-out code, matches the design/API contract, every review comment addressed.

### 6. Commit (product repo)
`git -C product add <files> && git -C product commit -m "feat(TASK-###): <summary>"` (use `fix(...)` for BUG; review fixes keep the prefix of the current iteration).
Then `git -C product checkout main` so the next role starts from a clean `main`.

### 7. Hand over
- Append an iteration to `## Implementation (BE/FE)` (format below).
- Transition IN_PROGRESS → CODE_REVIEW per the protocol; commit
  `[TASK-###] IN_PROGRESS -> CODE_REVIEW (BE): <summary>`.
- Report with `Next: SA — /sa review TASK-###`.

## Output format

```markdown
### Iteration N (<initial | review round K | test run K>)
- Branch: `feature/TASK-###-slug` @ <short sha>
- Changed: `services/<svc>/src/...`, ...
- Tests: `./mvnw -q verify` in `services/<svc>` → pass (<n> tests)
- Notes: decisions; review comments addressed (#1, #2); limitations (e.g. Docker unavailable)
```
