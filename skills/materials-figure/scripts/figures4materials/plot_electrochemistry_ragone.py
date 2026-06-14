#!/usr/bin/env python3
"""Ragone plot: energy density vs power density for batteries and supercapacitors."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CCC,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("electrochemistry_ragone.csv"))
    apply_pub_style()

    fig, ax = plt.subplots(figsize=(7, 5))

    samples = sorted(set(r["sample"] for r in rows))
    markers = {"LIB-Modified": "o", "LIB-Control": "s", "SC-Modified": "^", "SC-Control": "v"}
    colors = {
        "LIB-Modified": PALETTE_CCC["modified"],
        "LIB-Control": PALETTE_CCC["control"],
        "SC-Modified": PALETTE_CCC["optimal"],
        "SC-Control": PALETTE_CCC["neutral"],
    }

    for sample in samples:
        subset = [r for r in rows if r["sample"] == sample]
        e = column(subset, "energy_density_wh_kg", as_float=True)
        p = column(subset, "power_density_w_kg", as_float=True)
        ax.plot(p, e, marker=markers.get(sample, "o"), markersize=7, linewidth=2.0,
                color=colors.get(sample, "#333333"), label=sample)

    ax.set_xlabel("Power density (W/kg)")
    ax.set_ylabel("Energy density (Wh/kg)")
    ax.set_xscale("log")
    ax.legend(fontsize=8)

    saved = finalize_figure(fig, "electrochemistry_ragone", args.output_dir)
    print_caption("Ragone plot comparing energy and power density of battery and supercapacitor devices.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
