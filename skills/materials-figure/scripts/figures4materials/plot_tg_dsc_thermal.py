#!/usr/bin/env python3
"""TG-DSC combined thermal analysis plot."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_tg_dsc_overlay


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("tg_dsc_thermal.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    temp = column(rows, "temp_c", as_float=True)
    tga = column(rows, "tga_mass_pct", as_float=True)
    dsc = column(rows, "dsc_heatflow_mw_mg", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    make_tg_dsc_overlay(ax, temp, tga, dsc, palette=PALETTE_CBM)
    add_panel_label(ax, "(e)")
    fig.tight_layout()
    finalize_figure(fig, "tg_dsc_thermal", args.output_dir)
    print_caption(
        "TG-DSC thermal analysis showing mass loss and heat flow vs temperature. "
        "Mass-loss events and thermal transitions should be assigned with supporting literature or evolved gas analysis."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
