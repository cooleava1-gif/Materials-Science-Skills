#!/usr/bin/env python3
"""Sintering curve: relative density and porosity vs temperature."""

from __future__ import annotations

import argparse
import json
import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure

COLUMN_MAP = {
    "x_values": {"column": "temperature"},
    "y1_values": {"column": "relative_density_pct"},
    "y2_values": {"column": "open_porosity_pct"},
    "xlabel": {"value": "Sintering temperature (C)"},
    "ylabel1": {"value": "Relative density (%)"},
    "ylabel2": {"value": "Open porosity (%)"},
    "figure_name": {"value": "sintering_curve"},
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("sintering_curve.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)

    x_col = cmap.get("x_values", {}).get("column", "temperature")
    y1_col = cmap.get("y1_values", {}).get("column", "relative_density_pct")
    y2_col = cmap.get("y2_values", {}).get("column", "open_porosity_pct")

    temp = column(rows, x_col, as_float=True)
    density = column(rows, y1_col, as_float=True)
    porosity = column(rows, y2_col, as_float=True)

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(5, 3.5))

    color1 = PALETTE_CBM["control"]
    ax1.plot(temp, density, "o-", color=color1, linewidth=1.5, markersize=4, label="Relative density")
    ax1.set_xlabel(cmap.get("xlabel", {}).get("value", "Sintering temperature (C)"))
    ax1.set_ylabel(cmap.get("ylabel1", {}).get("value", "Relative density (%)"), color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = PALETTE_CBM["danger"]
    ax2.plot(temp, porosity, "s--", color=color2, linewidth=1.5, markersize=4, label="Open porosity")
    ax2.set_ylabel(cmap.get("ylabel2", {}).get("value", "Open porosity (%)"), color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)

    add_panel_label(ax1, "a")
    fig.tight_layout()

    fig_name = cmap.get("figure_name", {}).get("value", "sintering_curve")
    finalize_figure(fig, fig_name, output_dir=args.output_dir)
    print_caption("Sintering behavior: relative density and open porosity as functions of temperature.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
