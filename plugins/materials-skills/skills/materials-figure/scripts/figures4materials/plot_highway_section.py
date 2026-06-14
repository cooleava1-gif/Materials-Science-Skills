#!/usr/bin/env python3
"""Pavement cross-section diagram with layer properties."""

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

    rows = read_csv(data_path("highway_pavement_structure.csv"))
    apply_pub_style()

    fig, ax = plt.subplots(figsize=(8, 5))

    layers = column(rows, "layer_name")
    thickness = column(rows, "thickness_mm", as_float=True)
    modulus = column(rows, "elastic_modulus_mpa", as_float=True)

    colors = ["#2D2D2D", "#4B6F8A", "#6B7B8D", "#8B8B6B", "#A89070"]
    y_pos = 0
    total_thickness = sum(thickness)
    bar_width = 0.6

    for i, (layer, thick, mod) in enumerate(zip(layers, thickness, modulus)):
        height_ratio = thick / total_thickness * 10
        rect = ax.barh(y_pos, bar_width, height=-height_ratio, left=0.2, color=colors[i % len(colors)],
                       edgecolor="white", linewidth=1.5)
        ax.text(0.5, y_pos - height_ratio / 2, f"{layer}\n{int(thick)} mm\nE = {int(mod)} MPa",
                ha="center", va="center", fontsize=8, fontweight="bold",
                color="white" if i < 3 else "#333333")
        y_pos -= height_ratio

    ax.set_xlim(0, 1)
    ax.set_ylim(y_pos - 0.5, 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Typical Flexible Pavement Cross-Section", fontsize=11, fontweight="bold", pad=15)

    saved = finalize_figure(fig, "highway_pavement_section", args.output_dir)
    print_caption("Pavement cross-section diagram showing layer thicknesses and elastic moduli.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
