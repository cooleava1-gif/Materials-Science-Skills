#!/usr/bin/env python3
"""Run release checks across all materials skills.

This root-level entrypoint delegates to the canonical implementation inside
``plugins/materials-skills/scripts/`` so the plugin package remains the single
source of truth for release validation.
"""

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
        "_materials_plugin_run_release_checks",
        PLUGIN_SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load plugin release checker: {PLUGIN_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_PLUGIN_MODULE = _load_plugin_module()
FIGURE_HARD_WORKFLOW_FILES = _PLUGIN_MODULE.FIGURE_HARD_WORKFLOW_FILES
FIGURE_REPRESENTATIVE_ASSET_FILES = _PLUGIN_MODULE.FIGURE_REPRESENTATIVE_ASSET_FILES
WRITING_MATURITY_FILES = _PLUGIN_MODULE.WRITING_MATURITY_FILES
WRITING_STATE_MACHINE_FILES = _PLUGIN_MODULE.WRITING_STATE_MACHINE_FILES
collect_paper_production_orchestrator_issues = _PLUGIN_MODULE.collect_paper_production_orchestrator_issues
collect_writing_maturity_issues = _PLUGIN_MODULE.collect_writing_maturity_issues
collect_writing_state_machine_issues = _PLUGIN_MODULE.collect_writing_state_machine_issues
check_skill_basics = _PLUGIN_MODULE.check_skill_basics
check_experiment_record_files = _PLUGIN_MODULE.check_experiment_record_files
check_experiment_record = _PLUGIN_MODULE.check_experiment_record


def main() -> int:
    return _PLUGIN_MODULE.main()


if __name__ == "__main__":
    raise SystemExit(main())
