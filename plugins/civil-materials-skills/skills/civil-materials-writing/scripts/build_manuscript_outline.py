#!/usr/bin/env python3
"""Build a civil-materials manuscript argument outline."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_outline(topic: str, paper_type: str, journal_family: str) -> str:
    return f"""# Civil Materials Manuscript Outline

Topic: {topic}
Paper type: {paper_type}
Journal family: {journal_family}

## One-sentence argument

Because the durability and mechanism basis of {topic} must be demonstrated under reviewer-safe conditions, this manuscript should connect material design, measured performance, mechanism evidence, and application boundary in one evidence chain.

## Claim-evidence-boundary table

| Claim | Evidence needed | Boundary |
|---|---|---|
| Modified emulsion improves bonding | Pull-off or shear bond strength with control and replicates | Valid only under reported curing and conditioning |
| Waterborne epoxy contributes to curing/network formation | FTIR plus SEM, fluorescence, rheology, or thermal evidence | Do not claim full mechanism from one technique |
| Material is durable | Moisture, aging, freeze-thaw, or service-condition retention | Field durability needs field or simulated-service validation |

## Abstract

Use background-gap-method-result-implication, with missing evidence marked.

## Introduction

Build the gap chain from tack coat bonding limitations to waterborne epoxy design rationale.

## Methods

Report materials, dosage, mixing, curing, test standards, replicate count, and statistics.

## Results and Discussion

Move from result to comparison to mechanism to limitation.

## Missing evidence to confirm

- exact material specifications,
- replicate count and statistics,
- wet or aged conditioning,
- mechanism evidence beyond a single spectrum,
- target-journal formatting and current author instructions.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--paper-type", default="experimental-manuscript")
    parser.add_argument("--journal-family", default="CBM")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_outline(args.topic, args.paper_type, args.journal_family), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
