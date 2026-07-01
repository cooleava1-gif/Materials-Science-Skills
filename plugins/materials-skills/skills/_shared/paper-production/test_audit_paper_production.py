#!/usr/bin/env python3
"""Unit tests for audit_paper_production.py.

Covers weakness CSV auditing, gate report markdown auditing, helper parsing
functions, and the integrated audit_files() entry point.
Uses pytest with tmp_path for all file I/O.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

import pytest

# Ensure the paper-production package is importable when running pytest
# from the _shared directory or project root.
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from audit_paper_production import (
    ALLOWED_GATE_STATUS,
    ALLOWED_REGRESSION_STATUS,
    ALLOWED_WEAKNESS_STATUS,
    REQUIRED_GATE_NAMES,
    WEAKNESS_REQUIRED_FIELDS,
    audit_files,
    audit_gate_report,
    audit_weakness_routing,
    _parse_routed_weakness_ids,
    _split_markdown_row,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_weakness_csv(
    path: Path,
    rows: list[dict[str, str]],
    *,
    fields: list[str] | None = None,
) -> Path:
    """Write a weakness-routing CSV and return the path.

    *fields* overrides the header columns (useful for testing missing columns).
    """
    header = fields or WEAKNESS_REQUIRED_FIELDS
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def _valid_weakness_row(**overrides: str) -> dict[str, str]:
    """Return a minimal valid weakness row, with optional field overrides."""
    base = {
        "weakness_id": "W-001",
        "source": "reviewer-1",
        "severity": "major",
        "weakness_type": "evidence-gap",
        "evidence_gap": "no replication data",
        "route_to": "materials-data",
        "required_fix": "provide raw data",
        "expected_artifact": "raw_data.csv",
        "status": "open",
        "regression_check": "pending",
    }
    base.update(overrides)
    return base


def _write_gate_markdown(
    path: Path,
    rows: list[dict[str, str]],
    *,
    fields: list[str] | None = None,
) -> Path:
    """Write a gate-report markdown table and return the path."""
    header = fields or [
        "gate_id", "gate_name", "status", "evidence_checked",
        "missing_inputs", "routed_weakness_ids", "next_skill", "reviewer_risk",
    ]
    lines: list[str] = []
    # Header row
    lines.append("| " + " | ".join(header) + " |")
    # Separator row
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    # Data rows
    for row in rows:
        cells = [row.get(f, "") for f in header]
        lines.append("| " + " | ".join(cells) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _valid_gate_row(**overrides: str) -> dict[str, str]:
    """Return a minimal valid gate row, with optional field overrides."""
    base = {
        "gate_id": "G1",
        "gate_name": "Literature Coverage",
        "status": "pass",
        "evidence_checked": "yes",
        "missing_inputs": "none",
        "routed_weakness_ids": "None",
        "next_skill": "materials-writing",
        "reviewer_risk": "low",
    }
    base.update(overrides)
    return base


def _all_seven_gates(weakness_ids_str: str = "None") -> list[dict[str, str]]:
    """Return 7 valid gate rows covering all REQUIRED_GATE_NAMES."""
    gates = []
    for idx, name in enumerate(REQUIRED_GATE_NAMES, start=1):
        gates.append(_valid_gate_row(
            gate_id=f"G{idx}",
            gate_name=name,
            routed_weakness_ids=weakness_ids_str,
        ))
    return gates


# ---------------------------------------------------------------------------
# Weakness routing tests
# ---------------------------------------------------------------------------

class TestAuditWeaknessRouting:
    """Tests for audit_weakness_routing()."""

    def test_valid_weakness_csv_passes(self, tmp_path: Path) -> None:
        """A well-formed CSV with one valid row should produce no issues."""
        csv_path = tmp_path / "weakness.csv"
        _write_weakness_csv(csv_path, [_valid_weakness_row()])

        issues, ids = audit_weakness_routing(csv_path)
        assert issues == [], f"Expected no issues, got: {issues}"
        assert ids == {"W-001"}

    def test_weakness_missing_field(self, tmp_path: Path) -> None:
        """CSV missing the 'severity' column should report a missing-field issue."""
        csv_path = tmp_path / "weakness.csv"
        fields_without_severity = [f for f in WEAKNESS_REQUIRED_FIELDS if f != "severity"]
        _write_weakness_csv(
            csv_path,
            [{"weakness_id": "W-001", "source": "reviewer-1"}],
            fields=fields_without_severity,
        )

        issues, ids = audit_weakness_routing(csv_path)
        assert len(issues) > 0
        assert any("severity" in i.lower() for i in issues), (
            f"Expected an issue mentioning 'severity', got: {issues}"
        )

    def test_weakness_duplicate_id(self, tmp_path: Path) -> None:
        """Two rows with the same weakness_id should report a duplicate."""
        csv_path = tmp_path / "weakness.csv"
        row = _valid_weakness_row()
        _write_weakness_csv(csv_path, [row, row])  # identical rows

        issues, ids = audit_weakness_routing(csv_path)
        assert any("duplicate" in i.lower() or "duplicates" in i.lower() for i in issues), (
            f"Expected a duplicate-id issue, got: {issues}"
        )

    def test_weakness_invalid_status(self, tmp_path: Path) -> None:
        """A row with status='unknown' should report an invalid status."""
        csv_path = tmp_path / "weakness.csv"
        _write_weakness_csv(csv_path, [_valid_weakness_row(status="unknown")])

        issues, ids = audit_weakness_routing(csv_path)
        assert any("status" in i.lower() and "unknown" in i for i in issues), (
            f"Expected an invalid-status issue, got: {issues}"
        )

    def test_weakness_invalid_regression(self, tmp_path: Path) -> None:
        """A row with regression_check='maybe' should report an invalid value."""
        csv_path = tmp_path / "weakness.csv"
        _write_weakness_csv(csv_path, [_valid_weakness_row(regression_check="maybe")])

        issues, ids = audit_weakness_routing(csv_path)
        assert any("regression_check" in i and "maybe" in i for i in issues), (
            f"Expected an invalid regression_check issue, got: {issues}"
        )

    def test_weakness_empty_id(self, tmp_path: Path) -> None:
        """A row with an empty weakness_id should be flagged."""
        csv_path = tmp_path / "weakness.csv"
        _write_weakness_csv(csv_path, [_valid_weakness_row(weakness_id="")])

        issues, ids = audit_weakness_routing(csv_path)
        assert any("empty" in i.lower() or "weakness_id" in i for i in issues), (
            f"Expected an empty-id issue, got: {issues}"
        )


# ---------------------------------------------------------------------------
# Gate report tests
# ---------------------------------------------------------------------------

class TestAuditGateReport:
    """Tests for audit_gate_report()."""

    def test_valid_gate_report_passes(self, tmp_path: Path) -> None:
        """A markdown file with all 7 required gates and valid data should pass."""
        md_path = tmp_path / "gate.md"
        _write_gate_markdown(md_path, _all_seven_gates())

        issues = audit_gate_report(md_path, weakness_ids=set())
        assert issues == [], f"Expected no issues, got: {issues}"

    def test_gate_missing_required_name(self, tmp_path: Path) -> None:
        """Only 6 of 7 required gates should report the missing gate name."""
        md_path = tmp_path / "gate.md"
        # Omit the last required gate
        gates = _all_seven_gates()[:-1]
        _write_gate_markdown(md_path, gates)

        issues = audit_gate_report(md_path, weakness_ids=set())
        missing_name = REQUIRED_GATE_NAMES[-1]
        assert any(missing_name in i for i in issues), (
            f"Expected missing gate '{missing_name}' in issues, got: {issues}"
        )

    def test_gate_unknown_weakness_ref(self, tmp_path: Path) -> None:
        """A gate referencing W-999 not in weakness_ids should be flagged."""
        md_path = tmp_path / "gate.md"
        gates = _all_seven_gates(weakness_ids_str="W-999")
        _write_gate_markdown(md_path, gates)

        # Pass an empty weakness set so W-999 is unknown
        issues = audit_gate_report(md_path, weakness_ids=set())
        assert any("W-999" in i for i in issues), (
            f"Expected an unknown weakness reference to W-999, got: {issues}"
        )

    def test_gate_duplicate_id(self, tmp_path: Path) -> None:
        """Two rows with the same gate_id should report a duplicate."""
        md_path = tmp_path / "gate.md"
        gates = _all_seven_gates()
        # Duplicate the first gate row (same gate_id and gate_name)
        gates.append(gates[0])
        _write_gate_markdown(md_path, gates)

        issues = audit_gate_report(md_path, weakness_ids=set())
        assert any("duplicate" in i.lower() or "duplicates" in i.lower() for i in issues), (
            f"Expected a duplicate gate_id issue, got: {issues}"
        )

    def test_gate_invalid_status(self, tmp_path: Path) -> None:
        """A gate row with status='maybe' should report an invalid status."""
        md_path = tmp_path / "gate.md"
        gates = _all_seven_gates()
        gates[0]["status"] = "maybe"
        _write_gate_markdown(md_path, gates)

        issues = audit_gate_report(md_path, weakness_ids=set())
        assert any("status" in i.lower() and "maybe" in i for i in issues), (
            f"Expected an invalid-status issue, got: {issues}"
        )


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------

class TestHelpers:
    """Tests for _parse_routed_weakness_ids() and _split_markdown_row()."""

    def test_parse_routed_weakness_ids(self) -> None:
        """Semicolon- and comma-separated IDs should be split and stripped."""
        result = _parse_routed_weakness_ids("W-001; W-002, W-003")
        assert result == ["W-001", "W-002", "W-003"]

    def test_parse_routed_weakness_ids_none(self) -> None:
        """Empty string or 'None' should return an empty list."""
        assert _parse_routed_weakness_ids("") == []
        assert _parse_routed_weakness_ids("None") == []
        assert _parse_routed_weakness_ids("  ") == []

    def test_split_markdown_row(self) -> None:
        """A markdown table row should be split into stripped cells."""
        row = _split_markdown_row("| G1 | Literature Coverage | pass |")
        assert row == ["G1", "Literature Coverage", "pass"]


# ---------------------------------------------------------------------------
# Integration test
# ---------------------------------------------------------------------------

class TestAuditFilesIntegration:
    """Integration test for audit_files()."""

    def test_audit_files_integration(self, tmp_path: Path) -> None:
        """Create valid CSV and MD files, call audit_files(), expect pass."""
        csv_path = tmp_path / "weakness.csv"
        md_path = tmp_path / "gate.md"

        # Write a valid weakness CSV with two rows
        _write_weakness_csv(csv_path, [
            _valid_weakness_row(weakness_id="W-001"),
            _valid_weakness_row(weakness_id="W-002", status="fixed", regression_check="pass"),
        ])

        # Write a valid gate report referencing W-001
        gates = _all_seven_gates(weakness_ids_str="W-001")
        _write_gate_markdown(md_path, gates)

        result = audit_files(csv_path, md_path)
        assert result["status"] == "pass", (
            f"Expected status 'pass', got: {result}"
        )
        assert result["issues"]["weakness_routing"] == []
        assert result["issues"]["gate_report"] == []
