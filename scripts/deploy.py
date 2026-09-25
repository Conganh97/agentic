#!/usr/bin/env python3
"""Build product images, push GHCR, compose up on this machine (ADR-0011).

Usage:
  python3 scripts/deploy.py --env DEV|STG|PROD [--component NAME] [--skip-push] [--skip-up]
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import repo  # noqa: E402

ENVS = {
    "DEV": {"file": "dev.yml", "env": ".env.dev", "channel": "dev",
            "api": 18081, "web": 15173},
    "STG": {"file": "stg.yml", "env": ".env.stg", "channel": "stg",
            "api": 28081, "web": 25173},
    "PROD": {"file": "prod.yml", "env": ".env.prod", "channel": "prod",
             "api": 8080, "web": 80},
}


def fail(msg: str, code: int = 1) -> None:
    print(f"deploy.py: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd: list[str], cwd=None, check=True, input_text=None) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, input=input_text)
    if check and result.returncode != 0:
        fail(f"`{' '.join(cmd)}` failed: {(result.stderr or result.stdout).strip()}")
    return result


def need_docker() -> None:
    if not shutil.which("docker"):
        fail("Docker missing: human installs Docker Desktop")
    if run(["docker", "info"], check=False).returncode != 0:
        fail("Docker is not running")


def ghcr_login(owner: str) -> None:
    if not shutil.which("gh"):
        fail("GitHub CLI missing: `brew install gh && gh auth login`")
    token = run(["gh", "auth", "token"]).stdout.strip()
    if not token:
        fail("gh auth token empty: human runs `gh auth login` and `gh auth refresh -s write:packages`")
    login = run(
        ["docker", "login", "ghcr.io", "-u", owner, "--password-stdin"],
        input_text=token,
        check=False,
    )
    if login.returncode != 0:
        fail(
            "GHCR login failed. Human: `gh auth refresh -s write:packages` "
            f"then retry. {(login.stderr or login.stdout).strip()}"
        )


def sha_of(path: pathlib.Path) -> str:
    return run(["git", "rev-parse", "--short", "HEAD"], cwd=path).stdout.strip()


def image_name(owner: str, component: str, channel: str, sha: str) -> tuple[str, str]:
    base = f"ghcr.io/{owner.lower()}/product-{component.lower()}"
    return f"{base}:{channel}-{sha}", f"{base}:{channel}"


def write_env(path: pathlib.Path, values: dict[str, str], defaults: dict) -> None:
    lines = [
        f"GITHUB_OWNER={values.get('GITHUB_OWNER', '')}",
        f"API_IMAGE={values.get('API_IMAGE', '')}",
        f"WEB_IMAGE={values.get('WEB_IMAGE', '')}",
        f"POSTGRES_DB={values.get('POSTGRES_DB', 'app')}",
        f"POSTGRES_USER={values.get('POSTGRES_USER', 'app')}",
        f"POSTGRES_PASSWORD={values.get('POSTGRES_PASSWORD', 'app')}",
        f"API_PORT={values.get('API_PORT', str(defaults['api']))}",
        f"WEB_PORT={values.get('WEB_PORT', str(defaults['web']))}",
        f"DB_PORT={values.get('DB_PORT', '')}",
    ]
    path.write_text("\n".join(lines) + "\n")


def load_env(path: pathlib.Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text().splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip()
    return out


def smoke(url: str, timeout: int = 45) -> str:
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                return f"{resp.status} {url}"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = str(exc)
            time.sleep(2)
    fail(f"smoke failed {url}: {last}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--env", required=True, choices=sorted(ENVS))
    p.add_argument("--component")
    p.add_argument("--skip-push", action="store_true")
    p.add_argument("--skip-up", action="store_true")
    args = p.parse_args()
    spec = ENVS[args.env]
    channel = spec["channel"]
    cfg = repo.config()
    owner = cfg["GitHub owner"]
    rows = repo.registry()
    if args.component:
        if args.component not in rows:
            fail(f"{args.component} is not in the project.md registry")
        rows = {args.component: rows[args.component]}
    if not rows:
        fail("no components registered; DevOps creates them with scripts/repo.py create", 2)
    if not args.component:
        be_n = sum(1 for r in rows.values() if r["type"].upper() == "BE")
        fe_n = sum(1 for r in rows.values() if r["type"].upper() == "FE")
        if be_n > 1:
            fail("compose has one API_IMAGE; pass --component or update ops/compose for multiple services", 2)
        if fe_n > 1:
            fail("compose has one WEB_IMAGE; pass --component or update ops/compose for multiple frontends", 2)

    need_docker()
    if not args.skip_push:
        ghcr_login(owner)

    pushed: dict[str, str] = {}
    for name, row in rows.items():
        path = ROOT / row["path"]
        dockerfile = path / "Dockerfile"
        if not path.is_dir() or not (path / ".git").exists():
            fail(f"{row['path']} is missing — DevOps /repo create {name} {row['type'].lower()}")
        if not dockerfile.is_file():
            fail(f"{row['path']} has no Dockerfile — copy templates/ops and commit on ops/TASK-###")
        sha = sha_of(path)
        tagged, floating = image_name(owner, name, channel, sha)
        print(f"building {tagged}")
        run(["docker", "build", "-t", tagged, "-t", floating, "."], cwd=path)
        if not args.skip_push:
            run(["docker", "push", tagged])
            run(["docker", "push", floating])
        pushed[name] = tagged
        print(f"image {tagged}")

    env_path = ROOT / "ops" / "compose" / spec["env"]
    values = load_env(env_path)
    values["GITHUB_OWNER"] = owner
    for name, row in rows.items():
        kind = row["type"].upper()
        if kind == "BE":
            values["API_IMAGE"] = pushed[name]
        if kind == "FE":
            values["WEB_IMAGE"] = pushed[name]
    values.setdefault("API_PORT", str(spec["api"]))
    values.setdefault("WEB_PORT", str(spec["web"]))
    write_env(env_path, values, spec)
    print(f"wrote {env_path.relative_to(ROOT)}")

    if args.skip_up:
        return 0

    compose = ROOT / "ops" / "compose" / spec["file"]
    if not compose.is_file():
        fail(f"missing {compose}")
    cmd = ["docker", "compose", "-f", str(compose), "--env-file", str(env_path), "up", "-d"]
    run(cmd, cwd=ROOT / "ops" / "compose")
    print("compose up")

    api_port = values.get("API_PORT") or str(spec["api"])
    web_port = values.get("WEB_PORT") or str(spec["web"])
    if values.get("API_IMAGE"):
        print(smoke(f"http://127.0.0.1:{api_port}/actuator/health"))
    if values.get("WEB_IMAGE"):
        print(smoke(f"http://127.0.0.1:{web_port}/"))
    print("deploy ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
