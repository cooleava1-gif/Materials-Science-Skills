#!/usr/bin/env python3
"""Modal analysis: measured vs analytical natural frequencies and damping ratios."""

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

    rows = read_csv(data_path("bridge_modal.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    modes = column(rows, "mode_number", as_float=True)
    measured_f = column(rows, "natural_frequency_hz", as_float=True)
    analytical_f = column(rows, "analytical", as_float=True)
    damping = column(rows, "damping_ratio_pct", as_float=True)

    x = np.arange(len(modes))
    w = 0.3

    # Panel (a): Frequency comparison
    bars_m = ax1.bar(x - w/2, measured_f, w, color=PALETTE_CEMENT["modified"], edgecolor="white", linewidth=0.7, label="Measured")
    bars_a = ax1.bar(x + w/2, analytical_f, w, color=PALETTE_CEMENT["control"], edgecolor="white", linewidth=0.7, label="Analytical")
    annotate_bars(ax1, bars_m, measured_f, fmt="{:.1f}", fontsize=6)
    annotate_bars(ax1, bars_a, analytical_f, fmt="{:.1f}", fontsize=6)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"Mode {int(m)}" for m in modes], fontsize=8)
    ax1.set_ylabel("Natural frequency (Hz)")
    ax1.legend(fontsize=8)
    add_panel_label(ax1, "a")

    # Panel (b): Damping ratio
    bars_d = ax2.bar(x, damping, 0.45, color=PALETTE_CEMENT["durability"], edgecolor="white", linewidth=0.7)
    annotate_bars(ax2, bars_d, damping, fmt="{:.1f}", fontsize=7)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"Mode {int(m)}" for m in modes], fontsize=8)
    ax2.set_ylabel("Damping ratio (%)")
    tighten_ylimits(ax2, list(damping), margin=0.2, ymin=0)
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "bridge_modal", args.output_dir)
    print_caption("Modal analysis results: measured vs analytical natural frequencies and damping ratios for first 5 modes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
