import json
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_MODULES = [
    "materials-research",
    "materials-reader",
    "materials-citation",
    "materials-polishing",
    "materials-response",
    "materials-paper2ppt",
    "materials-pptx",
    "materials-figure",
    "materials-data",
]

REQUIRED_PRESSURE_THEMES = [
    "overclaim",
    "fake citation",
    "journal mismatch",
    "missing experimental conditions",
    "literal translation",
    "weak novelty",
    "figure caption",
    "pptx missing data",
    "FAIR data",
    "reviewer response",
    "statistics",
    "scope creep",
]


class AllModulePressureSuiteTest(unittest.TestCase):
    def test_pressure_suite_has_many_scenarios_and_all_modules_are_covered(self):
        pressure_dir = SKILL_ROOT / "tests" / "pressure-tests"
        files = sorted(pressure_dir.glob("*.md"))

        self.assertGreaterEqual(len(files), 12)
        combined = "\n".join(path.read_text(encoding="utf-8") for path in files)

        for module in REQUIRED_MODULES:
            self.assertIn(module, combined, f"{module} should be covered by pressure tests")
        for theme in REQUIRED_PRESSURE_THEMES:
            self.assertIn(theme, combined, f"{theme} pressure theme should exist")
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertIn("## Prompt", text)
            self.assertIn("## Expected Behavior", text)
            self.assertIn("## Failure Signs", text)

    def test_examples_library_has_one_entry_per_module(self):
        examples_dir = SKILL_ROOT / "examples" / "library"
        files = sorted(examples_dir.glob("*.md"))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in files)

        self.assertGreaterEqual(len(files), len(REQUIRED_MODULES) + 1)
        self.assertTrue((examples_dir / "library-index.md").exists())
        for module in REQUIRED_MODULES:
            self.assertIn(module, combined, f"{module} should have an example-library entry")
        for path in files:
            text = path.read_text(encoding="utf-8")
            if path.name != "library-index.md":
                self.assertIn("## Use Case", text)
                self.assertIn("## Example Output Shape", text)
                self.assertIn("## Quality Bar", text)

    def test_pressure_asset_audit_script_passes(self):
        script = SKILL_ROOT / "scripts" / "audit_pressure_assets.py"
        self.assertTrue(script.exists(), "audit_pressure_assets.py should exist")

        result = subprocess.run(
            [sys.executable, str(script), "--skill-root", str(SKILL_ROOT), "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)

        self.assertEqual(report["status"], "pass")
        self.assertGreaterEqual(report["pressure_test_count"], 12)
        self.assertGreaterEqual(report["example_count"], len(REQUIRED_MODULES) + 1)
        self.assertEqual(sorted(report["covered_modules"]), sorted(REQUIRED_MODULES))

    def test_router_exposes_pressure_suite_and_example_library(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        pressure_ref = SKILL_ROOT / "references" / "pressure-test-suite.md"

        self.assertTrue(pressure_ref.exists())
        self.assertTrue(pressure_ref.exists())
        self.assertTrue((SKILL_ROOT / "tests" / "pressure-tests").exists())
        self.assertTrue((SKILL_ROOT / "examples" / "library" / "library-index.md").exists())
        self.assertTrue((SKILL_ROOT / "examples" / "library" / "library-index.md").exists())
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        self.assertIn("pressure-test-suite", manifest_text)
        self.assertIn("example-library", manifest_text)
        self.assertTrue((SKILL_ROOT / "examples" / "library").exists())

    def test_release_maturity_references_cover_statistics_standards_and_broader_domains(self):
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        civil_generic = (SKILL_ROOT / "static" / "fragments" / "domain" / "civil-generic.md").read_text(
            encoding="utf-8"
        )
        journal_shortlist = (SKILL_ROOT / "references" / "journal-shortlist.md").read_text(encoding="utf-8")

        for reference in [
            "statistical-methods.md",
            "test-standards-mapping.md",
            "standards-mapping.md",
            "characterization-guide.md",
            "sustainability-claims-guide.md",
            "thesis-timeline.md",
        ]:
            self.assertTrue((SKILL_ROOT / "references" / reference).exists())
            self.assertIn(reference, manifest_text)
        for reference in [
            "statistical-methods.md",
            "test-standards-mapping.md",
            "standards-mapping.md",
            "characterization-guide.md",
            "sustainability-claims-guide.md",
            "thesis-timeline.md",
        ]:
            self.assertTrue((SKILL_ROOT / "references" / reference).exists())

        for domain in ["steel-metal", "geotechnical-materials", "timber-masonry", "waterproofing-sealants"]:
            self.assertIn(domain, manifest_text)
        for phrase in ["steel and metallic structures", "geotechnical and rock-soil", "waterproofing and sealants"]:
            self.assertIn(phrase, civil_generic)
        for journal in ["Cement and Concrete Research", "Journal of Materials in Civil Engineering", "Resources, Conservation and Recycling", "Fuel"]:
            self.assertIn(journal, journal_shortlist)

    def test_execution_level_guides_include_required_practical_content(self):
        checks = {
            "references/statistical-methods.md": ["ANOVA", "Tukey", "Shapiro-Wilk", "mean", "SD"],
            "references/standards-mapping.md": ["GB/T", "ASTM", "EN", "JTG", "AASHTO"],
            "references/characterization-guide.md": ["FTIR", "SEM", "fluorescence", "XRD", "TG/DTG", "rheology"],
            "references/sustainability-claims-guide.md": ["functional unit", "LCA", "screening", "tradeoff", "waterborne epoxy"],
            "references/thesis-timeline.md": ["First 4 Weeks", "Months 3-6", "review paper", "experimental manuscript"],
            "examples/library/manuscript-paragraph-examples.md": ["Context", "Gap", "Results", "Mechanism", "Implication"],
        }

        for relative, phrases in checks.items():
            with self.subTest(relative=relative):
                path = SKILL_ROOT / relative
                self.assertTrue(path.exists(), f"{relative} should exist")
                text = path.read_text(encoding="utf-8")
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_minor_optimization_references_are_cross_linked_and_methods_ready(self):
        statistical = (SKILL_ROOT / "references" / "statistical-methods.md").read_text(encoding="utf-8")
        standards = (SKILL_ROOT / "references" / "standards-mapping.md").read_text(encoding="utf-8")
        test_standards = (SKILL_ROOT / "references" / "test-standards-mapping.md").read_text(encoding="utf-8")
        examples = (SKILL_ROOT / "examples" / "library" / "manuscript-paragraph-examples.md").read_text(
            encoding="utf-8"
        )

        for phrase in ["Kruskal-Wallis + Dunn", "Bonferroni", "Post-hoc Dunn"]:
            self.assertIn(phrase, statistical)
        self.assertIn("Companion reference", standards)
        self.assertIn("test-standards-mapping.md", standards)
        self.assertIn("Companion reference", test_standards)
        self.assertIn("standards-mapping.md", test_standards)
        for phrase in ["Methods paragraph", "Material specification", "Formulation design", "Specimen preparation"]:
            self.assertIn(phrase, examples)


if __name__ == "__main__":
    unittest.main()
