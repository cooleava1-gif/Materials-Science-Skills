#!/usr/bin/env python3
"""Compressive stress-strain curve for aerogel insulation."""

from __future__ import annotations

import argparse
import matplotlib.pyplot as plt
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("insulation_stress_strain.csv"))
    strain = column(rows, "strain_pct", as_float=True)
    stress = column(rows, "stress_mpa", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(4.5, 3))

    ax.plot(strain, stress, "-", color=PALETTE_CBM["control"], linewidth=1.5)
    ax.axvline(x=10, color="gray", linestyle="--", linewidth=0.8, label="10% strain (typical failure criterion)")
    ax.set_xlabel("Strain (%)")
    ax.set_ylabel("Compressive stress (MPa)")
    ax.legend(fontsize=8)
    ax.set_xlim(0, max(strain))

    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "insulation_stress_strain", output_dir=args.output_dir, )
    print_caption("Compressive stress-strain curve for aerogel insulation. Vertical dashed line: 10% strain failure criterion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
