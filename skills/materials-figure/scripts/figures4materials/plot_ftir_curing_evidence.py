#!/usr/bin/env python3
"""FTIR overlay for curing-evidence figure preparation."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, tighten_ylimits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("ftir_spectra.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    wavenumber = column(rows, "wavenumber_cm1", as_float=True)
    control = column(rows, "control_abs", as_float=True)
    modified = column(rows, "modified_abs", as_float=True)

    apply_pub_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [2, 1]})

    # ── Panel (a): Full FTIR overlay ──
    ax1.plot(wavenumber, control, "-", color=PALETTE_CBM["control"], linewidth=1.8, label="Base emulsion")
    ax1.plot(wavenumber, modified, "-", color=PALETTE_CBM["modified"], linewidth=1.8, label="Epoxy modified")
    peak_annotations = {1730: "C=O", 1240: "C-O-C", 915: "epoxy ring"}
    for pos, label in peak_annotations.items():
        ax1.axvline(pos, color=PALETTE_CBM["danger"], linewidth=0.8, linestyle="--", alpha=0.6)
        ax1.text(pos, ax1.get_ylim()[1] * 0.95, label, ha="center", va="top", fontsize=7, rotation=90, color=PALETTE_CBM["danger"])
    ax1.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax1.set_ylabel("Absorbance (a.u.)")
    ax1.invert_xaxis()
    tighten_ylimits(ax1, control + modified, margin=0.1, ymin=0)
    ax1.legend(fontsize=7)
    add_panel_label(ax1, "a")

    # ── Panel (b): Difference spectrum (modified - control) ──
    diff = [m - c for m, c in zip(modified, control)]
    colors_diff = [PALETTE_CBM["optimal"] if d >= 0 else PALETTE_CBM["danger"] for d in diff]
    ax2.barh(range(len(wavenumber)), diff, color=colors_diff, height=0.8, edgecolor="white", linewidth=0.3)
    ax2.set_yticks(range(len(wavenumber)))
    ax2.set_yticklabels([f"{int(w)}" for w in wavenumber], fontsize=6)
    ax2.set_xlabel("\u0394 Absorbance (modified \u2212 control)")
    ax2.set_ylabel("Wavenumber (cm$^{-1}$)")
    ax2.axvline(0, color="#333333", linewidth=0.6)
    ax2.invert_yaxis()
    add_panel_label(ax2, "b")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "ftir_curing_evidence", args.output_dir)
    print_caption(
        "FTIR evidence for curing mechanism: (a) overlaid spectra of base and waterborne epoxy modified emulsified asphalt "
        "with peak assignments, (b) difference spectrum showing positive (new bonds) and negative (consumed groups) changes. "
        "Peak labels are assignment cues and should be supported by complementary morphology or thermal data before mechanism claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
