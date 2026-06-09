#!/usr/bin/env python3
"""Audit sentence length and reviewer-risk language in civil-materials prose."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


RISK_RULES = [
    ("overclaim-proof", r"\b(prove|proved|proves|confirm|confirmed|demonstrate|demonstrated)\b", "Use only with direct evidence; otherwise use suggest/indicate/show."),
    ("absolute", r"\b(completely|fully|perfectly|entirely|always|never)\b", "Absolute wording is rarely reviewer-safe."),
    ("unsupported-sustainability", r"\b(environmentally friendly|green|eco-friendly|sustainable)\b", "State LCA/resource/emission boundary or soften the claim."),
    ("novelty-priority", r"\b(first|novel|new|unprecedented)\b", "Requires live literature support or a precise gap statement."),
    ("statistics", r"\b(significant|significantly)\b", "Use only when statistical significance is reported."),
    ("vague-quality", r"\b(excellent|good|obvious|remarkable|superior)\b", "Replace vague praise with measured comparison."),
    ("mechanism-risk", r"\b(mechanism was confirmed|confirmed the mechanism|proved the mechanism)\b", "Mechanism confirmation needs direct mechanism evidence."),
]


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def audit_sentence(sentence: str, max_words: int) -> dict[str, str] | None:
    words = re.findall(r"[A-Za-z0-9%./-]+", sentence)
    flags: list[str] = []
    advice: list[str] = []
    if len(words) > max_words:
        flags.append("long-sentence")
        advice.append(f"Split or tighten; {len(words)} words exceeds {max_words}.")
    lower = sentence.lower()
    for label, pattern, message in RISK_RULES:
        if re.search(pattern, lower):
            flags.append(label)
            advice.append(message)
    if not flags:
        return None
    return {
        "words": str(len(words)),
        "flags": ";".join(flags),
        "advice": " ".join(advice),
        "sentence": sentence,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="UTF-8 text file to audit")
    parser.add_argument("--max-words", type=int, default=30)
    parser.add_argument("--format", choices=["text", "csv"], default="text")
    parser.add_argument("--output", help="Optional output path for CSV format.")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8-sig")
    rows = []
    for idx, sentence in enumerate(split_sentences(text), 1):
        row = audit_sentence(sentence, args.max_words)
        if row:
            row["sentence_id"] = str(idx)
            rows.append(row)
    if args.format == "csv":
        output = Path(args.output or "civil-materials-language-audit.csv")
        with output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["sentence_id", "words", "flags", "advice", "sentence"])
            writer.writeheader()
            writer.writerows(rows)
        print(output)
        return 0
    for row in rows:
        print(f"Sentence {row['sentence_id']}: words={row['words']} flags={row['flags']}")
        print(row["advice"])
        print(row["sentence"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
