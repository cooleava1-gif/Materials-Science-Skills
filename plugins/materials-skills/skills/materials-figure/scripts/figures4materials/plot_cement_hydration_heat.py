#!/usr/bin/env python3
"""Isothermal calorimetry: heat evolution rate and cumulative heat of hydration."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CEMENT,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("cement_hydration_heat.csv"))
    apply_pub_style()

    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax2 = ax1.twinx()

    time = column(rows, "time_hours", as_float=True)
    rate = column(rows, "heat_rate_w_per_kg", as_float=True)
    cumul = column(rows, "cumulative_heat_j_per_g", as_float=True)
    ctrl_rate = column(rows, "control_rate", as_float=True)
    ctrl_cumul = column(rows, "control_cumulative", as_float=True)

    ax1.plot(time, rate, color=PALETTE_CEMENT["modified"], linewidth=2.2, label="Modified — rate")
    ax1.plot(time, ctrl_rate, color=PALETTE_CEMENT["control"], linewidth=2.2, linestyle="--", label="Control — rate")
    ax1.fill_between(time, 0, rate, color=PALETTE_CEMENT["modified"], alpha=0.10)

    ax2.plot(time, cumul, color=PALETTE_CEMENT["durability"], linewidth=2.2, label="Modified — cumulative")
    ax2.plot(time, ctrl_cumul, color=PALETTE_CEMENT["neutral"], linewidth=2.2, linestyle="--", label="Control — cumulative")

    ax1.set_xlabel("Time (hours)")
    ax1.set_ylabel("Heat evolution rate (W/kg)")
    ax2.set_ylabel("Cumulative heat (J/g)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="center right")

    saved = finalize_figure(fig, "cement_hydration_heat", args.output_dir)
    print_caption("Isothermal calorimetry curves comparing modified and control cementitious systems.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
