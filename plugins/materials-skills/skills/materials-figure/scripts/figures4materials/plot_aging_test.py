#!/usr/bin/env python3
"""Aging test durability for WER-EA systems."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("aging_test.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    aging_time = column(rows, "aging_time", as_float=True)
    bonding_series = [
        column(rows, "bonding_retention_pure", as_float=True),
        column(rows, "bonding_retention_5%_wer", as_float=True),
        column(rows, "bonding_retention_10%_wer", as_float=True),
        column(rows, "bonding_retention_15%_wer", as_float=True),
    ]
    elongation_series = [
        column(rows, "elongation_retention_pure", as_float=True),
        column(rows, "elongation_retention_5%_wer", as_float=True),
        column(rows, "elongation_retention_10%_wer", as_float=True),
        column(rows, "elongation_retention_15%_wer", as_float=True),
    ]
    labels = ["Pure asphalt", "5% WER", "10% WER", "15% WER"]

    apply_pub_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    make_line_trend(
        ax1,
        aging_time,
        bonding_series,
        labels,
        PALETTE_CBM,
        xlabel="Aging time (days)",
        ylabel="Bonding retention (%)",
    )
    ax1.set_xlim(0, 14)
    ax1.set_ylim(50, 105)
    ax1.set_title("Bonding strength retention", fontsize=10)
    add_panel_label(ax1, "(a)")

    make_line_trend(
        ax2,
        aging_time,
        elongation_series,
        labels,
        PALETTE_CBM,
        xlabel="Aging time (days)",
        ylabel="Elongation retention (%)",
    )
    ax2.set_xlim(0, 14)
    ax2.set_ylim(30, 105)
    ax2.set_title("Elongation retention", fontsize=10)
    add_panel_label(ax2, "(b)")

    fig.tight_layout()
    finalize_figure(fig, "aging_durability", args.output_dir)
    print_caption(
        "Aging durability for pure asphalt and WER-EA systems showing bonding and elongation retention. "
        "Aging resistance requires matching FTIR evidence for chemical stability; lab aging may not represent field conditions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())