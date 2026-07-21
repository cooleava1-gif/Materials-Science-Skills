from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-html-deck" / "SKILL.md"


def test_deck_router_keeps_browser_qa_and_asset_contract() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "strict playwright",
        "asset manifest",
        "screenshots",
        "speaker notes",
        "source_type",
        "material_family",
        "materials-figure",
        "materials-writing",
        "do not fabricate",
    ):
        assert required in text


def test_deck_router_removes_generic_architecture_and_style_catalogue() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Architecture" not in text
    assert "assertion-evidence`, `dense-research" not in text
    assert "## Toolchain notes" not in text
    assert len(text.split()) <= 360
