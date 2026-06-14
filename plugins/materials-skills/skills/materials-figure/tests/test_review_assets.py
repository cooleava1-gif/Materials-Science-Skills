import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"


class PaperDerivedReviewAssetsTest(unittest.TestCase):
    def test_paper_derived_reference_documents_learning_boundary(self):
        reference = SKILL_ROOT / "references" / "paper-derived-visual-patterns.md"
        self.assertTrue(reference.exists(), "paper-derived-visual-patterns.md should exist")
        text = reference.read_text(encoding="utf-8")

        for phrase in [
            "paper-derived visual patterns",
            "small review",
            "do not copy paper figures",
            "claim-evidence-boundary",
            "dosage-workability-window",
            "performance-comparison",
            "test-matrix-standard",
            "microstructure-image-plate",
            "interface-mechanism-map",
            "30 assets",
        ]:
            self.assertIn(phrase, text)

    def test_review_asset_specs_define_thirty_sanitized_assets(self):
        spec = SKILL_ROOT / "assets" / "review-first" / "asset-specs.csv"
        self.assertTrue(spec.exists(), "review-first asset-specs.csv should exist")
        with spec.open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))

        self.assertGreaterEqual(len(rows), 30)
        required_columns = {
            "asset_id",
            "family",
            "review_use",
            "panel_structure",
            "required_evidence",
            "claim_boundary",
            "caption_pattern",
            "source_learning_basis",
        }
        self.assertEqual(required_columns, set(rows[0]))

        families = {row["family"] for row in rows}
        for family in [
            "dosage-workability-window",
            "performance-comparison",
            "test-matrix-standard",
            "microstructure-image-plate",
            "interface-mechanism-map",
            "characterization-evidence-panel",
            "durability-retention",
            "review-taxonomy-map",
        ]:
            self.assertIn(family, families)

        combined = "\n".join(",".join(row.values()) for row in rows)
        self.assertNotIn("C:\\Users", combined)
        self.assertIn("template only", combined)
        for row in rows:
            self.assertTrue(row["claim_boundary"], f"{row['asset_id']} needs claim boundary")
            self.assertTrue(row["required_evidence"], f"{row['asset_id']} needs required evidence")

    def test_review_gallery_demo_regenerates_ten_review_assets(self):
        script = SCRIPTS_ROOT / "review_gallery_demo.py"
        self.assertTrue(script.exists(), "review_gallery_demo.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(script), "--output-dir", tmp],
                check=True,
                capture_output=True,
                text=True,
            )

            outputs = sorted(Path(tmp).glob("*.svg"))
            self.assertEqual(len(outputs), 10)
            self.assertIn("review_framework_map.svg", result.stdout)
            for svg in outputs:
                text = svg.read_text(encoding="utf-8")
                self.assertIn("<svg", text)
                self.assertIn("Materials Science Review Assets", text)
                self.assertIn("template only", text)
                self.assertIn("claim boundary", text)

    def test_generated_review_assets_are_available_in_skill_package(self):
        generated_dir = SKILL_ROOT / "assets" / "review-first" / "generated"
        self.assertTrue(generated_dir.exists(), "review-first generated assets should exist")
        svgs = sorted(generated_dir.glob("*.svg"))
        self.assertEqual(len(svgs), 10)

        expected = {
            "review_framework_map.svg",
            "material_mechanism_performance_challenges.svg",
            "evidence_chain_map.svg",
            "interface_mechanism_boundary.svg",
            "bonding_test_method_map.svg",
            "dosage_viscosity_bonding_window.svg",
            "ftir_sem_rheology_evidence_panel.svg",
            "durability_retention_challenge_map.svg",
            "research_gap_matrix.svg",
            "graphical_abstract_review.svg",
        }
        self.assertEqual(expected, {svg.name for svg in svgs})


if __name__ == "__main__":
    unittest.main()
