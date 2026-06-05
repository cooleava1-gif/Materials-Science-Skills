#!/usr/bin/env python3
"""Generate review-first SVG templates for civil-materials small reviews."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
from textwrap import wrap


PALETTE = {
    "paper": "#FFFCF4",
    "ink": "#26302C",
    "muted": "#66736D",
    "line": "#DED6C6",
    "blue": "#3F6F8F",
    "orange": "#C87538",
    "green": "#477662",
    "gold": "#D5A04F",
    "red": "#B35A52",
    "sand": "#F2E7D2",
}


ASSETS = [
    {
        "filename": "review_framework_map.svg",
        "title": "Review Framework Map",
        "subtitle": "materials -> mechanisms -> performance -> durability -> gaps",
        "family": "review-taxonomy-map",
        "nodes": ["Materials", "Mechanisms", "Performance", "Durability", "Gaps"],
        "claim": "Organizes a small review scope; does not prove a material ranking.",
    },
    {
        "filename": "material_mechanism_performance_challenges.svg",
        "title": "Material-Mechanism-Performance-Challenge Map",
        "subtitle": "classification for review synthesis",
        "family": "review-taxonomy-map",
        "nodes": ["Modifiers", "Curing", "Bonding", "Service", "Challenges"],
        "claim": "Classification depends on search scope and cited evidence.",
    },
    {
        "filename": "evidence_chain_map.svg",
        "title": "Evidence Chain Map",
        "subtitle": "claim -> microstructure -> chemistry -> interface -> durability",
        "family": "interface-mechanism-map",
        "nodes": ["Claim", "Microstructure", "Chemistry", "Interface", "Durability"],
        "claim": "Arrows are hypotheses until supported by matched experiments.",
    },
    {
        "filename": "interface_mechanism_boundary.svg",
        "title": "Interface Mechanism Boundary",
        "subtitle": "droplet, curing, aggregate surface, water path",
        "family": "interface-mechanism-map",
        "nodes": ["Emulsion", "Epoxy", "Aggregate", "Water", "Bond"],
        "claim": "Mechanism strength requires FTIR, imaging, rheology, and bonding data.",
    },
    {
        "filename": "bonding_test_method_map.svg",
        "title": "Bonding Test Method Map",
        "subtitle": "substrate, tack coat rate, conditioning, loading, metric",
        "family": "test-matrix-standard",
        "nodes": ["Substrate", "Rate", "Curing", "Loading", "Metric"],
        "claim": "Cross-study comparison is limited when standards differ.",
    },
    {
        "filename": "dosage_viscosity_bonding_window.svg",
        "title": "Dosage-Viscosity-Bonding Window",
        "subtitle": "dosage, workability, bonding, storage stability",
        "family": "dosage-workability-window",
        "nodes": ["Dosage", "Viscosity", "Bonding", "Storage", "Window"],
        "claim": "Optimal dosage is conditional on workability and test protocol.",
    },
    {
        "filename": "ftir_sem_rheology_evidence_panel.svg",
        "title": "FTIR-SEM-Rheology Evidence Panel",
        "subtitle": "chemical cue, morphology cue, rheology cue",
        "family": "characterization-evidence-panel",
        "nodes": ["FTIR", "SEM/FM", "Rheology", "Bonding", "Limit"],
        "claim": "No single characterization method proves the full mechanism.",
    },
    {
        "filename": "durability_retention_challenge_map.svg",
        "title": "Durability Retention Challenge Map",
        "subtitle": "water, aging, freeze-thaw, heat, retained performance",
        "family": "durability-retention",
        "nodes": ["Water", "Aging", "Freeze", "Heat", "Retention"],
        "claim": "Retention needs baseline values, protocol, uncertainty, and failure mode.",
    },
    {
        "filename": "research_gap_matrix.svg",
        "title": "Research Gap Matrix",
        "subtitle": "mature lab evidence vs missing long-term validation",
        "family": "review-taxonomy-map",
        "nodes": ["Lab", "Field", "Mechanism", "Standards", "Gap"],
        "claim": "Gap strength depends on transparent screening and citation mapping.",
    },
    {
        "filename": "graphical_abstract_review.svg",
        "title": "Graphical Abstract for Review",
        "subtitle": "problem, material design, mechanism, performance, outlook",
        "family": "review-taxonomy-map",
        "nodes": ["Problem", "Design", "Mechanism", "Performance", "Outlook"],
        "claim": "Summary visual must not imply universal performance improvement.",
    },
]


def text_lines(text: str, width: int = 66) -> list[str]:
    return wrap(text, width=width) or [text]


def svg_text_block(x: int, y: int, text: str, *, size: int, color: str, weight: str = "400", width: int = 66) -> list[str]:
    lines = []
    for index, line in enumerate(text_lines(text, width=width)):
        lines.append(
            f'<text x="{x}" y="{y + index * (size + 7)}" font-family="DejaVu Sans, Arial, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}">{escape(line)}</text>'
        )
    return lines


def svg_asset(asset: dict[str, object], index: int) -> str:
    width, height = 1120, 720
    accents = [PALETTE["blue"], PALETTE["orange"], PALETTE["green"], PALETTE["gold"], PALETTE["red"]]
    accent = accents[index % len(accents)]
    nodes = [str(node) for node in asset["nodes"]]

    card_parts: list[str] = []
    for node_index, node in enumerate(nodes):
        x = 95 + node_index * 188
        y = 300 + (node_index % 2) * 34
        card_parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="140" height="88" rx="20" fill="#FFFFFF" stroke="{accent}" stroke-width="2"/>',
                f'<circle cx="{x + 30}" cy="{y + 34}" r="18" fill="{accent}" opacity="0.72"/>',
                f'<text x="{x + 30}" y="{y + 40}" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">{node_index + 1}</text>',
                f'<text x="{x + 82}" y="{y + 39}" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" font-weight="700" fill="{PALETTE["ink"]}">{escape(node)}</text>',
                f'<text x="{x + 82}" y="{y + 63}" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="11" fill="{PALETTE["muted"]}">template only</text>',
            ]
        )
        if node_index < len(nodes) - 1:
            y_mid = y + 44
            card_parts.append(
                f'<path d="M{x + 144},{y_mid} C{x + 158},{y_mid - 18} {x + 174},{y_mid - 18} {x + 184},{y_mid}" '
                f'fill="none" stroke="{accent}" stroke-width="3" marker-end="url(#arrow)"/>'
            )

    claim = str(asset["claim"])
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            "<defs>",
            f'<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{accent}"/></marker>',
            f'<linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{PALETTE["paper"]}"/><stop offset="100%" stop-color="{PALETTE["sand"]}"/></linearGradient>',
            "</defs>",
            '<rect width="100%" height="100%" fill="url(#wash)"/>',
            f'<circle cx="1030" cy="92" r="110" fill="{accent}" opacity="0.10"/>',
            f'<circle cx="88" cy="660" r="145" fill="{accent}" opacity="0.08"/>',
            f'<text x="560" y="54" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="18" font-weight="700" fill="{PALETTE["muted"]}">Civil Materials Review Assets</text>',
            f'<text x="560" y="104" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="34" font-weight="700" fill="{PALETTE["ink"]}">{escape(str(asset["title"]))}</text>',
            f'<text x="560" y="138" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="16" fill="{PALETTE["muted"]}">{escape(str(asset["subtitle"]))}</text>',
            f'<rect x="90" y="185" width="940" height="90" rx="24" fill="#FFFFFF" stroke="{PALETTE["line"]}" stroke-width="2"/>',
            f'<text x="126" y="222" font-family="DejaVu Sans, Arial, sans-serif" font-size="15" font-weight="700" fill="{accent}">source learning basis</text>',
            f'<text x="126" y="253" font-family="DejaVu Sans, Arial, sans-serif" font-size="18" fill="{PALETTE["ink"]}">{escape(str(asset["family"]))}; sanitized caption-family pattern; template only</text>',
            f'<rect x="70" y="286" width="980" height="180" rx="30" fill="#FFFFFF" opacity="0.72" stroke="{PALETTE["line"]}" stroke-width="2"/>',
            *card_parts,
            f'<rect x="115" y="520" width="890" height="118" rx="26" fill="{accent}" opacity="0.13" stroke="{accent}" stroke-width="2"/>',
            f'<text x="150" y="557" font-family="DejaVu Sans, Arial, sans-serif" font-size="16" font-weight="700" fill="{PALETTE["ink"]}">claim boundary</text>',
            *svg_text_block(150, 590, claim, size=17, color=PALETTE["ink"], weight="500", width=82),
            f'<text x="970" y="690" text-anchor="end" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" fill="{PALETTE["muted"]}">template only - replace with real data, standards, citations, and original images</text>',
            "</svg>",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parents[1] / "assets" / "review-first" / "generated"),
        help="Directory for generated SVG templates.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for index, asset in enumerate(ASSETS):
        path = output_dir / str(asset["filename"])
        path.write_text(svg_asset(asset, index), encoding="utf-8")
        print(path.name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
