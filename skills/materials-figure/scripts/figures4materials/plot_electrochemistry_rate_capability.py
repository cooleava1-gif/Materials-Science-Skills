#!/usr/bin/env python3
"""Rate capability: capacity at varying C-rates with recovery test."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CCC,
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

    rows = read_csv(data_path("electrochemistry_rate_capability.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    c_rates = column(rows, "c_rate", as_float=True)
    capacity = column(rows, "capacity_mah_g", as_float=True)
    retention = column(rows, "capacity_retention_pct", as_float=True)

    x = np.arange(len(c_rates))
    bars = ax1.bar(x, capacity, 0.55, color=PALETTE_CCC["modified"], edgecolor="white", linewidth=0.7)
    annotate_bars(ax1, bars, capacity, fmt="{:.0f}", fontsize=7)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{r}C" for r in c_rates], fontsize=8)
    ax1.set_ylabel("Specific capacity (mAh/g)")
    tighten_ylimits(ax1, list(capacity), margin=0.15, ymin=0)
    add_panel_label(ax1, "a")

    ax2.plot(x, retention, color=PALETTE_CCC["modified"], linewidth=2.2, marker="o", markersize=6)
    for i, (rate, ret) in enumerate(zip(c_rates, retention)):
        ax2.annotate(f"{ret:.1f}%", (i, ret), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=7)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{r}C" for r in c_rates], fontsize=8)
    ax2.set_ylabel("Capacity retention (%)")
    ax2.set_ylim(40, 105)
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "electrochemistry_rate_capability", args.output_dir)
    print_caption("Rate capability: specific capacity and retention at varying C-rates with recovery test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
