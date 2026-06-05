#!/usr/bin/env python3
"""Dosage-performance trend for waterborne epoxy modified emulsified asphalt."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("dosage_performance.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    dosage = column(rows, "dosage_pct", as_float=True)
    bonding = column(rows, "bond_strength_mpa", as_float=True)
    stability = column(rows, "storage_stability_pct", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    make_line_trend(
        ax,
        dosage,
        [bonding, [value / 100 for value in stability]],
        ["Bond strength (MPa)", "Storage stability / 100"],
        PALETTE_CBM,
        xlabel="Waterborne epoxy content (%)",
        ylabel="Normalized performance",
    )
    ax.axvspan(10, 15, color=PALETTE_CBM["accent"], alpha=0.18, label="candidate range")
    add_panel_label(ax, "(b)")
    fig.tight_layout()
    finalize_figure(fig, "dosage_performance_curve", args.output_dir)
    print_caption(
        "Dosage-performance trend showing bond strength and storage-stability response. "
        "The highlighted range is a candidate optimum, not proof of field durability."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
