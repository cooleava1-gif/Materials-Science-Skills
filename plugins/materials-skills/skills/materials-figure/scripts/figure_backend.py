#!/usr/bin/env python3
"""Persisted figure-backend preference for materials-figure.

get      — print the saved backend (or "python (default)").
set X    — persist python|r as the exclusive backend preference.

The preference file is .materials/figure_backend.json under the current
project (git-ignored by convention); MATERIALS_FIGURE_BACKEND=r|python
overrides the file. Adapted from nature-skills' backend preference pattern
(Apache-2.0).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

VALID = {"python", "r"}


def pref_path() -> Path:
    return Path(".materials") / "figure_backend.json"


def get_saved() -> str | None:
    env = os.environ.get("MATERIALS_FIGURE_BACKEND", "").strip().lower()
    if env in VALID:
        return env
    path = pref_path()
    if path.is_file():
        try:
            value = json.loads(path.read_text(encoding="utf-8")).get("backend")
        except (json.JSONDecodeError, OSError):
            return None
        if value in VALID:
            return value
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["get", "set"])
    parser.add_argument("backend", nargs="?", choices=sorted(VALID))
    args = parser.parse_args()

    if args.action == "get":
        value = get_saved()
        print(value if value else "python (default)")
        return 0

    if args.backend is None:
        parser.error("set requires a backend: python|r")
    path = pref_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"backend": args.backend}, indent=2), encoding="utf-8")
    print(f"saved: {args.backend}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
