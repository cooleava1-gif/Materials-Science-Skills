#!/usr/bin/env python3
"""Kong et al. (2024) CBM 419: Bonding strength comparison across WER dosages.

Source: Kong L, Su S, Wang Z, et al. Microscale mechanism and key factors of
waterborne epoxy resin emulsified asphalt enhancing interlayer bonding
performance and shear resistance of bridge deck pavement.
Construction and Building Materials, 2024, 419: 135570.

Reproduces: Fig. 7 — Pull-off bonding strength under dry and moisture conditions.
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
    groups = ["Dry state", "Moisture-conditioned"]
    values = [
        [0.43, 0.52, 0.68, 0.82, 0.71],
        [0.28, 0.35, 0.49, 0.61, 0.52],
    ]
    errors = [
        [0.03, 0.04, 0.03, 0.04, 0.05],
        [0.02, 0.03, 0.03, 0.04, 0.03],
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    make_grouped_bar(
        ax, labels, groups, values, PALETTE_CBM,
        error_bars=errors, ylabel="Pull-off bonding strength (MPa)",
    )
    ax.set_xlabel("WER dosage (% by evaporation residue)")
    ax.set_ylim(0, 1.0)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "kong2024_bonding_strength", args.output_dir)

    print(
        "Caption: Pull-off bonding strength of WER-EA tack coat under dry and "
        "moisture-conditioned states at different WER dosages. Error bars "
        "represent standard deviation (n=3). Optimal dosage is 15% WER by "
        "evaporation residue. Claim boundary: strength improvement does not "
        "alone confirm mechanism; FTIR/SEM evidence needed for mechanism claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
