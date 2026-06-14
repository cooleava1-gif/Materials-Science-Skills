#!/usr/bin/env python3
"""Mechanism diagram for WER-EA system."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("mechanism_diagram.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    components = column(rows, "component")
    roles = column(rows, "role")
    certainty = column(rows, "certainty")
    connection_strength = column(rows, "connection_strength", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create a simple network diagram
    # Central node: WER-EA system
    center_x, center_y = 0.5, 0.5
    radius = 0.35

    # Draw central node
    circle = plt.Circle((center_x, center_y), 0.08, color=PALETTE_CBM["modified"], alpha=0.9)
    ax.add_patch(circle)
    ax.text(center_x, center_y, "WER-EA\nSystem", ha="center", va="center", fontsize=8, fontweight="bold")

    # Draw component nodes around the center
    angles = np.linspace(0, 2 * np.pi, len(components), endpoint=False)
    for i, (component, role, cert, strength) in enumerate(zip(components, roles, certainty, connection_strength)):
        angle = angles[i]
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)

        # Color based on certainty
        if cert == "measured":
            color = PALETTE_CBM["control"]
        elif cert == "inferred":
            color = PALETTE_CBM["accent"]
        else:
            color = PALETTE_CBM["neutral"]

        # Draw connection line
        ax.plot([center_x, x], [center_y, y], color=color, linewidth=strength * 3, alpha=0.6)

        # Draw node
        circle = plt.Circle((x, y), 0.06, color=color, alpha=0.8)
        ax.add_patch(circle)
        ax.text(x, y, f"{component}\n({role})", ha="center", va="center", fontsize=6)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("WER-EA System Mechanism Diagram", fontsize=12, fontweight="bold")

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE_CBM["control"], markersize=10, label="Measured"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE_CBM["accent"], markersize=10, label="Inferred"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE_CBM["neutral"], markersize=10, label="Speculative"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=8)

    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "mechanism_diagram", args.output_dir)
    print_caption(
        "Mechanism diagram for WER-EA system showing component relationships and evidence certainty. "
        "Solid lines indicate measured evidence; dashed lines indicate inferred relationships."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())