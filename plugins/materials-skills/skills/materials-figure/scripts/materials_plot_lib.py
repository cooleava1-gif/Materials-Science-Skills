"""Materials science publication-ready matplotlib helper functions."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg", force=False)
import matplotlib.pyplot as plt
import numpy as np


PUB_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "svg.fonttype": "none",
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 1.5,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "xtick.major.width": 1.2,
    "ytick.major.width": 1.2,
    "legend.frameon": False,
    "legend.fontsize": 8,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "figure.dpi": 100,
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

# Unified low-saturation palette (single hue family for related variants)
PALETTE_SINGLE_HUE = {
    "light": "#B4C0E4",
    "mid":   "#7884B4",
    "dark":  "#484878",
    "darker": "#2C2C58",
}

# Extended semantic palette with more roles
PALETTE_SEMANTIC = {
    "control":    "#4B6F8A",
    "modified":   "#C47B45",
    "optimal":    "#4F7C6A",
    "mechanism":  "#8B6F47",
    "comparison": "#8C8C8C",
    "danger":     "#B85450",
    "accent":     "#D4A574",
    "baseline":   "#A8B8C8",
}

DEFAULT_COLORS_SINGLE_HUE = [
    PALETTE_SINGLE_HUE["light"],
    PALETTE_SINGLE_HUE["mid"],
    PALETTE_SINGLE_HUE["dark"],
    PALETTE_SINGLE_HUE["darker"],
]

# ── Domain-specific palettes ─────────────────────────────────────────────────

PALETTE_ASPHALT = {
    "control":    "#6B7B8D",
    "modified":   "#8B6914",
    "optimal":    "#4A7C59",
    "moisture":   "#5B8FA8",
    "aging":      "#C47B45",
    "mechanism":  "#8B6F47",
    "danger":     "#B85450",
    "neutral":    "#8C8C8C",
}

PALETTE_CEMENT = {
    "control":    "#7A7A7A",
    "modified":   "#4B6F8A",
    "optimal":    "#4F7C6A",
    "hydration":  "#C47B45",
    "mechanism":  "#8B6F47",
    "durability": "#5B8FA8",
    "danger":     "#B85450",
    "neutral":    "#9E9E9E",
}

PALETTE_POLYMER = {
    "control":    "#4B6F8A",
    "modified":   "#9A4D8E",
    "optimal":    "#4F7C6A",
    "mechanism":  "#C47B45",
    "thermal":    "#B85450",
    "mechanical": "#5B8FA8",
    "danger":     "#D4574E",
    "neutral":    "#8C8C8C",
}

PALETTE_CERAMIC = {
    "control":    "#8C8C8C",
    "modified":   "#C47B45",
    "optimal":    "#4F7C6A",
    "mechanism":  "#8B6F47",
    "thermal":    "#B85450",
    "mechanical": "#4B6F8A",
    "danger":     "#D4574E",
    "neutral":    "#9E9E9E",
}

# ── NMI pastel palette (editorial multi-panel figures) ────────────────────────

PALETTE_NMI_PASTEL = {
    "baseline_dark":  "#484878",
    "baseline_mid":   "#7884B4",
    "baseline_soft":  "#B4C0E4",
    "ours_tiny":      "#E4E4F0",
    "ours_base":      "#E4CCD8",
    "ours_large":     "#F0C0CC",
    "bg_lilac":       "#E0E0F0",
    "bg_aqua":        "#E0F0F0",
    "bg_peach":       "#F0E0D0",
    "neutral_light":  "#D8D8D8",
    "neutral_mid":    "#A8A8A8",
    "neutral_dark":   "#606060",
    "delta_up":       "#2E9E44",
    "delta_down":     "#E53935",
}

DEFAULT_COLORS_NMI_PASTEL = [
    PALETTE_NMI_PASTEL["baseline_dark"],
    PALETTE_NMI_PASTEL["baseline_mid"],
    PALETTE_NMI_PASTEL["baseline_soft"],
    PALETTE_NMI_PASTEL["ours_tiny"],
    PALETTE_NMI_PASTEL["ours_base"],
    PALETTE_NMI_PASTEL["ours_large"],
]

# ── Domain palette registry (for dynamic lookup) ─────────────────────────────

DOMAIN_PALETTES = {
    "asphalt":  PALETTE_ASPHALT,
    "cement":   PALETTE_CEMENT,
    "polymer":  PALETTE_POLYMER,
    "ceramic":  PALETTE_CERAMIC,
    "cbm":      PALETTE_CBM,
    "ccc":      PALETTE_CCC,
}


def get_domain_palette(domain: str) -> dict[str, str]:
    """Return the palette for a material domain, falling back to PALETTE_CBM."""
    return DOMAIN_PALETTES.get(domain.lower(), PALETTE_CBM)



def luminance_text_color(hex_color: str) -> str:
    """Return 'white' or '#333333' (dark) based on background luminance."""
    c = hex_color.lstrip('#')
    if len(c) != 6:
        return '#333333'
    r, g, b = int(c[0:2], 16) / 255, int(c[2:4], 16) / 255, int(c[4:6], 16) / 255
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return 'white' if luminance < 0.5 else '#333333'



def apply_pub_style(rc: dict | None = None) -> None:
    """Apply journal-safe rcParams for materials figures."""

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


# ── Supplementary chart types ──────────────────────────────────


def make_heatmap(
    ax: plt.Axes,
    data: "np.ndarray",
    row_labels: list[str],
    col_labels: list[str],
    palette: dict[str, str] | None = None,
    *,
    cmap: str = "YlOrRd",
    annot: bool = True,
    fmt: str = ".2f",
    vmin: float | None = None,
    vmax: float | None = None,
) -> plt.Axes:
    """Correlation matrix or property heatmap.

    Parameters
    ----------
    data : 2-D array (n_rows, n_cols)
    row_labels, col_labels : axis tick labels
    cmap : matplotlib colormap name
    annot : write numeric value in each cell
    fmt : format string for annotations
    """
    im = ax.imshow(data, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=8)
    if annot:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                ax.text(j, i, format(data[i, j], fmt), ha="center", va="center", fontsize=7)
    ax.figure.colorbar(im, ax=ax, shrink=0.8)
    return ax


def make_stacked_bar(
    ax: plt.Axes,
    labels: list[str],
    series_dict: dict[str, list[float]],
    palette: dict[str, str],
    *,
    ylabel: str | None = None,
) -> plt.Axes:
    """Stacked bar chart for material composition or cumulative contributions.

    Parameters
    ----------
    labels : x-axis category labels
    series_dict : {series_name: [values_per_category]}
    palette : color palette (uses _series_colors for auto-assignment)
    """
    series_names = list(series_dict.keys())
    colors = _series_colors(palette, len(series_names))
    x = np.arange(len(labels))
    bottoms = np.zeros(len(labels))
    for idx, name in enumerate(series_names):
        values = np.array(series_dict[name])
        ax.bar(x, values, bottom=bottoms, label=name, color=colors[idx], width=0.6)
        bottoms += values
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.legend(fontsize=8, frameon=False)
    return ax


def make_boxplot(
    ax: plt.Axes,
    groups: list[str],
    data_dict: dict[str, list[float]],
    palette: dict[str, str],
    *,
    ylabel: str | None = None,
    show_points: bool = True,
) -> plt.Axes:
    """Box plot for multi-group distribution comparison.

    Parameters
    ----------
    groups : group names (x-axis labels)
    data_dict : {group_name: [raw_data_values]}
    show_points : overlay individual data points as scatter
    """
    colors = _series_colors(palette, len(groups))
    positions = range(1, len(groups) + 1)
    box_data = [data_dict.get(g, []) for g in groups]
    bp = ax.boxplot(box_data, positions=positions, patch_artist=True, widths=0.5)
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    if show_points:
        for i, (g, color) in enumerate(zip(groups, colors)):
            vals = data_dict.get(g, [])
            jitter = np.random.default_rng(42).uniform(-0.1, 0.1, len(vals))
            ax.scatter([i + 1 + j for j in jitter], vals, color=color, s=12, zorder=5, alpha=0.8)
    ax.set_xticks(list(positions))
    ax.set_xticklabels(groups, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel)
    return ax


def make_tga_dtg_overlay(
    ax: plt.Axes,
    temp: "np.ndarray",
    tga_pct: "np.ndarray",
    dtg_rate: "np.ndarray",
    labels: tuple[str, str] = ("TGA", "DTG"),
    palette: dict[str, str] | None = None,
    *,
    xlabel: str = "Temperature (°C)",
) -> tuple[plt.Axes, plt.Axes]:
    """Dual Y-axis TGA/DTG overlay for thermal analysis.

    Returns (ax_tga, ax_dtg) for further customization.
    """
    colors = _series_colors(palette or PALETTE_CBM, 2)
    ax_tga = ax
    ax_tga.plot(temp, tga_pct, color=colors[0], linewidth=1.5, label=labels[0])
    ax_tga.set_xlabel(xlabel)
    ax_tga.set_ylabel("Mass (%)", color=colors[0])
    ax_tga.tick_params(axis="y", labelcolor=colors[0])

    ax_dtg = ax_tga.twinx()
    ax_dtg.plot(temp, dtg_rate, color=colors[1], linewidth=1.5, linestyle="--", label=labels[1])
    ax_dtg.set_ylabel("DTG (%/°C)", color=colors[1])
    ax_dtg.tick_params(axis="y", labelcolor=colors[1])

    # Combined legend
    lines1, labels1 = ax_tga.get_legend_handles_labels()
    lines2, labels2 = ax_dtg.get_legend_handles_labels()
    ax_tga.legend(lines1 + lines2, labels1 + labels2, fontsize=8, frameon=False)
    return ax_tga, ax_dtg


def annotate_bars(
    ax: plt.Axes,
    bars,
    values: Sequence[float],
    *,
    errors: Sequence[float] | None = None,
    fmt: str = "{:.0f}",
    fontsize: int = 7,
    offset_pts: float = 3,
) -> None:
    """Annotate each bar with its value, using luminance-adaptive text color.

    Parameters
    ----------
    ax : axes containing the bars
    bars : BarContainer returned by ax.bar()
    values : numeric values to print inside/on top of each bar
    errors : if provided, annotation sits above error bar cap
    fmt : format string for the value
    fontsize : text size in pt
    offset_pts : vertical offset above bar top in points
    """
    for bar, val in zip(bars, values):
        bar_color = bar.get_facecolor()
        r, g, b = bar_color[0], bar_color[1], bar_color[2]
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = "white" if luminance < 0.5 else "#333333"
        y_top = bar.get_height()
        if errors is not None:
            idx = list(bars).index(bar) if hasattr(bars, "__iter__") else 0
            try:
                y_top += errors[idx]
            except (IndexError, TypeError):
                pass
        ax.annotate(
            fmt.format(val),
            xy=(bar.get_x() + bar.get_width() / 2, y_top),
            xytext=(0, offset_pts),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize,
            color=text_color,
            fontweight="bold",
        )


def tighten_ylimits(
    ax: plt.Axes,
    data: Sequence[float] | np.ndarray,
    *,
    margin: float = 0.1,
    ymin: float | None = None,
) -> None:
    """Tighten y-axis to data range instead of using a fixed 0-max.

    Parameters
    ----------
    ax : target axes
    data : all y values across the plot
    margin : fraction of data range to add as padding (0.1 = 10%)
    ymin : explicit lower bound; if None, uses min(data) - margin * range
    """
    arr = np.asarray(data, dtype=float)
    dmin, dmax = float(np.nanmin(arr)), float(np.nanmax(arr))
    span = dmax - dmin if dmax != dmin else abs(dmax) * 0.1 or 1.0
    pad = span * margin
    bottom = ymin if ymin is not None else dmin - pad
    ax.set_ylim(bottom, dmax + pad)


def add_shared_legend(
    fig: plt.Figure,
    axes: Sequence[plt.Axes],
    *,
    loc: str = "upper center",
    bbox_to_anchor: tuple[float, float] = (0.5, 1.02),
    ncol: int | None = None,
    fontsize: int = 8,
) -> None:
    """Create one shared legend for multiple axes, placed above the figure.

    Parameters
    ----------
    fig : the figure
    axes : list of axes whose handles/labels will be merged
    loc : legend anchor location
    bbox_to_anchor : position relative to figure
    ncol : number of legend columns; auto-calculated if None
    fontsize : legend text size
    """
    handles, labels = [], []
    for ax in axes:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)
    seen = set()
    unique_handles, unique_labels = [], []
    for h, l in zip(handles, labels):
        if l not in seen:
            seen.add(l)
            unique_handles.append(h)
            unique_labels.append(l)
    if ncol is None:
        ncol = min(len(unique_labels), 4)
    for ax in axes:
        if ax.get_legend():
            ax.get_legend().remove()
    fig.legend(
        unique_handles,
        unique_labels,
        loc=loc,
        bbox_to_anchor=bbox_to_anchor,
        ncol=ncol,
        fontsize=fontsize,
        frameon=False,
    )


def _series_colors(palette: dict[str, str], count: int) -> list[str]:
    preferred = [
        "control", "modified", "optimal", "mechanism", "moisture", "aging",
        "hydration", "durability", "thermal", "mechanical", "accent", "danger",
        "comparison", "neutral", "baseline",
    ]
    colors = [palette[key] for key in preferred if key in palette]
    if not colors:
        colors = list(plt.rcParams["axes.prop_cycle"].by_key().get("color", ["#4B6F8A"]))
    while len(colors) < count:
        colors.extend(colors)
    return colors[:count]
