#!/usr/bin/env python3
"""Mechanical property radar chart for multi-index comparison."""

from __future__ import annotations

import argparse
import json
import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_radar

COLUMN_MAP = {
    "categories": {"column": "property"},
    "series": [
        {"key": "Control", "column": "control_index"},
        {"key": "Modified", "column": "modified_index"},
    ],
    "figure_name": {"value": "mechanical_property_radar"},
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("mechanical_properties.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)

    cat_col = cmap.get("categories", {}).get("column", "property")
    categories = column(rows, cat_col)

    series_specs = cmap.get("series", [])
    series_dict = {}
    for spec in series_specs:
        key = spec.get("key", "")
        col = spec.get("column", "")
        if key and col in rows[0]:
            series_dict[key] = column(rows, col, as_float=True)

    if not series_dict:
        # Fallback if series is empty or not in CSV
        control_col = next((c for c in ("control_index", "control", "pure") if c in rows[0]), list(rows[0].keys())[1])
        modified_col = next((c for c in ("modified_index", "modified", "wer") if c in rows[0]), list(rows[0].keys())[2])
        series_dict["Control"] = column(rows, control_col, as_float=True)
        series_dict["Modified"] = column(rows, modified_col, as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.2, 4.2), subplot_kw={"projection": "polar"})

    make_radar(
        ax,
        categories,
        series_dict,
        PALETTE_CBM,
        max_val=1.0,
    )
    add_panel_label(ax, "(e)", loc="top-left")
    fig.tight_layout()

    fig_name = cmap.get("figure_name", {}).get("value", "mechanical_property_radar")
    finalize_figure(fig, fig_name, args.output_dir)
    print_caption(
        "Normalized multi-index mechanical profile of control and modified systems. "
        "Radar normalization should be accompanied by raw values and uncertainty in the manuscript or supplement."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
