#!/usr/bin/env python3
"""Compressive and tensile strength development with curing age for cementitious systems."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CEMENT,
    add_panel_label,
    annotate_bars,
    apply_pub_style,
    finalize_figure,
    tighten_ylimits,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("cement_strength_age.csv"))
    apply_pub_style()

    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax2 = ax1.twinx()

    ages = column(rows, "age_days", as_float=True)
    comp = column(rows, "compressive_strength_mpa", as_float=True)
    comp_sd = column(rows, "compressive_sd", as_float=True)
    tens = column(rows, "splitting_tensile_mpa", as_float=True)
    tens_sd = column(rows, "tensile_sd", as_float=True)

    x = np.arange(len(ages))
    w = 0.35

    bars = ax1.bar(
        x - w / 2, comp, w,
        color=PALETTE_CEMENT["modified"],
        label="Compressive strength",
        edgecolor="white", linewidth=0.7,
        yerr=comp_sd, error_kw={"color": "#333333", "linewidth": 1, "capsize": 3},
    )
    annotate_bars(ax1, bars, comp, fmt="{:.1f}", fontsize=6.5)

    ax2.plot(
        x, tens,
        marker="o", markersize=6, linewidth=2.2,
        color=PALETTE_CEMENT["durability"],
        label="Splitting tensile strength",
    )
    ax2.fill_between(x, np.array(tens) - np.array(tens_sd), np.array(tens) + np.array(tens_sd),
                      color=PALETTE_CEMENT["durability"], alpha=0.15)

    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{int(d)}d" for d in ages], fontsize=9)
    ax1.set_xlabel("Curing age")
    ax1.set_ylabel("Compressive strength (MPa)")
    ax2.set_ylabel("Splitting tensile strength (MPa)")

    tighten_ylimits(ax1, list(comp), margin=0.15, ymin=0)
    tighten_ylimits(ax2, list(tens), margin=0.15, ymin=0)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="upper left")

    add_panel_label(ax1, "a")

    saved = finalize_figure(fig, "cement_strength_age", args.output_dir)
    print_caption("Compressive and tensile strength development with curing age (28-day reference mix).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
