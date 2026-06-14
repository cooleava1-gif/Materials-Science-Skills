#!/usr/bin/env python3
"""SEM analysis: particle size distribution histogram."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_grouped_bar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("sem_analysis.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    size_bins = column(rows, "particle_size_bin")
    frequency_series = [
        column(rows, "frequency_pure_asphalt", as_float=True),
        column(rows, "frequency_5%_wer", as_float=True),
        column(rows, "frequency_10%_wer", as_float=True),
        column(rows, "frequency_15%_wer", as_float=True),
    ]
    labels = ["Pure asphalt", "5% WER", "10% WER", "15% WER"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    make_grouped_bar(
        ax,
        size_bins,
        labels,
        frequency_series,
        PALETTE_CBM,
        bar_width=0.2,
        ylabel="Frequency (%)",
    )
    ax.set_xlabel("Particle size range (μm)")
    ax.set_ylim(0, 30)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "sem_particle_size_histogram", args.output_dir)
    print_caption(
        "SEM-based particle size distribution for pure asphalt and WER-EA emulsions. "
        "Smaller particle size at higher WER dosage indicates improved emulsification; "
        "morphology claims require representative SEM images with scale bars."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())