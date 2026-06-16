#!/usr/bin/env python3
"""Isothermal calorimetry hydration heat curves."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
    add_panel_label,
    apply_pub_style,
    finalize_figure,
    make_heat_flow_curve,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("hydration_heat.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    time_h = column(rows, "time_h", as_float=True)
    heat_flow = [
        column(rows, "heat_flow_mw_g_control", as_float=True),
        column(rows, "heat_flow_mw_g_modified", as_float=True),
    ]
    cum_heat = [
        column(rows, "cum_heat_j_g_control", as_float=True),
        column(rows, "cum_heat_j_g_modified", as_float=True),
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    make_heat_flow_curve(
        ax, time_h, heat_flow, ["Control", "Modified"], PALETTE_CBM,
        cumulative_heat=cum_heat, cum_labels=["Control cum.", "Modified cum."],
    )
    add_panel_label(ax, "(f)")
    fig.tight_layout()
    finalize_figure(fig, "hydration_heat", args.output_dir)
    print_caption(
        "Isothermal calorimetry: heat flow and cumulative heat for control and modified cementitious systems. "
        "Hydration kinetics depend on w/b ratio, temperature, and mixing protocol."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
