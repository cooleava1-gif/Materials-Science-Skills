#!/usr/bin/env python3
"""Generate richer SVG assets for the materials figure gallery."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path


PALETTE = {
    "ink": "#27312D",
    "muted": "#69746F",
    "grid": "#E7E1D4",
    "blue": "#4B6F8A",
    "orange": "#C47B45",
    "green": "#4F7C6A",
    "gold": "#D4A574",
    "red": "#B85450",
    "dark": "#17221E",
    "paper": "#FFFDF8",
}


ASSETS = [
    ("bonding_performance_matrix.svg", "Bonding Performance Matrix", "dry / wet / aged comparison", "Performance claim needs control, n, and error bars."),
    ("dosage_workability_window.svg", "Dosage-Workability Window", "strength vs. viscosity vs. stability", "Optimal dosage is conditional until construction workability is checked."),
    ("interface_mechanism_map.svg", "Interface Mechanism Map", "demulsification -> curing -> morphology -> bonding", "Solid arrows require matching FTIR/SEM/rheology evidence."),
    ("ftir_sem_evidence_pair.svg", "FTIR + SEM Evidence Pair", "chemical cue plus morphology cue", "FTIR alone should not carry the full mechanism claim."),
    ("moisture_aging_retention.svg", "Moisture-Aging Retention", "retention ratios across service screens", "Retention requires original strength and conditioning protocol."),
    ("storage_stability_timeline.svg", "Storage Stability Timeline", "1 d / 5 d / 7 d emulsion stability", "Storage stability must connect to bonding or workability."),
    ("pavement_layer_tackcoat.svg", "Pavement Layer Tack Coat", "substrate / tack coat / overlay system", "Construction relevance depends on substrate and application rate."),
    ("cement_hydration_evidence.svg", "Cement Hydration Evidence", "hydration products and pore refinement", "CCC claims require mechanism depth, not only strength."),
    ("lca_boundary_card.svg", "LCA Boundary Card", "functional unit and system boundary", "Sustainability claims need quantified boundary and comparison."),
    ("review_taxonomy_map.svg", "Review Taxonomy Map", "materials / tests / mechanisms / gaps", "A review figure should organize knowledge, not decorate it."),
]


def svg_asset(title: str, subtitle: str, boundary: str, index: int) -> str:
    width, height = 960, 620
    accent = [PALETTE["blue"], PALETTE["orange"], PALETTE["green"], PALETTE["gold"], PALETTE["red"]][index % 5]
    cards = []
    for i in range(4):
        x = 100 + i * 190
        y = 175 + (i % 2) * 120
        cards.append(
            f'<rect x="{x}" y="{y}" width="145" height="82" rx="16" fill="{accent}" opacity="{0.18 + i*0.08:.2f}" stroke="{accent}" stroke-width="2"/>'
        )
        cards.append(
            f'<circle cx="{x+35}" cy="{y+41}" r="{18+i*3}" fill="{accent}" opacity="0.55"/>'
        )
        cards.append(
            f'<text x="{x+78}" y="{y+46}" text-anchor="middle" font-family="DejaVu Sans" font-size="13" fill="{PALETTE["ink"]}">Step {i+1}</text>'
        )
        if i < 3:
            cards.append(
                f'<path d="M{x+148},{y+41} C{x+165},{y+35} {x+178},{y+35} {x+188},{y+41}" fill="none" stroke="{accent}" stroke-width="3" marker-end="url(#arrow)"/>'
            )
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            "<defs>",
            f'<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{accent}"/></marker>',
            "</defs>",
            f'<rect width="100%" height="100%" fill="{PALETTE["paper"]}"/>',
            f'<text x="{width/2}" y="42" text-anchor="middle" font-family="DejaVu Sans" font-size="18" font-weight="700" fill="{PALETTE["muted"]}">Materials Science Rich Gallery</text>',
            f'<text x="{width/2}" y="84" text-anchor="middle" font-family="DejaVu Sans" font-size="30" font-weight="700" fill="{PALETTE["ink"]}">{escape(title)}</text>',
            f'<text x="{width/2}" y="116" text-anchor="middle" font-family="DejaVu Sans" font-size="17" fill="{PALETTE["muted"]}">{escape(subtitle)}</text>',
            f'<rect x="78" y="145" width="804" height="270" rx="26" fill="#FFFFFF" stroke="{PALETTE["grid"]}" stroke-width="2"/>',
            *cards,
            f'<rect x="120" y="462" width="720" height="84" rx="18" fill="{accent}" opacity="0.12"/>',
            f'<text x="480" y="497" text-anchor="middle" font-family="DejaVu Sans" font-size="16" font-weight="700" fill="{PALETTE["ink"]}">Claim boundary</text>',
            f'<text x="480" y="526" text-anchor="middle" font-family="DejaVu Sans" font-size="15" fill="{PALETTE["ink"]}">{escape(boundary)}</text>',
            "</svg>",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1] / "assets" / "rich-gallery" / "generated"))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, (filename, title, subtitle, boundary) in enumerate(ASSETS):
        path = output_dir / filename
        path.write_text(svg_asset(title, subtitle, boundary, index), encoding="utf-8")
        print(path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
