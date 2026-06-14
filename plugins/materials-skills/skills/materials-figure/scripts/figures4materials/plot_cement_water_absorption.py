#!/usr/bin/env python3
"""Water absorption and porosity comparison across supplementary cementitious material blends."""

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

    rows = read_csv(data_path("cement_water_absorption.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    labels = column(rows, "mix_design")
    absorption = column(rows, "water_absorption_pct", as_float=True)
    abs_sd = column(rows, "absorption_sd", as_float=True)
    porosity = column(rows, "porosity_pct", as_float=True)
    por_sd = column(rows, "porosity_sd", as_float=True)

    x = np.arange(len(labels))

    # Panel (a): Water absorption
    colors = [PALETTE_CEMENT["control"] if l == "Control" else PALETTE_CEMENT["modified"] for l in labels]
    bars1 = ax1.bar(x, absorption, 0.6, color=colors, edgecolor="white", linewidth=0.7,
                    yerr=abs_sd, error_kw={"color": "#333333", "linewidth": 1, "capsize": 3})
    annotate_bars(ax1, bars1, absorption, fmt="{:.1f}", fontsize=7)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=7, rotation=30, ha="right")
    ax1.set_ylabel("Water absorption (%)")
    tighten_ylimits(ax1, list(absorption), margin=0.15, ymin=0)
    add_panel_label(ax1, "a")

    # Panel (b): Porosity
    bars2 = ax2.bar(x, porosity, 0.6, color=colors, edgecolor="white", linewidth=0.7,
                    yerr=por_sd, error_kw={"color": "#333333", "linewidth": 1, "capsize": 3})
    annotate_bars(ax2, bars2, porosity, fmt="{:.1f}", fontsize=7)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=7, rotation=30, ha="right")
    ax2.set_ylabel("Porosity (%)")
    tighten_ylimits(ax2, list(porosity), margin=0.15, ymin=0)
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "cement_water_absorption", args.output_dir)
    print_caption("Water absorption and porosity of cementitious mixes with supplementary cementitious materials.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
