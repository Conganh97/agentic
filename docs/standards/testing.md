# Testing Standards

Applies to verification of every task after MERGED. Stack and commands: `project.md`.

## Who tests what

| Level | Owner | Where | Reviewed by |
|-------|-------|-------|-------------|
| Unit, web slice, repository tests | BE / FE | `product/`, on the task branch | SA (code review) |
| Regression test for a bug | BE / FE | in the fix, on the task branch | SA |
| Acceptance (black-box) against AC | TEST | runs against the merged code; evidence in the task file | — |

TEST does not commit to `product/`. Missing or weak automated tests are a finding for the task (BUG when
an AC is untested and fails, otherwise a note in the Test run).

## Acceptance run

- Test what is on `product/main` (it contains `merge_commit`); record the exact sha tested.
- Run the full build/test command for every service/app the task touched; it must pass.
- Start the service as documented in `project.md` and exercise each AC as a black-box: observable input →
  observable output (HTTP request/response, UI behaviour, data state).
- Every AC gets its own check with evidence: the exact command and the relevant actual output
  (status code, body excerpt). An AC without evidence is not checked.
- Also try, within the task's scope: boundaries (e.g. exact limits ±1), empty/missing/invalid input, and
  the behaviour that the task must not break (earlier AC of the same service, pitfalls in `memory/lessons.md`).
- Stop every process you started; leave `product/` clean on `main`.

## Verdict

- **PASS**: build/tests pass and every AC passes with evidence.
- **FAIL**: any AC fails, the build/tests fail, or an in-scope check shows a defect that breaks the design
  or standards (e.g. 500 instead of 400, stack trace in a response).
- A test that passes only on retry is flaky → FAIL, with both results recorded.
- Defects outside the task's scope → a new BUG task (workflow §6), not a FAIL of this task.
- Environment problems (port busy, Docker down) are not a FAIL: report `NEEDS_INPUT` and keep TESTING.

## Bug report (in the Test run)

- Repro: numbered steps from a clean `main` (commands, input).
- Expected: quote the AC or design line.
- Actual: status/output excerpt (≤ 15 lines of logs; never secrets or personal data).
- Scope hint: suspected file/area if obvious — the fix belongs to BE/FE.
