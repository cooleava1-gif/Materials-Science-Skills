#!/usr/bin/env python3
"""Structural health monitoring: sensor response distribution across bridge elements."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CEMENT,
    add_panel_label,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("bridge_shm_response.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    sensors = column(rows, "sensor_id")
    accel = column(rows, "acceleration_g_peak", as_float=True)
    freq = column(rows, "frequency_hz", as_float=True)
    locations = column(rows, "location")

    x = np.arange(len(sensors))

    # Panel (a): Peak acceleration
    colors_a = [PALETTE_CEMENT["modified"] if a > 0.025 else PALETTE_CEMENT["control"] for a in accel]
    bars1 = ax1.barh(x, accel, 0.55, color=colors_a, edgecolor="white", linewidth=0.7)
    ax1.set_yticks(x)
    ax1.set_yticklabels([f"{s}\n{l}" for s, l in zip(sensors, locations)], fontsize=6.5)
    ax1.set_xlabel("Peak acceleration (g)")
    ax1.invert_yaxis()
    ax1.axvline(0.025, color="#B85450", linewidth=1, linestyle=":", alpha=0.7, label="Alert threshold")
    ax1.legend(fontsize=7)
    add_panel_label(ax1, "a")

    # Panel (b): Dominant frequency
    ax2.barh(x, freq, 0.55, color=PALETTE_CEMENT["durability"], edgecolor="white", linewidth=0.7)
    ax2.set_yticks(x)
    ax2.set_yticklabels([f"{s}" for s in sensors], fontsize=7)
    ax2.set_xlabel("Dominant frequency (Hz)")
    ax2.invert_yaxis()
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "bridge_shm", args.output_dir)
    print_caption("Structural health monitoring sensor response: peak acceleration and dominant frequency by sensor location.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
