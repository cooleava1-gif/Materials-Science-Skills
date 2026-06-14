#!/usr/bin/env python3
"""FWD deflection basin comparison across pavement condition states."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_ASPHALT,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("highway_deflection_basin.csv"))
    apply_pub_style()

    fig, ax = plt.subplots(figsize=(7, 4.5))

    distance = column(rows, "sensor_distance_mm", as_float=True)
    good = column(rows, "section_good", as_float=True)
    fair = column(rows, "section_fair", as_float=True)
    poor = column(rows, "section_poor", as_float=True)

    ax.plot(distance, good, color=PALETTE_ASPHALT["optimal"], linewidth=2.2, marker="o", markersize=5, label="Good condition (PCI > 70)")
    ax.plot(distance, fair, color=PALETTE_ASPHALT["modified"], linewidth=2.2, marker="s", markersize=5, label="Fair condition (PCI 40–70)")
    ax.plot(distance, poor, color=PALETTE_ASPHALT["danger"], linewidth=2.2, marker="^", markersize=5, label="Poor condition (PCI < 40)")

    ax.fill_between(distance, 0, good, color=PALETTE_ASPHALT["optimal"], alpha=0.08)
    ax.fill_between(distance, 0, fair, color=PALETTE_ASPHALT["modified"], alpha=0.08)

    ax.set_xlabel("Distance from load center (mm)")
    ax.set_ylabel("Surface deflection (0.01 mm)")
    ax.legend(fontsize=8)
    ax.set_xlim(0, 2100)

    saved = finalize_figure(fig, "highway_deflection_basin", args.output_dir)
    print_caption("FWD deflection basin profiles for pavement sections in good, fair, and poor condition.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
