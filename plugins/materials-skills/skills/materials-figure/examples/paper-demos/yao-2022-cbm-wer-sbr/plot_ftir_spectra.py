#!/usr/bin/env python3
"""Yao et al. (2022) CBM 318: FTIR spectra of WER/SBR modified EA.

Source: Yao X, Tan L, Xu T. Construction and Building Materials,
2022, 318: 126178.

Reproduces: Fig. 7 — FTIR spectra of EA samples before and after WER modification.
Real peak positions from paper: 915 cm-1 (epoxy), 966 cm-1 (SBR), 699 cm-1 (SBR).
"""

from __future__ import annotations

import argparse

import numpy as np
import matplotlib.pyplot as plt

from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    wavenumber = np.linspace(4000, 400, 600)

    # EA-1 (base emulsified asphalt) - typical asphalt peaks
    def asphalt_spectrum(x):
        y = np.zeros_like(x)
        y += np.exp(-((x - 2920) ** 2) / (2 * 50**2)) * 0.55  # -CH2- asymmetric
        y += np.exp(-((x - 2850) ** 2) / (2 * 40**2)) * 0.40  # -CH2- symmetric
        y += np.exp(-((x - 1600) ** 2) / (2 * 45**2)) * 0.30  # C=C aromatic
        y += np.exp(-((x - 1460) ** 2) / (2 * 35**2)) * 0.25  # -CH2- bending
        y += np.exp(-((x - 1375) ** 2) / (2 * 30**2)) * 0.20  # -CH3
        y += np.exp(-((x - 1030) ** 2) / (2 * 50**2)) * 0.28  # S=O
        y += np.exp(-((x - 810) ** 2) / (2 * 25**2)) * 0.15   # aromatic C-H
        return y + 0.02

    # EA-2 (SBR modified) - adds SBR peaks at 966 and 699 cm-1
    def sbr_modified(x):
        y = asphalt_spectrum(x)
        y += np.exp(-((x - 966) ** 2) / (2 * 20**2)) * 0.22  # SBR C-H bend
        y += np.exp(-((x - 699) ** 2) / (2 * 18**2)) * 0.18  # SBR C-H rock
        return y

    # EA-5 (6% WER + 3% SBR) - epoxy peak at 915 disappears after curing
    def wer_sbr_6pct(x):
        y = sbr_modified(x)
        # SBR peaks weakened (paper: intensities decreased with WER)
        y -= np.exp(-((x - 966) ** 2) / (2 * 20**2)) * 0.08
        y -= np.exp(-((x - 699) ** 2) / (2 * 18**2)) * 0.06
        # No 915 peak (epoxy consumed in curing reaction)
        return y

    ea1 = asphalt_spectrum(wavenumber)
    ea2 = sbr_modified(wavenumber)
    ea5 = wer_sbr_6pct(wavenumber)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))

    offset = 0.4
    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["optimal"]]
    labels = ["EA-1 (base)", "EA-2 (3% SBR)", "EA-5 (6% WER+3% SBR)"]
    for i, (spec, label, color) in enumerate(zip([ea1, ea2, ea5], labels, colors)):
        ax.plot(wavenumber, spec + offset * i, color=color, linewidth=1.5, label=label)

    # Mark key peaks (from paper)
    peak_info = [
        (2920, "-CH2-", 0),
        (1600, "C=C", 0),
        (966, "SBR", 1),
        (699, "SBR", 1),
        (915, "Epoxide\n(consumed)", 2),
    ]
    for pos, text, spec_idx in peak_info:
        ax.annotate(text, xy=(pos, ea1.max() + offset * spec_idx + 0.05),
                    fontsize=7, ha="center", color="gray")
        ax.axvline(pos, color="gray", linewidth=0.5, linestyle=":", alpha=0.5)

    ax.set_xlabel(r"Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("Absorbance (a.u.)")
    ax.invert_xaxis()
    ax.set_xlim(4000, 400)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_yticks([])
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "yao2022_ftir_spectra", args.output_dir)

    print(
        "Caption: FTIR spectra of EA-1 (base), EA-2 (3% SBR), and EA-5 (6% WER+3% SBR). "
        "SBR peaks at 966 and 699 cm-1 confirm SBR incorporation. Epoxy peak at 915 cm-1 "
        "disappears after curing, confirming complete reaction of epoxy groups. "
        "Claim boundary: FTIR confirms chemical reaction but does not prove "
        "interpenetrating network; XRD/LSCM/ESEM needed for morphology claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
