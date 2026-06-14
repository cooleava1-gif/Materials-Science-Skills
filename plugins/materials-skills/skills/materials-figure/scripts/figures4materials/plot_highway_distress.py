#!/usr/bin/env python3
"""Pavement distress progression: rutting, cracking, and roughness vs pavement age."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_ASPHALT,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("highway_distress_progression.csv"))
    apply_pub_style()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))

    age = column(rows, "pavement_age_years", as_float=True)

    # Panel (a): Rutting
    rut = column(rows, "average_rutting_mm", as_float=True)
    rut_sd = column(rows, "rutting_sd", as_float=True)
    ax1.fill_between(age, np.array(rut) - np.array(rut_sd), np.array(rut) + np.array(rut_sd),
                     color=PALETTE_ASPHALT["modified"], alpha=0.15)
    ax1.plot(age, rut, color=PALETTE_ASPHALT["modified"], linewidth=2.2, marker="o", markersize=4)
    ax1.axhline(12, color="#B85450", linewidth=1, linestyle=":", alpha=0.7, label="Threshold (12 mm)")
    ax1.set_xlabel("Pavement age (years)")
    ax1.set_ylabel("Average rutting depth (mm)")
    ax1.legend(fontsize=7.5)
    ax1.set_title("Rutting", fontsize=10)

    # Panel (b): Cracking
    tc = column(rows, "transverse_cracking_pct", as_float=True)
    tc_sd = column(rows, "cracking_sd", as_float=True)
    lc = column(rows, "longitudinal_cracking_m_per_100m", as_float=True)
    ax2.fill_between(age, np.array(tc) - np.array(tc_sd), np.array(tc) + np.array(tc_sd),
                     color=PALETTE_ASPHALT["modified"], alpha=0.15)
    ax2.plot(age, tc, color=PALETTE_ASPHALT["modified"], linewidth=2.2, marker="o", markersize=4, label="Transverse (%)")
    ax2.plot(age, lc, color=PALETTE_ASPHALT["moisture"], linewidth=2.2, marker="s", markersize=4, label="Longitudinal (m/100m)")
    ax2.set_xlabel("Pavement age (years)")
    ax2.set_ylabel("Cracking extent")
    ax2.legend(fontsize=7.5)
    ax2.set_title("Cracking", fontsize=10)

    # Panel (c): Roughness (IRI)
    iri = column(rows, "iri_m_per_km", as_float=True)
    iri_sd = column(rows, "iri_sd", as_float=True)
    ax3.fill_between(age, np.array(iri) - np.array(iri_sd), np.array(iri) + np.array(iri_sd),
                     color=PALETTE_ASPHALT["modified"], alpha=0.15)
    ax3.plot(age, iri, color=PALETTE_ASPHALT["modified"], linewidth=2.2, marker="o", markersize=4)
    ax3.axhline(4.0, color="#B85450", linewidth=1, linestyle=":", alpha=0.7, label="Threshold (4.0 m/km)")
    ax3.set_xlabel("Pavement age (years)")
    ax3.set_ylabel("IRI (m/km)")
    ax3.legend(fontsize=7.5)
    ax3.set_title("Roughness", fontsize=10)

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "highway_distress_progression", args.output_dir)
    print_caption("Pavement distress progression over time: rutting, cracking, and international roughness index.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
