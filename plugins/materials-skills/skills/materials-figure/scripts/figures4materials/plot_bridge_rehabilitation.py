#!/usr/bin/env python3
"""Rehabilitation effectiveness: stiffness increase vs load rating, deflection, and cost."""

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

    rows = read_csv(data_path("bridge_rehabilitation.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    stiff = column(rows, "stiffness_increase_pct", as_float=True)
    rf = column(rows, "load_rating_factor", as_float=True)
    defl_red = column(rows, "deflection_reduction_pct", as_float=True)
    freq_inc = column(rows, "frequency_increase_pct", as_float=True)
    cost = column(rows, "cost_ratio", as_float=True)

    # Panel (a): Rating and deflection vs stiffness
    ax1.plot(stiff, rf, color=PALETTE_CEMENT["modified"], linewidth=2.2, marker="o", markersize=5, label="Load rating factor")
    ax1.axhline(1.0, color="#B85450", linewidth=1.2, linestyle="--", alpha=0.7)
    ax1.set_xlabel("Stiffness increase (%)")
    ax1.set_ylabel("Load rating factor", color=PALETTE_CEMENT["modified"])
    ax1.set_ylim(0.5, 2.2)

    ax1b = ax1.twinx()
    ax1b.plot(stiff, defl_red, color=PALETTE_CEMENT["durability"], linewidth=2.2, marker="s", markersize=5, label="Deflection reduction")
    ax1b.set_ylabel("Deflection reduction (%)", color=PALETTE_CEMENT["durability"])

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=7.5, loc="upper left")

    # Panel (b): Cost-effectiveness
    ax2.plot(stiff, cost, color=PALETTE_CEMENT["modified"], linewidth=2.2, marker="^", markersize=6)
    ax2.fill_between(stiff, 1.0, cost, color=PALETTE_CEMENT["modified"], alpha=0.10)
    ax2.set_xlabel("Stiffness increase (%)")
    ax2.set_ylabel("Cost ratio (relative to baseline)")

    ax2b = ax2.twinx()
    ax2b.plot(stiff, freq_inc, color=PALETTE_CEMENT["durability"], linewidth=2.2, marker="D", markersize=5)
    ax2b.set_ylabel("Frequency increase (%)", color=PALETTE_CEMENT["durability"])

    ax2.legend(["Cost ratio"], fontsize=7.5, loc="upper left")
    ax2b.legend(["Frequency increase"], fontsize=7.5, loc="center right")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "bridge_rehabilitation", args.output_dir)
    print_caption("Rehabilitation effectiveness: load rating improvement, deflection reduction, and cost-effectiveness analysis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
