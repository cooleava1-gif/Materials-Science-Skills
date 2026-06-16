#!/usr/bin/env python3
"""Zhang et al. (2017) CBM 155: Shear strength vs WER content.

Source: Zhang Q, Xu Y, Wen Z. Construction and Building Materials,
2017, 153: 774-782.

Reproduces: Fig. 10 — Shear strength of composite plate at different WER contents.
All data points extracted from the published figure.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    # Real data extracted from Fig. 10
    wer_content = [2, 3, 4, 5, 6]
    shear_strength = [1.53, 1.72, 1.60, 1.43, 1.37]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.plot(wer_content, shear_strength, "o-", color=PALETTE_CBM["control"],
            linewidth=2.5, markersize=8, markerfacecolor=PALETTE_CBM["control"],
            markeredgecolor="white", markeredgewidth=1.5)

    # Mark optimal point
    ax.annotate("Optimal (1.72 MPa)", xy=(3, 1.72), xytext=(4.2, 1.73),
                fontsize=8, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=PALETTE_CBM["danger"], lw=1.2),
                color=PALETTE_CBM["danger"])

    ax.set_xlabel("WER content (%)")
    ax.set_ylabel("Shear strength (MPa)")
    ax.set_xlim(1.5, 6.5)
    ax.set_ylim(1.30, 1.80)
    ax.set_xticks(wer_content)
    ax.set_xticklabels([str(w) for w in wer_content])
    ax.grid(color="#E8E2D6", linewidth=0.8, alpha=0.8)
    add_panel_label(ax, "(b)")
    fig.tight_layout()
    finalize_figure(fig, "zhang2017_shear_strength", args.output_dir)

    print(
        "Caption: Shear strength of WER-SBR modified emulsified asphalt vs WER "
        "content (data from Fig. 10). Optimal WER content is 3% (1.72 MPa). "
        "Strength decreases beyond 3% due to excessive crosslinking causing brittleness. "
        "Claim boundary: shear strength is performance evidence; DSC/FTIR needed "
        "for crosslinking mechanism confirmation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
