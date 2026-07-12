"""Regression tests for template-driven submission package outputs."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import build_submission_package
import generate_checklist
import generate_cover_letter
import validate_journal_templates
from template_support import load_template


def manifest_for(journal: str, article_type: str = "research-article") -> dict:
    return {
        "target_journal": journal,
        "article_type": article_type,
        "title": "Template-driven submission test",
        "corresponding_author": "Test Author",
        "funding": "Test Grant",
        "conflicts": "No competing interests.",
        "data_availability_status": "ready",
        "code_availability_status": "ready",
        "live_verification_acknowledged": True,
    }


class TemplateDrivenOutputTests(unittest.TestCase):
    def test_nature_materials_omits_disabled_keywords_and_funding(self) -> None:
        template = load_template("nature-materials")
        manifest = manifest_for("nature-materials", "short-communication")

        checklist = generate_checklist.render_checklist(template, "short-communication")
        declarations = build_submission_package.render_declarations(manifest, template)
        cover_letter = generate_cover_letter.render_cover_letter(manifest, template, "")

        self.assertNotIn("Keywords", checklist)
        self.assertNotIn("Funding:", declarations)
        self.assertNotIn("Funding:", cover_letter)

        with tempfile.TemporaryDirectory() as directory:
            package_dir = Path(directory) / "submission-package"
            written = build_submission_package.write_package(
                package_dir,
                manifest,
                template,
                {},
                {"G6": "not_applicable", "G7": "not_applicable"},
                "",
            )
            self.assertNotIn("keywords.md", written)
            self.assertFalse((package_dir / "keywords.md").exists())

    def test_jmca_omits_disabled_funding_in_all_declaration_outputs(self) -> None:
        template = load_template("jmca")
        manifest = manifest_for("jmca", "perspective")

        declarations = build_submission_package.render_declarations(manifest, template)
        cover_letter = build_submission_package.render_cover_letter_inline(manifest, template, "")

        self.assertNotIn("Funding:", declarations)
        self.assertNotIn("Funding:", cover_letter)

    def test_building_environment_letter_marks_abstract_not_required(self) -> None:
        template = load_template("building-environment")
        letter = next(
            item for item in template["article_types"] if item["id"] == "letter"
        )

        checklist = generate_checklist.render_checklist(template, "letter")

        self.assertIn("abstract", letter.get("required_fields_exclude", []))
        self.assertIn("No abstract required for this article type", checklist)
        self.assertNotIn("abstract within", checklist)

    def test_validator_rejects_missing_article_type_field_exclusion(self) -> None:
        content = """
journal_id: example
article_types:
  - id: letter
    submission_label: Letter
    abstract_required: false
required_fields:
  - title
  - abstract
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.yaml"
            path.write_text(content, encoding="utf-8")
            path.with_suffix(".md").write_text("# Example\n", encoding="utf-8")
            issues: list[str] = []

            validate_journal_templates.validate_template(path, issues)

        self.assertTrue(
            any("disables abstract" in issue for issue in issues),
            issues,
        )

    def test_invalid_article_type_dry_run_does_not_raise_while_listing_files(self) -> None:
        manifest = SKILL_DIR / "evals" / "invalid-acta-review.yaml"
        stdout = StringIO()
        stderr = StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = build_submission_package.main(
                ["--manifest", str(manifest), "--dry-run"]
            )

        self.assertEqual(0, status)
        self.assertIn("article_type 'review-article' not in", stderr.getvalue())
        self.assertIn("Files that would be written:", stdout.getvalue())

    def test_disabled_data_availability_is_omitted_from_declarations(self) -> None:
        template = copy.deepcopy(load_template("nature-materials"))
        template["declaration_requirements"]["data_availability"] = False
        manifest = manifest_for("nature-materials")

        declarations = build_submission_package.render_declarations(manifest, template)
        cover_letter = generate_cover_letter.render_cover_letter(manifest, template, "")

        self.assertNotIn("Data availability", declarations)
        self.assertNotIn("Data availability", cover_letter)

    def test_validator_rejects_invalid_declaration_requirement_value(self) -> None:
        content = """
journal_id: example
article_types:
  - id: research-article
    submission_label: Article
required_fields:
  - title
declaration_requirements:
  data_availability: "false"
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.yaml"
            path.write_text(content, encoding="utf-8")
            path.with_suffix(".md").write_text("# Example\n", encoding="utf-8")
            issues: list[str] = []

            validate_journal_templates.validate_template(path, issues)

        self.assertTrue(
            any("invalid declaration requirement" in issue for issue in issues),
            issues,
        )


if __name__ == "__main__":
    unittest.main()
