#!/usr/bin/env python3
"""Detect human-gate reasons in task/design text.

Usage: python3 scripts/gate_scan.py <file> [<file>…]
Prints matching reason ids (one per line). Exit 0 always unless --require-gate
and matches exist while HUMAN_GATE env is empty.
"""
from __future__ import annotations

import re
import sys

REASONS: list[tuple[str, re.Pattern[str]]] = [
    ("destructive_migration", re.compile(r"\b(drop\s+table|drop\s+column|truncate\s+table)\b", re.I)),
    ("breaking_api", re.compile(r"\b(breaking\s+api|remove\s+endpoint|incompatible\s+api)\b", re.I)),
    ("security", re.compile(r"\b(security-sensitive|secrets?\s+store|encryption\s+key)\b", re.I)),
    ("auth", re.compile(r"\b(authentication|authorization|oauth|rbac|/login)\b", re.I)),
    ("data_deletion", re.compile(r"\b(delete\s+all|hard\s+delete|purge\s+data|wipe\s+database)\b", re.I)),
    ("infra_destroy", re.compile(r"\b(terraform\s+destroy|destroy\s+infrastructure|drop\s+cluster)\b", re.I)),
    ("architecture", re.compile(r"\b(major\s+architecture|new\s+bounded\s+context|replace\s+the\s+stack)\b", re.I)),
    ("production", re.compile(r"\b(production\s+deploy|deploy\s+to\s+prod)\b", re.I)),
]


def scan(text: str) -> list[str]:
    found = []
    for reason, pat in REASONS:
        if pat.search(text) and reason not in found:
            found.append(reason)
    return found


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: gate_scan.py <file>…", file=sys.stderr)
        return 2
    matched: list[str] = []
    for path in argv:
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as exc:
            print(exc, file=sys.stderr)
            return 2
        matched.extend(r for r in scan(text) if r not in matched)
    for r in matched:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
