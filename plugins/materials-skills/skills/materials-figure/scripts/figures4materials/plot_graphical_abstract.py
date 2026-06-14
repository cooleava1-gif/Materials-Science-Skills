#!/usr/bin/env python3
"""Graphical abstract for WER-EA review."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("graphical_abstract.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    panels = column(rows, "panel")
    categories = column(rows, "category")
    labels = column(rows, "label")
    descriptions = column(rows, "description")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(10, 4))

    # Create graphical abstract with 5 panels
    panel_width = 1.5
    panel_height = 2.5
    spacing = 0.3
    start_x = 0.5

    colors = [
        PALETTE_CBM["danger"],      # Problem
        PALETTE_CBM["modified"],    # Material design
        PALETTE_CBM["control"],     # Evidence chain
        PALETTE_CBM["optimal"],     # Application
        PALETTE_CBM["accent"],      # Gap
    ]

    for i, (panel, category, label, desc) in enumerate(zip(panels, categories, labels, descriptions)):
        x = start_x + i * (panel_width + spacing)
        y = 1.5

        # Draw panel box
        rect = plt.Rectangle((x, y - panel_height / 2), panel_width, panel_height,
                             facecolor=colors[i], alpha=0.8, edgecolor="black", linewidth=1.5)
        ax.add_patch(rect)

        # Add category label
        ax.text(x + panel_width / 2, y + panel_height / 2 - 0.2, category,
               ha="center", va="center", fontsize=9, fontweight="bold")

        # Add main label
        ax.text(x + panel_width / 2, y + 0.1, label,
               ha="center", va="center", fontsize=8, fontweight="bold")

        # Add description
        ax.text(x + panel_width / 2, y - panel_height / 2 + 0.3, desc,
               ha="center", va="center", fontsize=6, style="italic")

        # Draw arrow to next panel
        if i < len(panels) - 1:
            ax.annotate("", xy=(x + panel_width + 0.05, y),
                       xytext=(x + panel_width + spacing - 0.05, y),
                       arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    # Add title
    ax.text(start_x + 4 * (panel_width + spacing) / 2, 3.5,
           "Waterborne Epoxy Modified Emulsified Asphalt (WER-EA)",
           ha="center", va="center", fontsize=12, fontweight="bold")

    # Add subtitle
    ax.text(start_x + 4 * (panel_width + spacing) / 2, 3.0,
           "From Material Design to Pavement Application",
           ha="center", va="center", fontsize=10)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "graphical_abstract", args.output_dir)
    print_caption(
        "Graphical abstract for WER-EA review showing the research narrative from problem to gap. "
        "Each panel represents a key aspect of the review; claims must be evidence-bound."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())