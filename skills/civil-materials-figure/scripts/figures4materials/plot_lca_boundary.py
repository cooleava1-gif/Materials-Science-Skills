#!/usr/bin/env python3
"""LCA boundary diagram for WER-EA systems."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("lca_boundary.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    categories = column(rows, "category")
    contributions = column(rows, "contribution", as_float=True)
    notes = column(rows, "notes")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create horizontal bar chart
    y_pos = range(len(categories))
    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["optimal"],
              PALETTE_CBM["mechanism"], PALETTE_CBM["accent"], PALETTE_CBM["neutral"]]

    bars = ax.barh(y_pos, contributions, color=colors[:len(categories)], alpha=0.8, edgecolor="black", linewidth=0.5)

    # Add percentage labels
    for i, (bar, contribution) in enumerate(zip(bars, contributions)):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height() / 2,
               f"{contribution:.0f}%", ha="left", va="center", fontsize=9)

    # Add notes
    for i, (category, note) in enumerate(zip(categories, notes)):
        ax.text(contributions[i] + 5, i, f"({note})", ha="left", va="center", fontsize=7, style="italic")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.set_xlabel("Contribution (%)")
    ax.set_title("LCA Boundary for WER-EA Tack Coat System", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 50)
    ax.grid(axis="x", alpha=0.3)

    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "lca_boundary", args.output_dir)
    print_caption(
        "LCA boundary diagram for WER-EA tack coat system showing life cycle stage contributions. "
        "Sustainability claims require complete LCA with functional unit and system boundary definition."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())