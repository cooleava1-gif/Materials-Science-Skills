#!/usr/bin/env python3
"""Dosage window: normalized performance metrics vs. WER dosage."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("dosage_window.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    dosage = column(rows, "dosage")
    x = np.arange(len(dosage))
    normalized_series = [
        column(rows, "normalized_strength", as_float=True),
        column(rows, "normalized_viscosity", as_float=True),
        column(rows, "normalized_stability", as_float=True),
        column(rows, "normalized_workability", as_float=True),
    ]
    labels = ["Bonding strength", "Viscosity (inverse)", "Emulsion stability", "Workability"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    make_line_trend(
        ax,
        x,
        normalized_series,
        labels,
        PALETTE_CBM,
        xlabel="WER dosage (% by dry residue)",
        ylabel="Normalized performance (0–1)",
    )

    # Highlight optimal dosage window
    optimal_start, optimal_end = 2, 3  # 10% to 15%
    ax.axvspan(optimal_start - 0.1, optimal_end + 0.1, alpha=0.15, color=PALETTE_CBM["optimal"], label="Optimal window")
    ax.axvline(x=optimal_start, color=PALETTE_CBM["optimal"], linestyle=":", linewidth=1.2)
    ax.axvline(x=optimal_end, color=PALETTE_CBM["optimal"], linestyle=":", linewidth=1.2)

    ax.set_xticks(x)
    ax.set_xticklabels(dosage)
    ax.set_xlim(-0.2, len(dosage) - 0.8)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(loc="upper left", fontsize=8)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "dosage_window_normalized", args.output_dir)
    print_caption(
        "Normalized performance metrics versus WER dosage showing optimal window at 10–15%. "
        "Optimal dosage is conditional on construction workability and emulsion stability; "
        "mechanism claims require matching FTIR/SEM evidence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())