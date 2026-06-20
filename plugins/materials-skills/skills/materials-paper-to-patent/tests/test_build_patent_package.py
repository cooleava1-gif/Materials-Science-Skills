"""Unit tests for build_patent_package.py orchestration."""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from build_patent_package import main, validate  # noqa: E402


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "civil-concrete-strengthening" / "draft.json"
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_patent_package.py"


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


def test_main_reports_structural_validation_errors(tmp_path, monkeypatch):
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    del data["claims"]
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    output_dir = tmp_path / "package"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_patent_package.py",
            str(draft),
            "--output-dir",
            str(output_dir),
            "--prefix",
            "case",
        ],
    )

    try:
        main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("expected SystemExit")

    reports = list(output_dir.glob("*.txt"))
    assert len(reports) == 1
    assert "missing_top_key" in reports[0].read_text(encoding="utf-8")


def test_flowchart_cli_writes_svg_and_png(tmp_path):
    steps = tmp_path / "steps.json"
    steps.write_text(
        json.dumps(
            [
                {"label": "称量水泥", "kind": "step"},
                {"label": "标准养护", "kind": "result"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    svg = tmp_path / "figure-1.svg"
    png = tmp_path / "figure-1.png"
    flowchart_script = SCRIPT.parent / "render_flowchart_svg.py"

    result = subprocess.run(
        [
            sys.executable,
            str(flowchart_script),
            str(steps),
            "--output",
            str(svg),
            "--png-output",
            str(png),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert svg.exists()
    assert png.exists()
    assert png.stat().st_size > 0


def test_cli_builds_example_package(tmp_path):
    output_dir = tmp_path / "package"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(EXAMPLE),
            "--output-dir",
            str(output_dir),
            "--prefix",
            "case",
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert (output_dir / "case-figures" / "figure-1.png").exists()
    assert (output_dir / "case-权利要求书.docx").exists()
    assert (output_dir / "case-说明书.docx").exists()
    assert (output_dir / "case-说明书摘要.docx").exists()
    assert (output_dir / "case-摘要附图.docx").exists()
    assert (output_dir / "case-完整审阅稿.docx").exists()
    assert (output_dir / "case-草稿验证报告.txt").exists()
    assert (output_dir / "case-权利要求检查.txt").exists()
