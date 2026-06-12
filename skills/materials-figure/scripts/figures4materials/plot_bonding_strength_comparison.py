#!/usr/bin/env python3
"""Bonding strength grouped bar chart for tack coat comparison."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, annotate_bars, apply_pub_style, finalize_figure, make_grouped_bar, tighten_ylimits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("bonding_strength.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    labels = column(rows, "dosage")
    values = [column(rows, "dry_mean", as_float=True), column(rows, "wet_mean", as_float=True)]
    errors = [column(rows, "dry_sd", as_float=True), column(rows, "wet_sd", as_float=True)]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    bars = make_grouped_bar(
        ax,
        labels,
        ["Dry", "Moisture-conditioned"],
        values,
        PALETTE_CBM,
        error_bars=errors,
        ylabel="Pull-off strength (MPa)",
    )
    ax.set_xlabel("Waterborne epoxy content (% by dry residue)")
    all_vals = [v for group in values for v in group]
    all_errs = [v for group in errors for v in group]
    tighten_ylimits(ax, [v + e for v, e in zip(all_vals, all_errs)], margin=0.15, ymin=0)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "bonding_strength_comparison", args.output_dir)
    print_caption(
        "Pull-off bond strength of waterborne epoxy modified emulsified asphalt tack coat under dry and moisture-conditioned states. "
        "Error bars represent SD (n = 3); mechanism claims require separate FTIR/SEM evidence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
