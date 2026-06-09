#!/usr/bin/env python3
"""FTIR overlay for curing-evidence figure preparation."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_ftir_overlay


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
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    make_ftir_overlay(
        ax,
        wavenumber,
        [control, modified],
        ["Base emulsion", "Waterborne epoxy modified"],
        PALETTE_CBM,
        peak_annotations={1730: "C=O", 1240: "C-O-C", 915: "epoxy"},
    )
    add_panel_label(ax, "(c)")
    fig.tight_layout()
    finalize_figure(fig, "ftir_curing_evidence", args.output_dir)
    print_caption(
        "FTIR spectra of base and waterborne epoxy modified emulsified asphalt. "
        "Peak labels are assignment cues and should be supported by complementary morphology or thermal data before mechanism claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
