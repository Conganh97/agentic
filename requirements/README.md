# Requirements

Copy `templates/requirement.md` → `requirements/REQ-###-<kebab-slug>.md`.

```
python3 scripts/req.py hash requirements/REQ-###-<slug>.md
```

Set `content_hash`, then HUMAN sets `status: APPROVED`. Body edit → bump `revision` and re-hash.

Child tasks use `parent: REQ-###`. REQ status owners: workflow §13.
