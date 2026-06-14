#!/usr/bin/env python3
"""Traffic loading spectrum: axle load distribution and axle type breakdown."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_ASPHALT,
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

    rows = read_csv(data_path("highway_traffic_spectrum.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    loads = column(rows, "axle_load_kn", as_float=True)
    freq = column(rows, "frequency_pct", as_float=True)
    single = column(rows, "single_axle_pct", as_float=True)
    tandem = column(rows, "tandem_axle_pct", as_float=True)
    tridem = column(rows, "tridem_axle_pct", as_float=True)

    x = np.arange(len(loads))

    # Panel (a): Load frequency distribution
    bars = ax1.bar(x, freq, 0.55, color=PALETTE_ASPHALT["modified"], edgecolor="white", linewidth=0.7)
    annotate_bars(ax1, bars, freq, fmt="{:.1f}", fontsize=6.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{int(l)}" for l in loads], fontsize=8)
    ax1.set_xlabel("Axle load (kN)")
    ax1.set_ylabel("Frequency (%)")
    tighten_ylimits(ax1, list(freq), margin=0.15, ymin=0)
    add_panel_label(ax1, "a")

    # Panel (b): Axle type breakdown (stacked bar)
    ax2.bar(x, single, 0.55, color=PALETTE_ASPHALT["optimal"], edgecolor="white", linewidth=0.7, label="Single axle")
    ax2.bar(x, tandem, 0.55, bottom=single, color=PALETTE_ASPHALT["modified"], edgecolor="white", linewidth=0.7, label="Tandem axle")
    ax2.bar(x, tridem, 0.55, bottom=np.array(single) + np.array(tandem), color=PALETTE_ASPHALT["mechanism"], edgecolor="white", linewidth=0.7, label="Tridem axle")
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{int(l)}" for l in loads], fontsize=8)
    ax2.set_xlabel("Axle load (kN)")
    ax2.set_ylabel("Percentage (%)")
    ax2.legend(fontsize=7.5, loc="upper right")
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "highway_traffic_spectrum", args.output_dir)
    print_caption("Traffic loading spectrum: axle load distribution and axle type breakdown from weigh-in-motion data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
