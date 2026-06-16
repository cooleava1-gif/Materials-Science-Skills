#!/usr/bin/env python3
"""Multi-panel functional materials characterization: dielectric, frequency sweep, P-E loop, impedance."""

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

    dielectric_rows = read_csv(data_path("functional_dielectric.csv"))
    freq_rows = read_csv(data_path("functional_freq_sweep.csv"))
    pe_rows = read_csv(data_path("functional_pe_loop.csv"))
    imp_rows = read_csv(data_path("functional_impedance.csv"))

    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    ax1, ax2, ax3, ax4 = axes.flat

    # -- Panel (a): Dielectric constant & loss vs Nb doping --
    dopant = column(dielectric_rows, "dopant_x", as_float=True)
    dopant_pct = np.asarray(dopant, dtype=float) * 100
    eps = column(dielectric_rows, "dielectric_mean", as_float=True)
    eps_sd = column(dielectric_rows, "dielectric_sd", as_float=True)
    loss = column(dielectric_rows, "loss_mean", as_float=True)
    loss_sd = column(dielectric_rows, "loss_sd", as_float=True)
    ax1.errorbar(dopant_pct, eps, yerr=eps_sd, fmt="o-", color=PALETTE_CBM["control"], linewidth=2, markersize=5, capsize=3, label="Dielectric constant")
    ax1b = ax1.twinx()
    ax1b.errorbar(dopant_pct, loss, yerr=loss_sd, fmt="s--", color=PALETTE_CBM["modified"], linewidth=2, markersize=5, capsize=3, label="Loss tangent")
    ax1.set_xlabel("Nb doping (mol%)")
    ax1.set_ylabel("Dielectric constant (εr)", color=PALETTE_CBM["control"])
    ax1.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax1b.set_ylabel("Loss tangent (tan δ)", color=PALETTE_CBM["modified"])
    ax1b.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    tighten_ylimits(ax1, [v + e for v, e in zip(eps, eps_sd)], margin=0.10, ymin=1000)
    tighten_ylimits(ax1b, [v + e for v, e in zip(loss, loss_sd)], margin=0.10, ymin=0.01)
    lines1, l1 = ax1.get_legend_handles_labels()
    lines2, l2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, l1 + l2, fontsize=7, loc="upper left")
    add_panel_label(ax1, "a")

    # -- Panel (b): Dielectric constant & loss vs frequency --
    freq = column(freq_rows, "log_freq_hz", as_float=True)
    eps_freq = column(freq_rows, "dielectric", as_float=True)
    loss_freq = column(freq_rows, "loss", as_float=True)
    ax2.plot(freq, eps_freq, "o-", color=PALETTE_CBM["control"], linewidth=2, markersize=4, label="εr")
    ax2b = ax2.twinx()
    ax2b.plot(freq, loss_freq, "s--", color=PALETTE_CBM["modified"], linewidth=2, markersize=4, label="tan δ")
    ax2.set_xlabel("log Frequency (Hz)")
    ax2.set_ylabel("Dielectric constant (εr)", color=PALETTE_CBM["control"])
    ax2.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax2b.set_ylabel("Loss tangent (tan δ)", color=PALETTE_CBM["modified"])
    ax2b.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    tighten_ylimits(ax2, eps_freq, margin=0.08, ymin=800)
    tighten_ylimits(ax2b, loss_freq, margin=0.08, ymin=0.005)
    lines1, l1 = ax2.get_legend_handles_labels()
    lines2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, l1 + l2, fontsize=7, loc="upper right")
    add_panel_label(ax2, "b")

    # -- Panel (c): P-E hysteresis loops --
    samples_pe = set(column(pe_rows, "sample_id"))
    for sample, color_key in zip(sorted(samples_pe), ["control", "modified"]):
        rows = [r for r in pe_rows if r["sample_id"] == sample]
        field = column(rows, "field_kV_per_cm", as_float=True)
        pol = column(rows, "polarization", as_float=True)
        ax3.plot(field, pol, "-", color=PALETTE_CBM[color_key], linewidth=2, label=sample)
    ax3.axhline(0, color="#888888", linewidth=0.5)
    ax3.axvline(0, color="#888888", linewidth=0.5)
    ax3.set_xlabel("Electric field (kV/cm)")
    ax3.set_ylabel("Polarization (µC/cm²)")
    ax3.legend(fontsize=7)
    add_panel_label(ax3, "c")

    # -- Panel (d): Impedance Nyquist plot --
    z_real = column(imp_rows, "z_real", as_float=True)
    z_imag = column(imp_rows, "z_imag", as_float=True)
    ax4.plot(z_real, z_imag, "o-", color=PALETTE_CBM["control"], linewidth=2, markersize=5)
    ax4.set_xlabel("Z' (Ω)")
    ax4.set_ylabel("-Z'' (Ω)")
    ax4.set_xlim(0, max(z_real) * 1.1)
    ax4.set_ylim(min(z_imag) * 1.3, 0)
    ax4.annotate("Grain boundary", xy=(z_real[3], z_imag[3]), xytext=(z_real[3] + 100, z_imag[3] + 20),
                 fontsize=7, arrowprops=dict(arrowstyle="->", color=PALETTE_CBM["danger"]),
                 color=PALETTE_CBM["danger"])
    add_panel_label(ax4, "d")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "functional_multipanel", output_dir=args.output_dir)
    print_caption(
        "Multi-panel functional materials characterization: (a) dielectric constant and loss tangent vs Nb doping in BaTiO₃, "
        "(b) frequency-dependent dielectric relaxation showing Debye-like dispersion, (c) P-E hysteresis loops comparing "
        "undoped and 2 mol% Nb-doped BaTiO₃, (d) impedance Nyquist plot with grain and grain-boundary arc assignment."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
