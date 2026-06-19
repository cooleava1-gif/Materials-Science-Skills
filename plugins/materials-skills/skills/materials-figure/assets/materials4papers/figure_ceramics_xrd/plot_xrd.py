#!/usr/bin/env python3
"""XRD phase identification for Al2O3-ZrO2 composite ceramics."""

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import csv


def plot_xrd_pattern(fig_name: str):
    """Plot XRD pattern showing Al2O3, t-ZrO2, and m-ZrO2 phases."""
    # Load data
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "data" / "xrd_data.csv"
    rows = list(csv.DictReader(open(data_path)))
    tth = [float(r["two_theta"]) for r in rows]
    alumina = [float(r["alumina_intensity"]) for r in rows]
    zirconia_t = [float(r["zirconia_t_intensity"]) for r in rows]
    zirconia_m = [float(r["zirconia_m_intensity"]) for r in rows]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot patterns
    ax.plot(tth, alumina, label="Al₂O₃", lw=1.5, color="#4B6F8A")
    ax.plot(tth, zirconia_t, label="t-ZrO₂", lw=1.5, color="#C47B45")
    ax.plot(tth, zirconia_m, "--", label="m-ZrO₂", lw=1.5, alpha=0.7, color="#8B4513")

    # Labels and title
    ax.set_xlabel("2θ (°)", fontsize=14)
    ax.set_ylabel("Intensity (a.u.)", fontsize=14)
    ax.set_title("XRD Pattern: Al₂O₃-ZrO₂ Composite", fontsize=16)

    # Legend
    ax.legend(fontsize=11, frameon=False)

    # Annotate key peaks
    peak_annotations = [
        (30.2, "t-ZrO₂ (101)"),
        (35.2, "Al₂O₃ (104)"),
        (43.4, "Al₂O₃ (113)"),
        (50.2, "t-ZrO₂ (200)"),
        (60.2, "t-ZrO₂ (211)")
    ]
    y_max = max(max(alumina), max(zirconia_t), max(zirconia_m))
    for pos, lbl in peak_annotations:
        ax.annotate(lbl, (pos, y_max * 0.85), fontsize=9, rotation=45, ha="center")

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

    plot_xrd_pattern("./figures/xrd_pattern.png")
    print("Figure saved: figures/xrd_pattern.png")
