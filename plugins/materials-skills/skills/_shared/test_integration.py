#!/usr/bin/env python3
"""Integration tests: doe -> data -> writing full-chain data flow.

Verifies that experiment-record.yaml serves as a correct data bus
shared across materials-doe, materials-data, and materials-writing skills.

These tests:
  - Use subprocess.run to call each script.
  - Use tempfile.TemporaryDirectory for scratch space.
  - Do NOT depend on external network or MCP services.
  - Must be run from the project root directory.
"""

from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

# ---------------------------------------------------------------------------
# Path constants (relative to project root)
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[4]  # _shared -> skills -> materials-skills -> plugins -> project root
SHARED_DIR = PROJECT_ROOT / "plugins" / "materials-skills" / "skills" / "_shared"
VALIDATE_SCRIPT = SHARED_DIR / "validate_experiment_record.py"
BUILD_FAIR_SCRIPT = PROJECT_ROOT / "plugins" / "materials-skills" / "skills" / "materials-data" / "scripts" / "build_fair_package.py"
BUILD_OUTLINE_SCRIPT = PROJECT_ROOT / "plugins" / "materials-skills" / "skills" / "materials-writing" / "scripts" / "build_manuscript_outline.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_generic_record() -> Dict[str, Any]:
    """Return a valid experiment-record dict with domain-neutral content.

    Uses 3 factors, 2 response variables, and 9 runs (L9-style).
    Design type is 'custom' because the JSON Schema enum does not include
    'orthogonal'; 'custom' is the correct way to represent it.
    """
    factor_names = ["factor_A", "factor_B", "factor_C"]
    levels = [1, 2, 3]

    runs: List[Dict[str, Any]] = []
    # L9 orthogonal array: 9 runs, 3 factors, 3 levels each
    l9_array = [
        (1, 1, 1), (1, 2, 2), (1, 3, 3),
        (2, 1, 2), (2, 2, 3), (2, 3, 1),
        (3, 1, 3), (3, 2, 1), (3, 3, 2),
    ]
    for idx, (a, b, c) in enumerate(l9_array, start=1):
        runs.append({
            "run_id": f"R{idx}",
            "factor_levels": {
                "factor_A": levels[a - 1],
                "factor_B": levels[b - 1],
                "factor_C": levels[c - 1],
            },
        })

    return {
        "version": "1.0.0",
        "record_type": "experiment-design",
        "study_id": "integration-test-001",
        "title": "Generic integration test study",
        "created_by": "test-suite",
        "created_at": "2026-06-30",
        "factors": [
            {"name": "factor_A", "type": "continuous", "unit": "degC", "levels": levels},
            {"name": "factor_B", "type": "continuous", "unit": "MPa", "levels": levels},
            {"name": "factor_C", "type": "continuous", "unit": "wt%", "levels": levels},
        ],
        "response_variables": [
            {"name": "response_X", "unit": "MPa"},
            {"name": "response_Y", "unit": "%"},
        ],
        "design": {
            "type": "custom",
            "notes": "L9 orthogonal array",
            "runs": runs,
        },
    }


def _write_record(tmpdir: Path, record: Dict[str, Any], name: str = "experiment-record.yaml") -> Path:
    """Write a record dict to a YAML file and return the path."""
    path = tmpdir / name
    path.write_text(yaml.dump(record, default_flow_style=False, allow_unicode=True), encoding="utf-8")
    return path


def _run_script(script_path: Path, args: List[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run a Python script via subprocess.run and return the CompletedProcess."""
    cmd = [sys.executable, str(script_path)] + args
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or PROJECT_ROOT,
        encoding="utf-8",
    )


def _make_domain_record(
    domain: str,
    family: str,
    factors: List[Dict[str, Any]],
    responses: List[Dict[str, str]],
) -> Dict[str, Any]:
    """Build a valid experiment record for a given materials domain."""
    factor_names = [f["name"] for f in factors]
    runs: List[Dict[str, Any]] = []
    # Generate 4 simple runs using the first level of each factor
    for idx in range(1, 5):
        fl = {}
        for f in factors:
            lvls = f.get("levels", [1, 2])
            fl[f["name"]] = lvls[(idx - 1) % len(lvls)]
        runs.append({"run_id": f"R{idx}", "factor_levels": fl})

    return {
        "version": "1.0.0",
        "record_type": "experiment-design",
        "study_id": f"cross-domain-{domain}-001",
        "title": f"Cross-domain test: {domain}",
        "created_by": "test-suite",
        "created_at": "2026-06-30",
        "direction_profile": {
            "domain": domain,
            "material_family": family,
        },
        "factors": factors,
        "response_variables": responses,
        "design": {
            "type": "full-factorial",
            "runs": runs,
        },
    }


# ---------------------------------------------------------------------------
# Test 1: doe -> data chain
# ---------------------------------------------------------------------------

class TestDoeToDataChain:
    """Verify that an experiment-record generated by doe can be consumed
    by data's build_fair_package.py."""

    def test_doe_to_data_chain(self) -> None:
        record = _make_generic_record()

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            record_path = _write_record(tmpdir, record)

            # Step 1: validate the record with --strict
            result_val = _run_script(VALIDATE_SCRIPT, [str(record_path), "--strict"])
            assert result_val.returncode == 0, (
                f"validate_experiment_record.py failed:\n"
                f"stdout: {result_val.stdout}\nstderr: {result_val.stderr}"
            )
            report = json.loads(result_val.stdout)
            assert report["valid"] is True

            # Step 2: call build_fair_package.py with the record
            output_dir = tmpdir / "fair_output"
            output_dir.mkdir()
            result_fair = _run_script(BUILD_FAIR_SCRIPT, [
                "--topic", "Generic materials integration test",
                "--output-dir", str(output_dir),
                "--experiment-record", str(record_path),
            ])
            assert result_fair.returncode == 0, (
                f"build_fair_package.py failed:\n"
                f"stdout: {result_fair.stdout}\nstderr: {result_fair.stderr}"
            )

            # Step 3: verify generated directory structure
            # The script prints the package_dir path; find it
            package_dir_name = result_fair.stdout.strip().split("\n")[-1].strip()
            package_dir = Path(package_dir_name)
            assert package_dir.is_dir(), f"Package dir not found: {package_dir}"

            expected_files = [
                package_dir / "raw_data" / "experiment_data_template.csv",
                package_dir / "metadata.md",
                package_dir / "README.md",
                package_dir / "fair_audit.md",
            ]
            for fpath in expected_files:
                assert fpath.exists(), f"Expected file missing: {fpath}"

            # Step 4: verify CSV columns contain factor/response names (not hardcoded)
            csv_path = package_dir / "raw_data" / "experiment_data_template.csv"
            csv_text = csv_path.read_text(encoding="utf-8")
            reader = csv.reader(io.StringIO(csv_text))
            headers = next(reader)

            factor_names = [f["name"] for f in record["factors"]]
            response_names = [r["name"] for r in record["response_variables"]]
            for name in factor_names + response_names:
                assert name in headers, (
                    f"CSV header missing expected column '{name}'. "
                    f"Got headers: {headers}"
                )

            # Ensure no hardcoded asphalt-specific columns
            hardcoded_cols = ["asphalt_content", "binder_type", "modifier_dosage"]
            for col in hardcoded_cols:
                assert col not in headers, (
                    f"CSV header contains hardcoded column '{col}': {headers}"
                )


# ---------------------------------------------------------------------------
# Test 2: doe -> writing chain
# ---------------------------------------------------------------------------

class TestDoeToWritingChain:
    """Verify that the writing skill's build_manuscript_outline.py produces
    generic output that is not contaminated by domain-specific hardcoded content."""

    def test_doe_to_writing_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            output_path = tmpdir / "outline.md"

            topic = "Advanced high-strength lightweight concrete optimization"
            result = _run_script(BUILD_OUTLINE_SCRIPT, [
                "--topic", topic,
                "--output", str(output_path),
            ])
            assert result.returncode == 0, (
                f"build_manuscript_outline.py failed:\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

            assert output_path.is_file(), f"Output file not created: {output_path}"
            outline_text = output_path.read_text(encoding="utf-8")

            # Verify 6 expected section titles are present
            expected_sections = [
                "One-sentence argument",
                "Claim-evidence-boundary table",
                "Abstract",
                "Introduction",
                "Results and Discussion",
                "Missing evidence to confirm",
            ]
            for section in expected_sections:
                assert section in outline_text, (
                    f"Expected section '{section}' not found in outline output"
                )

            # Verify no hardcoded domain-specific content
            hardcoded_terms = [
                "waterborne epoxy",
                "tack coat",
                "emulsified asphalt",
            ]
            outline_lower = outline_text.lower()
            for term in hardcoded_terms:
                assert term.lower() not in outline_lower, (
                    f"Outline contains hardcoded term '{term}': output is not generic"
                )


# ---------------------------------------------------------------------------
# Test 3: validate_experiment_record catches errors
# ---------------------------------------------------------------------------

class TestValidateExperimentRecordCatchesErrors:
    """Verify that validate_experiment_record.py correctly rejects invalid records."""

    def test_missing_response_variables(self) -> None:
        """A record missing the required 'response_variables' field should fail."""
        record = _make_generic_record()
        # Remove the required field
        del record["response_variables"]

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            record_path = _write_record(tmpdir, record, name="invalid-record.yaml")

            result = _run_script(VALIDATE_SCRIPT, [str(record_path), "--strict"])
            assert result.returncode == 1, (
                f"Expected exit code 1 for invalid record, got {result.returncode}.\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

            report = json.loads(result.stdout)
            assert report["valid"] is False
            # Either schema_errors or semantic_warnings should be non-empty
            has_errors = (
                len(report.get("schema_errors", [])) > 0
                or len(report.get("semantic_warnings", [])) > 0
            )
            assert has_errors, (
                "Expected non-empty schema_errors or semantic_warnings for invalid record"
            )

    def test_missing_factors(self) -> None:
        """A record missing the required 'factors' field should fail."""
        record = _make_generic_record()
        del record["factors"]

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            record_path = _write_record(tmpdir, record, name="no-factors-record.yaml")

            result = _run_script(VALIDATE_SCRIPT, [str(record_path), "--strict"])
            assert result.returncode == 1, (
                f"Expected exit code 1 for record without factors, got {result.returncode}"
            )
            report = json.loads(result.stdout)
            assert report["valid"] is False

    def test_invalid_version_format(self) -> None:
        """A record with non-semver version should be caught by strict checks."""
        record = _make_generic_record()
        record["version"] = "not-a-version"

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            record_path = _write_record(tmpdir, record, name="bad-version-record.yaml")

            result = _run_script(VALIDATE_SCRIPT, [str(record_path), "--strict"])
            assert result.returncode == 1, (
                f"Expected exit code 1 for bad version, got {result.returncode}"
            )
            report = json.loads(result.stdout)
            assert report["valid"] is False


# ---------------------------------------------------------------------------
# Test 4: cross-domain record validation
# ---------------------------------------------------------------------------

class TestCrossDomainRecordValidation:
    """Verify that records from different materials domains all pass validation
    and can be consumed by build_fair_package.py."""

    @pytest.fixture
    def domain_records(self) -> Dict[str, Dict[str, Any]]:
        """Return experiment records for three different materials domains."""
        ceramics = _make_domain_record(
            domain="ceramics",
            family="oxide-ceramics",
            factors=[
                {"name": "sintering_temperature", "type": "continuous", "unit": "degC", "levels": [1200, 1400, 1600]},
                {"name": "holding_time", "type": "continuous", "unit": "h", "levels": [1, 2, 4]},
                {"name": "pressure", "type": "continuous", "unit": "MPa", "levels": [10, 20, 30]},
            ],
            responses=[
                {"name": "density", "unit": "g/cm3"},
                {"name": "flexural_strength", "unit": "MPa"},
            ],
        )
        polymers = _make_domain_record(
            domain="polymers",
            family="thermoplastics",
            factors=[
                {"name": "catalyst_loading", "type": "continuous", "unit": "wt%", "levels": [0.5, 1.0, 2.0]},
                {"name": "reaction_time", "type": "continuous", "unit": "h", "levels": [2, 4, 8]},
                {"name": "monomer_ratio", "type": "continuous", "unit": "ratio", "levels": [1, 2, 3]},
            ],
            responses=[
                {"name": "yield", "unit": "%"},
                {"name": "molecular_weight", "unit": "g/mol"},
            ],
        )
        metals = _make_domain_record(
            domain="metals",
            family="steel-alloys",
            factors=[
                {"name": "alloy_content", "type": "continuous", "unit": "wt%", "levels": [1, 3, 5]},
                {"name": "heat_treatment_temp", "type": "continuous", "unit": "degC", "levels": [800, 900, 1000]},
                {"name": "cooling_rate", "type": "continuous", "unit": "degC/s", "levels": [1, 5, 10]},
            ],
            responses=[
                {"name": "tensile_strength", "unit": "MPa"},
                {"name": "elongation", "unit": "%"},
            ],
        )
        return {"ceramics": ceramics, "polymers": polymers, "metals": metals}

    def test_cross_domain_validation(self, domain_records: Dict[str, Dict[str, Any]]) -> None:
        """All three domain records pass validation."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)

            for domain_name, record in domain_records.items():
                record_path = _write_record(tmpdir, record, name=f"record-{domain_name}.yaml")
                result = _run_script(VALIDATE_SCRIPT, [str(record_path), "--strict"])
                assert result.returncode == 0, (
                    f"Validation failed for {domain_name} record:\n"
                    f"stdout: {result.stdout}\nstderr: {result.stderr}"
                )
                report = json.loads(result.stdout)
                assert report["valid"] is True, (
                    f"{domain_name} record should be valid but got: {report}"
                )

    def test_cross_domain_fair_package(self, domain_records: Dict[str, Dict[str, Any]]) -> None:
        """All three domain records can be consumed by build_fair_package.py."""
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)

            for domain_name, record in domain_records.items():
                record_path = _write_record(tmpdir, record, name=f"record-{domain_name}.yaml")
                output_dir = tmpdir / f"fair_{domain_name}"
                output_dir.mkdir()

                result = _run_script(BUILD_FAIR_SCRIPT, [
                    "--topic", f"Cross-domain test: {domain_name}",
                    "--output-dir", str(output_dir),
                    "--experiment-record", str(record_path),
                ])
                assert result.returncode == 0, (
                    f"build_fair_package.py failed for {domain_name}:\n"
                    f"stdout: {result.stdout}\nstderr: {result.stderr}"
                )

                # Verify the CSV template contains domain-specific factor/response names
                package_dir_name = result.stdout.strip().split("\n")[-1].strip()
                package_dir = Path(package_dir_name)
                csv_path = package_dir / "raw_data" / "experiment_data_template.csv"
                assert csv_path.exists(), f"CSV template missing for {domain_name}"

                csv_text = csv_path.read_text(encoding="utf-8")
                reader = csv.reader(io.StringIO(csv_text))
                headers = next(reader)

                factor_names = [f["name"] for f in record["factors"]]
                response_names = [r["name"] for r in record["response_variables"]]
                for name in factor_names + response_names:
                    assert name in headers, (
                        f"{domain_name}: CSV header missing '{name}'. Got: {headers}"
                    )
