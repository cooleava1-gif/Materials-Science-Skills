from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-data" / "SKILL.md"


def test_data_router_keeps_schema_fair_and_provenance_gates() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "input_source",
        "experiment-record-schema",
        "raw data",
        "processed data",
        "figures",
        "units",
        "test standards",
        "sample ids",
        "mixture ids",
        "replicate counts",
        "data availability",
        "never invent",
        "build_fair_package.py",
    ):
        assert required in text


def test_data_router_removes_generic_layered_architecture() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Layered architecture" not in text
    assert "Prepare materials datasets that a reviewer" not in text
    assert len(text.split()) <= 260
