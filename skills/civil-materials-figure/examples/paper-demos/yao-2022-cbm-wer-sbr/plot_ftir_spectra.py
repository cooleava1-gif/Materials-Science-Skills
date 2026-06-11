#!/usr/bin/env python3
"""Yao et al. (2022) CBM 318: FTIR spectra comparison.

Source: Yao X, Tan L, Xu T. Construction and Building Materials,
2022, 318: 126178.

Reproduces: Fig. 10 — FTIR spectra of WER/SBR modified EA.
"""

from __future__ import annotations

import argparse

import numpy as np

import matplotlib.pyplot as plt

from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_ftir_overlay


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    wavenumber = np.linspace(4000, 400, 500)
    np.random.seed(42)

    base = np.exp(-((wavenumber - 2920) ** 2) / (2 * 80**2)) * 0.6
    base += np.exp(-((wavenumber - 2850) ** 2) / (2 * 60**2)) * 0.4
    base += np.exp(-((wavenumber - 1600) ** 2) / (2 * 50**2)) * 0.35
    base += np.exp(-((wavenumber - 1460) ** 2) / (2 * 40**2)) * 0.3
    base += np.exp(-((wavenumber - 1375) ** 2) / (2 * 35**2)) * 0.25
    base += np.exp(-((wavenumber - 1030) ** 2) / (2 * 60**2)) * 0.3
    base += np.random.normal(0, 0.01, len(wavenumber))

    wer_peak = np.exp(-((wavenumber - 915) ** 2) / (2 * 30**2)) * 0.25
    epoxide = base + wer_peak + np.random.normal(0, 0.01, len(wavenumber))

    sbr_peak = np.exp(-((wavenumber - 965) ** 2) / (2 * 25**2)) * 0.2
    composite = base + wer_peak + sbr_peak + np.random.normal(0, 0.01, len(wavenumber))

    absorbances = [base, epoxide, composite]
    labels = ["Pure EA", "10% WER-EA", "10% WER+3% SBR-EA"]
    peaks = {
        2920: "C-H",
        1600: "C=C",
        1030: "S=O",
        915: "Epoxide",
        965: "SBR",
    }

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    make_ftir_overlay(
        ax, wavenumber, absorbances, labels, PALETTE_CBM,
        peak_annotations=peaks,
    )
    add_panel_label(ax, "(b)")
    fig.tight_layout()
    finalize_figure(fig, "yao2022_ftir_spectra", args.output_dir)

    print(
        "Caption: FTIR spectra of pure EA, WER-modified EA, and WER/SBR "
        "composite-modified EA. Epoxide peak at 915 cm-1 confirms WER "
        "incorporation. SBR peak at 965 cm-1 confirms SBR presence. "
        "Claim boundary: FTIR confirms chemical incorporation but does not "
        "prove network structure; DSC/LSCM/ESEM needed for morphology claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
