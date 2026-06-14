#!/usr/bin/env python3
"""Stacked composition bar chart for material formulation fractions."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_stacked_composition_bar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("stacked_composition.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    mixes = column(rows, "mix")
    series = {
        "Asphalt": column(rows, "Asphalt", as_float=True),
        "Water": column(rows, "Water", as_float=True),
        "Emulsifier": column(rows, "Emulsifier", as_float=True),
        "WER": column(rows, "WER", as_float=True),
    }

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.6, 3.7))
    make_stacked_composition_bar(ax, mixes, series, PALETTE_ASPHALT, ylabel="Mass fraction (%)")
    ax.set_ylim(0, 100)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "stacked_composition", args.output_dir)
    print_caption(
        "Stacked composition chart for emulsified asphalt formulations. Fractions are formulation inputs and should be checked against mass-balance records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
