from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-reader" / "SKILL.md"


def test_reader_router_keeps_source_and_figure_boundaries() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "source_format",
        "output_type",
        "terminology ledger",
        "source_map.json",
        "source anchor",
        "page",
        "paragraph",
        "figure",
        "distinguish what the paper says",
        "overclaim",
        "reader-package",
    ):
        assert required in text


def test_reader_router_removes_generic_layered_architecture() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Layered architecture" not in text
    assert "Read and organize materials papers" not in text
    assert len(text.split()) <= 220
