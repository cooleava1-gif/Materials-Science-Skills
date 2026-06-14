#!/usr/bin/env python3
"""3D response surface for materials optimization."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import data_path, print_caption, read_csv
from materials_plot_lib import apply_pub_style, finalize_figure, make_3d_surface


def grid_from_rows(rows: list[dict[str, str]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_vals = sorted({float(row["wer_pct"]) for row in rows})
    y_vals = sorted({float(row["curing_temp_c"]) for row in rows})
    z_lookup = {(float(row["wer_pct"]), float(row["curing_temp_c"])): float(row["bond_strength_mpa"]) for row in rows}
    x_grid, y_grid = np.meshgrid(x_vals, y_vals)
    z_grid = np.array([[z_lookup[(x, y)] for x in x_vals] for y in y_vals], dtype=float)
    return x_grid, y_grid, z_grid


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("response_surface_grid.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    x_grid, y_grid, z_grid = grid_from_rows(rows)

    apply_pub_style()
    fig = plt.figure(figsize=(6.2, 4.3))
    ax = fig.add_subplot(111, projection="3d")
    make_3d_surface(
        ax,
        x_grid,
        y_grid,
        z_grid,
        xlabel="WER content (%)",
        ylabel="Curing temp (C)",
        zlabel="Bond strength (MPa)",
    )
    ax.text2D(0.02, 0.98, "a", transform=ax.transAxes, ha="left", va="top", fontsize=12, fontweight="bold")
    fig.tight_layout()
    finalize_figure(fig, "3d_response_surface", args.output_dir)
    print_caption(
        "3D response surface for bond strength across epoxy content and curing temperature. Surface geometry summarizes the measured grid and should not be extrapolated outside it."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
