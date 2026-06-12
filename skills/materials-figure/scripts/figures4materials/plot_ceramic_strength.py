#!/usr/bin/env python3
"""Flexural strength comparison across ceramic compositions."""

from __future__ import annotations

import argparse
import matplotlib.pyplot as plt
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_grouped_bar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("ceramic_composition_strength.csv"))
    comp = column(rows, "composition")
    strength = column(rows, "strength_mpa", as_float=True)
    sd = column(rows, "sd", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(4.5, 3.5))

    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["optimal"], PALETTE_CBM["danger"], PALETTE_CBM["mechanism"]]
    bars = ax.bar(comp, strength, color=colors, width=0.6, edgecolor="black", linewidth=0.5)

    for i, (val, err) in enumerate(zip(strength, sd)):
        ax.errorbar(i, val, yerr=err, fmt="none", color="black", capsize=3, capthick=1)

    ax.set_ylabel("Flexural strength (MPa)")
    ax.set_xlabel("Composition")
    ax.set_ylim(0, max(strength) * 1.3)
    fig.autofmt_xdate(rotation=30, ha="right")

    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "ceramic_strength_comparison", output_dir=args.output_dir, )
    print_caption("Flexural strength of different ceramic compositions (mean +/- SD).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
