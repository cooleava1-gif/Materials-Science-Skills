#!/usr/bin/env python3
"""Water absorption and saturation curves for civil porous materials."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("civil_water_absorption.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    time_h = column(rows, "time_h", as_float=True)
    series = [
        column(rows, "absorption_control_pct", as_float=True),
        column(rows, "absorption_treated_pct", as_float=True),
        column(rows, "absorption_coated_pct", as_float=True),
    ]
    labels = ["Control", "Treated", "Coated"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    make_line_trend(
        ax,
        time_h,
        series,
        labels,
        PALETTE_CBM,
        xlabel="Immersion time (h)",
        ylabel="Water absorption (%)",
    )
    ax.set_xlim(0, None)
    ax.set_ylim(0, None)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "civil_water_absorption", args.output_dir)
    print_caption(
        "Water absorption kinetics for control, treated, and coated civil porous materials. "
        "Saturation trends depend on pore structure and surface treatment; field exposure should be verified separately."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
