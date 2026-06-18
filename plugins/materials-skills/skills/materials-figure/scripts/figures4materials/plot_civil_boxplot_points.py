#!/usr/bin/env python3
"""Box-and-whisker plot with individual data points for civil material properties."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_boxplot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("civil_boxplot_points.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    groups = column(rows, "group")
    values = [column(rows, "value", as_float=True)]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    make_boxplot(
        ax,
        groups,
        values,
        PALETTE_CBM,
        ylabel="Property value",
        show_points=True,
    )
    add_panel_label(ax, "(b)")
    fig.tight_layout()
    finalize_figure(fig, "civil_boxplot_points", args.output_dir)
    print_caption(
        "Distribution of measured property values across material groups. "
        "Boxplots summarize central tendency and spread; overlap between groups requires statistical testing."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
