#!/usr/bin/env python3
"""Bridge deterioration: condition state distribution and load rating vs age."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CEMENT,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("bridge_deterioration.csv"))
    apply_pub_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    age = column(rows, "bridge_age_years", as_float=True)
    cs1 = column(rows, "condition_state_1_pct", as_float=True)
    cs2 = column(rows, "condition_state_2_pct", as_float=True)
    cs3 = column(rows, "condition_state_3_pct", as_float=True)
    cs4 = column(rows, "condition_state_4_pct", as_float=True)
    rf = column(rows, "rating_factor", as_float=True)

    # Panel (a): Condition state stacked area
    ax1.stackplot(age, cs1, cs2, cs3, cs4,
                  colors=["#4F7C6A", "#C47B45", "#B85450", "#2D2D2D"],
                  labels=["CS1 - Good", "CS2 - Fair", "CS3 - Poor", "CS4 - Critical"])
    ax1.set_xlabel("Bridge age (years)")
    ax1.set_ylabel("Condition state distribution (%)")
    ax1.legend(fontsize=7, loc="center right")
    ax1.set_ylim(0, 100)
    ax1.set_title("Condition State Deterioration", fontsize=10)

    # Panel (b): Rating factor
    ax2.plot(age, rf, color=PALETTE_CEMENT["modified"], linewidth=2.2, marker="o", markersize=5)
    ax2.axhline(1.0, color="#B85450", linewidth=1.5, linestyle="--", label="Posting threshold (RF = 1.0)")
    ax2.fill_between(age, 0, rf, where=[r < 1.0 for r in rf], color="#B85450", alpha=0.15)
    ax2.set_xlabel("Bridge age (years)")
    ax2.set_ylabel("Load rating factor")
    ax2.set_ylim(0, 2.2)
    ax2.legend(fontsize=8)
    ax2.set_title("Load Rating Deterioration", fontsize=10)

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "bridge_deterioration", args.output_dir)
    print_caption("Bridge deterioration modeling: condition state distribution and load rating factor vs bridge age.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
