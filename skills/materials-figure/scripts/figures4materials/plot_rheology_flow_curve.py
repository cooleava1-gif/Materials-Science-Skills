#!/usr/bin/env python3
"""Rheology flow curve for emulsified asphalt or cement paste."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_flow_curve


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("rheology_flow.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    shear_rate = column(rows, "shear_rate_s1", as_float=True)
    viscosity = [column(rows, "viscosity_control", as_float=True), column(rows, "viscosity_modified", as_float=True)]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    make_flow_curve(ax, shear_rate, viscosity, ["Control", "Modified"], PALETTE_CBM)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "rheology_flow_curve", args.output_dir)
    print_caption(
        "Viscosity vs shear rate for control and modified formulations. "
        "Flow curves support workability and constructability assessment but do not independently prove field rheology."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
