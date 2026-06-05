import json
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_MODULES = [
    "civil-materials-research",
    "civil-materials-reader",
    "civil-materials-citation",
    "civil-materials-polishing",
    "civil-materials-response",
    "civil-materials-paper2ppt",
    "civil-materials-pptx",
    "civil-materials-figure",
    "civil-materials-data",
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
        self.assertIn("references/pressure-test-suite.md", skill_text)
        self.assertIn("examples/library/library-index.md", skill_text)
        self.assertIn("pressure-test-suite", manifest_text)
        self.assertIn("example-library", manifest_text)


if __name__ == "__main__":
    unittest.main()
