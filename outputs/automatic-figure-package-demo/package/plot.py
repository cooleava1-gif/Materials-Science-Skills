#!/usr/bin/env python3
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


RECOMMENDATION = {'chart_type': 'errorbar_trend', 'title': 'Bond strength (MPa) trend with uncertainty', 'x_column': 'WER content (%)', 'y_column': 'Bond strength (MPa)', 'error_column': 'SD', 'group_column': 'Condition', 'reasons': ['Numeric x column `WER content (%)`, numeric response `Bond strength (MPa)`, and error column `SD` support an errorbar trend.', 'Dosage/content wording suggests an optimization or dosage-performance claim.'], 'reviewer_risks': ['State replicate count (n) in caption or methods before using the figure as manuscript evidence.', 'Define error bars as SD, SE, CI, or range.', 'Do not call a dosage optimum unless the caption names the tested range and supporting durability evidence.'], 'export_formats': ['SVG', 'PNG'], 'claim_boundary': 'Supports a measured trend with uncertainty; optimum language needs statistics and durability context.'}


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
        data = {}
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
    print("\n".join(outputs))


if __name__ == "__main__":
    main()
