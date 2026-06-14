#!/usr/bin/env python3
"""Contour response map for two-factor materials optimization."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_contour_map


def grid_from_rows(rows: list[dict[str, str]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_vals = sorted({float(row["wer_pct"]) for row in rows})
    y_vals = sorted({float(row["curing_temp_c"]) for row in rows})
    z_lookup = {(float(row["wer_pct"]), float(row["curing_temp_c"])): float(row["bond_strength_mpa"]) for row in rows}
    x_grid, y_grid = np.meshgrid(x_vals, y_vals)
    z_grid = np.array([[z_lookup[(x, y)] for x in x_vals] for y in y_vals], dtype=float)
    return x_grid, y_grid, z_grid


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("contour_response_map.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    x_grid, y_grid, z_grid = grid_from_rows(rows)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    make_contour_map(
        ax,
        x_grid,
        y_grid,
        z_grid,
        xlabel="Waterborne epoxy content (%)",
        ylabel="Curing temperature (C)",
    )
    ax.scatter(x_grid.ravel(), y_grid.ravel(), s=18, color=PALETTE_ASPHALT["neutral"], edgecolor="white", linewidth=0.5)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "contour_response_map", args.output_dir)
    print_caption(
        "Contour response map of bond strength as a function of epoxy content and curing temperature. Experimental grid points are overlaid to limit interpolation claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
