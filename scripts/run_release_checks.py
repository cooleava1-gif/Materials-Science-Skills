#!/usr/bin/env python3
"""Run release checks across all materials skills.

This root-level entrypoint delegates to the canonical implementation inside
``plugins/materials-skills/scripts/`` so the plugin package remains the single
source of truth for release validation.
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
