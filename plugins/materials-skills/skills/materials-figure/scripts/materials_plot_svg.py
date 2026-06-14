#!/usr/bin/env python3
"""Create a simple publication-style SVG bar chart from label,value CSV data."""

from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path


def read_rows(path: Path) -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        required = {"label", "value"}
        fieldnames = set(reader.fieldnames or [])
        if not required.issubset(fieldnames):
            raise ValueError("CSV must include columns: label, value")
        for row_number, row in enumerate(reader, start=2):
            label = (row.get("label") or "").strip()
            if not label:
                raise ValueError(f"row {row_number}: label must not be empty")
            try:
                value = float(row.get("value") or "")
            except ValueError as exc:
                raise ValueError(f"row {row_number}: value must be numeric") from exc
            rows.append((label, value))
    if not rows:
        raise ValueError("CSV has no rows")
    return rows


def make_svg(rows: list[tuple[str, float]], title: str, ylabel: str) -> str:
    width, height = 900, 560
    left, right, top, bottom = 90, 40, 70, 110
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_value = max(v for _, v in rows) or 1.0
    bar_gap = 18
    bar_w = (plot_w - bar_gap * (len(rows) - 1)) / len(rows)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="34" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700">{escape(title)}</text>',
        f'<text x="24" y="{top + plot_h/2}" transform="rotate(-90 24 {top + plot_h/2})" text-anchor="middle" font-family="Arial" font-size="16">{escape(ylabel)}</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#333" stroke-width="1.5"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#333" stroke-width="1.5"/>',
    ]
    for idx in range(5):
        value = max_value * idx / 4
        y = top + plot_h - (value / max_value) * plot_h
        parts.append(f'<line x1="{left-5}" y1="{y:.1f}" x2="{left+plot_w}" y2="{y:.1f}" stroke="#E5E1D8" stroke-width="1"/>')
        parts.append(f'<text x="{left-10}" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="12">{value:.2g}</text>')
    for i, (label, value) in enumerate(rows):
        x = left + i * (bar_w + bar_gap)
        bar_h = (value / max_value) * plot_h
        y = top + plot_h - bar_h
        color = "#4F7C6A" if i == 0 else "#C47B45"
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="{color}"/>')
        parts.append(f'<text x="{x + bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" font-family="Arial" font-size="13">{value:.3g}</text>')
        parts.append(f'<text x="{x + bar_w/2:.1f}" y="{top + plot_h + 28}" text-anchor="middle" font-family="Arial" font-size="13">{escape(label)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--title", default="Civil materials performance")
    parser.add_argument("--ylabel", default="Value")
    parser.add_argument("--output", default="materials-figure.svg")
    args = parser.parse_args()

    try:
        rows = read_rows(Path(args.csv_file))
    except ValueError as exc:
        parser.exit(2, f"error: {exc}\n")
    Path(args.output).write_text(make_svg(rows, args.title, args.ylabel), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
