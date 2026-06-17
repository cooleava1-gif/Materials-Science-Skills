#!/usr/bin/env python3
"""Generic tensile stress-strain curves for materials comparison."""

from __future__ import annotations

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure

COLUMN_MAP = {
    "x_values": {"column": "strain_pct"},
    "y_values": {"column": "stress_mpa"},
    "group_by": {"column": "condition"},
    "xlabel": {"value": "Strain (%)"},
    "ylabel": {"value": "Stress (MPa)"},
    "figure_name": {"value": "stress_strain_comparison"},
}

def _find_yield(strain: list[float], stress: list[float], offset: float = 0.002):
    for i in range(1, len(strain) - 1):
        if stress[i] > 0 and i > 0:
            slope = (stress[i] - stress[i - 1]) / (strain[i] - strain[i - 1] + 1e-12)
            secant = stress[i] / (strain[i] + 1e-12)
            if slope < 0.5 * secant:
                return strain[i], stress[i]
    return None, None

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("stress_strain.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)

    # Check if there is a group_by column (long format)
    group_col = cmap.get("group_by", {}).get("column")
    x_col = cmap.get("x_values", {}).get("column", "strain_pct")
    y_col = cmap.get("y_values", {}).get("column", "stress_mpa")

    # If the group_col is not in the CSV, fallback to checking strain vs strain_pct
    if not group_col or group_col not in rows[0]:
        # Wide format
        # Find which column contains strain/strain_pct
        if x_col in rows[0]:
            strain_col = x_col
        elif "strain" in rows[0]:
            strain_col = "strain"
        elif "strain_pct" in rows[0]:
            strain_col = "strain_pct"
        else:
            raise KeyError(f"No strain/x_values column found in {args.data}")

        strain = column(rows, strain_col, as_float=True)
        sample_cols = [k for k in rows[0] if k != strain_col]

        apply_pub_style()
        fig, ax = plt.subplots(figsize=(6.2, 4.2))
        colors = list(PALETTE_CBM.values())

        for idx, col_name in enumerate(sample_cols):
            stress = column(rows, col_name, as_float=True)
            color = colors[idx % len(colors)]
            ax.plot(strain, stress, linewidth=2.0, label=col_name, color=color)
            y_s, s_s = _find_yield(strain, stress)
            if y_s is not None:
                ax.annotate(
                    "Yield", xy=(y_s, s_s), fontsize=7, color=color,
                    textcoords="offset points", xytext=(10, -10),
                    arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
                )
            s_max = max(stress)
            idx_max = stress.index(s_max)
            if s_max > 0:
                ax.annotate(
                    "UTS", xy=(strain[idx_max], s_max), fontsize=7, color=color,
                    textcoords="offset points", xytext=(10, 5),
                    arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
                )
    else:
        # Long format (group by condition)
        # Find unique groups in order of appearance
        groups = []
        for r in rows:
            val = r[group_col]
            if val not in groups:
                groups.append(val)

        apply_pub_style()
        fig, ax = plt.subplots(figsize=(6.2, 4.2))
        colors = list(PALETTE_CBM.values())

        for idx, group_name in enumerate(groups):
            subset = [r for r in rows if r[group_col] == group_name]
            strain = [float(r[x_col]) for r in subset if r[x_col]]
            stress = [float(r[y_col]) for r in subset if r[y_col]]
            color = colors[idx % len(colors)]
            ax.plot(strain, stress, linewidth=2.0, label=group_name, color=color)
            y_s, s_s = _find_yield(strain, stress)
            if y_s is not None:
                ax.annotate(
                    "Yield", xy=(y_s, s_s), fontsize=7, color=color,
                    textcoords="offset points", xytext=(10, -10),
                    arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
                )
            s_max = max(stress)
            idx_max = stress.index(s_max)
            if s_max > 0:
                ax.annotate(
                    "UTS", xy=(strain[idx_max], s_max), fontsize=7, color=color,
                    textcoords="offset points", xytext=(10, 5),
                    arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
                )

    xlabel = cmap.get("xlabel", {}).get("value", "Strain")
    ylabel = cmap.get("ylabel", {}).get("value", "Stress (MPa)")
    fig_name = cmap.get("figure_name", {}).get("value", "stress_strain_comparison")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, fig_name, args.output_dir)
    print_caption(
        "Tensile stress-strain curves comparing multiple samples. "
        "Yield point, ultimate tensile strength (UTS), and failure strain indicate "
        "ductility and load-bearing capacity; annotations are heuristic and should "
        "be verified against raw data."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
