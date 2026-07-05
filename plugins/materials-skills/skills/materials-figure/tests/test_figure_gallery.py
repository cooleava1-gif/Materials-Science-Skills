import json
import unittest
from pathlib import Path

from PIL import Image


SKILL_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_PROOF_ASSETS = [
    "reader_package_proof_wall.png",
    "wer_ea_figure_proof_board.png",
    "sbr_wer_performance_proof_board.png",
    "interlayer_fatigue_proof_board.png",
]


def has_visual_signal(path: Path) -> bool:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        extrema = rgba.getextrema()
        return rgba.width >= 1200 and rgba.height >= 700 and any(
            (high - low) >= 40 for low, high in extrema[:3]
        )


class FigureGalleryAssetsTest(unittest.TestCase):
    def test_gallery_reference_and_shipped_assets_exist(self):
        gallery_ref = SKILL_ROOT / "references" / "figure-gallery.md"
        production_spec = SKILL_ROOT / "references" / "figure-production-spec.md"
        gallery_assets = SKILL_ROOT / "assets" / "gallery"

        self.assertTrue(gallery_ref.exists())
        self.assertTrue(production_spec.exists())
        self.assertTrue((gallery_assets / "fig9-multipanel-xrd-sem-perf.svg").exists())
        self.assertTrue((gallery_assets / "fig12-evidence-chain.png").exists())

        gallery_text = gallery_ref.read_text(encoding="utf-8")
        for phrase in ["visual style example", "style", "figure"]:
            self.assertIn(phrase, gallery_text.lower())

    def test_showcase_proof_assets_exist_and_have_visual_signal(self):
        showcase_root = SKILL_ROOT / "assets" / "showcase-proof"
        self.assertTrue(showcase_root.exists())
        for filename in SHOWCASE_PROOF_ASSETS:
            path = showcase_root / filename
            self.assertTrue(path.exists(), f"{filename} should exist")
            self.assertTrue(has_visual_signal(path), f"{filename} should be content-bearing")

    def test_showcase_manifest_records_current_boards(self):
        manifest_path = SKILL_ROOT / "assets" / "showcase-proof" / "showcase_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        boards = manifest["boards"]
        self.assertEqual(sorted(board["file"] for board in boards), sorted(SHOWCASE_PROOF_ASSETS))
        for board in boards:
            self.assertTrue(board["title"])
            self.assertTrue(board["source"])


if __name__ == "__main__":
    unittest.main()
