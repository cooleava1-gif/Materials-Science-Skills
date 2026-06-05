"""Civil materials publication-ready matplotlib helper functions."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg", force=False)
import matplotlib.pyplot as plt
import numpy as np


PUB_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 1.4,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.frameon": False,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
}

PALETTE_CBM = {
    "control": "#4B6F8A",
    "modified": "#C47B45",
    "optimal": "#4F7C6A",
    "mechanism": "#8B6F47",
    "accent": "#D4A574",
    "danger": "#B85450",
    "neutral": "#8C8C8C",
}

PALETTE_CCC = {
    "control": "#3A5A7C",
    "modified": "#C17817",
    "optimal": "#2D6A4F",
    "mechanism": "#7A4F2E",
    "accent": "#D4A574",
    "danger": "#9B2335",
    "neutral": "#6B6B6B",
}


def apply_pub_style(rc: dict | None = None) -> None:
    """Apply journal-safe rcParams for civil-materials figures."""

    merged = {**PUB_RC, **(rc or {})}
    plt.rcParams.update(merged)


def make_grouped_bar(
    ax,
    labels: Sequence[str],
    groups: Sequence[str],
    values: Sequence[Sequence[float]],
    palette: dict[str, str],
    *,
    bar_width: float = 0.35,
    error_bars: Sequence[Sequence[float]] | None = None,
    ylabel: str | None = None,
):
    """Draw a grouped bar chart with optional error bars."""

    data = np.asarray(values, dtype=float)
    if data.shape != (len(groups), len(labels)):
        raise ValueError("values must be shaped as groups x labels")
    errors = np.asarray(error_bars, dtype=float) if error_bars is not None else None
    if errors is not None and errors.shape != data.shape:
        raise ValueError("error_bars must match values shape")

    x = np.arange(len(labels))
    offsets = (np.arange(len(groups)) - (len(groups) - 1) / 2) * bar_width
    colors = _series_colors(palette, len(groups))
    bars = []
    for index, group in enumerate(groups):
        yerr = errors[index] if errors is not None else None
        bars.append(
            ax.bar(
                x + offsets[index],
                data[index],
                width=bar_width,
                label=group,
                color=colors[index],
                yerr=yerr,
                capsize=3 if yerr is not None else 0,
                edgecolor="white",
                linewidth=0.7,
            )
        )
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(axis="y", color="#E8E2D6", linewidth=0.8, alpha=0.8)
    return bars


def make_line_trend(
    ax,
    x: Sequence[float],
    y_series: Sequence[Sequence[float]],
    labels: Sequence[str],
    palette: dict[str, str],
    *,
    xlabel: str | None = None,
    ylabel: str | None = None,
    fill_between: Sequence[Sequence[float]] | None = None,
):
    """Draw one or more line trends, optionally with symmetric uncertainty bands."""

    x_values = np.asarray(x, dtype=float)
    colors = _series_colors(palette, len(y_series))
    lines = []
    for index, series in enumerate(y_series):
        y_values = np.asarray(series, dtype=float)
        line = ax.plot(x_values, y_values, marker="o", linewidth=2.2, label=labels[index], color=colors[index])
        lines.extend(line)
        if fill_between is not None:
            spread = np.asarray(fill_between[index], dtype=float)
            ax.fill_between(x_values, y_values - spread, y_values + spread, color=colors[index], alpha=0.18)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(color="#E8E2D6", linewidth=0.8, alpha=0.8)
    ax.legend()
    return lines


def make_radar(
    ax,
    categories: Sequence[str],
    series_dict: dict[str, Sequence[float]],
    palette: dict[str, str],
    *,
    max_val: float | None = None,
    n_ticks: int = 5,
):
    """Draw a radar chart on a polar axis."""

    if getattr(ax, "name", "") != "polar":
        raise ValueError("make_radar requires a polar axis")
    count = len(categories)
    if count < 3:
        raise ValueError("radar chart requires at least three categories")
    angles = np.linspace(0, 2 * np.pi, count, endpoint=False).tolist()
    angles += angles[:1]
    colors = _series_colors(palette, len(series_dict))
    max_value = max_val or max(max(values) for values in series_dict.values())
    for index, (label, values) in enumerate(series_dict.items()):
        closed = list(values) + list(values[:1])
        ax.plot(angles, closed, color=colors[index], linewidth=2, label=label)
        ax.fill(angles, closed, color=colors[index], alpha=0.18)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, max_value)
    ax.set_yticks(np.linspace(0, max_value, n_ticks))
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.15))
    return ax


def make_xrd_pattern(
    ax,
    two_theta: Sequence[float],
    intensities: Sequence[Sequence[float]],
    labels: Sequence[str],
    palette: dict[str, str],
    *,
    offset: float = 0.5,
    peak_annotations: dict[float, str] | None = None,
):
    """Draw stacked XRD patterns with optional peak labels."""

    x = np.asarray(two_theta, dtype=float)
    colors = _series_colors(palette, len(intensities))
    for index, intensity in enumerate(intensities):
        y = np.asarray(intensity, dtype=float) + offset * index
        ax.plot(x, y, color=colors[index], linewidth=1.7, label=labels[index])
    for position, label in (peak_annotations or {}).items():
        ax.axvline(position, color=palette.get("neutral", "#8C8C8C"), linewidth=0.8, linestyle="--")
        ax.text(position, ax.get_ylim()[1], label, ha="center", va="bottom", fontsize=8)
    ax.set_xlabel(r"2 theta (degree)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.legend()
    return ax


def make_ftir_overlay(
    ax,
    wavenumber: Sequence[float],
    absorbances: Sequence[Sequence[float]],
    labels: Sequence[str],
    palette: dict[str, str],
    *,
    peak_annotations: dict[float, str] | None = None,
    invert_y: bool = False,
):
    """Draw overlaid FTIR spectra with peak annotations."""

    x = np.asarray(wavenumber, dtype=float)
    colors = _series_colors(palette, len(absorbances))
    for index, absorbance in enumerate(absorbances):
        ax.plot(x, absorbance, color=colors[index], linewidth=1.8, label=labels[index])
    for position, label in (peak_annotations or {}).items():
        ax.axvline(position, color=palette.get("danger", "#B85450"), linewidth=0.9, linestyle="--")
        ax.text(position, ax.get_ylim()[1], label, ha="center", va="bottom", fontsize=8, rotation=90)
    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("Absorbance (a.u.)")
    ax.invert_xaxis()
    if invert_y:
        ax.invert_yaxis()
    ax.legend()
    ax.grid(color="#E8E2D6", linewidth=0.7, alpha=0.65)
    return ax


def add_panel_label(ax, label: str, *, loc: str = "top-left", fontsize: int = 12):
    """Add a journal-style subfigure label such as (a)."""

    positions = {
        "top-left": (0.02, 0.98, "left", "top"),
        "top-right": (0.98, 0.98, "right", "top"),
        "bottom-left": (0.02, 0.02, "left", "bottom"),
        "bottom-right": (0.98, 0.02, "right", "bottom"),
    }
    if loc not in positions:
        raise ValueError(f"unsupported panel label loc: {loc}")
    x, y, ha, va = positions[loc]
    return ax.text(x, y, label, transform=ax.transAxes, ha=ha, va=va, fontsize=fontsize, fontweight="bold")


def add_error_bars(ax, x: Sequence[float], y: Sequence[float], error: Sequence[float], *, color: str = "black", capsize: int = 3):
    """Add error bars to existing points or bars."""

    return ax.errorbar(x, y, yerr=error, fmt="none", ecolor=color, capsize=capsize, linewidth=1)


def finalize_figure(
    fig,
    name: str,
    output_dir: str | Path = "./figures/",
    *,
    formats: Iterable[str] = ("svg", "png"),
    dpi: int = 300,
) -> list[str]:
    """Export a figure in one or more formats and close it."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    written = []
    for fmt in formats:
        path = output_path / f"{name}.{fmt.lstrip('.')}"
        fig.savefig(path, dpi=dpi)
        written.append(str(path))
    plt.close(fig)
    return written


def _series_colors(palette: dict[str, str], count: int) -> list[str]:
    preferred = ["control", "modified", "optimal", "mechanism", "accent", "danger", "neutral"]
    colors = [palette[key] for key in preferred if key in palette]
    if not colors:
        colors = list(plt.rcParams["axes.prop_cycle"].by_key().get("color", ["#4B6F8A"]))
    while len(colors) < count:
        colors.extend(colors)
    return colors[:count]
