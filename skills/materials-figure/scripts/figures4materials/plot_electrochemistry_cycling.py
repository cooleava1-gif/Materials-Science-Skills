#!/usr/bin/env python3
"""Cycling stability: capacity retention and coulombic efficiency vs cycle number."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CCC,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("electrochemistry_cycling.csv"))
    apply_pub_style()

    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax2 = ax1.twinx()

    cycles = column(rows, "cycle_number", as_float=True)
    capacity = column(rows, "capacity_mah_g", as_float=True)
    efficiency = column(rows, "coulombic_efficiency", as_float=True)

    ax1.plot(cycles, capacity, color=PALETTE_CCC["modified"], linewidth=2.2, marker="o", markersize=4, label="Specific capacity")
    ax2.plot(cycles, efficiency, color=PALETTE_CCC["optimal"], linewidth=2.2, marker="s", markersize=3, linestyle="--", label="Coulombic efficiency")

    ax1.set_xlabel("Cycle number")
    ax1.set_ylabel("Specific capacity (mAh/g)")
    ax2.set_ylabel("Coulombic efficiency (%)")
    ax1.set_ylim(0, max(capacity) * 1.15)
    ax2.set_ylim(80, 102)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="center right")

    saved = finalize_figure(fig, "electrochemistry_cycling", args.output_dir)
    print_caption("Long-term cycling stability with capacity retention and coulombic efficiency.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
