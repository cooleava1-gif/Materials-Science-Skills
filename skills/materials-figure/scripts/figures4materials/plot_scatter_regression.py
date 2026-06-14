#!/usr/bin/env python3
"""Scatter regression for dosage-property relationships."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_scatter_regression


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("scatter_regression.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    wer = column(rows, "wer_pct", as_float=True)
    strength = column(rows, "bond_strength_mpa", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    make_scatter_regression(
        ax,
        wer,
        strength,
        PALETTE_ASPHALT,
        xlabel="Waterborne epoxy content (%)",
        ylabel="Bond strength (MPa)",
        label="Measured mean",
    )
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "scatter_regression", args.output_dir)
    print_caption(
        "Scatter regression of waterborne epoxy content versus bond strength. The fitted line summarizes association only; "
        "dosage optimization requires durability and workability checks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
