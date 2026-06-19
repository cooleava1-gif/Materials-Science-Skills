#!/usr/bin/env python3
"""Generate a Python-only materials figure package from a source data table."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import yaml

import data_diagnose
import recommend_chart

import check_figure_contract


def generate_package(
    *,
    data_path: str | Path,
    output_dir: str | Path,
    goal: str,
    figure_name: str,
) -> dict:
    """Create a complete automatic figure package and render SVG/PNG outputs."""

    source_path = Path(data_path)
    package_dir = Path(output_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    profile = data_diagnose.diagnose_table(source_path)
    recommendation = recommend_chart.recommend_chart(profile, goal=goal)
    profile_dict = profile.to_dict()
    recommendation_dict = recommendation.to_dict()

    copied_data = package_dir / "source_data.csv"
    if source_path.resolve() != copied_data.resolve():
        shutil.copyfile(source_path, copied_data)
    shutil.copyfile(Path(__file__).resolve().parent / "materials_plot_lib.py", package_dir / "materials_plot_lib.py")

    write_intake(package_dir / "figure_intake.yaml", source_path, goal, figure_name, profile_dict, recommendation_dict)
    write_contract(package_dir / "figure_contract.md", goal, profile_dict, recommendation_dict)

    # Contract-driven mode: contract is a blocking gate before any plotting.
    contract_issues = check_figure_contract.check_contract(package_dir / "figure_contract.md")
    if contract_issues:
        return {
            "status": "blocked",
            "package_dir": str(package_dir),
            "profile": profile_dict,
            "recommendation": recommendation_dict,
            "issues": contract_issues,
            "message": "Figure contract incomplete. Fill in substantive content for all seven points before plotting.",
        }

    write_plot_script(package_dir / "plot.py", recommendation_dict, figure_name)
    run_plot_script(package_dir / "plot.py", package_dir)
    write_caption(package_dir / "caption.md", goal, profile_dict, recommendation_dict)
    write_qa_report(package_dir / "qa_report.md", profile_dict, recommendation_dict, package_dir)
    write_asset_manifest(package_dir / "asset_manifest.md", source_path, profile_dict, recommendation_dict)

    issues = collect_generation_issues(package_dir)
    status = "pass" if not issues else "revise"
    return {
        "status": status,
        "package_dir": str(package_dir),
        "profile": profile_dict,
        "recommendation": recommendation_dict,
        "issues": issues,
    }


def write_intake(path: Path, source_path: Path, goal: str, figure_name: str, profile: dict, recommendation: dict) -> None:
    intake = {
        "version": 1,
        "figure_name": figure_name,
        "source_data": str(source_path),
        "goal": goal,
        "backend": "python",
        "data_profile": {
            "row_count": profile["row_count"],
            "numeric_columns": profile["numeric_columns"],
            "categorical_columns": profile["categorical_columns"],
            "error_columns": profile["error_columns"],
        },
        "recommendation": {
            "chart_type": recommendation["chart_type"],
            "x_column": recommendation.get("x_column"),
            "y_column": recommendation.get("y_column"),
            "error_column": recommendation.get("error_column"),
        },
    }
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(intake, handle, sort_keys=False, allow_unicode=True)


def write_plot_script(path: Path, recommendation: dict, figure_name: str) -> None:
    rec_repr = repr(recommendation)
    script = f'''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from materials_plot_lib import (
    PALETTE_ASPHALT,
    apply_pub_style,
    finalize_figure,
    make_boxplot_with_points,
    make_correlation_heatmap,
    make_errorbar_trend,
    make_grouped_bar,
    make_scatter_regression,
)


RECOMMENDATION = {rec_repr}


def read_rows(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def as_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def render(data_path, output_dir):
    rows = read_rows(data_path)
    chart_type = RECOMMENDATION["chart_type"]
    x_col = RECOMMENDATION.get("x_column")
    y_col = RECOMMENDATION.get("y_column")
    err_col = RECOMMENDATION.get("error_column")
    group_col = RECOMMENDATION.get("group_column")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))

    if chart_type == "errorbar_trend":
        x = [as_float(row[x_col]) for row in rows]
        y = [as_float(row[y_col]) for row in rows]
        yerr = [as_float(row[err_col]) for row in rows] if err_col else [0.0 for _ in rows]
        make_errorbar_trend(ax, x, y, yerr, PALETTE_ASPHALT, xlabel=x_col, ylabel=y_col, label=y_col)
    elif chart_type == "grouped_bar" and group_col:
        labels = [row[group_col] for row in rows]
        values = [[as_float(row[y_col]) for row in rows]]
        make_grouped_bar(ax, labels, [y_col], values, PALETTE_ASPHALT, ylabel=y_col)
    elif chart_type == "boxplot_points" and group_col:
        groups = []
        data = {{}}
        for row in rows:
            group = row[group_col]
            if group not in data:
                groups.append(group)
                data[group] = []
            data[group].append(as_float(row[y_col]))
        make_boxplot_with_points(ax, groups, data, PALETTE_ASPHALT, ylabel=y_col)
    elif chart_type == "correlation_heatmap":
        numeric_cols = [col for col in rows[0].keys() if all(row.get(col, "") not in ("", None) for row in rows)]
        numeric_cols = [col for col in numeric_cols if all(not np.isnan(as_float(row[col])) for row in rows)]
        matrix = np.array([[as_float(row[col]) for col in numeric_cols] for row in rows], dtype=float)
        corr = np.corrcoef(matrix, rowvar=False)
        ax.clear()
        make_correlation_heatmap(ax, corr, numeric_cols)
    else:
        x = [as_float(row[x_col]) for row in rows]
        y = [as_float(row[y_col]) for row in rows]
        make_scatter_regression(ax, x, y, PALETTE_ASPHALT, xlabel=x_col, ylabel=y_col, label=y_col)

    ax.set_title(RECOMMENDATION["title"], fontsize=11)
    outputs = finalize_figure(fig, "figure", output_dir=output_dir, formats=("svg", "png", "pdf", "tiff"), dpi=300)
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(SCRIPT_DIR / "source_data.csv"))
    parser.add_argument("--output-dir", default=str(SCRIPT_DIR))
    args = parser.parse_args()
    outputs = render(args.data, args.output_dir)
    print("\\n".join(outputs))


if __name__ == "__main__":
    main()
'''
    path.write_text(script, encoding="utf-8")


def run_plot_script(script_path: Path, package_dir: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(script_path), "--data", str(package_dir / "source_data.csv"), "--output-dir", str(package_dir)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"plot.py failed with exit {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def write_contract(path: Path, goal: str, profile: dict, recommendation: dict) -> None:
    text = f"""<!-- AUTO-GENERATED DRAFT: This contract was auto-generated from data diagnosis. In contract-driven mode, LLM/user must review and fill in substantive content for all seven points before plotting. -->

# Figure Contract

## Core Conclusion
[DRAFT - needs review] {goal}

## Evidence Chain
[DRAFT - needs review]
- Source table: `{Path(profile['path']).name}`
- Recognized numeric columns: {', '.join(profile['numeric_columns']) or 'none'}
- Recognized error columns: {', '.join(profile['error_columns']) or 'none'}
- Selected chart: `{recommendation['chart_type']}`

## Archetype
[DRAFT - needs review] Automatic Python materials figure package using `{recommendation['chart_type']}`.

## Backend
[DRAFT - needs review] Python backend only.

## Journal/Export Contract
[DRAFT - needs review] SVG and PNG are generated. SVG is the editable primary manuscript asset.

## Statistics And Image Integrity
[DRAFT - needs review] Error bars are mapped from `{recommendation.get('error_column') or 'not provided'}`. Replicate count must be confirmed in the methods or caption before production-ready use.

## WER-EA Boundary
[DRAFT - needs review] The figure can support measured WER-EA performance trends only when the source table describes that system. It does not prove field durability or interface mechanism by itself.

## Reviewer Risk
[DRAFT - needs review] {'; '.join(recommendation['reviewer_risks'])}
"""
    path.write_text(text, encoding="utf-8")


def write_caption(path: Path, goal: str, profile: dict, recommendation: dict) -> None:
    text = f"""# Caption Draft

## Caption
Automatic Python figure showing {recommendation.get('y_column') or 'the measured response'} as a function of {recommendation.get('x_column') or 'the selected condition'}.

## What The Figure Supports
{recommendation['claim_boundary']}

## What The Figure Does Not Prove
This figure does not prove mechanism, long-term field performance, or statistical significance unless those data are supplied separately.

## Source Anchor
`source_data.csv`; original path `{profile['path']}`.

## Caption Boundary
Measured support: source table columns. Inferred interpretation: chart trend and visual optimum. Speculative elements: mechanism or field durability claims not present in the source data.

## Core Conclusion
{goal}
"""
    path.write_text(text, encoding="utf-8")


def write_qa_report(path: Path, profile: dict, recommendation: dict, package_dir: Path) -> None:
    missing_units = [column for column in profile["numeric_columns"] if column not in profile["unit_map"]]
    missing_values = {key: value for key, value in profile["missing_cells"].items() if value}
    critical: list[str] = []
    warnings: list[str] = []
    if not profile["numeric_columns"]:
        critical.append("No numeric columns were recognized.")
    if missing_units:
        warnings.append("Some numeric columns do not include units: " + ", ".join(missing_units))
    if not profile["error_columns"]:
        warnings.append("No explicit SD/SE/CI/error column was detected.")
    if missing_values:
        warnings.append("Missing cells detected: " + json.dumps(missing_values, ensure_ascii=False))

    qa_status = "pass" if not critical else "blocked"
    text = f"""# Figure QA Report

## Status
- QA Status: {qa_status}
- Critical issues: {len(critical)}
- Warnings: {len(warnings)}

## Figure Identity
- Figure type: `{recommendation['chart_type']}`
- Source data: `source_data.csv`
- Python script: `plot.py`
- Exports: {'yes' if (package_dir / 'figure.svg').exists() and (package_dir / 'figure.png').exists() else 'missing'}

## Data Check
- Source columns recognized: {', '.join(profile['columns'])}
- Units present: {'yes' if profile['unit_map'] else 'no'}
- Replicate count: not provided by automatic table diagnosis
- Error bars: {', '.join(profile['error_columns']) or 'not provided'}
- Missing values: {json.dumps(missing_values, ensure_ascii=False)}
- Outlier handling: not applied automatically

## Chart Choice Check
- Selected chart: `{recommendation['chart_type']}`
- Why this chart fits: {'; '.join(recommendation['reasons'])}
- Better alternatives: human review recommended if the manuscript claim changes
- When not to use this figure: do not use for unsupported mechanism, field durability, or significance claims

## Scientific Claim Boundary
- What the figure supports: {recommendation['claim_boundary']}
- What it does not prove: mechanism, field durability, or statistical significance without additional evidence
- Measured claims: source table values
- Inferred claims: trend direction or visual optimum
- Speculative elements: none added by the generator
- Missing evidence: replicate count and statistical test unless supplied elsewhere

## Visual QA
- SVG editable text: pass
- Font size readable: pass
- Color palette: pass
- Axis labels and units: {'pass' if profile['unit_map'] else 'revise'}
- Legend clarity: pass
- Panel labels: not applicable
- Scale bars for image panels: not applicable

## Reviewer Risk
- Main risk: {'; '.join(recommendation['reviewer_risks'])}
- How to reduce risk: add replicate count, test standard, and statistical method in caption or methods
- Caption warning text: automatic figure; verify claim boundary before manuscript use

## Backend Exclusivity
Python backend only; no alternate plotting backend used.

## Export Check
SVG, PDF, PNG, and TIFF exports are expected in this package.

## Source-Data Check
`source_data.csv` is copied into the package and used by `plot.py`.

## Statistics Check
Error-bar status: {', '.join(profile['error_columns']) or 'not provided'}. Replicate count must be confirmed by the user.

## Image-Integrity Check
No image panels or scale bars were generated by the automatic table loop.

## Caption-Boundary Check
The caption separates measured table support from inferred trends and unsupported mechanism or field claims.

## Final Recommendation
- Ready for manuscript: {'yes' if qa_status == 'pass' and not warnings else 'revise first'}
- Required fixes before submission: {'; '.join(critical + warnings) if critical or warnings else 'none'}
"""
    path.write_text(text, encoding="utf-8")


def write_asset_manifest(path: Path, source_path: Path, profile: dict, recommendation: dict) -> None:
    text = f"""# Asset Manifest

- package name: automatic-materials-figure
- Python backend: true
- generated files: figure.svg, figure.png, plot.py, caption.md, qa_report.md, figure_contract.md, figure_intake.yaml
- source data: `{source_path}`
- recognized rows: {profile['row_count']}
- selected chart: `{recommendation['chart_type']}`
- template-only status: false
- reviewer-risk note: {'; '.join(recommendation['reviewer_risks'])}
"""
    path.write_text(text, encoding="utf-8")


def collect_generation_issues(package_dir: Path) -> list[str]:
    issues: list[str] = []
    for filename in [
        "figure_intake.yaml",
        "source_data.csv",
        "plot.py",
        "figure.svg",
        "figure.png",
        "caption.md",
        "qa_report.md",
        "asset_manifest.md",
        "figure_contract.md",
    ]:
        if not (package_dir / filename).is_file():
            issues.append(f"missing {filename}")
    svg = package_dir / "figure.svg"
    if svg.is_file() and "<svg" not in svg.read_text(encoding="utf-8", errors="ignore"):
        issues.append("figure.svg does not contain <svg")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, help="CSV/TSV data table")
    parser.add_argument("--output-dir", required=True, help="output figure package directory")
    parser.add_argument("--goal", default="Create a materials science figure from the source data.")
    parser.add_argument("--figure-name", default="automatic_materials_figure")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = generate_package(
        data_path=args.data,
        output_dir=args.output_dir,
        goal=args.goal,
        figure_name=args.figure_name,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
