# Bugs

Persistent defect records (workflow item: BUG lifecycle). One file per product defect.

- Template: `templates/bug.md`
- Id: `BUG-###` (next free number), file `bugs/BUG-###-<kebab-slug>.md`
- TEST creates a file when a test run FAILs (TESTING → BUG on the task)
- Close only after regression testing on `main` (`status: CLOSED`, `fix_commit` set)

Do not store secrets or personal data in evidence excerpts.
