import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = REPO_ROOT / "skills"
DOE_ROOT = SKILLS_ROOT / "materials-doe"
RESEARCH_ROOT = SKILLS_ROOT / "materials-research"
CONTRACT_PATH = REPO_ROOT / "_shared" / "contracts" / "doe-handoff.yaml"


class DoeSkillStructureTest(unittest.TestCase):
    def test_manifest_exists_and_has_required_keys(self):
        path = DOE_ROOT / "manifest.yaml"
        self.assertTrue(path.exists(), "manifest.yaml not found")
        manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
        for key in ["version", "always_load", "axes", "references", "handoffs"]:
            self.assertIn(key, manifest, f"Missing key: {key}")

    def test_manifest_axes_have_detect_and_values(self):
        manifest = yaml.safe_load((DOE_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        for axis_name, axis in manifest["axes"].items():
            with self.subTest(axis=axis_name):
                self.assertIn("detect", axis)
                self.assertIn("default", axis)
                self.assertIn("values", axis)
                for val_name, val in axis["values"].items():
                    self.assertIn("path", val, f"{axis_name}.{val_name} missing path")
                    self.assertIn("triggers", val, f"{axis_name}.{val_name} missing triggers")

    def test_skill_md_exists_with_frontmatter(self):
        path = DOE_ROOT / "SKILL.md"
        self.assertTrue(path.exists(), "SKILL.md not found")
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---"), "SKILL.md missing frontmatter")
        self.assertIn("name: materials-doe", text)
        self.assertIn("version:", text)
        self.assertIn("## Protocol", text)
        self.assertIn("## Gates", text)

    def test_readme_exists(self):
        path = DOE_ROOT / "README.md"
        self.assertTrue(path.exists(), "README.md not found")
        text = path.read_text(encoding="utf-8")
        self.assertIn("materials-doe", text)

    def test_always_load_files_exist(self):
        manifest = yaml.safe_load((DOE_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        for rel_path in manifest["always_load"]:
            full = (DOE_ROOT / rel_path).resolve()
            with self.subTest(path=rel_path):
                self.assertTrue(full.exists(), f"always_load file missing: {rel_path}")

    def test_doe_handoff_contract_exists(self):
        self.assertTrue(CONTRACT_PATH.exists(), "doe-handoff.yaml not found")
        contract = yaml.safe_load(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(contract["produced_by"], "materials-doe")
        self.assertIn("materials-writing", contract["consumed_by"])
        self.assertIn("materials-figure", contract["consumed_by"])

    def test_companion_skill_registered_in_research(self):
        manifest = yaml.safe_load((RESEARCH_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertIn("companion_skills", manifest)
        self.assertIn("doe", manifest["companion_skills"])
        self.assertEqual(manifest["companion_skills"]["doe"], "materials-doe")


if __name__ == "__main__":
    unittest.main()
