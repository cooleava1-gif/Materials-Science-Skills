#!/usr/bin/env python3
"""Water absorption curves for durability assessment."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
    add_panel_label,
    apply_pub_style,
    finalize_figure,
    make_absorption_curve,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("water_absorption.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    time_days = column(rows, "time_days", as_float=True)
    mass_gain = [
        column(rows, "mass_gain_pct_control", as_float=True),
        column(rows, "mass_gain_pct_modified", as_float=True),
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    make_absorption_curve(ax, time_days, mass_gain, ["Control", "Modified"], PALETTE_CBM)
    add_panel_label(ax, "(j)")
    fig.tight_layout()
    finalize_figure(fig, "water_absorption", args.output_dir)
    print_caption(
        "Water absorption mass gain vs square root of time. "
        "Absorption kinetics follow Fickian diffusion only within this measurement window; long-term saturation requires extended immersion."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
