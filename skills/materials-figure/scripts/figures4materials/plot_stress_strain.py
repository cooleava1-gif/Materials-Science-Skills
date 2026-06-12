#!/usr/bin/env python3
"""Generic tensile stress-strain curves for materials comparison."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def _find_yield(strain: list[float], stress: list[float], offset: float = 0.002):
    for i in range(1, len(strain) - 1):
        if stress[i] > 0 and i > 0:
            slope = (stress[i] - stress[i - 1]) / (strain[i] - strain[i - 1] + 1e-12)
            secant = stress[i] / (strain[i] + 1e-12)
            if slope < 0.5 * secant:
                return strain[i], stress[i]
    return None, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("stress_strain.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    strain = column(rows, "strain", as_float=True)
    sample_cols = [k for k in rows[0] if k != "strain"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    colors = list(PALETTE_CBM.values())

    for idx, col_name in enumerate(sample_cols):
        stress = column(rows, col_name, as_float=True)
        color = colors[idx % len(colors)]
        ax.plot(strain, stress, linewidth=2.0, label=col_name, color=color)
        y_s, s_s = _find_yield(strain, stress)
        if y_s is not None:
            ax.annotate(
                "Yield", xy=(y_s, s_s), fontsize=7, color=color,
                textcoords="offset points", xytext=(10, -10),
                arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
            )
        s_max = max(stress)
        idx_max = stress.index(s_max)
        if s_max > 0:
            ax.annotate(
                "UTS", xy=(strain[idx_max], s_max), fontsize=7, color=color,
                textcoords="offset points", xytext=(10, 5),
                arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
            )

    ax.set_xlabel("Strain")
    ax.set_ylabel("Stress (MPa)")
    ax.legend()
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "stress_strain_comparison", args.output_dir)
    print_caption(
        "Tensile stress-strain curves comparing multiple samples. "
        "Yield point, ultimate tensile strength (UTS), and failure strain indicate "
        "ductility and load-bearing capacity; annotations are heuristic and should "
        "be verified against raw data."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
