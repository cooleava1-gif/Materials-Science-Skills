#!/usr/bin/env python3
"""Polar performance profile for normalized multi-index data."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_polar_plot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("polar_performance.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    metrics = column(rows, "metric")
    theta = column(rows, "angle_rad", as_float=True)
    score = column(rows, "normalized_score", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(4.8, 4.8), subplot_kw={"projection": "polar"})
    make_polar_plot(ax, theta, score, "15% WER", PALETTE_ASPHALT)
    ax.set_xticks(theta)
    ax.set_xticklabels(metrics, fontsize=8)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "polar_performance", args.output_dir)
    print_caption(
        "Polar performance profile for normalized WER-EA indices. Scores are screening indicators; raw values and normalization method must be reported."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
