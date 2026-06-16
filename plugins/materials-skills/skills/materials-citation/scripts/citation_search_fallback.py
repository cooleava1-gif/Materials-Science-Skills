#!/usr/bin/env python3
"""Standalone materials citation search — no MCP dependency.

Queries CrossRef directly via stdlib (urllib) and produces a citation matrix CSV.
Use this script when the MCP server is not installed or unavailable.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

CROSSREF_API = "https://api.crossref.org/works"
USER_AGENT = "materials-citation-fallback/1.0 (mailto:unknown@example.com)"

JOURNAL_FAMILIES: dict[str, str] = {
    "CBM": "Construction and Building Materials",
    "CBM-TRANSPORTATION": "Construction and Building Materials in Transportation",
    "CCC": "Cement and Concrete Composites",
    "CCR": "Cement and Concrete Research",
    "CSCM": "Case Studies in Construction Materials",
    "JMCE": "Journal of Materials in Civil Engineering",
    "JBE": "Journal of Building Engineering",
    "MAS": "Materials and Structures",
    "JCP": "Journal of Cleaner Production",
    "RCR": "Resources, Conservation and Recycling",
    "FUEL": "Fuel",
    "MCR": "Magazine of Concrete Research",
    "RMPD": "Road Materials and Pavement Design",
    "IJPE": "International Journal of Pavement Engineering",
    "JRE": "Journal of Road Engineering",
}

DEFAULT_JOURNAL_FAMILIES = ("CBM", "CCC", "CCR", "JBE", "RMPD", "IJPE", "JRE", "CSCM", "JCP")

EVIDENCE_LAYER_KEYWORDS: dict[str, tuple[str, ...]] = {
    "material_formulation": (
        "waterborne epoxy", "epoxy resin", "epoxy dosage", "resin dosage",
        "formulation", "modifier content", "emulsifier", "mix design", "material design",
    ),
    "emulsion_stability": (
        "emulsion stability", "storage stability", "zeta potential", "particle size",
        "settlement", "segregation", "sieve residue", "stability test",
    ),
    "bonding_interface_performance": (
        "bonding", "bond strength", "pull-off", "interface", "interlayer",
        "adhesion", "adhesive", "tack coat", "shear strength", "direct tension",
    ),
    "rheology": (
        "rheology", "rheological property", "viscosity", "brookfield",
        "flow curve", "shear rate", "dsr", "dynamic shear rheometer",
    ),
    "curing_demulsification": (
        "demulsification", "demulsify", "breaking behavior", "breaking rate",
        "emulsion breaking", "epoxy curing", "curing reaction", "crosslink",
        "cross-link", "amine", "epoxy network", "gel time", "phase compatibility",
    ),
    "microstructure_chemistry": (
        "ftir", "fourier transform infrared", "sem", "scanning electron microscopy",
        "fluorescence", "microscopy", "afm", "chemical bond", "functional group",
        "microstructure", "phase morphology",
    ),
    "moisture_aging_durability": (
        "moisture", "water damage", "aging", "ageing", "freeze-thaw",
        "freeze thaw", "durability", "fatigue", "rutting",
    ),
    "service_field_relevance": (
        "service condition", "field performance", "field trial", "road construction",
        "pavement construction", "field construction", "traffic", "pavement section", "in situ",
    ),
    "review_background": (
        "review", "recent progress", "state of the art", "research gap",
        "knowledge gap", "bibliometric",
    ),
}

MECHANISM_LAYERS = {"curing_demulsification", "microstructure_chemistry"}
DURABILITY_LAYERS = {"moisture_aging_durability", "service_field_relevance"}
PERFORMANCE_LAYERS = {
    "bonding_interface_performance", "emulsion_stability", "rheology",
    "curing_demulsification", "material_formulation",
}

DEFAULT_CLAIMS = [
    "Research gap and novelty",
    "Material design rationale",
    "Performance improvement",
    "Mechanism explanation",
    "Durability or service-condition relevance",
]

CSV_FIELDS = [
    "claim_id", "priority", "claim_or_need", "evidence_layer",
    "source_role", "source_quality", "mechanism_directness",
    "durability_relevance", "service_relevance", "reader_anchor",
    "figure_handoff", "reviewer_risk", "search_query", "target_journals",
    "evidence_type", "candidate_source", "candidate_doi", "candidate_year",
    "status", "manuscript_location", "risk_note",
]


def _normalize(text: str | None) -> str:
    return " ".join((text or "").lower().replace("_", " ").split())


def _contains_keyword(text: str, keyword: str) -> bool:
    kw = _normalize(keyword)
    if not kw:
        return False
    return re.search(rf"(?<![a-z0-9]){re.escape(kw)}(?![a-z0-9])", text) is not None


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(_contains_keyword(text, k) for k in keywords)


def expand_journal_terms(aliases: list[str]) -> list[str]:
    expanded: list[str] = []
    for alias in aliases:
        norm = _normalize(alias).replace("-", " ").replace("_", " ")
        canonical = JOURNAL_FAMILIES.get(alias.upper())
        if canonical and canonical not in expanded:
            expanded.append(canonical)
        elif alias.strip() and alias.strip() not in expanded:
            expanded.append(alias.strip())
    return expanded or [JOURNAL_FAMILIES[k] for k in DEFAULT_JOURNAL_FAMILIES]


def classify_evidence_layers(text: str) -> list[str]:
    normalized = _normalize(text)
    if not normalized:
        return []
    return [
        layer for layer, keywords in EVIDENCE_LAYER_KEYWORDS.items()
        if _contains_any(normalized, keywords)
    ]


def evidence_type_for_claim(text: str) -> str:
    normalized = _normalize(text)
    layers = set(classify_evidence_layers(normalized))
    if _contains_any(normalized, ("mechanism", "microstructure", "chemical", "ftir")):
        return "mechanism"
    if layers & MECHANISM_LAYERS:
        return "mechanism"
    if _contains_any(normalized, ("durability", "moisture", "aging", "freeze", "service")):
        return "durability"
    if layers & DURABILITY_LAYERS:
        return "durability"
    if _contains_any(normalized, ("review", "gap", "progress", "state of the art")):
        return "review/positioning"
    if layers & PERFORMANCE_LAYERS:
        return "performance"
    return "primary evidence"


def _default_layer(evidence_type: str) -> str:
    mapping = {
        "mechanism": "microstructure_chemistry",
        "durability": "moisture_aging_durability",
        "review/positioning": "review_background",
        "performance": "bonding_interface_performance",
    }
    return mapping.get(evidence_type, "material_formulation")


def _source_role(evidence_type: str) -> str:
    return "review evidence" if evidence_type == "review/positioning" else "primary experimental evidence"


def _mechanism_directness(evidence_type: str) -> str:
    return "direct mechanism evidence needed" if evidence_type == "mechanism" else "not a mechanism claim"


def _durability_relevance(evidence_type: str, layer: str) -> str:
    if evidence_type == "durability" or layer in DURABILITY_LAYERS:
        return "direct durability evidence needed"
    return "not a durability claim"


def _service_relevance(layer: str) -> str:
    return "direct service or field evidence needed" if layer == "service_field_relevance" else "lab-scale unless field evidence is mapped"


def split_items(value: str) -> list[str]:
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def read_claims(path: str | None) -> list[str]:
    if not path:
        return DEFAULT_CLAIMS
    claims_path = Path(path)
    if not claims_path.exists():
        raise FileNotFoundError(f"claims file not found: {path}")
    lines = claims_path.read_text(encoding="utf-8").splitlines()
    claims = [line.strip(" -\t") for line in lines if line.strip()]
    return claims or DEFAULT_CLAIMS


def crossref_search(query: str, rows: int = 5) -> list[dict]:
    params = {
        "query": query,
        "rows": str(rows),
        "select": "DOI,title,author,container-title,published-print,published-online,"
                  "volume,issue,page,ISSN,abstract,type",
    }
    url = f"{CROSSREF_API}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("message", {}).get("items", [])
        return items
    except (URLError, json.JSONDecodeError, OSError) as exc:
        print(f"  CrossRef query failed: {exc}", file=sys.stderr)
        return []


def extract_year(item: dict) -> str:
    for key in ("published-print", "published-online"):
        parts = item.get(key, {}).get("date-parts", [[]])
        if parts and parts[0] and parts[0][0]:
            return str(parts[0][0])
    return ""


def extract_authors(item: dict) -> str:
    authors = item.get("author", [])
    if not authors:
        return "Unknown"
    names = []
    for a in authors[:3]:
        family = a.get("family", "")
        given = a.get("given", "")
        names.append(f"{family} {given}".strip())
    if len(authors) > 3:
        names.append("et al.")
    return "; ".join(names)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Research topic or material system.")
    parser.add_argument("--journals", default="CBM,JBE,RMPD,IJPE", help="Comma-separated journal aliases.")
    parser.add_argument("--claims-file", help="Optional text file with one claim per line.")
    parser.add_argument("--output", default="materials-citation-matrix.csv")
    parser.add_argument("--max-per-claim", type=int, default=3, help="Max CrossRef results per claim.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between CrossRef queries (seconds).")
    args = parser.parse_args()

    topic = args.topic.strip()
    if not topic:
        raise ValueError("--topic must not be empty")

    journals = split_items(args.journals)
    journal_terms = expand_journal_terms(journals)
    claims = read_claims(args.claims_file)
    rows = []

    for idx, claim in enumerate(claims, 1):
        evidence_type = evidence_type_for_claim(claim)
        layer = (classify_evidence_layers(claim) or [_default_layer(evidence_type)])[0]

        journal_query = " OR ".join(f'"{j}"' for j in journal_terms)
        claim_query = claim.replace("Research gap and novelty", "review OR recent progress")
        query = f'("{topic}") AND ({claim_query}) AND ({journal_query})'

        print(f"[{idx}/{len(claims)}] Searching: {claim[:60]}...")
        items = crossref_search(query, rows=args.max_per_claim)

        if items:
            for item in items:
                title = (item.get("title") or [""])[0]
                journal = (item.get("container-title") or [""])[0]
                doi = item.get("DOI", "")
                year = extract_year(item)
                authors = extract_authors(item)

                rows.append({
                    "claim_id": f"CIT-{idx:03d}",
                    "priority": "must-fix" if idx <= 2 else "strengthen",
                    "claim_or_need": claim,
                    "evidence_layer": layer,
                    "source_role": _source_role(evidence_type),
                    "source_quality": "screening needed",
                    "mechanism_directness": _mechanism_directness(evidence_type),
                    "durability_relevance": _durability_relevance(evidence_type, layer),
                    "service_relevance": _service_relevance(layer),
                    "reader_anchor": "[reader anchor needed]",
                    "figure_handoff": "not assessed",
                    "reviewer_risk": "must-fix" if idx <= 2 else "strengthen",
                    "search_query": query,
                    "target_journals": "; ".join(journal_terms),
                    "evidence_type": evidence_type,
                    "candidate_source": f"{authors}. {title}. {journal}, {year}.",
                    "candidate_doi": doi,
                    "candidate_year": year,
                    "status": "candidate found",
                    "manuscript_location": "[assign section]",
                    "risk_note": "Inspect abstract/publisher page before citing.",
                })
        else:
            rows.append({
                "claim_id": f"CIT-{idx:03d}",
                "priority": "must-fix" if idx <= 2 else "strengthen",
                "claim_or_need": claim,
                "evidence_layer": layer,
                "source_role": _source_role(evidence_type),
                "source_quality": "screening needed",
                "mechanism_directness": _mechanism_directness(evidence_type),
                "durability_relevance": _durability_relevance(evidence_type, layer),
                "service_relevance": _service_relevance(layer),
                "reader_anchor": "[reader anchor needed]",
                "figure_handoff": "not assessed",
                "reviewer_risk": "must-fix" if idx <= 2 else "strengthen",
                "search_query": query,
                "target_journals": "; ".join(journal_terms),
                "evidence_type": evidence_type,
                "candidate_source": "[no result found]",
                "candidate_doi": "",
                "candidate_year": "",
                "status": "search needed",
                "manuscript_location": "[assign section]",
                "risk_note": "Do not make this claim until a confirmed source is mapped.",
            })

        if idx < len(claims):
            time.sleep(args.delay)

    with Path(args.output).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nOutput: {args.output} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
