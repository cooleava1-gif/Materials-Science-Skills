#!/usr/bin/env python3
"""Freeze-thaw durability: relative dynamic modulus and penetration depth."""

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

    rows = read_csv(data_path("cement_freeze_thaw.csv"))
    apply_pub_style()

    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax2 = ax1.twinx()

    cycles = column(rows, "cycle_count", as_float=True)
    modulus = column(rows, "relative_dynamic_modulus_pct", as_float=True)
    ctrl_mod = column(rows, "control_modulus", as_float=True)
    depth = column(rows, "depth_of_penetration_mm", as_float=True)
    ctrl_depth = column(rows, "control_penetration", as_float=True)

    ax1.plot(cycles, modulus, color=PALETTE_CEMENT["modified"], linewidth=2.2, marker="o", markersize=5, label="Modified — RDM")
    ax1.plot(cycles, ctrl_mod, color=PALETTE_CEMENT["control"], linewidth=2.2, marker="s", markersize=5, linestyle="--", label="Control — RDM")

    ax2.plot(cycles, depth, color=PALETTE_CEMENT["durability"], linewidth=2.2, marker="^", markersize=5, label="Modified — penetration")
    ax2.plot(cycles, ctrl_depth, color=PALETTE_CEMENT["neutral"], linewidth=2.2, marker="v", markersize=5, linestyle="--", label="Control — penetration")

    ax1.axhline(60, color="#B85450", linewidth=1, linestyle=":", alpha=0.7, label="Failure threshold (60% RDM)")

    ax1.set_xlabel("Freeze-thaw cycles")
    ax1.set_ylabel("Relative dynamic modulus (%)")
    ax2.set_ylabel("Depth of penetration (mm)")
    ax1.set_ylim(50, 105)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=7.5, loc="lower left")

    saved = finalize_figure(fig, "cement_freeze_thaw", args.output_dir)
    print_caption("Freeze-thaw durability: relative dynamic modulus and chloride penetration depth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
