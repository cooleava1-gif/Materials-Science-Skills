#!/usr/bin/env python3
"""Template plot script for figure packages."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from civil_materials_plot_lib import apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(Path(__file__).parent))
    args = parser.parse_args()

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("Template Figure")
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    finalize_figure(fig, "template_figure", args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())