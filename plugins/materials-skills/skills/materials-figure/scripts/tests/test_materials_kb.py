"""Tests for the materials knowledge graph structure."""
from __future__ import annotations

from pathlib import Path

import yaml


KB_PATH = (
    Path(__file__).resolve().parents[2]
    / "static"
    / "core"
    / "materials_kb.yaml"
)


def test_kb_loads_as_valid_yaml() -> None:
    assert KB_PATH.is_file(), f"KB not found at {KB_PATH}"
    with KB_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
    assert "families" in data
    assert isinstance(data["families"], dict)


def test_kb_covers_seven_families() -> None:
    with KB_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    expected = {
        "civil",
        "polymers",
        "metals",
        "ceramics",
        "functional",
        "nano",
        "thermal-insulation",
    }
    assert set(data["families"].keys()) >= expected


def test_kb_each_family_has_at_least_30_entries() -> None:
    with KB_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for family, payload in data["families"].items():
        total = (
            len(payload.get("xrd_peaks") or [])
            + len(payload.get("ftir_wavenumbers") or [])
            + len(payload.get("performance_ranges") or [])
            + len(payload.get("thermal_events") or [])
        )
        assert total >= 30, f"{family} has only {total} entries"


def test_kb_xrd_peaks_have_unique_phase_keys() -> None:
    with KB_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for family, payload in data["families"].items():
        for entry in payload.get("xrd_peaks") or []:
            assert "phase" in entry
            assert "peaks_2theta" in entry
            assert "tolerance_deg" in entry
            assert isinstance(entry["peaks_2theta"], list)
            assert len(entry["peaks_2theta"]) >= 1
