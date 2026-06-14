#!/usr/bin/env python3
"""Research gap matrix for WER-EA systems."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("research_gap_matrix.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    topics = column(rows, "topic")
    available = column(rows, "available_evidence")
    missing = column(rows, "missing_evidence")
    risk = column(rows, "reviewer_risk")
    next_tests = column(rows, "next_test")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create matrix visualization
    n_topics = len(topics)
    n_cols = 4  # available, missing, risk, next test

    # Create grid
    cell_width = 2.0
    cell_height = 0.8
    start_x = 0.5
    start_y = n_topics * cell_height

    # Draw headers
    headers = ["Available Evidence", "Missing Evidence", "Reviewer Risk", "Next Test"]
    for j, header in enumerate(headers):
        x = start_x + j * cell_width
        y = start_y + 0.2
        rect = plt.Rectangle((x, y - cell_height / 2), cell_width, cell_height,
                             facecolor=PALETTE_CBM["control"], alpha=0.9, edgecolor="black", linewidth=1)
        ax.add_patch(rect)
        ax.text(x + cell_width / 2, y, header, ha="center", va="center", fontsize=8, fontweight="bold")

    # Draw data cells
    risk_colors = {"Low": PALETTE_CBM["optimal"], "Moderate": PALETTE_CBM["accent"], "High": PALETTE_CBM["danger"]}

    for i, (topic, avail, miss, r, next_test) in enumerate(zip(topics, available, missing, risk, next_tests)):
        y = start_y - (i + 1) * cell_height

        # Topic label
        ax.text(start_x - 0.1, y, topic, ha="right", va="center", fontsize=8, fontweight="bold")

        # Available evidence
        x = start_x
        rect = plt.Rectangle((x, y - cell_height / 2), cell_width, cell_height,
                             facecolor=PALETTE_CBM["optimal"], alpha=0.6, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        ax.text(x + cell_width / 2, y, avail, ha="center", va="center", fontsize=7)

        # Missing evidence
        x = start_x + cell_width
        rect = plt.Rectangle((x, y - cell_height / 2), cell_width, cell_height,
                             facecolor=PALETTE_CBM["danger"], alpha=0.6, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        ax.text(x + cell_width / 2, y, miss, ha="center", va="center", fontsize=7)

        # Reviewer risk
        x = start_x + 2 * cell_width
        color = risk_colors.get(r, PALETTE_CBM["neutral"])
        rect = plt.Rectangle((x, y - cell_height / 2), cell_width, cell_height,
                             facecolor=color, alpha=0.7, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        ax.text(x + cell_width / 2, y, r, ha="center", va="center", fontsize=7)

        # Next test
        x = start_x + 3 * cell_width
        rect = plt.Rectangle((x, y - cell_height / 2), cell_width, cell_height,
                             facecolor=PALETTE_CBM["modified"], alpha=0.6, edgecolor="black", linewidth=0.5)
        ax.add_patch(rect)
        ax.text(x + cell_width / 2, y, next_test, ha="center", va="center", fontsize=7)

    ax.set_xlim(-1.5, start_x + 4 * cell_width + 0.5)
    ax.set_ylim(-0.5, start_y + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("WER-EA Research Gap Matrix", fontsize=12, fontweight="bold")

    # Add legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, facecolor=PALETTE_CBM["optimal"], alpha=0.6, label="Available"),
        plt.Rectangle((0, 0), 1, 1, facecolor=PALETTE_CBM["danger"], alpha=0.6, label="Missing"),
        plt.Rectangle((0, 0), 1, 1, facecolor=PALETTE_CBM["accent"], alpha=0.7, label="Moderate risk"),
        plt.Rectangle((0, 0), 1, 1, facecolor=PALETTE_CBM["danger"], alpha=0.7, label="High risk"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=8)

    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "research_gap_matrix", args.output_dir)
    print_caption(
        "Research gap matrix for WER-EA systems showing available evidence, missing evidence, reviewer risk, and recommended next tests. "
        "Gap strength depends on search boundary; reviewer risk should guide research prioritization."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())