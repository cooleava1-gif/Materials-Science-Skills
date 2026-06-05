#!/usr/bin/env python3
"""Create a civil materials literature search and citation matrix CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


MCP_ROOT = Path(__file__).resolve().parents[1] / "mcp"
sys.path.insert(0, str(MCP_ROOT))

from academic_search.domain.classifier import evidence_type_for_claim
from academic_search.domain.journals import expand_journal_terms


DEFAULT_CLAIMS = [
    "Research gap and novelty",
    "Material design rationale",
    "Performance improvement",
    "Mechanism explanation",
    "Durability or service-condition relevance",
]


def split_items(value: str) -> list[str]:
    items = []
    for item in value.replace(";", ",").split(","):
        cleaned = item.strip()
        if cleaned and cleaned not in items:
            items.append(cleaned)
    return items


def read_claims(path: str | None) -> list[str]:
    if not path:
        return DEFAULT_CLAIMS
    claims_path = Path(path)
    if not claims_path.exists():
        raise FileNotFoundError(f"claims file not found: {path}")
    lines = claims_path.read_text(encoding="utf-8").splitlines()
    claims = [line.strip(" -\t") for line in lines if line.strip()]
    return claims or DEFAULT_CLAIMS


def build_query(topic: str, claim: str, journals: list[str]) -> str:
    journal_terms = " OR ".join(f'"{journal}"' for journal in expand_journal_terms(journals))
    claim_terms = claim.replace("Research gap and novelty", "review OR recent progress")
    return f'("{topic}") AND ({claim_terms}) AND ({journal_terms})'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Research topic or material system.")
    parser.add_argument("--journals", default="CBM,JBE,RMPD,IJPE", help="Comma-separated journal aliases.")
    parser.add_argument("--claims-file", help="Optional text file with one claim/evidence need per line.")
    parser.add_argument("--output", default="civil-materials-citation-matrix.csv")
    args = parser.parse_args()

    topic = args.topic.strip()
    if not topic:
        raise ValueError("--topic must not be empty")

    journals = split_items(args.journals)
    journal_terms = expand_journal_terms(journals)
    claims = read_claims(args.claims_file)
    rows = []
    for idx, claim in enumerate(claims, 1):
        rows.append(
            {
                "priority": "must-fix" if idx <= 2 else "strengthen",
                "claim_or_need": claim,
                "search_query": build_query(topic, claim, journals),
                "target_journals": "; ".join(journal_terms),
                "evidence_type": evidence_type_for_claim(claim),
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
