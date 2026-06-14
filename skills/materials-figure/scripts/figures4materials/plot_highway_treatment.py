#!/usr/bin/env python3
"""Rehabilitation treatment comparison: cost-effectiveness and PCI recovery."""

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

    rows = read_csv(data_path("highway_treatment_comparison.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    treatments = column(rows, "treatment")
    cost = column(rows, "initial_cost_per_km", as_float=True)
    pci_5 = column(rows, "pci_at_5_years", as_float=True)
    pci_10 = column(rows, "pci_at_10_years", as_float=True)
    pci_15 = column(rows, "pci_at_15_years", as_float=True)
    life = column(rows, "life_extension_years", as_float=True)

    x = np.arange(len(treatments))

    # Panel (a): PCI trajectory
    ax1.plot(x, pci_5, color=PALETTE_ASPHALT["optimal"], linewidth=2.2, marker="o", markersize=5, label="At 5 years")
    ax1.plot(x, pci_10, color=PALETTE_ASPHALT["modified"], linewidth=2.2, marker="s", markersize=5, label="At 10 years")
    ax1.plot(x, pci_15, color=PALETTE_ASPHALT["mechanism"], linewidth=2.2, marker="^", markersize=5, label="At 15 years")
    ax1.axhline(55, color="#B85450", linewidth=1, linestyle=":", alpha=0.7, label="Minimum acceptable PCI")
    ax1.set_xticks(x)
    ax1.set_xticklabels(treatments, fontsize=7, rotation=25, ha="right")
    ax1.set_ylabel("Pavement Condition Index (PCI)")
    ax1.legend(fontsize=7.5)
    add_panel_label(ax1, "a")

    # Panel (b): Life extension vs cost
    bars = ax2.bar(x, life, 0.55, color=PALETTE_ASPHALT["modified"], edgecolor="white", linewidth=0.7)
    annotate_bars(ax2, bars, life, fmt="{:.0f}", fontsize=7)
    ax2.set_xticks(x)
    ax2.set_xticklabels(treatments, fontsize=7, rotation=25, ha="right")
    ax2.set_ylabel("Life extension (years)")
    tighten_ylimits(ax2, list(life), margin=0.15, ymin=0)
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "highway_treatment_comparison", args.output_dir)
    print_caption("Rehabilitation treatment comparison: PCI trajectory and life extension for different maintenance strategies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
