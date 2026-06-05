#!/usr/bin/env python3
"""Mechanical property radar chart for multi-index comparison."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_radar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("mechanical_properties.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    categories = column(rows, "property")
    control = column(rows, "control_index", as_float=True)
    modified = column(rows, "modified_index", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.2, 4.2), subplot_kw={"projection": "polar"})
    make_radar(
        ax,
        categories,
        {"Control": control, "Modified": modified},
        PALETTE_CBM,
        max_val=1.0,
    )
    add_panel_label(ax, "(e)", loc="top-left")
    fig.tight_layout()
    finalize_figure(fig, "mechanical_property_radar", args.output_dir)
    print_caption(
        "Normalized multi-index mechanical profile of control and modified emulsified asphalt tack coat. "
        "Radar normalization should be accompanied by raw values and uncertainty in the manuscript or supplement."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
