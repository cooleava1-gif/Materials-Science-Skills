#!/usr/bin/env python3
"""Freeze-thaw cycle durability for WER-EA systems."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("freeze_thaw_cycle.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    cycles = column(rows, "cycle", as_float=True)
    strength_series = [
        column(rows, "strength_retention_pure", as_float=True),
        column(rows, "strength_retention_5%_wer", as_float=True),
        column(rows, "strength_retention_10%_wer", as_float=True),
        column(rows, "strength_retention_15%_wer", as_float=True),
    ]
    labels = ["Pure asphalt", "5% WER", "10% WER", "15% WER"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    make_line_trend(
        ax,
        cycles,
        strength_series,
        labels,
        PALETTE_CBM,
        xlabel="Freeze-thaw cycles",
        ylabel="Strength retention (%)",
    )
    ax.set_xlim(0, 30)
    ax.set_ylim(50, 105)
    ax.axhline(y=80, color=PALETTE_CBM["danger"], linestyle=":", linewidth=1.2, label="80% threshold")
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "freeze_thaw_durability", args.output_dir)
    print_caption(
        "Freeze-thaw durability for pure asphalt and WER-EA systems showing strength retention. "
        "Durability improvement requires matching microstructure evidence; accelerated testing may not represent field conditions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())