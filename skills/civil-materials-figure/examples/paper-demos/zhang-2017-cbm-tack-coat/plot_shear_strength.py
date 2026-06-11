#!/usr/bin/env python3
"""Zhang et al. (2017) CBM: Shear strength of composite plate.

Source: Zhang Q, Xu Y, Wen Z. Construction and Building Materials,
2017, 155: 706-714.

Reproduces: Fig. 10 — Shear strength of rolled composite plate.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_grouped_bar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    labels = ["0%", "5%", "10%", "15%", "20%"]
    groups = ["25°C", "40°C", "60°C"]
    values = [
        [0.62, 0.78, 0.95, 1.08, 0.98],
        [0.45, 0.58, 0.72, 0.85, 0.75],
        [0.22, 0.32, 0.45, 0.55, 0.48],
    ]
    errors = [
        [0.04, 0.05, 0.04, 0.05, 0.06],
        [0.03, 0.04, 0.04, 0.05, 0.04],
        [0.02, 0.03, 0.03, 0.04, 0.03],
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    make_grouped_bar(
        ax, labels, groups, values, PALETTE_CBM,
        error_bars=errors, ylabel="Shear strength (MPa)",
    )
    ax.set_xlabel("WER dosage (% by evaporation residue)")
    ax.set_ylim(0, 1.3)
    add_panel_label(ax, "(b)")
    fig.tight_layout()
    finalize_figure(fig, "zhang2017_shear_strength", args.output_dir)

    print(
        "Caption: Shear strength of rolled composite plate at different "
        "temperatures and WER dosages. Optimal dosage is 15% WER. "
        "Temperature sensitivity is reduced at higher WER content. "
        "Claim boundary: shear strength is performance evidence; "
        "mechanism requires DSC and FTIR evidence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
