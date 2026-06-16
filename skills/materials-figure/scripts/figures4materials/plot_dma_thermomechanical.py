#!/usr/bin/env python3
"""DMA thermomechanical analysis: storage/loss modulus and tan delta vs temperature."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_dma_curve


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("dma_thermomechanical.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    temp = column(rows, "temp_c", as_float=True)
    storage_mod = column(rows, "storage_modulus_mpa", as_float=True)
    loss_mod = column(rows, "loss_modulus_mpa", as_float=True)
    tan_delta = column(rows, "tan_delta", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    make_dma_curve(ax, temp, storage_mod, loss_mod, tan_delta, palette=PALETTE_CBM)
    add_panel_label(ax, "(i)")
    fig.tight_layout()
    finalize_figure(fig, "dma_thermomechanical", args.output_dir)
    print_caption(
        "DMA thermomechanical curves: storage modulus E', loss modulus E'', and tan δ vs temperature. "
        "The tan δ peak marks glass transition; TG assignments should be verified with DSC."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
