#!/usr/bin/env python3
"""Create a civil materials literature search and citation matrix CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


JOURNAL_ALIASES = {
    "CBM": "Construction and Building Materials",
    "CCC": "Cement and Concrete Composites",
    "JBE": "Journal of Building Engineering",
    "RMPD": "Road Materials and Pavement Design",
    "IJPE": "International Journal of Pavement Engineering",
    "CSCM": "Case Studies in Construction Materials",
}


DEFAULT_CLAIMS = [
    "Research gap and novelty",
    "Material design rationale",
    "Performance improvement",
    "Mechanism explanation",
    "Durability or service-condition relevance",
]


def split_items(value: str) -> list[str]:
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def read_claims(path: str | None) -> list[str]:
    if not path:
        return DEFAULT_CLAIMS
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    claims = [line.strip(" -\t") for line in lines if line.strip()]
    return claims or DEFAULT_CLAIMS


def build_query(topic: str, claim: str, journals: list[str]) -> str:
    journal_terms = " OR ".join(f'"{JOURNAL_ALIASES.get(j, j)}"' for j in journals)
    claim_terms = claim.replace("Research gap and novelty", "review OR recent progress")
    return f'("{topic}") AND ({claim_terms}) AND ({journal_terms})'


def evidence_type(claim: str) -> str:
    lower = claim.lower()
    if "mechanism" in lower or "机理" in lower:
        return "mechanism"
    if "durability" in lower or "service" in lower or "耐久" in lower:
        return "durability"
    if "performance" in lower or "strength" in lower or "粘结" in lower:
        return "performance"
    if "gap" in lower or "novelty" in lower:
        return "review/positioning"
    return "primary evidence"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Research topic or material system.")
    parser.add_argument("--journals", default="CBM,JBE,RMPD,IJPE", help="Comma-separated journal aliases.")
    parser.add_argument("--claims-file", help="Optional text file with one claim/evidence need per line.")
    parser.add_argument("--output", default="civil-materials-citation-matrix.csv")
    args = parser.parse_args()

    journals = split_items(args.journals)
    claims = read_claims(args.claims_file)
    rows = []
    for idx, claim in enumerate(claims, 1):
        rows.append(
            {
                "priority": "must-fix" if idx <= 2 else "strengthen",
                "claim_or_need": claim,
                "search_query": build_query(args.topic, claim, journals),
                "target_journals": "; ".join(journals),
                "evidence_type": evidence_type(claim),
                "candidate_source": "[search needed]",
                "status": "search needed",
                "manuscript_location": "[assign section]",
                "risk_note": "Do not make this claim until a confirmed source is mapped.",
            }
        )

    fieldnames = [
        "priority",
        "claim_or_need",
        "search_query",
        "target_journals",
        "evidence_type",
        "candidate_source",
        "status",
        "manuscript_location",
        "risk_note",
    ]
    with Path(args.output).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
