#!/usr/bin/env python3
"""Durability retention grouped bar chart for civil materials."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, annotate_bars, apply_pub_style, finalize_figure, make_grouped_bar, tighten_ylimits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("civil_durability_retention.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    conditions = column(rows, "condition")
    values = [
        column(rows, "control_retention_pct", as_float=True),
        column(rows, "modified_retention_pct", as_float=True),
    ]
    errors = [
        column(rows, "control_sd", as_float=True),
        column(rows, "modified_sd", as_float=True),
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    make_grouped_bar(
        ax,
        conditions,
        ["Control", "Modified"],
        values,
        PALETTE_CBM,
        error_bars=errors,
        ylabel="Retention ratio (%)",
    )
    all_vals = [v for group in values for v in group]
    tighten_ylimits(ax, all_vals, margin=0.12, ymin=40)
    ax.set_ylim(40, 105)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "civil_durability_retention", args.output_dir)
    print_caption(
        "Property retention of control and modified civil materials after conditioning. "
        "Laboratory durability screening is valid only within the reported exposure conditions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
