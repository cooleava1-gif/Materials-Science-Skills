#!/usr/bin/env python3
"""Compatibility entrypoint for plugin handoff validation."""

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
        "_materials_plugin_validate_handoffs",
        PLUGIN_SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load plugin handoff validator: {PLUGIN_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PLUGIN_MODULE = _load_plugin_module()
load_contract = _PLUGIN_MODULE.load_contract
collect_manifest_handoff_topology = _PLUGIN_MODULE.collect_manifest_handoff_topology
validate_all = _PLUGIN_MODULE.validate_all


def main() -> int:
    return _PLUGIN_MODULE.main()


if __name__ == "__main__":
    raise SystemExit(main())
