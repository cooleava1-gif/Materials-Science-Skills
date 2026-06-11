#!/usr/bin/env python3
"""Property correlation heatmap for WER-EA systems."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_heatmap


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("property_correlation.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    properties = [row["property"] for row in rows]
    correlation_matrix = []
    for row in rows:
        correlation_matrix.append([float(row[prop]) for prop in properties])
    data = np.array(correlation_matrix)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    make_heatmap(
        ax,
        data,
        properties,
        properties,
        PALETTE_CBM,
        cmap="RdYlGn",
        annot=True,
        fmt=".2f",
        vmin=0,
        vmax=1,
    )
    ax.set_title("Property correlation matrix for WER-EA systems", fontsize=10)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "property_correlation_heatmap", args.output_dir)
    print_caption(
        "Property correlation matrix for WER-EA systems showing relationships between bonding, viscosity, stability, workability, and durability. "
        "High correlation does not imply causation; mechanism evidence requires independent characterization."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())