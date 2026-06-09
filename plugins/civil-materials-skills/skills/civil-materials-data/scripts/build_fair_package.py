#!/usr/bin/env python3
"""Build a civil-materials FAIR dataset package scaffold."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CSV_HEADER = "sample_id,formulation_id,asphalt_type,emulsifier_type,waterborne_epoxy_type,epoxy_dosage,binder_type,water_binder_ratio,curing_condition,demulsification_condition,test_standard,temperature,humidity,aging_condition,replicate_count,measured_property,value,unit,raw_or_processed,processing_note\n"


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return cleaned[:70] or "civil_materials_dataset"


def build_package(topic: str, domain: str, journal: str, output_dir: Path) -> Path:
    package_dir = output_dir / f"{slug(topic)}_{journal.lower()}_fair_package"
    raw_dir = package_dir / "raw_data"
    processed_dir = package_dir / "processed_data"
    figures_dir = package_dir / "figures"
    for directory in (raw_dir, processed_dir, figures_dir):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ".gitkeep").write_text("", encoding="utf-8")

    (raw_dir / "experiment_data_template.csv").write_text(CSV_HEADER, encoding="utf-8")
    (package_dir / "metadata.md").write_text(metadata(topic, domain, journal), encoding="utf-8")
    (package_dir / "README.md").write_text(readme(topic, journal), encoding="utf-8")
    (package_dir / "data_availability_statement.md").write_text(data_availability(journal), encoding="utf-8")
    (package_dir / "fair_audit.md").write_text(fair_audit(), encoding="utf-8")
    return package_dir


def metadata(topic: str, domain: str, journal: str) -> str:
    return f"""# Dataset Metadata

## Study Identity

- topic: {topic}
- material_domain: {domain}
- target_journal: {journal}
- manuscript_section: [needs confirmation]
- data_contact: [needs confirmation]
- repository_or_supplement_url: [needs confirmation]

## Civil Materials Fields

- sample_id: [stable sample identifier]
- formulation_id: [mix or binder formulation identifier]
- asphalt_type: [needs confirmation]
- emulsifier_type: [needs confirmation]
- waterborne_epoxy_type: [needs confirmation]
- epoxy_dosage: [needs confirmation]
- binder_type: [needs confirmation]
- water_binder_ratio: [needs confirmation]
- curing_condition: [needs confirmation]
- demulsification_condition: [needs confirmation]
- test_standard: [needs confirmation]
- temperature: [needs confirmation]
- humidity: [needs confirmation]
- aging_condition: [needs confirmation]
- replicate_count: [needs confirmation]

## Processing

- raw_data_location: raw_data/
- processed_data_location: processed_data/
- figure_data_location: figures/
- processing_note: [needs confirmation]
- uncertainty_type: [SD/SE/CI/not applicable]
"""


def readme(topic: str, journal: str) -> str:
    return f"""# Dataset README

## Topic

{topic}

## Target Journal

{journal}

## Folder Structure

- `raw_data/`: original experimental records or instrument-export tables.
- `processed_data/`: cleaned, averaged, normalized, or figure-ready tables.
- `figures/`: figure files or figure-ready assets.
- `metadata.md`: sample, condition, unit, and processing metadata.
- `data_availability_statement.md`: manuscript-ready data availability language.
- `fair_audit.md`: FAIR checklist result.

## Reuse Notes

Check units, test_standard, replicate_count, temperature, humidity, curing_condition, and aging_condition before reusing this dataset.
"""


def data_availability(journal: str) -> str:
    return f"""# Data Availability Statement

For {journal} submission: Data supporting the findings of this study are provided in the accompanying dataset package, including raw experimental records, processed tables, figure-ready data, metadata, and processing notes.

If some raw files cannot be shared publicly, replace this with a request-only or mixed-availability statement and explain the access constraint.
"""


def fair_audit() -> str:
    return """# FAIR Audit

| FAIR item | Status | Evidence | Action |
|---|---|---|---|
| Findable | pass | metadata.md and README.md are present | Confirm repository URL if public |
| Accessible | pass | data_availability_statement.md is present | Confirm access constraints |
| Interoperable | pass | CSV template is present in raw_data | Add processed CSV after analysis |
| Reusable | pass | units, standards, replicates, and conditions are represented in metadata | Replace placeholders with confirmed values |
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--domain", default="asphalt")
    parser.add_argument("--journal", default="generic")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    package_dir = build_package(args.topic, args.domain, args.journal, Path(args.output_dir))
    print(package_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
