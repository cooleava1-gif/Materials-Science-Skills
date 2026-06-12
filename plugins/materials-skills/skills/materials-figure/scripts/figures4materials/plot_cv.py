#!/usr/bin/env python3
"""Cyclic Voltammetry (CV) curves for electrochemical characterization."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def _annotate_peaks(ax, voltage: list[float], current: list[float], color: str, threshold: float = 0.4):
    arr = np.array(current)
    v_arr = np.array(voltage)
    mean_c = np.mean(arr)
    std_c = np.std(arr) or 1.0
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1] and arr[i] > mean_c + threshold * std_c:
            ax.annotate(
                f"{v_arr[i]:.2f} V", xy=(v_arr[i], arr[i]), fontsize=7, color=color,
                textcoords="offset points", xytext=(5, 5),
                arrowprops=dict(arrowstyle="->", color=color, lw=0.7),
            )
        if arr[i] < arr[i - 1] and arr[i] < arr[i + 1] and arr[i] < mean_c - threshold * std_c:
            ax.annotate(
                f"{v_arr[i]:.2f} V", xy=(v_arr[i], arr[i]), fontsize=7, color=color,
                textcoords="offset points", xytext=(5, -10),
                arrowprops=dict(arrowstyle="->", color=color, lw=0.7),
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("cv_curve.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    voltage = column(rows, "voltage", as_float=True)
    sample_cols = [k for k in rows[0] if k != "voltage"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    colors = list(PALETTE_CBM.values())

    for idx, col_name in enumerate(sample_cols):
        current = column(rows, col_name, as_float=True)
        color = colors[idx % len(colors)]
        ax.plot(voltage, current, linewidth=1.8, label=col_name, color=color)
        _annotate_peaks(ax, voltage, current, color)

    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Current (mA)")
    ax.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    ax.legend()
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "cv_curve_comparison", args.output_dir)
    print_caption(
        "Cyclic voltammetry curves showing current vs voltage. "
        "Anodic (oxidation) peaks appear in the positive-current region; "
        "cathodic (reduction) peaks in the negative-current region. "
        "Peak positions and separation indicate reversibility and redox kinetics."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
