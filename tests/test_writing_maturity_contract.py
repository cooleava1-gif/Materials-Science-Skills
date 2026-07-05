import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "materials-skills"
WRITING_ROOT = PLUGIN_ROOT / "skills" / "materials-writing"


class WritingMaturityContractTest(unittest.TestCase):
    def test_section_level_factory_files_define_material_paper_moves(self):
        expected = {
            "abstract-claim-arc.md": [
                "background pain",
                "method",
                "key result",
                "mechanism explanation",
                "application boundary",
                "sentence pattern",
            ],
            "introduction-gap-ladder.md": [
                "field progress",
                "unresolved contradiction",
                "evidence gap",
                "paper entry",
                "sentence pattern",
            ],
            "results-discussion-evidence-chain.md": [
                "observation",
                "quantitative result",
                "mechanism evidence",
                "alternative explanation exclusion",
                "sentence pattern",
            ],
            "conclusion-boundary.md": [
                "contribution",
                "limitation",
                "next step",
                "overclaim",
                "sentence pattern",
            ],
            "review-synthesis-patterns.md": [
                "classification",
                "controversy",
                "trend",
                "research gap",
                "sentence pattern",
            ],
        }
        root = WRITING_ROOT / "references" / "section-patterns"
        for name, phrases in expected.items():
            path = root / name
            self.assertTrue(path.exists(), f"{path} should exist")
            text = path.read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase, text, f"{name} should contain {phrase}")

    def test_material_phrase_banks_have_replaceable_sentences_and_red_flags(self):
        expected_terms = {
            "wer-ea.md": [
                "bonding",
                "demulsification",
                "curing",
                "interfacial energy",
                "emulsion stability",
            ],
            "thermal-insulation.md": [
                "thermal conductivity",
                "density",
                "pore structure",
                "hygrothermal aging",
                "fire performance",
            ],
            "polymer-composites.md": [
                "interfacial bonding",
                "fiber orientation",
                "interlaminar shear",
                "fatigue",
                "fracture mechanism",
            ],
        }
        root = WRITING_ROOT / "references" / "phrase-banks"
        for name, terms in expected_terms.items():
            path = root / name
            self.assertTrue(path.exists(), f"{path} should exist")
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for heading in ["phrase-bank", "reviewer-red-flags", "safe-claim-patterns"]:
                self.assertIn(heading, lowered, f"{name} should contain {heading}")
            for term in terms:
                self.assertIn(term, lowered, f"{name} should cover {term}")
            self.assertIn("[", text, f"{name} should include replaceable bracketed sentence slots")
            self.assertIn("The ", text, f"{name} should include directly reusable English sentence patterns")

    def test_material_manuscript_audit_flags_missing_evidence_and_context(self):
        script = WRITING_ROOT / "scripts" / "audit_materials_manuscript.py"
        self.assertTrue(script.exists(), "materials writing audit script should exist")

        weak_text = """
        Figure 1 shows that the modifier proves the curing mechanism and causes
        higher bonding performance. The polymer network improves the interface.
        """
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "weak.md"
            draft.write_text(weak_text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(script), "--input", str(draft), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        issue_ids = {issue["id"] for issue in payload["issues"]}
        self.assertTrue(
            {
                "mechanism_without_characterization",
                "causality_overclaim",
                "missing_test_standard",
                "missing_sample_preparation",
                "missing_durability_or_application_boundary",
                "figure_caption_text_mismatch",
            }.issubset(issue_ids)
        )

    def test_release_gate_tracks_writing_maturity_assets(self):
        release_text = (PLUGIN_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")
        for phrase in [
            "WRITING_MATURITY_FILES",
            "abstract-claim-arc.md",
            "introduction-gap-ladder.md",
            "results-discussion-evidence-chain.md",
            "conclusion-boundary.md",
            "review-synthesis-patterns.md",
            "phrase-banks/wer-ea.md",
            "audit_materials_manuscript.py",
        ]:
            self.assertIn(phrase, release_text)


if __name__ == "__main__":
    unittest.main()
