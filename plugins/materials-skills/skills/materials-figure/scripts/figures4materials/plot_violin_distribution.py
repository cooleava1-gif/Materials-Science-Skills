#!/usr/bin/env python3
"""Violin distribution plot for replicate-rich retention data."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_violin_plot


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
    parser.add_argument("--data", default=str(data_path("violin_distribution.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    groups, data = grouped_values(read_csv(args.data), "condition", "retention_pct")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    make_violin_plot(ax, groups, data, PALETTE_ASPHALT, ylabel="Retention (%)")
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "violin_distribution", args.output_dir)
    print_caption(
        "Violin distribution of retention under dry, wet, and aged states. Distribution shape is descriptive and should not replace statistical testing."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
