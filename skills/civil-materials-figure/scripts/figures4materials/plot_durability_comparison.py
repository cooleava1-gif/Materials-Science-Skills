#!/usr/bin/env python3
from __future__ import annotations
import argparse
import matplotlib.pyplot as plt
from matplotlib import gridspec
from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend

def main() -> int:
    parser = argparse.ArgumentParser(description="Durability comparison")
    parser.add_argument("--data", default=str(data_path("durability_comparison.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()
    rows = read_csv(args.data)
    labels = ["Pure asphalt", "10% WER"]
    ft_cycles = column(rows, "freeze_thaw_cycles", as_float=True)
    ft_series = [column(rows, "freeze_thaw_retention_pure", as_float=True), column(rows, "freeze_thaw_retention_10pct_wer", as_float=True)]
    aging_days = column(rows, "aging_days", as_float=True)
    aging_series = [column(rows, "aging_retention_pure", as_float=True), column(rows, "aging_retention_10pct_wer", as_float=True)]
    apply_pub_style()
    fig = plt.figure(figsize=(10, 4.5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    make_line_trend(ax1, ft_cycles, ft_series, labels, PALETTE_CBM, xlabel="Freeze-thaw cycles", ylabel="Strength retention (%)")
    ax1.set_xlim(0, 30)
    ax1.set_ylim(50, 105)
    ax1.axhline(y=80, color=PALETTE_CBM["danger"], linestyle=":", linewidth=1.2, alpha=0.7)
    ax1.text(15, 81, "80% threshold", fontsize=7, color=PALETTE_CBM["danger"], ha="center")
    ax1.set_title("Freeze-thaw durability", fontsize=10)
    add_panel_label(ax1, "(a)")
    make_line_trend(ax2, aging_days, aging_series, labels, PALETTE_CBM, xlabel="Aging time (days)", ylabel="Bonding retention (%)")
    ax2.set_xlim(0, 14)
    ax2.set_ylim(50, 105)
    ax2.axhline(y=80, color=PALETTE_CBM["danger"], linestyle=":", linewidth=1.2, alpha=0.7)
    ax2.text(7, 81, "80% threshold", fontsize=7, color=PALETTE_CBM["danger"], ha="center")
    ax2.set_title("Thermal aging durability", fontsize=10)
    add_panel_label(ax2, "(b)")
    fig.suptitle("WER-EA Durability Comparison", fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    finalize_figure(fig, "durability_comparison", args.output_dir)
    print_caption("Durability comparison for WER-EA systems.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
