#!/usr/bin/env python3
"""Inspect materials skill architecture contracts.

This root-level entrypoint delegates to the canonical implementation inside
``plugins/materials-skills/scripts/`` so the plugin package remains the single
source of truth for architecture validation.
"""

from __future__ import annotations

import sys
import importlib.util
from pathlib import Path


PLUGIN_SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "materials-skills"
    / "scripts"
    / Path(__file__).name
)
PLUGIN_SCRIPTS_DIR = PLUGIN_SCRIPT.parent


def _load_plugin_module():
    if str(PLUGIN_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(PLUGIN_SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location(
        "_materials_plugin_check_skill_architecture",
        PLUGIN_SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load plugin architecture checker: {PLUGIN_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PLUGIN_MODULE = _load_plugin_module()
inspect_skill = _PLUGIN_MODULE.inspect_skill
inspect_all = _PLUGIN_MODULE.inspect_all


def main() -> int:
    return _PLUGIN_MODULE.main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
