#!/usr/bin/env python3
"""Weibull probability plot for strength distribution analysis."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_weibull_plot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("weibull_strength.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    strength = column(rows, "strength_mpa", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    make_weibull_plot(ax, strength, labels=["Compressive strength"], palette=PALETTE_CBM)
    add_panel_label(ax, "(g)")
    fig.tight_layout()
    finalize_figure(fig, "weibull_strength", args.output_dir)
    print_caption(
        "Weibull probability plot of compressive strength. "
        "The Weibull modulus m quantifies strength reliability; a larger m indicates lower variability. "
        "Sample size and specimen preparation affect the estimated modulus."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
