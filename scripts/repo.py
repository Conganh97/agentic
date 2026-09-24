#!/usr/bin/env python3
"""Manage product component repositories (one git repo + GitHub remote per service / frontend).

Usage:
  scripts/repo.py create <component> --type be|fe   create local repo + GitHub repo, push main, register
  scripts/repo.py push <component> [--branch B]     push a branch (main only if every new commit is a
                                                    reviewed merge recorded as merge_commit in a task)
  scripts/repo.py status                            list components: branch, clean, ahead of origin
Config and registry: "## Repositories" in project.md.
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = ROOT / "project.md"
REGISTRY_HEADER = "| Component | Type | Path | Remote |"

GITIGNORE = {
    "be": "target/\n.idea/\n*.iml\n.vscode/\n.DS_Store\n.env\n",
    "fe": "node_modules/\ndist/\ncoverage/\n.vscode/\n.DS_Store\n.env\n.env.local\n",
}
TEMPLATES = ROOT / "templates" / "ops"


def fail(msg):
    print(f"repo.py: {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        fail(f"`{' '.join(cmd)}` failed: {(result.stderr or result.stdout).strip()}")
    return result.stdout.strip()


def config():
    text = PROJECT.read_text()
    values = {}
    for key in ("GitHub owner", "Repo name", "Visibility"):
        m = re.search(rf"^- {key}: `([^`]*)`", text, re.M)
        if not m or not m.group(1) or "TODO" in m.group(1):
            fail(f"set '- {key}: `...`' in project.md ## Repositories")
        values[key] = m.group(1)
    return values


def registry():
    rows, inside = {}, False
    for line in PROJECT.read_text().splitlines():
        if line.startswith(REGISTRY_HEADER):
            inside = True
            continue
        if inside:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells[0] and not set(cells[0]) <= set("-: "):
                rows[cells[0]] = {"type": cells[1], "path": cells[2].strip("`"), "remote": cells[3]}
    return rows


def register(component, kind, path, remote):
    lines = PROJECT.read_text().splitlines(keepends=True)
    i = next((n for n, l in enumerate(lines) if l.startswith(REGISTRY_HEADER)), None)
    if i is None:
        fail(f"registry table '{REGISTRY_HEADER}' not found in project.md")
    j = i + 2
    while j < len(lines) and lines[j].startswith("|"):
        j += 1
    lines.insert(j, f"| {component} | {kind.upper()} | `{path}` | {remote} |\n")
    PROJECT.write_text("".join(lines))


def need_gh():
    if not shutil.which("gh"):
        fail("GitHub CLI missing: human runs `brew install gh && gh auth login` once")
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        fail("GitHub CLI not logged in: human runs `gh auth login` once")


def seed_ops(path, kind):
    """DevOps-owned Docker + GHA so the repo is born with a pushable image pipeline."""
    src = "Dockerfile.be" if kind == "be" else "Dockerfile.fe"
    shutil.copy(TEMPLATES / src, path / "Dockerfile")
    if kind == "fe":
        shutil.copy(TEMPLATES / "nginx.conf", path / "nginx.conf")
    wf = path / ".github" / "workflows"
    wf.mkdir(parents=True, exist_ok=True)
    shutil.copy(TEMPLATES / "ci.yml", wf / "ci.yml")


def create(component, kind):
    if not re.fullmatch(r"[a-z][a-z0-9-]*", component):
        fail("component must be kebab-case, e.g. user-service or frontend")
    if component in registry():
        fail(f"{component} is already registered in project.md")
    cfg = config()
    need_gh()
    rel = f"product/services/{component}" if kind == "be" else f"product/{component}"
    path = ROOT / rel
    name = cfg["Repo name"].replace("<component>", component)
    full = f"{cfg['GitHub owner']}/{name}"
    path.mkdir(parents=True, exist_ok=True)
    if not (path / ".git").exists():
        if any(path.iterdir()):
            fail(f"{rel} exists, is not empty and is not a git repo")
        run(["git", "init", "-q", "-b", "main"], cwd=path)
        (path / "README.md").write_text(f"# {component}\n\nPart of the product. Conventions: team repo `project.md`.\n")
        (path / ".gitignore").write_text(GITIGNORE[kind])
        seed_ops(path, kind)
        run(["git", "add", "README.md", ".gitignore", "Dockerfile", ".github"], cwd=path)
        if kind == "fe":
            run(["git", "add", "nginx.conf"], cwd=path)
        run(["git", "commit", "-q", "-m", "chore: initial repository"], cwd=path)
    if run(["git", "remote"], cwd=path):
        fail(f"{rel} already has a remote")
    run(["gh", "repo", "create", full, f"--{cfg['Visibility']}", "--source", str(path), "--remote", "origin",
         "--push"])
    remote = f"https://github.com/{full}"
    register(component, kind, rel, remote)
    print(f"created {rel} -> {remote} (main pushed, registered in project.md)")


def merge_commits_in_tasks():
    shas = set()
    for task in (ROOT / "tasks").glob("TASK-*.md"):
        m = re.search(r"^merge_commit:\s*`?([0-9a-f]{7,40})", task.read_text(), re.M)
        if m:
            shas.add(m.group(1)[:7])
    return shas


def push(component, branch):
    reg = registry().get(component) or fail(f"{component} is not registered in project.md")
    path = ROOT / reg["path"]
    if run(["git", "status", "--porcelain"], cwd=path):
        fail(f"{reg['path']} has uncommitted changes")
    run(["git", "rev-parse", "--verify", "-q", branch], cwd=path)
    if branch == "main":
        run(["git", "fetch", "-q", "origin"], cwd=path)
        has_remote_main = subprocess.run(["git", "rev-parse", "--verify", "-q", "origin/main"], cwd=path,
                                         capture_output=True).returncode == 0
        if has_remote_main:
            new = run(["git", "rev-list", "--first-parent", "--parents", "origin/main..main"], cwd=path).splitlines()
            recorded = merge_commits_in_tasks()
            for line in new:
                sha, *parents = line.split()
                if len(parents) < 2 or sha[:7] not in recorded:
                    fail(f"main commit {sha[:7]} is not a reviewed merge recorded as merge_commit in a task; "
                         "main is pushed only after SA merges")
    run(["git", "push", "-q", "origin", f"{branch}:{branch}"], cwd=path)
    print(f"pushed {component} {branch} -> {reg['remote']}")


def status():
    reg = registry()
    if not reg:
        print("no components registered")
    for name, r in reg.items():
        path = ROOT / r["path"]
        if not (path / ".git").exists():
            print(f"{name:24} MISSING {r['path']}")
            continue
        branch = run(["git", "branch", "--show-current"], cwd=path)
        dirty = "dirty" if run(["git", "status", "--porcelain"], cwd=path) else "clean"
        ahead = run(["git", "rev-list", "--count", "origin/main..main"], cwd=path, check=False) or "?"
        print(f"{name:24} {branch:36} {dirty:6} main ahead of origin: {ahead}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create")
    c.add_argument("component")
    c.add_argument("--type", choices=["be", "fe"], required=True)
    s = sub.add_parser("push")
    s.add_argument("component")
    s.add_argument("--branch", default="main")
    sub.add_parser("status")
    a = p.parse_args()
    if a.cmd == "create":
        create(a.component, a.type)
    elif a.cmd == "push":
        push(a.component, a.branch)
    else:
        status()


if __name__ == "__main__":
    main()
