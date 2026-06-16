"""Tests for trigger file extraction and consistency.

Validates:
- Every manifest domain/family/journal entry has a corresponding trigger file.
- Every trigger file contains valid YAML with id and triggers list.
- Trigger count meets minimum thresholds (≥2 per domain).
- Trigger files match the material registry entries (file naming consistency).
"""

import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
TRIGGERS_DIR = REPO_ROOT / "_shared" / "triggers"
MANIFEST_FILE = REPO_ROOT / "skills" / "materials-research" / "manifest.yaml"
ROUTING_ONLY_DOMAINS = {"general"}
ROUTING_ONLY_FAMILIES = {"neutral"}


class TriggerFilePresenceTests(unittest.TestCase):
    """Every manifest axis value should have a corresponding trigger file."""

    def setUp(self):
        with open(MANIFEST_FILE, encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

    def test_all_domains_have_trigger_files(self):
        domain_values = self.manifest["axes"]["domain"]["values"]
        missing = []
        for did in domain_values:
            if did in ROUTING_ONLY_DOMAINS:
                continue
            if not (TRIGGERS_DIR / "domain" / f"{did}.yaml").exists():
                missing.append(did)
        self.assertFalse(missing, f"Domain trigger files missing: {missing}")

    def test_all_families_have_trigger_files(self):
        family_values = self.manifest["axes"]["material_family"]["values"]
        missing = []
        for fid in family_values:
            if fid in ROUTING_ONLY_FAMILIES:
                continue
            if not (TRIGGERS_DIR / "family" / f"{fid}.yaml").exists():
                missing.append(fid)
        self.assertFalse(missing, f"Family trigger files missing: {missing}")

    def test_all_journals_have_trigger_files(self):
        journal_values = self.manifest["axes"]["journal"]["values"]
        missing = []
        for jid in journal_values:
            if not (TRIGGERS_DIR / "journal" / f"{jid}.yaml").exists():
                missing.append(jid)
        self.assertFalse(missing, f"Journal trigger files missing: {missing}")


class TriggerFileContentTests(unittest.TestCase):
    """Every trigger file must contain valid data."""

    def test_all_trigger_files_have_id_and_triggers(self):
        for subdir in ("domain", "family", "journal"):
            dir_path = TRIGGERS_DIR / subdir
            if not dir_path.exists():
                continue
            for path in sorted(dir_path.glob("*.yaml")):
                with self.subTest(file=f"{subdir}/{path.name}"):
                    with open(path, encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    self.assertIn("id", data, f"{path.name} missing 'id'")
                    self.assertIn("triggers", data, f"{path.name} missing 'triggers'")
                    self.assertGreaterEqual(
                        len(data["triggers"]), 2,
                        f"{path.name}: only {len(data['triggers'])} triggers (need ≥2)"
                    )
                    self.assertEqual(data["id"], path.stem, f"{path.name}: id mismatch")

    def test_no_empty_triggers(self):
        for subdir in ("domain", "family", "journal"):
            dir_path = TRIGGERS_DIR / subdir
            if not dir_path.exists():
                continue
            for path in sorted(dir_path.glob("*.yaml")):
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                for t in data.get("triggers", []):
                    self.assertTrue(
                        isinstance(t, str) and t.strip(),
                        f"{path.name}: empty trigger found"
                    )


class TriggerRegistryConsistencyTests(unittest.TestCase):
    """Trigger file ids should match registry entry ids (for domain triggers)."""

    def test_domain_triggers_match_registry_entries(self):
        registry_dir = REPO_ROOT / "_shared" / "material-registry" / "entries"
        registry_ids = {p.stem for p in registry_dir.glob("*.yaml")}
        trigger_ids = {p.stem for p in (TRIGGERS_DIR / "domain").glob("*.yaml")}
        manifest_domain_ids = set(
            yaml.safe_load(MANIFEST_FILE.read_text(encoding="utf-8"))["axes"]["domain"]["values"]
        )
        routing_only = manifest_domain_ids - registry_ids
        self.assertEqual(
            registry_ids, trigger_ids,
            f"Mismatch: registry has {len(registry_ids)} entries, "
            f"triggers have {len(trigger_ids)} files"
        )
        self.assertLessEqual(
            routing_only,
            ROUTING_ONLY_DOMAINS,
            f"Unexpected non-registry domain routes: {sorted(routing_only)}",
        )


if __name__ == "__main__":
    unittest.main()
