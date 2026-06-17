#!/usr/bin/env python3
"""Contour response map for two-factor materials optimization."""

from __future__ import annotations

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_contour_map

COLUMN_MAP = {
    "x_values": {"column": "wer_pct"},
    "y_values": {"column": "curing_temp_c"},
    "z_values": {"column": "bond_strength_mpa"},
    "xlabel": {"value": "Waterborne epoxy content (%)"},
    "ylabel": {"value": "Curing temperature (C)"},
    "figure_name": {"value": "contour_response_map"},
}

def grid_from_rows(rows: list[dict[str, str]], x_col: str, y_col: str, z_col: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_vals = sorted({float(row[x_col]) for row in rows if row[x_col]})
    y_vals = sorted({float(row[y_col]) for row in rows if row[y_col]})
    z_lookup = {(float(row[x_col]), float(row[y_col])): float(row[z_col]) for row in rows if row[x_col] and row[y_col] and row[z_col]}
    x_grid, y_grid = np.meshgrid(x_vals, y_vals)
    z_grid = np.array([[z_lookup[(x, y)] for x in x_vals] for y in y_vals], dtype=float)
    return x_grid, y_grid, z_grid

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("contour_response_map.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)

    x_col = cmap.get("x_values", {}).get("column", "wer_pct")
    y_col = cmap.get("y_values", {}).get("column", "curing_temp_c")
    z_col = cmap.get("z_values", {}).get("column", "bond_strength_mpa")

    # Check fallback names if default is missing
    if x_col not in rows[0]:
        x_col = next((c for c in ("wer_pct", "power", "power_w", "x") if c in rows[0]), rows[0].keys().__iter__().__next__())
    if y_col not in rows[0]:
        y_col = next((c for c in ("curing_temp_c", "speed", "speed_mm_s", "y") if c in rows[0]), list(rows[0].keys())[1])
    if z_col not in rows[0]:
        z_col = next((c for c in ("bond_strength_mpa", "density", "relative_density_pct", "z") if c in rows[0]), list(rows[0].keys())[2])

    x_grid, y_grid, z_grid = grid_from_rows(rows, x_col, y_col, z_col)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.6, 4.0))

    xlabel = cmap.get("xlabel", {}).get("value", "Waterborne epoxy content (%)")
    ylabel = cmap.get("ylabel", {}).get("value", "Curing temperature (C)")
    fig_name = cmap.get("figure_name", {}).get("value", "contour_response_map")

    # Adapt labels to actual columns if fallback triggered
    if x_col in ("power", "power_w") and xlabel == "Waterborne epoxy content (%)":
        xlabel = "Laser Power (W)"
    if y_col in ("speed", "speed_mm_s") and ylabel == "Curing temperature (C)":
        ylabel = "Scan Speed (mm/s)"

    make_contour_map(
        ax,
        x_grid,
        y_grid,
        z_grid,
        xlabel=xlabel,
        ylabel=ylabel,
    )
    ax.scatter(x_grid.ravel(), y_grid.ravel(), s=18, color=PALETTE_ASPHALT["neutral"], edgecolor="white", linewidth=0.5)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, fig_name, args.output_dir)
    print_caption(
        f"Contour response map of {z_col} as a function of {xlabel} and {ylabel}. Experimental grid points are overlaid to limit interpolation claims."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
