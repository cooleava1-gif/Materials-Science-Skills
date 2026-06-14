#!/usr/bin/env python3
"""Generate SVG examples for the materials figure gallery."""

from __future__ import annotations

import argparse
import math
from html import escape
from pathlib import Path


PRESETS = {
    "cbm": {
        "font": "Arial",
        "background": "#FFFFFF",
        "axis": "#2F332F",
        "grid": "#E8E2D6",
        "control": "#6B7568",
        "primary": "#B65C38",
        "secondary": "#E0A04B",
        "mechanism": "#3E6F8E",
        "durability": "#5D7F4F",
    },
    "ccc": {
        "font": "Arial",
        "background": "#FFFFFF",
        "axis": "#26313A",
        "grid": "#DDE6EA",
        "control": "#657B83",
        "primary": "#2F6F8F",
        "secondary": "#8A6FB0",
        "mechanism": "#C46A2B",
        "durability": "#4C8C7A",
    },
    "rmpd_ijpe": {
        "font": "Arial",
        "background": "#FFFFFF",
        "axis": "#2E2E2E",
        "grid": "#E6E6DE",
        "control": "#717171",
        "primary": "#D08A2D",
        "secondary": "#4E7998",
        "mechanism": "#7A5D3B",
        "durability": "#5B7C3A",
    },
    "jbe": {
        "font": "Arial",
        "background": "#FFFFFF",
        "axis": "#30353B",
        "grid": "#E4E7EC",
        "control": "#67717D",
        "primary": "#2E7D6B",
        "secondary": "#D18B47",
        "mechanism": "#536FA3",
        "durability": "#6E8B55",
    },
}


def svg_shell(title: str, body: str, preset: dict[str, str], width: int = 960, height: int = 620) -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<rect width="100%" height="100%" fill="{preset["background"]}"/>',
            f'<text x="{width/2}" y="34" text-anchor="middle" font-family="{preset["font"]}" font-size="18" font-weight="700">Materials Science Figure Gallery</text>',
            f'<text x="{width/2}" y="58" text-anchor="middle" font-family="{preset["font"]}" font-size="24" font-weight="700">{escape(title)}</text>',
            body,
            "</svg>",
        ]
    )


def text(x: float, y: float, value: str, preset: dict[str, str], size: int = 14, anchor: str = "middle", weight: str = "400") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{preset["font"]}" font-size="{size}" font-weight="{weight}" fill="{preset["axis"]}">{escape(value)}</text>'


def bonding_strength_bar(preset: dict[str, str]) -> str:
    data = [("Control", 0.42), ("WE-3", 0.58), ("WE-5", 0.73), ("WE-7", 0.69)]
    left, top, plot_w, plot_h = 110, 105, 760, 370
    max_value = 0.8
    bar_w = 110
    gap = 72
    parts = [
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="{preset["axis"]}" stroke-width="2"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="{preset["axis"]}" stroke-width="2"/>',
        text(30, top + plot_h / 2, "Bond strength (MPa)", preset, 15, "middle"),
    ]
    for tick in range(5):
        value = max_value * tick / 4
        y = top + plot_h - value / max_value * plot_h
        parts.append(f'<line x1="{left-6}" y1="{y:.1f}" x2="{left+plot_w}" y2="{y:.1f}" stroke="{preset["grid"]}" stroke-width="1"/>')
        parts.append(text(left - 12, y + 5, f"{value:.2f}", preset, 12, "end"))
    for index, (label, value) in enumerate(data):
        x = left + 70 + index * (bar_w + gap)
        h = value / max_value * plot_h
        y = top + plot_h - h
        color = preset["control"] if index == 0 else preset["primary"]
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" rx="4" fill="{color}"/>')
        parts.append(text(x + bar_w / 2, y - 10, f"{value:.2f}", preset, 13))
        parts.append(text(x + bar_w / 2, top + plot_h + 30, label, preset, 13))
    parts.append(text(480, 560, "Claim boundary: performance difference only; mechanism needs FTIR/SEM/rheology.", preset, 13))
    return svg_shell("Bonding Strength Bar", "\n".join(parts), preset)


def dosage_performance_curve(preset: dict[str, str]) -> str:
    data = [(0, 0.42), (3, 0.58), (5, 0.73), (7, 0.69), (10, 0.61)]
    left, top, plot_w, plot_h = 105, 105, 770, 370
    x_max, y_max = 10, 0.8
    points = []
    parts = [
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="{preset["axis"]}" stroke-width="2"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="{preset["axis"]}" stroke-width="2"/>',
        f'<rect x="{left + 4.5/x_max*plot_w:.1f}" y="{top}" width="{2.5/x_max*plot_w:.1f}" height="{plot_h}" fill="{preset["secondary"]}" opacity="0.16"/>',
    ]
    for dosage, value in data:
        x = left + dosage / x_max * plot_w
        y = top + plot_h - value / y_max * plot_h
        points.append(f"{x:.1f},{y:.1f}")
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{preset["primary"]}"/>')
        parts.append(text(x, top + plot_h + 28, str(dosage), preset, 12))
    parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{preset["primary"]}" stroke-width="4" stroke-linejoin="round"/>')
    parts.append(text(480, 525, "Preferred range is a hypothesis until viscosity, storage stability, and durability are checked.", preset, 13))
    parts.append(text(480, 505, "Waterborne epoxy dosage (%)", preset, 15))
    return svg_shell("Dosage-Performance Curve", "\n".join(parts), preset)


def ftir_peak_annotation(preset: dict[str, str]) -> str:
    left, top, plot_w, plot_h = 105, 105, 770, 360
    points = []
    for i in range(160):
        t = i / 159
        x = left + t * plot_w
        y = top + 190 + 35 * math.sin(t * 7 * math.pi) - 90 * math.exp(-((t - 0.36) / 0.035) ** 2) - 70 * math.exp(-((t - 0.72) / 0.045) ** 2)
        points.append(f"{x:.1f},{y:.1f}")
    parts = [
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="{preset["axis"]}" stroke-width="2"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="{preset["axis"]}" stroke-width="2"/>',
        f'<polyline points="{" ".join(points)}" fill="none" stroke="{preset["mechanism"]}" stroke-width="3"/>',
    ]
    for x, label in [(left + 0.36 * plot_w, "1730 cm-1"), (left + 0.72 * plot_w, "1030 cm-1")]:
        parts.append(f'<line x1="{x:.1f}" y1="{top+40}" x2="{x:.1f}" y2="{top+plot_h}" stroke="{preset["primary"]}" stroke-width="1.5" stroke-dasharray="5 5"/>')
        parts.append(text(x, top + 32, label, preset, 13))
    parts.append(text(480, 528, "Caption must name peak assignment and avoid overclaiming complete reaction pathways.", preset, 13))
    return svg_shell("FTIR Peak Annotation", "\n".join(parts), preset)


def sem_fluorescence_plate(preset: dict[str, str]) -> str:
    parts = []
    labels = [("a", "Control SEM"), ("b", "Modified SEM"), ("c", "Control fluorescence"), ("d", "Modified fluorescence")]
    for idx, (panel, label) in enumerate(labels):
        col = idx % 2
        row = idx // 2
        x = 125 + col * 370
        y = 110 + row * 210
        fill = "#D7D2C8" if "SEM" in label else "#17221E"
        parts.append(f'<rect x="{x}" y="{y}" width="300" height="160" rx="6" fill="{fill}" stroke="{preset["axis"]}" stroke-width="1.4"/>')
        for dot in range(24):
            cx = x + 20 + (dot * 47 % 260)
            cy = y + 18 + (dot * 31 % 125)
            color = preset["secondary"] if "fluorescence" in label else preset["control"]
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{3 + dot % 5}" fill="{color}" opacity="0.55"/>')
        parts.append(text(x + 18, y + 23, panel, preset, 16, "middle", "700"))
        parts.append(text(x + 150, y + 188, label, preset, 13))
        parts.append(f'<line x1="{x+210}" y1="{y+142}" x2="{x+280}" y2="{y+142}" stroke="#FFFFFF" stroke-width="4"/>')
        parts.append(text(x + 245, y + 134, "20 um", preset, 11))
    parts.append(text(480, 585, "Image panels support observed morphology; quantification needs repeated fields or image analysis.", preset, 13))
    return svg_shell("SEM/Fluorescence Plate", "\n".join(parts), preset)


def durability_radar(preset: dict[str, str]) -> str:
    center_x, center_y, radius = 480, 315, 170
    metrics = ["Moisture", "Aging", "Freeze-thaw", "Fatigue", "Rutting"]
    control = [0.62, 0.58, 0.55, 0.61, 0.60]
    modified = [0.82, 0.78, 0.74, 0.79, 0.76]
    parts = []
    for ring in range(1, 5):
        r = radius * ring / 4
        points = [_polar(center_x, center_y, r, idx, len(metrics)) for idx in range(len(metrics))]
        parts.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="{preset["grid"]}" stroke-width="1"/>')
    for idx, metric in enumerate(metrics):
        axis = _polar(center_x, center_y, radius, idx, len(metrics))
        parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{axis.split(",")[0]}" y2="{axis.split(",")[1]}" stroke="{preset["grid"]}" stroke-width="1"/>')
        label = _polar(center_x, center_y, radius + 45, idx, len(metrics))
        lx, ly = [float(value) for value in label.split(",")]
        parts.append(text(lx, ly, metric, preset, 12))
    for values, color, opacity in [(control, preset["control"], "0.20"), (modified, preset["durability"], "0.34")]:
        points = [_polar(center_x, center_y, radius * value, idx, len(metrics)) for idx, value in enumerate(values)]
        parts.append(f'<polygon points="{" ".join(points)}" fill="{color}" opacity="{opacity}" stroke="{color}" stroke-width="3"/>')
    parts.append(text(480, 575, "Normalized durability profile; raw values and uncertainty should remain available.", preset, 13))
    return svg_shell("Durability Radar", "\n".join(parts), preset)


def mechanism_schematic(preset: dict[str, str]) -> str:
    boxes = [
        (80, 180, "Emulsion\nstability"),
        (265, 180, "Demulsification"),
        (450, 180, "Epoxy\ncuring"),
        (635, 180, "Interface\nnetwork"),
        (450, 385, "Bonding and\nmoisture resistance"),
    ]
    parts = []
    for x, y, label in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="145" height="92" rx="12" fill="{preset["grid"]}" stroke="{preset["axis"]}" stroke-width="1.5"/>')
        for i, line in enumerate(label.splitlines()):
            parts.append(text(x + 72.5, y + 38 + i * 20, line, preset, 14, "middle", "700" if i == 0 else "400"))
    arrows = [(225, 226, 265, 226), (410, 226, 450, 226), (595, 226, 635, 226), (522, 272, 522, 385)]
    for x1, y1, x2, y2 in arrows:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{preset["primary"]}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.insert(0, '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#B65C38"/></marker></defs>')
    parts.append(text(480, 555, "Solid arrows require measured support; dashed or missing links must be marked in captions.", preset, 13))
    return svg_shell("Mechanism Schematic", "\n".join(parts), preset)


def _polar(cx: float, cy: float, r: float, index: int, total: int) -> str:
    angle = -math.pi / 2 + index * 2 * math.pi / total
    return f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}"


GENERATORS = {
    "bonding_strength_bar.svg": bonding_strength_bar,
    "dosage_performance_curve.svg": dosage_performance_curve,
    "ftir_peak_annotation.svg": ftir_peak_annotation,
    "sem_fluorescence_plate.svg": sem_fluorescence_plate,
    "durability_radar.svg": durability_radar,
    "mechanism_schematic.svg": mechanism_schematic,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="gallery-generated", help="Directory for generated SVG files.")
    parser.add_argument("--preset", default="cbm", choices=sorted(PRESETS), help="Journal style preset.")
    parser.add_argument("--list", action="store_true", help="List available gallery SVG names without generating.")
    args = parser.parse_args()

    if args.list:
        for name in GENERATORS:
            print(name)
        return 0

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    preset = PRESETS[args.preset]
    for filename, generator in GENERATORS.items():
        path = output_dir / filename
        path.write_text(generator(preset), encoding="utf-8")
        print(path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
