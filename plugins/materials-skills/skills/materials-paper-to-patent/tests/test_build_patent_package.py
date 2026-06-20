"""Unit tests for build_patent_package.py orchestration."""

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from build_patent_package import validate  # noqa: E402


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "civil-concrete-strengthening" / "draft.json"


def test_example_validates():
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    validate(data)


def test_missing_title_raises():
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["title"] = ""
    try:
        validate(data)
    except ValueError as e:
        assert "title" in str(e) or "Missing" in str(e)
    else:
        raise AssertionError("expected ValueError")


def test_missing_figure_descriptions_raises():
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["specification"]["figure_descriptions"] = []
    try:
        validate(data)
    except ValueError as e:
        assert "figure" in str(e).lower()
    else:
        raise AssertionError("expected ValueError")


def test_missing_equations_key_raises():
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    del data["specification"]["equations"]
    try:
        validate(data)
    except ValueError as e:
        assert "equations" in str(e)
    else:
        raise AssertionError("expected ValueError")


def test_contains_core_formulas_but_no_equations_raises():
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["source_analysis"]["contains_core_formulas"] = True
    data["specification"]["equations"] = []
    try:
        validate(data)
    except ValueError as e:
        assert "core formulas" in str(e)
    else:
        raise AssertionError("expected ValueError")


def test_equation_without_latex_raises():
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["specification"]["equations"] = [{"number": "公式1", "latex": ""}]
    try:
        validate(data)
    except ValueError as e:
        assert "latex" in str(e)
    else:
        raise AssertionError("expected ValueError")
