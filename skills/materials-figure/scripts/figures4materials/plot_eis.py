#!/usr/bin/env python3
"""Electrochemical Impedance Spectroscopy (EIS) — Nyquist and Bode plots."""

from __future__ import annotations

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
    add_panel_label,
    apply_pub_style,
    finalize_figure,
)

COLUMN_MAP = {
    "frequency": {"column": "frequency"},
    "z_real": {"column": "z_real"},
    "z_imag": {"column": "z_imag"},
    "xlabel_nyquist": {"value": "Z$_{real}$ (\u03a9)"},
    "ylabel_nyquist": {"value": "-Z$_{imag}$ (\u03a9)"},
    "xlabel_bode": {"value": "Frequency (Hz)"},
    "ylabel_bode": {"value": "|Z| (\u03a9) / Phase (\u00b0)"},
    "figure_name": {"value": "eis_comparison"},
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("eis.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)

    freq_col = cmap.get("frequency", {}).get("column", "frequency")
    real_col = cmap.get("z_real", {}).get("column", "z_real")
    imag_col = cmap.get("z_imag", {}).get("column", "z_imag")

    z_real = column(rows, real_col, as_float=True)
    z_imag = column(rows, imag_col, as_float=True)

    # Support automatic log_freq_hz to frequency conversion if needed
    if freq_col == "log_freq_hz" or (freq_col not in rows[0] and "log_freq_hz" in rows[0]):
        freq_vals = column(rows, "log_freq_hz", as_float=True)
        frequency = [10 ** f for f in freq_vals]
        freq_col = "log_freq_hz"
    else:
        frequency = column(rows, freq_col, as_float=True)

    condition_cols = [k for k in rows[0] if k not in (real_col, imag_col, freq_col, "log_freq_hz")]

    apply_pub_style()
    fig, (ax_nyq, ax_bode) = plt.subplots(1, 2, figsize=(9.0, 4.2))
    colors = list(PALETTE_CBM.values())

    if condition_cols:
        for idx, col_name in enumerate(condition_cols):
            zr = column(rows, f"{col_name}_z_real", as_float=True) if f"{col_name}_z_real" in rows[0] else z_real
            zi = column(rows, f"{col_name}_z_imag", as_float=True) if f"{col_name}_z_imag" in rows[0] else z_imag
            fr = column(rows, f"{col_name}_frequency", as_float=True) if f"{col_name}_frequency" in rows[0] else frequency
            color = colors[idx % len(colors)]
            ax_nyq.plot(zr, [-z for z in zi], linewidth=1.8, label=col_name, color=color)
            z_mag = np.sqrt(np.array(zr) ** 2 + np.array(zi) ** 2)
            phase = np.degrees(np.arctan2(np.array(zi), np.array(zr)))
            ax_bode.plot(fr, z_mag, linewidth=1.5, label=f"|Z| {col_name}", color=color)
            ax_bode.plot(fr, abs(phase), linewidth=1.5, linestyle="--", color=color, alpha=0.7)
    else:
        ax_nyq.plot(z_real, [-z for z in z_imag], linewidth=1.8, color=colors[0], label="Data")
        z_mag = np.sqrt(np.array(z_real) ** 2 + np.array(z_imag) ** 2)
        phase = np.degrees(np.arctan2(np.array(z_imag), np.array(z_real)))
        ax_bode.plot(frequency, z_mag, linewidth=1.5, color=colors[0], label="|Z|")
        ax_bode.plot(frequency, abs(phase), linewidth=1.5, linestyle="--", color=colors[1], label="Phase")

    ax_nyq.set_xlabel(cmap.get("xlabel_nyquist", {}).get("value", "Z$_{real}$ (\u03a9)"))
    ax_nyq.set_ylabel(cmap.get("ylabel_nyquist", {}).get("value", "-Z$_{imag}$ (\u03a9)"))
    ax_nyq.set_aspect("equal")
    ax_nyq.legend(fontsize=7)
    add_panel_label(ax_nyq, "(a)")

    ax_bode.set_xlabel(cmap.get("xlabel_bode", {}).get("value", "Frequency (Hz)"))
    ax_bode.set_ylabel(cmap.get("ylabel_bode", {}).get("value", "|Z| (\u03a9) / Phase (\u00b0)"))
    ax_bode.set_xscale("log")
    ax_bode.legend(fontsize=7)
    add_panel_label(ax_bode, "(b)")

    fig.tight_layout()
    finalize_figure(fig, cmap.get("figure_name", {}).get("value", "eis_comparison"), args.output_dir)
    print_caption(
        "EIS spectra: (a) Nyquist plot \u2014 semicircle region reflects charge-transfer "
        "resistance, low-frequency tail indicates Warburg diffusion; "
        "(b) Bode plot \u2014 |Z| magnitude and phase angle vs frequency."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
