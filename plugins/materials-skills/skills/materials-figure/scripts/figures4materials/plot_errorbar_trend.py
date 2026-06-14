#!/usr/bin/env python3
"""Errorbar trend for aging or durability time series."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_ASPHALT, add_panel_label, apply_pub_style, finalize_figure, make_errorbar_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("errorbar_trend.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    days = column(rows, "aging_day", as_float=True)
    strength = column(rows, "strength_mean_mpa", as_float=True)
    sd = column(rows, "strength_sd_mpa", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    make_errorbar_trend(
        ax,
        days,
        strength,
        sd,
        PALETTE_ASPHALT,
        xlabel="Aging time (d)",
        ylabel="Bond strength (MPa)",
        label="15% WER",
    )
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "errorbar_trend", args.output_dir)
    print_caption(
        "Errorbar trend showing bond-strength loss during aging. Error bars represent SD and do not prove field service life without exposure validation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
