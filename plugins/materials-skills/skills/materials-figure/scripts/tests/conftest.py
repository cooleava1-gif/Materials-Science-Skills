"""conftest for validate_materials_claims tests.

Adds the parent ``scripts/`` directory to ``sys.path`` so that the test
module can import ``validate_materials_claims`` directly. The plan's
intended import path ``plugins.materials_skills.skills.materials_figure.
scripts.validate_materials_claims`` does not work on this repository
because the on-disk directory is ``plugins/materials-skills/`` (hyphen
in the name, which Python's import system rejects).
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
