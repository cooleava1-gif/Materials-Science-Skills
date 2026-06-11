#!/usr/bin/env python3
"""Literature screening flow diagram for WER-EA review."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("screening_flow.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    stages = column(rows, "stage")
    counts = column(rows, "count", as_float=True)
    descriptions = column(rows, "description")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create flow diagram
    box_height = 0.6
    box_width = 1.2
    spacing = 0.8
    start_y = len(stages) * spacing

    for i, (stage, count, desc) in enumerate(zip(stages, counts, descriptions)):
        y = start_y - i * spacing

        # Draw box
        if i < 6:  # Main flow
            color = PALETTE_CBM["control"]
            alpha = 0.9
        else:  # Exclusion reasons
            color = PALETTE_CBM["danger"]
            alpha = 0.7

        rect = plt.Rectangle((0.5 - box_width / 2, y - box_height / 2), box_width, box_height,
                             facecolor=color, alpha=alpha, edgecolor="black", linewidth=1)
        ax.add_patch(rect)

        # Add text
        ax.text(0.5, y + 0.1, f"{stage}", ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(0.5, y - 0.15, f"n = {int(count)}", ha="center", va="center", fontsize=8)

        # Draw arrow to next stage
        if i < 5:  # Main flow
            ax.annotate("", xy=(0.5, y - box_height / 2 - 0.05),
                       xytext=(0.5, y - spacing + box_height / 2 + 0.05),
                       arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    # Add exclusion boxes on the right
    exclusion_x = 2.5
    for i in range(6, len(stages)):
        y = start_y - i * spacing
        stage = stages[i]
        count = counts[i]
        desc = descriptions[i]

        rect = plt.Rectangle((exclusion_x - box_width / 2, y - box_height / 2), box_width, box_height,
                             facecolor=PALETTE_CBM["danger"], alpha=0.5, edgecolor="black", linewidth=1)
        ax.add_patch(rect)

        ax.text(exclusion_x, y + 0.1, f"{stage}", ha="center", va="center", fontsize=7)
        ax.text(exclusion_x, y - 0.15, f"n = {int(count)}", ha="center", va="center", fontsize=7)

        # Draw arrow from main flow
        if i == 6:
            ax.annotate("", xy=(exclusion_x - box_width / 2, y),
                       xytext=(0.5 + box_width / 2, start_y - 2 * spacing),
                       arrowprops=dict(arrowstyle="->", color=PALETTE_CBM["danger"], lw=1, linestyle="--"))

    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, start_y + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("WER-EA Literature Screening Flow", fontsize=12, fontweight="bold")

    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "literature_screening_flow", args.output_dir)
    print_caption(
        "Literature screening flow for WER-EA review showing inclusion/exclusion criteria and counts. "
        "Screening must be reproducible; exclusion reasons should be documented for transparency."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())