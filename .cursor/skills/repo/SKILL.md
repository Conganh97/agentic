---
name: repo
description: Creates the GitHub repository for a new product component (backend service or frontend) and pushes code to it under the push policy. Use when the user invokes /repo, e.g. "/repo create user-service be", "/repo push user-service", "/repo status", or when another skill needs a component repo that does not exist yet.
disable-model-invocation: true
---

# Repo Skill

Mechanical repository management for `product/`. Config and registry: `project.md` → "## Repositories";
decision: `docs/adr/0004-repo-per-component.md`. Everything goes through `python3 scripts/repo.py`.

| Invocation | Who may run it | Does |
|------------|----------------|------|
| `/repo create <component> be\|fe` | **DEVOPS first** (owns the repo + pipeline). BE/FE only if no DevOps task is in flight and they must proceed | local repo + Dockerfile + GHA, private GitHub remote, `main` pushed, registry row |
| `/repo push <component> [branch]` | BE/FE (their task branch), SA (`main` after merge), DEVOPS | pushes one branch, never forced |
| `/repo status` | anyone | branch, clean/dirty, commits of `main` not yet pushed |

## Rules

- Component names are kebab-case: `<name>-service` for backend, `frontend` for the web app.
- Create only components named in an approved design (task Design section or `docs/design/`).
  Anything else → `NEEDS_INPUT` for SA.
- `main` is pushed only when every new first-parent commit is a `--no-ff` merge whose sha is a task's
  `merge_commit`; the script enforces this. Never push `main` any other way, never force-push, never
  delete or rename GitHub repos (the shell guard blocks these).
- `gh` must be installed and logged in by a human once (`brew install gh && gh auth login`). If the script
  reports it missing → `NEEDS_INPUT` with that command; do not try other credentials.
- A failed push does not undo a merge or a transition: record "push failed: <error>" in your section
  (Implementation / Review / Deployment), report it, and continue.

## Procedure — `create`

1. Check the component is in the design and not yet in the registry (`/repo status`).
2. `python3 scripts/repo.py create <component> --type be|fe` (needs network + full permissions).
3. The script leaves `main` with `README.md`, `.gitignore`, `Dockerfile`, `.github/workflows/ci.yml`
   (FE also `nginx.conf`). App scaffolding (Spring Boot, Vite) is still on the feature branch.
   DevOps repairs those files if they already exist and are wrong.
4. Commit the updated `project.md` registry in the team repo together with your next task commit (or alone:
   `chore: register <component> repository`).

## Procedure — `push`

- Task branch: `python3 scripts/repo.py push <component> --branch <branch>` after the product commit.
- `main`: `python3 scripts/repo.py push <component>` right after the SA merge commit and after `merge_commit`
  is written to the task file on disk.
