#!/usr/bin/env python3
"""Cyclic Voltammetry (CV) curves at multiple scan rates for electrochemical characterization."""

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

    rows = read_csv(data_path("electrochemistry_cv.csv"))
    apply_pub_style()

    fig, ax = plt.subplots(figsize=(7, 4.5))

    scan_rates = sorted(set(column(rows, "scan_rate_mV_s", as_float=True)))
    colors = [PALETTE_CCC["control"], PALETTE_CCC["modified"], PALETTE_CCC["optimal"], PALETTE_CCC["mechanism"]]

    for i, rate in enumerate(scan_rates):
        subset = [r for r in rows if float(r["scan_rate_mV_s"]) == rate]
        v = column(subset, "voltage_v", as_float=True)
        c = column(subset, "current_mA_cm2", as_float=True)
        ax.plot(v, c, color=colors[i % len(colors)], linewidth=2.0, label=f"{int(rate)} mV/s")

    ax.set_xlabel("Potential (V vs. Ag/AgCl)")
    ax.set_ylabel("Current density (mA/cm²)")
    ax.legend(fontsize=9)

    saved = finalize_figure(fig, "electrochemistry_cv", args.output_dir)
    print_caption("Cyclic voltammetry curves at multiple scan rates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
