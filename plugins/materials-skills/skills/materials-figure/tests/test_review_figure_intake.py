import csv
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


REQUIRED_INTAKE_FIELDS = [
    "claim_id",
    "source_anchor",
    "citation_key_or_doi",
    "evidence_layer",
    "certainty_tier",
    "panel_role",
    "visual_encoding",
    "caption_boundary",
    "missing_evidence_marker",
    "reviewer_risk",
]

REQUIRED_CERTAINTY_TIERS = [
    "measured",
    "inferred",
    "speculative",
    "missing",
]

REQUIRED_QA_FIELDS = [
    "Source-Handoff Check",
    "Certainty-Tier Check",
    "Missing-Evidence Marker Check",
    "Caption-Boundary Check",
]


class ReviewFigureIntakeContractTest(unittest.TestCase):
    def test_intake_reference_and_template_define_required_fields(self):
        reference = SKILL_ROOT / "references" / "review-figure-intake.md"
        template = SKILL_ROOT / "assets" / "templates" / "review-figure-intake-template.csv"

        self.assertTrue(reference.exists(), "review-figure-intake.md should exist")
        self.assertTrue(template.exists(), "review-figure-intake-template.csv should exist")

        reference_text = reference.read_text(encoding="utf-8")
        for field in REQUIRED_INTAKE_FIELDS:
            self.assertIn(field, reference_text)

        with template.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual(REQUIRED_INTAKE_FIELDS, list(rows[0].keys()))
        self.assertGreaterEqual(len(rows), 4)
        self.assertEqual(set(REQUIRED_CERTAINTY_TIERS), {row["certainty_tier"] for row in rows})
        for row in rows:
            self.assertTrue(row["claim_id"])
            self.assertTrue(row["source_anchor"])
            self.assertTrue(row["caption_boundary"])

    def test_contracts_and_qa_distinguish_evidence_certainty(self):
        intake_text = (SKILL_ROOT / "references" / "review-figure-intake.md").read_text(encoding="utf-8")
        wer_text = (SKILL_ROOT / "references" / "wer-ea-review-figure-contract.md").read_text(encoding="utf-8")
        qa_text = (SKILL_ROOT / "references" / "figure-qa-contract.md").read_text(encoding="utf-8")
        template_text = (SKILL_ROOT / "assets" / "templates" / "wer-ea-figure-contract-template.md").read_text(
            encoding="utf-8"
        )

        for text in [intake_text, wer_text, qa_text, template_text]:
            for tier in REQUIRED_CERTAINTY_TIERS:
                self.assertIn(tier, text)

        for field in REQUIRED_QA_FIELDS:
            self.assertIn(field, qa_text)

        self.assertIn("reader handoff", intake_text)
        self.assertIn("citation matrix", intake_text)
        self.assertIn("mechanism maps", wer_text)
        self.assertIn("evidence heatmaps", wer_text)

    def test_skill_and_manifest_route_handoff_intake(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")

        for phrase in [
            "handoff_intake:",
            "references/review-figure-intake.md",
        ]:
            self.assertIn(phrase, manifest_text)

        for phrase in [
            "handoff_intake:",
            "references/review-figure-intake.md",
            "reader handoff",
            "citation matrix",
            "review figure intake",
            "evidence heatmap",
            "mechanism map",
        ]:
            self.assertIn(phrase, manifest_text)


if __name__ == "__main__":
    unittest.main()
