import csv
import unittest
from pathlib import Path



def _find_repo_root():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return p.parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = _find_repo_root()
PLUGIN_ROOT = REPO_ROOT / "plugins" / "materials-skills" / "skills" / "materials-reader"

REQUIRED_HANDOFF_FIELDS = {
    "claim_id",
    "source_anchor",
    "source_location",
    "original_excerpt",
    "measured_evidence",
    "inferred_mechanism",
    "boundary_or_missing_test",
    "citation_role",
    "evidence_type",
    "figure_archetype",
    "reviewer_risk",
    "handoff_target",
}


def csv_header(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return next(csv.reader(handle))


class ReaderHandoffContractTest(unittest.TestCase):
    def test_handoff_reference_and_templates_define_required_fields(self):
        reference = SKILL_ROOT / "references" / "evidence-to-review-handoff.md"
        templates = [
            SKILL_ROOT / "assets" / "templates" / "citation-handoff-template.csv",
            SKILL_ROOT / "assets" / "templates" / "figure-handoff-template.csv",
        ]

        self.assertTrue(reference.exists(), "evidence-to-review-handoff.md should exist")
        reference_text = reference.read_text(encoding="utf-8")
        for field in REQUIRED_HANDOFF_FIELDS | {"confidence_label", "missing_evidence_flag"}:
            self.assertIn(field, reference_text)

        for template in templates:
            self.assertTrue(template.exists(), f"{template.name} should exist")
            missing = REQUIRED_HANDOFF_FIELDS - set(csv_header(template))
            self.assertFalse(missing, f"{template.name} missing fields: {sorted(missing)}")

    def test_source_anchor_checklist_and_visual_linkage_fields_exist(self):
        checklist = SKILL_ROOT / "assets" / "templates" / "source-anchor-checklist.md"
        figure_template = SKILL_ROOT / "assets" / "templates" / "figure-table-card-template.md"

        self.assertTrue(checklist.exists(), "source-anchor-checklist.md should exist")
        checklist_text = checklist.read_text(encoding="utf-8")
        for phrase in [
            "PDF",
            "DOI/HTML",
            "pasted text",
            "source_anchor",
            "source_location",
            "confidence_label",
            "missing_evidence_flag",
        ]:
            self.assertIn(phrase, checklist_text)

        figure_text = figure_template.read_text(encoding="utf-8")
        for field in ["source_page", "crop_status", "interpretation_boundary", "review_figure_support"]:
            self.assertIn(field, figure_text)

    def test_skill_and_manifest_route_reader_handoff_reference(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")

        for expected in [
            "evidence-to-review-handoff",
        ]:
            self.assertIn(expected, manifest_text)
        for tpl in ["citation-handoff-template.csv", "figure-handoff-template.csv", "source-anchor-checklist.md"]:
            self.assertTrue((SKILL_ROOT / "assets" / "templates" / tpl).exists())

        for expected in [
            "evidence-to-review-handoff",
            "citation handoff",
            "figure handoff",
            "source-map-first",
        ]:
            self.assertIn(expected, manifest_text)

    def test_manifest_trigger_text_keeps_utf8_chinese_and_avoids_mojibake(self):
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")

        for expected in [
            "\u6587\u732ePDF",
            "\u7c98\u8d34",
            "\u7cbe\u8bfb",
            "\u5168\u6587\u9605\u8bfb",
            "\u7efc\u8ff0\u8868",
            "\u8bc1\u636e\u94fe",
            "\u56fe\u8868\u951a\u5b9a",
            "\u6c34\u6027\u73af\u6c27\u4e73\u5316\u6ca5\u9752",
        ]:
            self.assertIn(expected, manifest_text)

        for bad_marker in [
            "\u7eee\u6350",
            "\u93c2",
            "\u934f",
            "\u9350",
            "\u704f",
            "\u8e47",
            "\u59d8",
            "\u6b05",
        ]:
            self.assertNotIn(bad_marker, manifest_text)

    def test_root_reader_handoff_files_are_mirrored_into_plugin(self):
        files = [
            "SKILL.md",
            "manifest.yaml",
            "references/evidence-to-review-handoff.md",
            "assets/templates/citation-handoff-template.csv",
            "assets/templates/figure-handoff-template.csv",
            "assets/templates/source-anchor-checklist.md",
            "assets/templates/figure-table-card-template.md",
        ]

        for relative in files:
            root_file = SKILL_ROOT / relative
            plugin_file = PLUGIN_ROOT / relative
            self.assertTrue(plugin_file.exists(), f"plugin mirror missing {relative}")
            self.assertEqual(
                root_file.read_bytes(),
                plugin_file.read_bytes(),
                f"plugin mirror drift for {relative}",
            )


if __name__ == "__main__":
    unittest.main()
