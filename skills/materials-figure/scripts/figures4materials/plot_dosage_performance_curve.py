#!/usr/bin/env python3
"""Dosage-performance trend for waterborne epoxy modified emulsified asphalt."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, tighten_ylimits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("dosage_performance.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    dosage = column(rows, "dosage_pct", as_float=True)
    bonding = column(rows, "bond_strength_mpa", as_float=True)
    stability = column(rows, "storage_stability_pct", as_float=True)
    viscosity = column(rows, "viscosity_mpas", as_float=True)

    apply_pub_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8))

    # ── Panel (a): Bond strength and storage stability ──
    ax1.plot(dosage, bonding, "o-", color=PALETTE_CBM["control"], linewidth=1.8, markersize=6, label="Bond strength")
    ax1.set_xlabel("Waterborne epoxy content (%)")
    ax1.set_ylabel("Bond strength (MPa)", color=PALETTE_CBM["control"])
    ax1.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    tighten_ylimits(ax1, bonding, margin=0.12, ymin=0.35)

    ax1b = ax1.twinx()
    ax1b.plot(dosage, stability, "s--", color=PALETTE_CBM["modified"], linewidth=1.8, markersize=6, label="Storage stability")
    ax1b.set_ylabel("Storage stability (%)", color=PALETTE_CBM["modified"])
    ax1b.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    tighten_ylimits(ax1b, stability, margin=0.05, ymin=85)

    ax1.axvspan(10, 15, color=PALETTE_CBM["accent"], alpha=0.12, label="Candidate range")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc="lower right")
    add_panel_label(ax1, "a")

    # ── Panel (b): Viscosity trend ──
    ax2.plot(dosage, viscosity, "D-", color=PALETTE_CBM["danger"], linewidth=1.8, markersize=6)
    ax2.axhline(y=500, color="#8C8C8C", linestyle="--", linewidth=0.8, alpha=0.7, label="Spray limit (~500 mPa\u00b7s)")
    ax2.axvspan(10, 15, color=PALETTE_CBM["accent"], alpha=0.12)
    ax2.set_xlabel("Waterborne epoxy content (%)")
    ax2.set_ylabel("Viscosity (mPa\u00b7s)")
    tighten_ylimits(ax2, viscosity, margin=0.12, ymin=150)
    ax2.legend(fontsize=7)
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "dosage_performance_curve", args.output_dir)
    print_caption(
        "Dosage-performance relationship: (a) bond strength and storage stability with candidate optimum range, "
        "(b) viscosity trend with spray-application limit. The highlighted range is a candidate optimum, "
        "not proof of field durability."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
