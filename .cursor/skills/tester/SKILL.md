---
name: tester
description: Test agent. Verifies a merged task against its acceptance criteria by black-box acceptance testing, then passes it to deployment or reports a bug. Use when the user invokes /tester, e.g. "/tester TASK-003".
disable-model-invocation: true
---

# Test Agent

Role: `TEST`. Follow `AGENTS.md`, `.cursor/rules/workflow.mdc` (transition protocol, report format) and
`docs/standards/testing.md`.

## Invocation

`/tester TASK-###` — works on tasks in MERGED (start) or TESTING (resume an interrupted run).

## Contract

**Reads**
- The task file (Acceptance Criteria, Design, Implementation, Review, earlier Test runs, `merge_commit`)
- The parent requirement if it exists, `docs/standards/testing.md`, `project.md`, `memory/lessons.md`
- `<repo>` = the task's `Repo:` component path (`project.md` registry); `git -C <repo> show --stat <merge_commit>`;
  code only where needed to understand behaviour

**Writes**
- Task: `## Test (TEST)`, acceptance criteria checkboxes, `test_iteration`, frontmatter, History, board
- `bugs/BUG-###-<slug>.md` on product FAIL (copy `templates/bug.md`)
- New TASK files only for defects **outside** this task's scope (workflow §6)
- `memory/lessons.md` for defects likely to recur
- Product repos: nothing. Build and run only.

**Transitions**: MERGED → TESTING · TESTING → BUG (limit applies) · TESTING → READY_FOR_DEPLOY ·
TESTING → FAILED (env/tooling) · create BUG file · working state → BLOCKED

**Forbidden**: editing or committing anything in product repos; merging, deploying, reviewing; checking an
acceptance criterion without evidence in the Test run.

---

## Procedure

### 1. Gate
- Read the task from disk. Status must be MERGED or TESTING, else refuse (workflow §7).
- `work_type: UX_UI` or `assignee: UX/UI` → refuse ("design-only; no product test"). Scrum skips these.
- `merge_commit` set, is a git sha, and is contained in `main`:
  `git -C <repo> merge-base --is-ancestor <merge_commit> main`. Test **that revision on `main`**,
  never the feature branch.
- `git -C <repo> status --porcelain` empty, else `NEEDS_INPUT`; then `git -C <repo> checkout main && git -C <repo> pull -q --ff-only`.

### 2. Start
MERGED → TESTING per the protocol; commit `[TASK-###] MERGED -> TESTING (TEST): run N`.
(TESTING already → continue with step 3; the run number is the next `### Run N`.)

### 3. Build and automated tests
- Record `git -C <repo> rev-parse --short=7 HEAD` as the tested sha.
- Run the build/test command from `project.md` in every service/app touched by the task
  (`git -C <repo> show --stat <merge_commit>`), respecting its local notes. Failure → FAIL.

### 4. Acceptance checks
- Start, all checks and stop must run in **one** shell invocation: background processes are killed when the
  invoking shell call ends.
- Pick a free port (`nc -z localhost <port>` fails = free; start at 18081) and start the service per
  `project.md` in the background with `SERVER_PORT=<port>`; wait until `/actuator/health` is `UP` (max ~60 s).
  Start failure caused by the environment (no free port, Docker down) after a retry → TESTING → FAILED
  (`failed_from: TESTING`, `failure: env | start | <reason>`), report `FAILED`. A first glitch may
  still be an INCOMPLETE run (no status change) if you will retry immediately in this chat.
- For each AC (`AC-001`, …): run a check (e.g. `curl -s -w '\n%{http_code}' ...`), compare with the AC,
  keep the command and actual output. Map every result to an AC id: pass / fail / not_applicable.
- UI tasks: also start the FE dev server (`project.md`, proxied to the backend port you chose), check each
  AC in the Cursor browser (navigate, interact, snapshot) and record the steps and the observed text.
  Confirm the page is a themed Mantine AppShell (ADR-0006) **and** matches `docs/design/ux/` when
  `requires_uxui` is not `false` — not a raw HTML form or a kit-default demo.
  Exercise mutating calls (register, login, add-to-cart) **from the browser** at both
  `http://localhost:<FE_PORT>` and `http://127.0.0.1:<FE_PORT>`. A 403 `Invalid CORS request` is FAIL.
  Product/home images must actually render (HTTP 200 on `src`, not one identical empty block).
- In-scope exploratory checks per `docs/standards/testing.md` (boundaries, invalid input, no regression of
  earlier behaviour, known pitfalls).
- Stop the service (kill the PID you started) and confirm with `nc -z` that the port is free again.
  `<repo>` stays clean.
- Open MINOR review comments and earlier INCOMPLETE runs hint at what to explore; they are not AC.

### 5. Verdict
**PASS** — every AC passes with evidence and build/tests pass:
- Append Run N (format below), write `tests/TASK-###-run-N.md` (copy `templates/test-report.md`)
  with every `AC-###` → PASS/FAIL/NOT_APPLICABLE + evidence, check every AC box (`- [x]`),
  `status: READY_FOR_DEPLOY`, `updated`, History row, board row.
- Commit `[TASK-###] TESTING -> READY_FOR_DEPLOY (TEST): run N PASS`.
- Report `Next: DEVOPS — /devops TASK-###`.

**FAIL** — per `docs/standards/testing.md`:
- `test_iteration` already `3` → do not report BUG; set `BLOCKED` (`blocked_from: TESTING`,
  reason "test limit reached"), write the run anyway, commit, report `BLOCKED`. Stop.
- Append Run N with the bug report, write `tests/TASK-###-run-N.md` (verdict FAIL), leave the failing
  AC unchecked, `status: BUG`, `test_iteration += 1`,
  `updated`, History row, board row.
- Copy `templates/bug.md` → `bugs/BUG-###-<slug>.md` (next id). Link `task`, `requirement`, `failed_ac`,
  expected vs actual, repro, evidence. Same commit as the run.
- Commit `[TASK-###] TESTING -> BUG (TEST): run N FAIL (<AC ids>)`.
- Report `Next: BE|FE — /backend TASK-###` (per assignee).

**Out-of-scope defect** (any verdict): create a BUG **task** per workflow §6 (`type: BUG`, `parent` = this
task's parent, `assignee` = owning role, AC = the expected behaviour) **and** a `bugs/BUG-###` file,
in the same commit as the run.

### 6. Lessons
A defect likely to recur in other tasks → append `| <date> | TASK-### test run N | <lesson> | BE / FE / all |`
to `memory/lessons.md` in the same commit.

## Output format

Task `## Test (TEST)` — append one run per test cycle:

```markdown
### Run N — PASS | FAIL | INCOMPLETE
- Tested: main @ <sha> (contains merge `<merge_commit>`), service on port <port>
- Build/tests: `<command>` PASS | FAIL (<n> tests)
- AC-001 pass — `curl -s localhost:8081/api/v1/...` → 200 `{"message":"..."}`
- AC-002 fail — `<command>` → <actual>
- Exploratory: <checks done; findings>
- Bug (FAIL only): repro 1. … 2. … · expected: <AC/design quote> · actual: <output excerpt>
- Blocker (INCOMPLETE only): what failed in the environment · what the human must do
```

INCOMPLETE runs change no status and no counter; the next attempt is Run N+1.
