"""Tests for the materials knowledge validation engine."""
from __future__ import annotations

from pathlib import Path

import pytest

from validate_materials_claims import (
    Severity,
    ValidationIssue,
    ValidationReport,
    validate_figure_package,
)


SAMPLE_KB = """
families:
  ceramics:
    xrd_peaks:
      - phase: "t-ZrO2"
        peaks_2theta: [30.2, 34.8, 50.2]
        tolerance_deg: 0.5
        card: "PDF#50-1089"
    performance_ranges:
      - name: "Sintered density"
        typical_min: 5.5
        typical_max: 6.1
        warning_threshold: 0.20
"""


def test_report_creation() -> None:
    report = ValidationReport(package="x", errors=[], warnings=[])
    assert report.summary() == "0 errors, 0 warnings"
    assert report.exit_code() == 0


def test_xrd_peak_phase_mismatch_triggers_error(tmp_path: Path) -> None:
    kb = tmp_path / "kb.yaml"
    kb.write_text(SAMPLE_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "source_data.csv").write_text(
        "phase,two_theta,intensity\nAl2O3,30.2,100.0\n", encoding="utf-8"
    )
    (pkg / "figure_contract.md").write_text(
        "# contract\nphase: Al2O3\n", encoding="utf-8"
    )

    report = validate_figure_package(pkg, kb_path=kb)

    assert report.exit_code() == 1
    assert any(
        issue.rule == "xrd_peak_phase_mismatch" and issue.severity == Severity.ERROR
        for issue in report.errors
    )


def test_xrd_peak_correct_phase_passes(tmp_path: Path) -> None:
    kb = tmp_path / "kb.yaml"
    kb.write_text(SAMPLE_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "source_data.csv").write_text(
        "phase,two_theta,intensity\nt-ZrO2,30.2,100.0\n", encoding="utf-8"
    )
    (pkg / "figure_contract.md").write_text(
        "# contract\nphase: t-ZrO2\n", encoding="utf-8"
    )

    report = validate_figure_package(pkg, kb_path=kb)

    assert report.exit_code() == 0
    assert not report.errors


def test_performance_out_of_range_triggers_warning(tmp_path: Path) -> None:
    kb = tmp_path / "kb.yaml"
    kb.write_text(SAMPLE_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "source_data.csv").write_text(
        "metric,value\nSintered density,7.5\n", encoding="utf-8"
    )
    (pkg / "figure_contract.md").write_text(
        "# contract\nfamily: ceramics\n", encoding="utf-8"
    )

    report = validate_figure_package(pkg, kb_path=kb)

    assert any(
        issue.rule == "performance_out_of_range" and issue.severity == Severity.WARNING
        for issue in report.warnings
    )


def test_package_missing_source_data(tmp_path: Path) -> None:
    kb = tmp_path / "kb.yaml"
    kb.write_text(SAMPLE_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()

    report = validate_figure_package(pkg, kb_path=kb)

    assert report.exit_code() == 2
    assert any(issue.rule == "package_files_missing" for issue in report.errors)


# ---------------------------------------------------------------------------
# Phase alias / FTIR / contract-text / unit-hint regression tests for the
# original 790-line capabilities that were merged back into the 310-line
# engine.
# ---------------------------------------------------------------------------

ALIAS_KB = """
families:
  ceramics:
    xrd_peaks:
      - phase: "Al2O3 (alpha-corundum)"
        peaks_2theta: [25.57, 35.15, 37.77, 43.36]
        tolerance_deg: 0.5
        card: "PDF#46-1212"
      - phase: "ZrO2 (tetragonal)"
        peaks_2theta: [30.2, 34.6, 50.2]
        tolerance_deg: 0.5
        card: "PDF#79-1769"
    ftir_wavenumbers:
      - bond: "oxirane ring"
        wavenumbers: [915]
        tolerance: 20
      - bond: "C=O stretch"
        wavenumbers: [1730]
        tolerance: 20
      - bond: "Si-O stretch"
        wavenumbers: [1030]
        tolerance: 20
"""


def test_phase_alias_resolution(tmp_path: Path) -> None:
    """CSV uses alias 'alumina' which is not in the KB; alias resolution
    must map it to the canonical 'Al2O3 (alpha-corundum)' entry so the
    peak-position check finds a match and no error is raised.
    """
    kb = tmp_path / "kb.yaml"
    kb.write_text(ALIAS_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "source_data.csv").write_text(
        "phase,two_theta,intensity\nalumina,35.15,100.0\n", encoding="utf-8"
    )
    (pkg / "figure_contract.md").write_text(
        "# contract\nphase: alumina\n", encoding="utf-8"
    )

    report = validate_figure_package(pkg, kb_path=kb)

    assert report.exit_code() == 0
    assert not report.errors
    assert not any(
        issue.rule == "xrd_peak_phase_mismatch" for issue in report.errors
    )


def test_ftir_wavenumber_mismatch(tmp_path: Path) -> None:
    """A row claims 915 cm⁻¹ is C=O, but the KB puts 915 cm⁻¹ at the
    oxirane category. The validator must raise an
    ``ftir_wavenumber_group_mismatch`` ERROR.
    """
    kb = tmp_path / "kb.yaml"
    kb.write_text(ALIAS_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "source_data.csv").write_text(
        "wavenumber,functional_group\n915,C=O\n", encoding="utf-8"
    )
    (pkg / "figure_contract.md").write_text(
        "# contract\nbond: C=O\n", encoding="utf-8"
    )

    report = validate_figure_package(pkg, kb_path=kb)

    assert report.exit_code() == 1
    assert any(
        issue.rule == "ftir_wavenumber_group_mismatch"
        and issue.severity == Severity.ERROR
        for issue in report.errors
    )


def test_figure_contract_md_parsing(tmp_path: Path) -> None:
    """A figure_contract.md with 'XRD peak at 30.2° of Al2O3' must be
    parsed and validated. KB has no 'Al2O3' entry (it stores the
    canonical 'Al2O3 (alpha-corundum)'), so the alias resolver must
    match the prose. 30.2° does not match the Al2O3 peaks either, so
    a mismatch error is expected and demonstrates the prose path is
    exercised.
    """
    kb = tmp_path / "kb.yaml"
    kb.write_text(ALIAS_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    # CSV: an XRD claim that the alias resolver handles correctly so the
    # CSV pass is clean. The interesting claim is the prose one.
    (pkg / "source_data.csv").write_text(
        "phase,two_theta,intensity\nAl2O3 (alpha-corundum),35.15,100.0\n",
        encoding="utf-8",
    )
    (pkg / "figure_contract.md").write_text(
        "# contract\n\nThe XRD peak at 30.2° of alumina indicates "
        "a secondary phase.\n",
        encoding="utf-8",
    )

    report = validate_figure_package(pkg, kb_path=kb)

    # 30.2° is not an Al2O3 peak; the prose path should detect the
    # mismatch between the declared alumina phase and the actual peak.
    assert any(
        issue.context.get("source") == "figure_contract.md"
        for issue in report.errors
    )


def test_unit_hint_check(tmp_path: Path) -> None:
    """A figure_contract.md that reports 'compressive strength 50 GPa'
    for Portland cement should trigger a unit-hint warning because
    compressive_strength is documented as MPa in PROPERTY_UNIT_HINTS.
    """
    kb = tmp_path / "kb.yaml"
    kb.write_text(ALIAS_KB, encoding="utf-8")
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "source_data.csv").write_text(
        "metric,value,unit\nSintered density,5.8,g/cm3\n", encoding="utf-8"
    )
    (pkg / "figure_contract.md").write_text(
        "# contract\n\nPortland cement has a compressive strength of 50 GPa "
        "at 28 days.\n",
        encoding="utf-8",
    )

    report = validate_figure_package(pkg, kb_path=kb)

    assert any(
        issue.rule == "unit_hint_mismatch" and issue.severity == Severity.WARNING
        for issue in report.warnings
    )
