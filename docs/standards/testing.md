# Testing Standards

Acceptance after MERGED. Commands: `project.md`. TEST never commits to `product/`.

| Level | Owner | Where |
|-------|--------|--------|
| Unit / slice | BE / FE | task branch; SA reviews |
| Acceptance | TEST | `main` at `merge_commit`; evidence in the task |

## Run

- Build/test every touched app (`project.md`). Must pass.
- Start the service; each AC = one black-box check with command + output.
- Also: boundaries, empty/invalid input, no regression of earlier AC, `memory/lessons.md`.
- UI: matches `docs/design/ux/` + Figma (if linked); not a raw form. Browser POSTs from both
  `localhost` and `127.0.0.1` (403 CORS = FAIL). Images must load (not one blank/404 for all).
- Stop processes; leave `product/` clean.

## Verdict

**PASS** — build + every AC with evidence. **FAIL** — AC/design/standards miss (→ BUG).
Env/tooling → **FAILED** (workflow), not BUG. Flaky (pass only on retry) → FAIL.
READY_FOR_DEPLOY forbidden while an `AC-###` is unchecked.

Bug report: numbered repro, quoted expected, actual excerpt (no secrets).
