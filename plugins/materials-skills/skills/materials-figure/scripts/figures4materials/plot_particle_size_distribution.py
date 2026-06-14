#!/usr/bin/env python3
"""Particle size distribution: frequency and cumulative curves."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("particle_size_distribution.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    particle_size = column(rows, "particle_size", as_float=True)
    frequency_series = [
        column(rows, "frequency_5%_wer", as_float=True),
        column(rows, "frequency_10%_wer", as_float=True),
        column(rows, "frequency_15%_wer", as_float=True),
    ]
    cumulative_series = [
        column(rows, "cumulative_5%_wer", as_float=True),
        column(rows, "cumulative_10%_wer", as_float=True),
        column(rows, "cumulative_15%_wer", as_float=True),
    ]
    labels = ["5% WER", "10% WER", "15% WER"]

    apply_pub_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    # Frequency distribution
    make_line_trend(
        ax1,
        particle_size,
        frequency_series,
        labels,
        PALETTE_CBM,
        xlabel="Particle size (μm)",
        ylabel="Frequency (%)",
    )
    ax1.set_xscale("log")
    ax1.set_xlim(0.08, 600)
    ax1.set_ylim(0, 25)
    ax1.set_title("Frequency distribution", fontsize=10)
    add_panel_label(ax1, "(a)")

    # Cumulative distribution
    make_line_trend(
        ax2,
        particle_size,
        cumulative_series,
        labels,
        PALETTE_CBM,
        xlabel="Particle size (μm)",
        ylabel="Cumulative percentage (%)",
    )
    ax2.set_xscale("log")
    ax2.set_xlim(0.08, 600)
    ax2.set_ylim(0, 105)
    ax2.set_title("Cumulative distribution", fontsize=10)
    add_panel_label(ax2, "(b)")

    fig.tight_layout()
    finalize_figure(fig, "particle_size_distribution", args.output_dir)
    print_caption(
        "Particle size distribution for WER-EA emulsions at different WER dosages. "
        "Smaller particle size at 15% WER indicates better emulsification; "
        "stability claims require matching sedimentation or centrifugation tests."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())