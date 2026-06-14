#!/usr/bin/env python3
"""MIP pore size distribution: cumulative intrusion curves."""

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

    rows = read_csv(data_path("cement_pore_distribution.csv"))
    apply_pub_style()

    fig, ax = plt.subplots(figsize=(7, 4.5))

    diameter = column(rows, "pore_diameter_nm", as_float=True)
    modified = column(rows, "cumulative_intrusion_mL_per_g", as_float=True)
    control = column(rows, "control_intrusion", as_float=True)

    ax.semilogx(diameter, modified, color=PALETTE_CEMENT["modified"], linewidth=2.2, marker="o", markersize=4, label="Modified mix")
    ax.semilogx(diameter, control, color=PALETTE_CEMENT["control"], linewidth=2.2, marker="s", markersize=4, linestyle="--", label="Control mix")

    ax.axvspan(0, 10, alpha=0.06, color="#B85450", label="Gel pores (<10 nm)")
    ax.axvspan(10, 50, alpha=0.06, color="#C47B45", label="Mesopores (10–50 nm)")
    ax.axvspan(50, 10000, alpha=0.06, color="#5B8FA8", label="Capillary pores (>50 nm)")

    ax.set_xlabel("Pore diameter (nm)")
    ax.set_ylabel("Cumulative intrusion (mL/g)")
    ax.set_xlim(1, 200000)
    ax.legend(fontsize=7.5, loc="upper left")

    saved = finalize_figure(fig, "cement_pore_distribution", args.output_dir)
    print_caption("MIP pore size distribution comparing modified and control cementitious mixes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
