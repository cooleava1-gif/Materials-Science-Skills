"""Tests for validate_handoffs.py."""

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_handoffs


class TestValidateHandoffs(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.skills_root = Path(self.temp_dir.name)

        self._orig_skills_root = validate_handoffs.SKILLS_ROOT
        self._orig_contracts_dir = validate_handoffs.CONTRACTS_DIR
        self._orig_collect = validate_handoffs.collect_manifest_handoff_topology

        validate_handoffs.SKILLS_ROOT = self.skills_root
        validate_handoffs.CONTRACTS_DIR = self.skills_root / "_shared" / "contracts"
        validate_handoffs.CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)

        # Patch collect_manifest_handoff_topology so validate_all() uses our temp root.
        # The default parameter value is captured at module load time, so we wrap it.
        _skills_root = self.skills_root
        _orig = self._orig_collect
        validate_handoffs.collect_manifest_handoff_topology = (
            lambda skills_root=None: _orig(_skills_root)
        )

    def tearDown(self):
        validate_handoffs.SKILLS_ROOT = self._orig_skills_root
        validate_handoffs.CONTRACTS_DIR = self._orig_contracts_dir
        validate_handoffs.collect_manifest_handoff_topology = self._orig_collect
        self.temp_dir.cleanup()

    def _create_skill(self, name: str, manifest: dict):
        skill_dir = self.skills_root / name
        skill_dir.mkdir(parents=True)
        with open(skill_dir / "manifest.yaml", "w", encoding="utf-8") as f:
            yaml.dump(manifest, f)

    def _create_contract(self, name: str, content: dict | None = None):
        if content is None:
            content = {"description": f"Contract for {name}"}
        contract_path = validate_handoffs.CONTRACTS_DIR / f"{name}.yaml"
        with open(contract_path, "w", encoding="utf-8") as f:
            yaml.dump(content, f)

    def test_valid_handoff_topology_pass(self):
        """Two skills with matching provides/consumes should produce no issues."""
        self._create_skill("materials-provider", {
            "handoffs": {
                "provides": {
                    "test_handoff": {"description": "A test handoff"}
                }
            }
        })
        self._create_skill("materials-consumer", {
            "handoffs": {
                "consumes": [
                    {"handoff": "test_handoff", "from": "materials-provider"}
                ]
            }
        })
        self._create_contract("test_handoff", {
            "description": "Test handoff",
            "produced_by": "materials-provider",
            "consumed_by": ["materials-consumer"],
        })

        issues = validate_handoffs.validate_all()
        self.assertEqual(issues, {})

    def test_provides_not_mapping_fail(self):
        """Manifest with handoffs.provides not a dict should produce an issue."""
        self._create_skill("materials-broken", {
            "handoffs": {
                "provides": "not_a_mapping"
            }
        })

        issues = validate_handoffs.validate_all()
        self.assertIn("materials-broken", issues)
        self.assertTrue(
            any("handoffs.provides must be a mapping" in i
                for i in issues["materials-broken"])
        )

    def test_dangling_consume_fail(self):
        """Consuming a handoff no skill provides should produce a dangling issue."""
        self._create_skill("materials-consumer", {
            "handoffs": {
                "consumes": [
                    {"handoff": "nonexistent_handoff"}
                ]
            }
        })
        self._create_contract("nonexistent_handoff")

        issues = validate_handoffs.validate_all()
        self.assertIn("materials-consumer", issues)
        self.assertTrue(
            any("dangling" in i for i in issues["materials-consumer"])
        )

    def test_nonexistent_path_fail(self):
        """Passing a non-existent skills_root should return empty topology."""
        result = validate_handoffs.collect_manifest_handoff_topology(
            Path("/nonexistent/path/12345")
        )
        self.assertEqual(result["provides_by_skill"], {})
        self.assertEqual(result["consumes_by_skill"], {})
        self.assertEqual(result["issues"], {})