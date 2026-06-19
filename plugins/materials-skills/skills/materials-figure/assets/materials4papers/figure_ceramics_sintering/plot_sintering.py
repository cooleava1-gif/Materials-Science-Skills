#!/usr/bin/env python3
"""Sintering optimization: density and grain size vs temperature."""

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import csv


def plot_sintering_curves(fig_name: str):
    """Plot sintering temperature vs density and grain size."""
    # Load data
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "data" / "sintering_data.csv"
    rows = list(csv.DictReader(open(data_path)))
    T = [int(r["temperature"]) for r in rows]
    Al2O3_density = [float(r["Al2O3_density"]) for r in rows]
    Al2O3_SiC_density = [float(r["Al2O3_SiC_density"]) for r in rows]
    Al2O3_grain = [float(r["Al2O3_grain_size"]) for r in rows]
    Al2O3_SiC_grain = [float(r["Al2O3_SiC_grain_size"]) for r in rows]

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Density vs Temperature
    ax1.plot(T, Al2O3_density, "o-", label="Al₂O₃", lw=2, markersize=8, color="#4B6F8A")
    ax1.plot(T, Al2O3_SiC_density, "s--", label="Al₂O₃-5SiC", lw=2, markersize=8, color="#C47B45")
    ax1.set_xlabel("Sintering Temperature (°C)", fontsize=14)
    ax1.set_ylabel("Relative Density (g/cm³)", fontsize=14)
    ax1.set_title("Density vs Temperature", fontsize=16)
    ax1.legend(fontsize=11, frameon=False)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Grain size vs Temperature
    ax2.plot(T, Al2O3_grain, "o-", label="Al₂O₃", lw=2, markersize=8, color="#4B6F8A")
    ax2.plot(T, Al2O3_SiC_grain, "s--", label="Al₂O₃-5SiC", lw=2, markersize=8, color="#C47B45")
    ax2.set_xlabel("Sintering Temperature (°C)", fontsize=14)
    ax2.set_ylabel("Grain Size (µm)", fontsize=14)
    ax2.set_title("Grain Growth vs Temperature", fontsize=16)
    ax2.legend(fontsize=11, frameon=False)
    ax2.grid(True, alpha=0.3)

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

    plot_sintering_curves("./figures/sintering_curve.png")
    print("Figure saved: figures/sintering_curve.png")
