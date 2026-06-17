#!/usr/bin/env python3
"""Errorbar trend for aging, durability, or hardness profile time series."""

from __future__ import annotations

import argparse
import json
import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_errorbar_trend

COLUMN_MAP = {
    "x_values": {"column": "aging_day"},
    "y_values": {"column": "strength_mean_mpa"},
    "y_errors": {"column": "strength_sd_mpa"},
    "xlabel": {"value": "Aging time (d)"},
    "ylabel": {"value": "Bond strength (MPa)"},
    "label": {"value": "15% WER"},
    "figure_name": {"value": "errorbar_trend"},
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("errorbar_trend.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)

    x_col = cmap.get("x_values", {}).get("column", "aging_day")
    y_col = cmap.get("y_values", {}).get("column", "strength_mean_mpa")
    err_col = cmap.get("y_errors", {}).get("column", "strength_sd_mpa")

    # Smart fallbacks if mapped columns are missing
    if x_col not in rows[0]:
        if "distance_mm" in rows[0]:
            x_col = "distance_mm"
        elif "aging_day" in rows[0]:
            x_col = "aging_day"

    if y_col not in rows[0]:
        if "hardness_HV" in rows[0]:
            y_col = "hardness_HV"
        elif "strength_mean_mpa" in rows[0]:
            y_col = "strength_mean_mpa"

    days = column(rows, x_col, as_float=True)
    strength = column(rows, y_col, as_float=True)

    if err_col in rows[0]:
        sd = column(rows, err_col, as_float=True)
    else:
        sd = None

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.4, 3.6))

    xlabel = cmap.get("xlabel", {}).get("value", "Aging time (d)")
    ylabel = cmap.get("ylabel", {}).get("value", "Bond strength (MPa)")
    label_val = cmap.get("label", {}).get("value", "15% WER")

    # Update labels based on actual fallback columns
    if x_col == "distance_mm" and xlabel == "Aging time (d)":
        xlabel = "Distance from weld center (mm)"
    if y_col == "hardness_HV" and ylabel == "Bond strength (MPa)":
        ylabel = "Hardness (HV)"
    if x_col == "distance_mm" and label_val == "15% WER":
        label_val = "Hardness Profile"

    make_errorbar_trend(
        ax,
        days,
        strength,
        sd,
        PALETTE_ASPHALT,
        xlabel=xlabel,
        ylabel=ylabel,
        label=label_val,
    )
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, cmap.get("figure_name", {}).get("value", "errorbar_trend"), args.output_dir)
    print_caption(
        f"Errorbar trend showing {ylabel.lower()} vs {xlabel.lower()}."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
