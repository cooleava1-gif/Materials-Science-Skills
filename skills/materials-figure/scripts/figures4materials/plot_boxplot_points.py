#!/usr/bin/env python3
"""Boxplot with raw replicate points for group comparison."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_boxplot_with_points


def grouped_values(rows: list[dict[str, str]], group_col: str, value_col: str) -> tuple[list[str], dict[str, list[float]]]:
    groups: list[str] = []
    data: dict[str, list[float]] = {}
    for row in rows:
        group = row[group_col]
        if group not in data:
            groups.append(group)
            data[group] = []
        data[group].append(float(row[value_col]))
    return groups, data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("boxplot_points.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    groups, data = grouped_values(read_csv(args.data), "condition", "bond_strength_mpa")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.6, 3.7))
    make_boxplot_with_points(ax, groups, data, PALETTE_ASPHALT, ylabel="Bond strength (MPa)")
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "boxplot_points", args.output_dir)
    print_caption(
        "Boxplot with raw replicate points for bond strength. Points show individual measurements; box summaries should be reported with n and error definitions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
