#!/usr/bin/env python3
"""Creep-recovery curves for viscoelastic material characterization."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_creep_recovery


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("creep_recovery.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    time = column(rows, "time_s", as_float=True)
    strain = [column(rows, "strain_pct_control", as_float=True), column(rows, "strain_pct_modified", as_float=True)]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    make_creep_recovery(
        ax, time, strain, ["Control", "Modified"], PALETTE_CBM,
        recovery_zones=[(30, 40), (70, 80), (110, 120)],
    )
    add_panel_label(ax, "(c)")
    fig.tight_layout()
    finalize_figure(fig, "creep_recovery", args.output_dir)
    print_caption(
        "Creep-recovery response under multi-cycle loading. "
        "Recovery ratios depend on rest period and temperature; field prediction requires full MSCR or DSR characterization."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
