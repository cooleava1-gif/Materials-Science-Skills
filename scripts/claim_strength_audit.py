#!/usr/bin/env python3
"""Claim-strength audit engine for materials science manuscripts.

Scans manuscript text for overclaim vocabulary, missing evidence markers,
and claim-evidence mismatches.  Works with or without LLM assistance.

Usage:
    python scripts/claim_strength_audit.py --text "The mechanism was confirmed..."
    python scripts/claim_strength_audit.py --file manuscript.txt
    python scripts/claim_strength_audit.py --file manuscript.txt --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = REPO_ROOT / "_shared" / "material-registry" / "entries"


# ── Overclaim patterns ────────────────────────────────────────────────────
# Each entry: (description, regex_pattern, suggested_replacement)

OVERCLAIM_PATTERNS: list[tuple[str, str, str]] = [
    # Absolute certainty
    ("proves",        r"\bproves?\b",                          "suggests / is consistent with"),
    ("confirmed",     r"\bconfirms?\b",                         "indicates / supports"),
    ("demonstrates",  r"\bdemonstrates?\b(?!\s+that)",          "shows / indicates"),
    ("is caused by",  r"\bis caused by\b",                      "may be attributed to"),
    ("is the result of", r"\bis the result of\b",               "is consistent with"),

    # Statistical overclaim
    ("significantly improves (no p-value)", r"\bsignificantly\s+(improves?|increases?|reduces?|decreases?)\b",
     "improves/increases (add p-value or use 'notably')"),
    ("significantly higher (no p-value)",  r"\bsignificantly\s+(higher|lower|better|worse)\b",
     "higher/lower (add p-value or use 'markedly')"),

    # Novelty laundering
    ("first (unqualified)",   r"\bfirst(?:-of-its-kind|-ever)?\s+(report|study|demonstrate|synthesize|fabricate)\b",
     "precisely state what is new and cite prior work"),
    ("novel (unqualified)",   r"\bnovel\s+(approach|method|material|composite|system)\b(?!\s+\w)",
     "describe the specific difference from prior work"),

    # Mechanism overclaim
    ("mechanism confirmed (insufficient)", r"\bmechanism\s+(was|is)\s+(confirmed|demonstrated|proven|elucidated)\b",
     "mechanism is inferred / consistent with"),
    ("FTIR confirms (mechanism alone)",    r"\bFTIR\s+(confirm|prove|demonstrate)s?\b",
     "FTIR suggests / is consistent with"),
    ("XRD confirms (mechanism alone)",     r"\bXRD\s+(confirm|prove|demonstrate)s?\b",
     "XRD indicates"),

    # Sustainability overclaim
    ("green (unqualified)",   r"\b(green|environmentally friendly|eco-friendly)\s+(material|composite|product|solution)\b",
     "describe the environmental attribute precisely; avoid 'green' without LCA"),
    ("sustainable (unqualified)", r"\bsustainable\s+(material|composite|product|solution)\b",
     "'potentially sustainable' only if LCA boundary is stated"),
    ("low-carbon (unqualified)", r"\blow-carbon\s+(material|binder|concrete|cement)\b",
     "report carbon reduction with functional unit and boundary"),

    # Universal / field-ready claims
    ("field-ready (unqualified)", r"\b(field-ready|ready for field application|suitable for (field|engineering) application)\b",
     "pending field or simulated-service validation"),
    ("universal (overclaim)",    r"\b(universal|all-purpose|wide-ranging)\s+(application|solution|approach)\b",
     "describe the specific application range"),

    # Durability overclaim
    ("durability proven (single test)", r"\bdurability\s+(was|is)\s+(confirmed|demonstrated|proven)\b",
     "durability was assessed under [specified conditions]"),
    ("proves moisture resistance",      r"\bproves?\s+(moisture|water|aging|freeze-thaw)\s+resistance\b",
     "indicates improved resistance under tested conditions"),
]

# ── Downgrade lookup (from claim-strength-ladder.md) ──────────────────────

DOWNGRADE_MAP: dict[str, str] = {
    "proves": "suggests",
    "proved": "suggested",
    "proven": "suggested / supported",
    "confirmed": "indicated",
    "demonstrates": "indicates",
    "significantly improves": "improves (or add p-value)",
    "environmentally friendly": "potentially sustainable (with boundary)",
    "first": "precise gap (with literature check)",
}

MISSING_EVIDENCE_PATTERNS: list[tuple[str, str]] = [
    ("needs quantitative result", r"\[needs quantitative result\]"),
    ("needs control group",       r"\[needs control group\]"),
    ("needs mechanism evidence",  r"\[needs mechanism evidence\]"),
    ("needs evidence",            r"\[needs evidence:[^\]]*\]"),
    ("needs verification",        r"\[needs verification:[^\]]*\]"),
]


def scan_text(text: str) -> list[dict[str, Any]]:
    """Scan *text* for overclaim patterns and missing evidence markers.

    Returns a list of findings sorted by severity.
    """
    findings: list[dict[str, Any]] = []

    # --- Overclaim vocabulary scan ---
    for name, pattern, suggestion in OVERCLAIM_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Get surrounding context
            start = max(0, match.start() - 60)
            end = min(len(text), match.end() + 60)
            context = text[start:end].replace("\n", " ")
            # Trim to reasonable length
            if len(context) > 80:
                context = "..." + context.strip()[:80] + "..."

            findings.append({
                "type": "overclaim",
                "severity": "high" if name in ("proves", "confirmed", "mechanism confirmed (insufficient)",
                                                "first (unqualified)", "field-ready (unqualified)")
                             else "medium",
                "pattern": name,
                "match": match.group(),
                "suggestion": suggestion,
                "context": context.strip(),
                "position": match.start(),
            })

    # --- Missing evidence markers ---
    for name, pattern in MISSING_EVIDENCE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            findings.append({
                "type": "missing_evidence",
                "severity": "high",
                "pattern": name,
                "match": match.group(),
                "suggestion": "Provide the missing evidence before submission",
                "context": match.group(),
                "position": match.start(),
            })

    # Sort: high severity first, then by position
    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (severity_order.get(f["severity"], 99), f["position"]))
    return findings


def suggest_downgrades(text: str) -> list[dict[str, Any]]:
    """Find sentences where direct downgrades from claim-strength-ladder apply."""
    suggestions: list[dict[str, Any]] = []
    for word, replacement in DOWNGRADE_MAP.items():
        pattern = rf"\b{re.escape(word)}\b"
        for match in re.finditer(pattern, text, re.IGNORECASE):
            suggestions.append({
                "type": "downgrade",
                "severity": "medium",
                "pattern": word,
                "match": match.group(),
                "suggestion": f"Downgrade to: {replacement}",
                "position": match.start(),
            })
    return suggestions


def audit_text(text: str, material_ids: list[str] | None = None) -> dict[str, Any]:
    """Full audit of *text*.

    If *material_ids* are provided, cross-reference with registry claim_types.
    """
    findings = scan_text(text)
    downgrades = suggest_downgrades(text)
    all_issues = findings + downgrades

    # --- Registry cross-reference ---
    registry_notes: list[str] = []
    if material_ids:
        for mid in material_ids:
            path = REGISTRY_DIR / f"{mid}.yaml"
            if path.exists():
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                name = data.get("name", mid)
                for ct in data.get("claim_types", []) or []:
                    if isinstance(ct, dict):
                        risks = ct.get("common_risks", []) or []
                        for risk in risks:
                            # Check if text contains elements of this risk
                            if isinstance(risk, str) and any(kw in text.lower() for kw in risk.lower().split()[:3]):
                                registry_notes.append({
                                    "material": name,
                                    "claim_type": ct.get("type", ""),
                                    "risk": risk,
                                })

    # Split on sentence terminators followed by whitespace or end of string.
    sentence_count = len(
        [s for s in re.split(r"[.!?]+(?:\s+|$)", text) if s.strip()]
    )

    return {
        "text_length": len(text),
        "sentence_count": sentence_count,
        "total_issues": len(all_issues),
        "high_severity": sum(1 for i in all_issues if i.get("severity") == "high"),
        "findings": all_issues,
        "registry_alerts": registry_notes,
        "score": _compute_score(all_issues),
    }


def _compute_score(findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute an overall claim-strength score (0-100, higher = better)."""
    high = sum(1 for f in findings if f.get("severity") == "high" and f.get("type") == "overclaim")
    medium = sum(1 for f in findings if f.get("severity") == "medium" and f.get("type") == "overclaim")
    missing = sum(1 for f in findings if f.get("type") == "missing_evidence")

    deductions = high * 15 + medium * 5 + missing * 10
    score = max(0, 100 - deductions)

    if score >= 90:
        level = "excellent"
    elif score >= 70:
        level = "acceptable"
    elif score >= 40:
        level = "needs_revision"
    else:
        level = "problematic"

    return {"score": score, "level": level}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Text to audit")
    parser.add_argument("--file", help="Read text from file")
    parser.add_argument("--material", nargs="*", help="Material id(s) for registry cross-reference")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args(argv)

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return 1

    result = audit_text(text, material_ids=args.material)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Claim Strength Audit")
        print(f"{'=' * 60}")
        print(f"Score: {result['score']['score']}/100 ({result['score']['level']})")
        print(f"Issues: {result['total_issues']} ({result['high_severity']} high severity)")
        print()
        if result["findings"]:
            for f in result["findings"]:
                badge = "[HIGH]" if f["severity"] == "high" else "[MED]"
                ftype = f.get("type", f.get("pattern", "unknown"))
                label = f.get("pattern") or f.get("word", ftype)
                print(f"  {badge} [{f['severity'].upper()}] {ftype}: {label}")
                if f.get("match"):
                    print(f"     Found: {f['match']}")
                if f.get("suggestion"):
                    print(f"     Suggestion: {f['suggestion']}")
                if f.get("context"):
                    print(f"     Context: {f['context'][:100]}")
                print()
        if result["registry_alerts"]:
            print(f"Registry Alerts ({len(result['registry_alerts'])}):")
            for ra in result["registry_alerts"]:
                print(f"  {ra['material']} / {ra['claim_type']}: {ra['risk']}")

    return 0 if result["score"]["level"] in ("excellent", "acceptable") else 1


if __name__ == "__main__":
    raise SystemExit(main())
