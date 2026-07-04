#!/usr/bin/env python3
"""Inspect materials skill architecture contracts.

This root-level entrypoint delegates to the canonical implementation inside
``plugins/materials-skills/scripts/`` so the plugin package remains the single
source of truth for architecture validation.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PLUGIN_SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "materials-skills"
    / "scripts"
    / Path(__file__).name
)


def main() -> int:
    return subprocess.run([sys.executable, str(PLUGIN_SCRIPT)] + sys.argv[1:]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
