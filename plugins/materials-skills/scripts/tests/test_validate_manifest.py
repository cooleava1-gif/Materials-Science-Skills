"""Tests for validate_manifest.py."""

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_manifest


class TestValidateManifest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_base = Path(self.temp_dir.name)
        self.skills_root = self.temp_base / "skills"
        self.skills_root.mkdir(parents=True)

        self._orig_skills_root = validate_manifest.SKILLS_ROOT
        self._orig_contracts_dir = validate_manifest.CONTRACTS_DIR
        self._orig_registry_dir = validate_manifest.REGISTRY_DIR

        validate_manifest.SKILLS_ROOT = self.skills_root
        validate_manifest.CONTRACTS_DIR = self.temp_base / "nonexistent_contracts"
        validate_manifest.REGISTRY_DIR = self.temp_base / "nonexistent_registry"

    def tearDown(self):
        validate_manifest.SKILLS_ROOT = self._orig_skills_root
        validate_manifest.CONTRACTS_DIR = self._orig_contracts_dir
        validate_manifest.REGISTRY_DIR = self._orig_registry_dir
        self.temp_dir.cleanup()

    def _create_skill(self, name: str, manifest: dict):
        skill_dir = self.skills_root / name
        skill_dir.mkdir(parents=True)
        with open(skill_dir / "manifest.yaml", "w", encoding="utf-8") as f:
            yaml.dump(manifest, f)

    def test_valid_manifest_pass(self):
        """A manifest with proper axes and >=2 triggers should pass validation."""
        self._create_skill("materials-valid", {
            "axes": {
                "material_type": {
                    "values": {
                        "cement": {
                            "triggers": ["cement", "concrete", "portland"]
                        }
                    }
                }
            }
        })

        issues = validate_manifest.validate_skill("materials-valid")
        self.assertEqual(issues, [])

    def test_insufficient_triggers_fail(self):
        """An axis value with fewer than 2 triggers should produce an issue."""
        self._create_skill("materials-fail", {
            "axes": {
                "material_type": {
                    "values": {
                        "cement": {
                            "triggers": ["cement"]
                        }
                    }
                }
            }
        })

        issues = validate_manifest.validate_skill("materials-fail")
        self.assertTrue(len(issues) > 0)
        self.assertTrue(
            any("need >=2" in i for i in issues)
        )

    def test_invalid_yaml_fail(self):
        """A manifest with malformed YAML should produce a parse error."""
        skill_dir = self.skills_root / "materials-bad"
        skill_dir.mkdir(parents=True)
        with open(skill_dir / "manifest.yaml", "w", encoding="utf-8") as f:
            f.write("axes: [this: is: invalid: yaml: syntax\n")

        issues = validate_manifest.validate_skill("materials-bad")
        self.assertTrue(len(issues) > 0)
        self.assertIn("could not parse manifest.yaml", issues)