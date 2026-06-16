#!/usr/bin/env python3
"""Multi-panel nanomaterial characterization: size distribution, loading effect, XRD, UV-Vis."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
    add_panel_label,
    apply_pub_style,
    finalize_figure,
    tighten_ylimits,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    loading_rows = read_csv(data_path("nano_loading.csv"))
    size_rows = read_csv(data_path("nano_size_dist.csv"))
    xrd_rows = read_csv(data_path("nano_xrd.csv"))
    uvis_rows = read_csv(data_path("nano_uvis.csv"))

    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    ax1, ax2, ax3, ax4 = axes.flat

    # -- Panel (a): Size distribution histogram --
    samples = set(column(size_rows, "sample_id"))
    for sample, color_key in zip(sorted(samples), ["control", "modified"]):
        rows = [r for r in size_rows if r["sample_id"] == sample]
        sizes = column(rows, "size_nm", as_float=True)
        counts = column(rows, "count", as_float=True)
        ax1.plot(sizes, counts, "o-", color=PALETTE_CBM[color_key], linewidth=2, markersize=4, label=sample)
        ax1.fill_between(sizes, counts, alpha=0.15, color=PALETTE_CBM[color_key])
    ax1.set_xlabel("Particle size (nm)")
    ax1.set_ylabel("Frequency")
    ax1.legend(fontsize=7)
    add_panel_label(ax1, "a")

    # -- Panel (b): Tensile strength vs nano-SiO2 loading --
    loading = column(loading_rows, "loading_wt_pct", as_float=True)
    tensile = column(loading_rows, "tensile_mean", as_float=True)
    tensile_sd = column(loading_rows, "tensile_sd", as_float=True)
    modulus = column(loading_rows, "modulus_mean", as_float=True)
    modulus_sd = column(loading_rows, "modulus_sd", as_float=True)
    ax2.errorbar(loading, tensile, yerr=tensile_sd, fmt="o-", color=PALETTE_CBM["control"], linewidth=2, markersize=5, capsize=3, label="Tensile strength")
    ax2b = ax2.twinx()
    ax2b.errorbar(loading, modulus, yerr=modulus_sd, fmt="s--", color=PALETTE_CBM["modified"], linewidth=2, markersize=5, capsize=3, label="Tensile modulus")
    ax2.set_xlabel("Nano-SiO₂ loading (wt%)")
    ax2.set_ylabel("Tensile strength (MPa)", color=PALETTE_CBM["control"])
    ax2.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax2b.set_ylabel("Tensile modulus (GPa)", color=PALETTE_CBM["modified"])
    ax2b.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    tighten_ylimits(ax2, [v + e for v, e in zip(tensile, tensile_sd)], margin=0.10, ymin=50)
    tighten_ylimits(ax2b, [v + e for v, e in zip(modulus, modulus_sd)], margin=0.10, ymin=2.0)
    ax2.axvspan(1.0, 2.0, color=PALETTE_CBM["accent"], alpha=0.10, label="Optimum range")
    lines1, l1 = ax2.get_legend_handles_labels()
    lines2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, l1 + l2, fontsize=7, loc="lower right")
    add_panel_label(ax2, "b")

    # -- Panel (c): XRD pattern --
    xrd_angle = column(xrd_rows, "angle_deg", as_float=True)
    xrd_intensity = column(xrd_rows, "intensity_a_u", as_float=True)
    ax3.plot(xrd_angle, xrd_intensity, "-", color=PALETTE_CBM["control"], linewidth=1.8)
    ax3.fill_between(xrd_angle, xrd_intensity, alpha=0.15, color=PALETTE_CBM["control"])
    ax3.set_xlabel("2θ (degree)")
    ax3.set_ylabel("Intensity (a.u.)")
    peaks = [38, 44, 64, 77]
    peak_labels = ["(111)", "(200)", "(220)", "(311)"]
    for p, l in zip(peaks, peak_labels):
        ax3.axvline(p, color=PALETTE_CBM["danger"], linewidth=0.8, linestyle="--", alpha=0.6)
        ax3.text(p + 0.5, max(xrd_intensity) * 0.9, l, fontsize=7, color=PALETTE_CBM["danger"])
    add_panel_label(ax3, "c")

    # -- Panel (d): UV-Vis absorption spectrum --
    wavelength = column(uvis_rows, "wavelength_nm", as_float=True)
    absorbance = column(uvis_rows, "absorbance", as_float=True)
    ax4.plot(wavelength, absorbance, "-", color=PALETTE_CBM["control"], linewidth=2)
    ax4.fill_between(wavelength, absorbance, alpha=0.15, color=PALETTE_CBM["control"])
    peak_idx = int(np.argmax(absorbance))
    ax4.annotate(f"λmax = {wavelength[peak_idx]:.0f} nm",
                 xy=(wavelength[peak_idx], absorbance[peak_idx]),
                 xytext=(wavelength[peak_idx] + 30, absorbance[peak_idx] * 0.9),
                 fontsize=8, arrowprops=dict(arrowstyle="->", color=PALETTE_CBM["danger"]),
                 color=PALETTE_CBM["danger"])
    ax4.set_xlabel("Wavelength (nm)")
    ax4.set_ylabel("Absorbance (a.u.)")
    tighten_ylimits(ax4, absorbance, margin=0.08, ymin=0)
    add_panel_label(ax4, "d")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "nano_multipanel", output_dir=args.output_dir)
    print_caption(
        "Multi-panel nanomaterial characterization: (a) particle size distribution comparing citrate- and PEG-capped AgNPs, "
        "(b) tensile strength and modulus of nano-SiO₂/epoxy composites vs loading with optimum range, "
        "(c) XRD pattern of AgNPs with FCC peak assignments, (d) UV-Vis absorption spectrum showing plasmon resonance peak."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
