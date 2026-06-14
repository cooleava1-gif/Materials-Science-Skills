#!/usr/bin/env python3
"""Dual-axis trend for paired strength and workability metrics."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_dual_axis_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("dual_axis_trend.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    wer = column(rows, "wer_pct", as_float=True)
    strength = column(rows, "bond_strength_mpa", as_float=True)
    viscosity = column(rows, "viscosity_mpas", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.7, 3.7))
    make_dual_axis_trend(
        ax,
        wer,
        strength,
        viscosity,
        PALETTE_ASPHALT,
        left_label="Bond strength (MPa)",
        right_label="Viscosity (mPa s)",
    )
    ax.set_xlabel("Waterborne epoxy content (%)")
    ax.axvspan(10, 15, color=PALETTE_ASPHALT.get("mechanism", "#8B6F47"), alpha=0.12)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "dual_axis_trend", args.output_dir)
    print_caption(
        "Dual-axis trend comparing bond strength and viscosity across epoxy content. The shaded region marks a candidate balance, not a confirmed optimum."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
