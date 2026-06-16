#!/usr/bin/env python3
"""Particle size distribution (PSD) gradation curves."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_psd_curve


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("psd_gradation.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    sieve_size = column(rows, "sieve_size_mm", as_float=True)
    cumulative = [
        column(rows, "cumulative_passing_pct_gradation_a", as_float=True),
        column(rows, "cumulative_passing_pct_gradation_b", as_float=True),
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    make_psd_curve(ax, sieve_size, cumulative, ["Gradation A", "Gradation B"], PALETTE_CBM)
    add_panel_label(ax, "(b)")
    fig.tight_layout()
    finalize_figure(fig, "psd_gradation", args.output_dir)
    print_caption(
        "Particle size distribution of two gradations. "
        "PSD curves shape workability and packing density hypotheses; combined grading optimization requires additional tests."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
