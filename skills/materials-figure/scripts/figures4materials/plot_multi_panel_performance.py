#!/usr/bin/env python3
"""Multi-panel performance summary figure for WER-EA system."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
    apply_pub_style,
    finalize_figure,
    make_line_trend,
    make_multi_panel,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("multi_panel_performance.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    dosage = column(rows, "dosage_pct", as_float=True)
    bond = column(rows, "bond_strength_mpa", as_float=True)
    viscosity = column(rows, "viscosity_mpas", as_float=True)
    storage = column(rows, "storage_stability_pct", as_float=True)
    retention = column(rows, "retention_ratio", as_float=True)

    apply_pub_style()
    fig, axes = make_multi_panel(2, 2, figsize=(10, 7))

    make_line_trend(axes[0], dosage, [bond], ["Bond strength"], PALETTE_CBM,
                    xlabel="WER dosage (%)", ylabel="Bond strength (MPa)")
    axes[0].axvspan(10, 15, color=PALETTE_CBM["accent"], alpha=0.18)

    make_line_trend(axes[1], dosage, [viscosity], ["Viscosity"], PALETTE_CBM,
                    xlabel="WER dosage (%)", ylabel="Viscosity (mPa·s)")

    make_line_trend(axes[2], dosage, [storage], ["Storage stability"], PALETTE_CBM,
                    xlabel="WER dosage (%)", ylabel="Storage stability (%)")

    make_line_trend(axes[3], dosage, [retention], ["Durability retention"], PALETTE_CBM,
                    xlabel="WER dosage (%)", ylabel="Retention ratio")

    fig.tight_layout()
    finalize_figure(fig, "multi_panel_performance", args.output_dir)
    print_caption(
        "Multi-panel performance summary for waterborne epoxy emulsified asphalt system. "
        "The candidate dosage range (10-15%) balances bond strength, viscosity, storage stability, and durability retention. "
        "Each panel draws from separate test protocols; direct cross-panel trade-off conclusions require matched conditions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
