"""Tests for skill_manifest.py."""

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_manifest import discover_skill_dirs, discover_skill_names, iter_skill_manifests, load_yaml


class TestSkillManifest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.skills_root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_skill(self, name: str, manifest: dict):
        skill_dir = self.skills_root / name
        skill_dir.mkdir(parents=True)
        with open(skill_dir / "manifest.yaml", "w", encoding="utf-8") as f:
            yaml.dump(manifest, f)

    def test_load_valid_manifest(self):
        """Loading a valid manifest should return the correct dict."""
        self._create_skill("materials-test", {"name": "test-skill", "version": "1.0"})
        manifest = load_yaml(self.skills_root / "materials-test" / "manifest.yaml")
        self.assertIsInstance(manifest, dict)
        self.assertEqual(manifest["name"], "test-skill")
        self.assertEqual(manifest["version"], "1.0")

    def test_load_nonexistent_manifest_raises(self):
        """Loading a non-existent manifest should raise FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_yaml(self.skills_root / "nonexistent" / "manifest.yaml")

    def test_load_invalid_yaml_raises(self):
        """Loading malformed YAML should raise yaml.YAMLError."""
        skill_dir = self.skills_root / "materials-bad"
        skill_dir.mkdir(parents=True)
        manifest_path = skill_dir / "manifest.yaml"
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(": invalid yaml")

        with self.assertRaises(yaml.YAMLError):
            load_yaml(manifest_path)

    def test_iter_skill_manifests(self):
        """iter_skill_manifests should yield correct (name, dir, manifest) tuples."""
        self._create_skill("materials-alpha", {"name": "alpha"})
        self._create_skill("materials-beta", {"name": "beta"})

        results = list(iter_skill_manifests(self.skills_root))
        self.assertEqual(len(results), 2)

        names = [r[0] for r in results]
        self.assertIn("materials-alpha", names)
        self.assertIn("materials-beta", names)

        for _, skill_dir, manifest in results:
            self.assertTrue(skill_dir.is_dir())
            self.assertIsInstance(manifest, dict)
            self.assertIn("name", manifest)

    def test_discover_skill_dirs_ignores_non_materials(self):
        """Only materials-* directories with manifest.yaml should be discovered."""
        self._create_skill("materials-valid", {"name": "valid"})
        # Create a non-materials directory (should be ignored)
        other_dir = self.skills_root / "other-dir"
        other_dir.mkdir(parents=True)
        (other_dir / "manifest.yaml").write_text("name: other", encoding="utf-8")

        dirs = discover_skill_dirs(self.skills_root)
        self.assertEqual(len(dirs), 1)
        self.assertEqual(dirs[0].name, "materials-valid")

        names = discover_skill_names(self.skills_root)
        self.assertEqual(names, ["materials-valid"])