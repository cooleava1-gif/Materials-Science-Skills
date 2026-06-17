#!/usr/bin/env python3
"""Grouped bar chart for bonding strength comparison (COLUMN_MAP pattern).

Generic version: works with any material's data. The COLUMN_MAP at the top
declares which CSV columns provide each semantic role. Other materials can
reuse this script by providing a different data CSV (with their own column
names) and overriding COLUMN_MAP.

Usage:
    python plot_bonding_strength_comparison.py --data path/to/data.csv
    python plot_bonding_strength_comparison.py --data path/to/data.csv --column-map '{"series": ...}'
"""

from __future__ import annotations

import argparse
import json

import matplotlib.pyplot as plt

from _script_helpers import data_path, load_mapped_data, print_caption
from materials_plot_lib import PALETTE_CBM, add_panel_label, annotate_bars, apply_pub_style, finalize_figure, make_grouped_bar, tighten_ylimits

# ── Column map ────────────────────────────────────────────────────────────
# Override via --column-map or by creating a thin wrapper script that changes
# this dict.  Keys follow the COLUMN_MAP convention (see _script_helpers.py).

COLUMN_MAP = {
    "x_labels": {"column": "dosage"},
    "series": [
        {"key": "Dry",               "column": "dry_mean", "error": "dry_sd"},
        {"key": "Moisture-conditioned", "column": "wet_mean", "error": "wet_sd"},
    ],
    "xlabel":   {"value": "Waterborne epoxy content (% by dry residue)"},
    "ylabel":   {"value": "Pull-off strength (MPa)"},
    "panel":    {"value": "a"},
    "figure_name": {"value": "bonding_strength_comparison"},
}


def build_figure(data, column_map: dict) -> None:
    """Build the figure using mapped data."""
    series = column_map.get("series") or data.get("series", [])
    if not series:
        # The data already has 'series' populated by load_mapped_data
        pass

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 3.8))

    groups = [s["key"] for s in data.get("series", [])]
    values = [s["values"] for s in data.get("series", [])]
    errors = [s.get("errors") for s in data.get("series", [])]
    has_errors = any(e is not None for e in errors)

    bars = make_grouped_bar(
        ax,
        data.get("x_labels", []),
        groups,
        values,
        PALETTE_CBM,
        error_bars=errors if has_errors else None,
        ylabel=column_map.get("ylabel", ""),
    )

    if data.get("xlabel"):
        ax.set_xlabel(data["xlabel"])

    all_vals = [v for group in values for v in group]
    if has_errors:
        all_errs = [e for group in errors for e in (group or [0] * len(all_vals))]
        tighten_ylimits(ax, [v + e for v, e in zip(all_vals, all_errs)], margin=0.15, ymin=0)
    else:
        tighten_ylimits(ax, all_vals, margin=0.15, ymin=0)

    panel = column_map.get("panel", {}).get("value", "a") if isinstance(column_map.get("panel"), dict) else "a"
    add_panel_label(ax, panel)

    fig.tight_layout()
    finalize_figure(fig, column_map.get("figure_name", {}).get("value", "figure"), data.get("_output_dir", "."))

    caption = column_map.get("caption", {}).get("value", "")
    if caption:
        print_caption(caption)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("bonding_strength.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    data = load_mapped_data(args.data, cmap)
    data["_output_dir"] = args.output_dir

    build_figure(data, cmap)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
