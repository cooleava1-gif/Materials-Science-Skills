#!/usr/bin/env python3
"""Weibull reliability analysis: 3Y-TZP vs Al2O3-doped strength distribution."""

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import csv


def weibull_plot(strengths, label, color, ax):
    """Calculate and plot Weibull distribution for a given strength dataset."""
    s = np.array(strengths)
    n = len(s)
    F = (np.arange(1, n + 1) - 0.3) / (n + 0.4)
    ln_s = np.log(s)
    ln_ln = np.log(-np.log(1 - F))
    m = np.polyfit(ln_s, ln_ln, 1)[0]
    ax.plot(ln_s, ln_ln, "o-", color=color, linewidth=2, markersize=8,
            label=f"{label} (m={m:.1f})")
    return


def plot_weibull_distribution(fig_name: str):
    """Plot Weibull distribution for 3Y-TZP and Al2O3-doped ceramics."""
    # Load data
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "data" / "weibull_data.csv"
    rows = list(csv.DictReader(open(data_path)))
    s_3y = sorted(float(r["strength_3Y"]) for r in rows)
    s_3y_al = sorted(float(r["strength_3Y_Al2O3"]) for r in rows)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot Weibull distributions
    weibull_plot(s_3y, "3Y-TZP", "#4B6F8A", ax)
    weibull_plot(s_3y_al, "3Y-TZP + 0.5wt% Al₂O₃", "#C47B45", ax)

    # Labels and title
    ax.set_xlabel("ln(fracture strength) (MPa)", fontsize=14)
    ax.set_ylabel("ln(ln(1/(1-P_f)))", fontsize=14)
    ax.set_title("Weibull Plot: 3Y-TZP vs Al₂O₃-Doped", fontsize=16)

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

    plot_weibull_distribution("./figures/weibull_plot.png")
    print("Figure saved: figures/weibull_plot.png")
