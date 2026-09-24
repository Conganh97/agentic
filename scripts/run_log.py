#!/usr/bin/env python3
"""Append an orchestrator history row.

Usage:
  python3 scripts/run_log.py --run RUN-001 --actor SCRUM --req REQ-001 \\
      --task TASK-002 --from IN_PROGRESS --to CODE_REVIEW \\
      --reason "implementation completed" --evidence "commit abc123"
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOURNAL = ROOT / "runs" / "journal.md"
HEADER = """# Run journal

Append-only. Written by `python3 scripts/run_log.py` during `/scrum run`.

| Time | Run | Actor | Requirement | Task | From | To | Reason | Evidence |
|------|-----|-------|-------------|------|------|----|--------|----------|
"""


def now() -> str:
    out = subprocess.run(["date", "+%Y-%m-%d %H:%M"], capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run", required=True)
    p.add_argument("--actor", required=True)
    p.add_argument("--req", default="")
    p.add_argument("--task", default="")
    p.add_argument("--from", dest="frm", default="")
    p.add_argument("--to", default="")
    p.add_argument("--reason", default="")
    p.add_argument("--evidence", default="")
    args = p.parse_args()
    JOURNAL.parent.mkdir(exist_ok=True)
    if not JOURNAL.exists():
        JOURNAL.write_text(HEADER)
    row = (
        f"| {now()} | {args.run} | {args.actor} | {args.req} | {args.task} | "
        f"{args.frm} | {args.to} | {args.reason} | {args.evidence} |\n"
    )
    JOURNAL.write_text(JOURNAL.read_text() + row)
    run_file = ROOT / "runs" / f"{args.run}.md"
    if run_file.exists():
        run_file.write_text(run_file.read_text() + row.replace(f"| {args.run} |", "|"))
    print(row.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
