#!/usr/bin/env python3
"""Steel corrosion trend: errorbar plot of corrosion rate over time."""

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import csv


def plot_corrosion_trend(fig_name: str):
    """Plot steel corrosion rate over exposure time for different groups."""
    # Load data
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "data" / "corrosion_data.csv"
    rows = list(csv.DictReader(open(data_path)))

    # Group data
    groups = {}
    for r in rows:
        g = r["group"]
        groups.setdefault(g, ([], [], []))
        groups[g][0].append(float(r["x_value"]))
        groups[g][1].append(float(r["y_value"]))
        groups[g][2].append(float(r["y_error"]))

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot each group
    colors = {"A": "#4B6F8A", "B": "#C47B45", "C": "#4F7C6A"}
    for g, (xs, ys, errs) in groups.items():
        ax.errorbar(xs, ys, yerr=errs, fmt="o-", color=colors.get(g, "gray"),
                    linewidth=2, markersize=8, capsize=4, label=f"Group {g}")

    # Labels and title
    ax.set_xlabel("Exposure Time (years)", fontsize=14)
    ax.set_ylabel("Corrosion Rate (mm/year)", fontsize=14)
    ax.set_title("Steel Corrosion Trend by Group", fontsize=16)

    # Legend
    ax.legend(fontsize=11, frameon=False)

    # Grid
    ax.grid(True, alpha=0.3)

    # Layout and save
    fig.tight_layout()
    os.makedirs(os.path.dirname(fig_name), exist_ok=True)
    fig.savefig(fig_name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return


if __name__ == "__main__":
    # Set Nature-style rcParams
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 12
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.linewidth"] = 1.5

    plot_corrosion_trend("./figures/corrosion_trend.png")
    print("Figure saved: figures/corrosion_trend.png")
