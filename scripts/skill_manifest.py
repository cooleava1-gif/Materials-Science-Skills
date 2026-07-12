"""Root-level compatibility shim for materials skill discovery.

The canonical implementation lives in ``plugins/materials-skills/scripts``.
This file keeps historical imports such as ``scripts.skill_manifest`` working
without duplicating the discovery logic.
"""

from __future__ import annotations

import importlib.util
import sys
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
        "_materials_plugin_skill_manifest",
        PLUGIN_SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load plugin skill manifest helper: {PLUGIN_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PLUGIN_MODULE = _load_plugin_module()

discover_skill_dirs = _PLUGIN_MODULE.discover_skill_dirs
discover_skill_names = _PLUGIN_MODULE.discover_skill_names
iter_skill_manifests = _PLUGIN_MODULE.iter_skill_manifests
load_yaml = _PLUGIN_MODULE.load_yaml
DEFAULT_SKILLS_ROOT = _PLUGIN_MODULE.DEFAULT_SKILLS_ROOT
