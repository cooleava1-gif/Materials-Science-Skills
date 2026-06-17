#!/usr/bin/env python3
"""Generic potentiodynamic polarization curves for corrosion analysis."""

from __future__ import annotations

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure

COLUMN_MAP = {
    "x_values": {"column": "potential_mv"},
    "y_values": {"column": "current_log_a_cm2"},
    "group_by": {"column": "condition"},
    "xlabel": {"value": "Potential (mV vs SCE)"},
    "ylabel": {"value": "log |i| (A/cm²)"},
    "figure_name": {"value": "polarization_curve"},
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("metals_corrosion.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    colors = list(PALETTE_CBM.values())

    # Check if we should group by a column
    group_col = cmap.get("group_by", {}).get("column")
    x_col = cmap.get("x_values", {}).get("column", "potential_mv")
    y_col = cmap.get("y_values", {}).get("column", "current_log_a_cm2")

    if group_col and group_col in rows[0]:
        # Group by the specified column
        groups = []
        for r in rows:
            val = r[group_col]
            if val not in groups:
                groups.append(val)

        for idx, group_name in enumerate(groups):
            subset = [r for r in rows if r[group_col] == group_name]
            x_vals = [float(r[x_col]) for r in subset if r[x_col]]
            y_vals = [float(r[y_col]) for r in subset if r[y_col]]
            color = colors[idx % len(colors)]
            ax.plot(x_vals, y_vals, "-", linewidth=2, label=group_name, color=color)
    else:
        # No grouping, just plot the whole thing
        x_vals = [float(r[x_col]) for r in rows if r[x_col]]
        y_vals = [float(r[y_col]) for r in rows if r[y_col]]
        ax.plot(x_vals, y_vals, "-", linewidth=2, color=colors[0], label="Data")

    xlabel = cmap.get("xlabel", {}).get("value", "Potential (mV vs SCE)")
    ylabel = cmap.get("ylabel", {}).get("value", "log |i| (A/cm²)")
    fig_name = cmap.get("figure_name", {}).get("value", "polarization_curve")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(fontsize=7)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, fig_name, args.output_dir)
    print_caption(
        "Potentiodynamic polarization curves comparing corrosion behavior in solution. "
        "Corrosion potential (Ecorr) and corrosion current density (Icorr) determine "
        "passive film stability and general corrosion rate."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
