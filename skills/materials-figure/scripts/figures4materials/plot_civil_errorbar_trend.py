#!/usr/bin/env python3
"""Trend plot with error bars for civil material performance metrics."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_errorbar_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("civil_errorbar_trend.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    x = column(rows, "x_value", as_float=True)
    y = column(rows, "y_value", as_float=True)
    yerr = column(rows, "y_error", as_float=True)
    groups = column(rows, "group")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    make_errorbar_trend(
        ax,
        x,
        y,
        yerr,
        groups,
        PALETTE_CBM,
        xlabel="Independent variable",
        ylabel="Measured response",
    )
    add_panel_label(ax, "(c)")
    fig.tight_layout()
    finalize_figure(fig, "civil_errorbar_trend", args.output_dir)
    print_caption(
        "Performance trend with error bars across experimental groups. "
        "Error bars represent experimental variability; trend interpretation requires sample-size context."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
