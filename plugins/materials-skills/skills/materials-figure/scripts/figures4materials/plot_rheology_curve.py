#!/usr/bin/env python3
"""Rheology curve: viscosity vs. shear rate for WER-EA emulsions."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("rheology_curve.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    shear_rate = column(rows, "shear_rate", as_float=True)
    viscosity_series = [
        column(rows, "viscosity_5%", as_float=True),
        column(rows, "viscosity_10%", as_float=True),
        column(rows, "viscosity_15%", as_float=True),
        column(rows, "viscosity_20%", as_float=True),
    ]
    labels = ["5% WER", "10% WER", "15% WER", "20% WER"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    make_line_trend(
        ax,
        shear_rate,
        viscosity_series,
        labels,
        PALETTE_CBM,
        xlabel="Shear rate (s$^{-1}$)",
        ylabel="Viscosity (mPa·s)",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.08, 60)
    ax.set_ylim(10, 3000)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "rheology_viscosity_shear_rate", args.output_dir)
    print_caption(
        "Viscosity versus shear rate for waterborne epoxy modified emulsified asphalt at different WER dosages. "
        "Shear-thinning behavior indicates pseudoplastic flow; mechanism claims require additional rheological evidence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())