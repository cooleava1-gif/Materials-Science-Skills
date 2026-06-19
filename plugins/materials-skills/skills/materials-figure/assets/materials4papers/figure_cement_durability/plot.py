#!/usr/bin/env python3
"""Cement durability: retention percentage under different aging conditions."""

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import csv


def plot_durability_retention(fig_name: str):
    """Plot durability retention for control vs modified cement."""
    # Load data
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "data" / "durability_data.csv"
    rows = list(csv.DictReader(open(data_path)))
    conditions = [r["condition"] for r in rows]
    control = [float(r["control_retention_pct"]) for r in rows]
    modified = [float(r["modified_retention_pct"]) for r in rows]
    control_sd = [float(r["control_sd"]) for r in rows]
    modified_sd = [float(r["modified_sd"]) for r in rows]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # X positions
    x = np.arange(len(conditions))
    width = 0.35

    # Plot bars with error bars
    bars1 = ax.bar(x - width/2, control, width, label="Control", yerr=control_sd,
                   color="#4B6F8A", capsize=5, edgecolor="black", linewidth=1)
    bars2 = ax.bar(x + width/2, modified, width, label="Modified", yerr=modified_sd,
                   color="#C47B45", capsize=5, edgecolor="black", linewidth=1)

    # Labels and title
    ax.set_xlabel("Aging Condition", fontsize=14)
    ax.set_ylabel("Property Retention (%)", fontsize=14)
    ax.set_title("Durability Retention: Control vs Modified Cement", fontsize=16)

    # X-axis ticks
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, rotation=15, ha="right")

    # Legend
    ax.legend(fontsize=11, frameon=False)

    # Grid
    ax.grid(True, axis="y", alpha=0.3)

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

    plot_durability_retention("./figures/durability_retention.png")
    print("Figure saved: figures/durability_retention.png")
