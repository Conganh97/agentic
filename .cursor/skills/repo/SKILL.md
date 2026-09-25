---
name: repo
description: Create/push product GitHub repos via repo.py. Use when invoked as /repo, e.g. "/repo create user-service be".
disable-model-invocation: true
---

# Repo

`python3 scripts/repo.py`. Config: `project.md` → Repositories. ADR-0004.

| Command | Who | Result |
|---------|-----|--------|
| `create <component> --type be\|fe` | **DEVOPS first**; BE/FE fallback | local + GHCR-ready `Dockerfile` + `.github/workflows/ci.yml`, private remote, `main` pushed, registry row |
| `push <component> [--branch B]` | BE/FE branch; SA `main`; DEVOPS | one branch, never force |
| `status` | anyone | branch, dirty, `main` ahead of origin |

Repository creation ownership:
1. DEVOPS creates repositories first.
2. BE/FE may create a repository only when no DEVOPS bootstrap task is READY or IN_PROGRESS for it.
3. If DEVOPS bootstrap is READY or IN_PROGRESS, BE/FE must wait.
4. The repository must be named in the approved SA design / `project.md` registry.
5. Never create an unapproved component repository.

- Names: `<name>-service` (BE), `frontend` (FE).
- `main` push only for `--no-ff` shas recorded as `merge_commit`. No force-push, no `gh repo delete`.
- `gh` missing → `NEEDS_INPUT` (`brew install gh && gh auth login`). Failed push: note it, do not undo the merge.
- `NEEDS_INPUT` is an outcome, not a task status. Never `--no-verify`.
- Create: `repo.py create …` then commit registry (`chore: register <component> repository`).
  Seeded files: `Dockerfile`, `ci.yml`, FE `nginx.conf`. App scaffold (Spring / Vite) is on the feature branch.
- Push: after product commit, `repo.py push <c> --branch <branch>`. After SA merge + `merge_commit` on disk: `repo.py push <c>`.
