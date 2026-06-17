"""Contract tests for the Material Registry.

Validates that:
- The registry schema exists and is parseable.
- All 29 entries are valid YAML with required fields.
- The index matches the on-disk entries.
- Referenced file paths exist.
"""

import unittest
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = REPO_ROOT / "_shared" / "material-registry"
ENTRIES_DIR = REGISTRY_DIR / "entries"
INDEX_FILE = REGISTRY_DIR / "registry-index.yaml"
SCHEMA_FILE = REGISTRY_DIR / "registry-schema.yaml"
FAMILY_TRIGGER_DIR = REPO_ROOT / "_shared" / "triggers" / "family"

VALID_FAMILIES = {"civil", "polymers", "metals", "ceramics", "functional", "nano"}
VALID_TIERS = {"full", "partial", "skeleton", "generic"}

EXPECTED_ENTRIES = {  # id -> coverage_tier
    "asphalt-pavement": "full",
    "cement-concrete": "full",
    "construction-materials": "full",
    "steel-metal": "full",
    "geotechnical-materials": "full",
    "timber-masonry": "full",
    "waterproofing-sealants": "full",
    "sustainability-durability": "full",
    "civil-generic": "full",
    "thermoplastics": "full",
    "thermosets": "full",
    "rubber-elastomers": "full",
    "polymer-composites": "full",
    "thermal-insulation": "full",
    "ferrous-alloys": "full",
    "nonferrous-alloys": "full",
    "high-temperature-alloys": "full",
    "additive-metals": "full",
    "structural-ceramics": "full",
    "functional-ceramics": "full",
    "refractories": "full",
    "bioceramics": "full",
    "semiconductors": "skeleton",
    "dielectrics-piezoelectrics": "skeleton",
    "photonic-optoelectronic": "skeleton",
    "nanoparticles": "skeleton",
    "nano-thin-films": "skeleton",
    "2d-materials": "skeleton",
    "nanocomposites": "skeleton",
}


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


class RegistrySchemaTests(unittest.TestCase):
    def test_schema_file_exists(self):
        self.assertTrue(SCHEMA_FILE.exists())

    def test_schema_is_valid_yaml(self):
        schema = _load_yaml(SCHEMA_FILE)
        self.assertIn("version", schema)
        self.assertIn("fields", schema)
        self.assertIn("required", schema)

    def test_schema_defines_all_field_types(self):
        schema = _load_yaml(SCHEMA_FILE)
        fields = schema.get("fields", {})
        for field_name in ("name", "id", "family", "coverage_tier", "description", "skill_mapping"):
            self.assertIn(field_name, fields, f"schema missing field definition: {field_name}")

    def test_schema_family_values_match_family_triggers(self):
        schema = _load_yaml(SCHEMA_FILE)
        schema_families = set(schema["fields"]["family"]["values"])
        trigger_families = {path.stem for path in FAMILY_TRIGGER_DIR.glob("*.yaml")}
        self.assertEqual(trigger_families, schema_families)


class RegistryEntryTests(unittest.TestCase):
    def setUp(self):
        self.entry_files = sorted(ENTRIES_DIR.glob("*.yaml"))
        self.assertGreaterEqual(
            len(self.entry_files), 29,
            f"Expected ≥29 entries, found {len(self.entry_files)}"
        )

    def test_all_entries_valid_yaml_with_required_fields(self):
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)
                for field in ("name", "id", "family", "coverage_tier", "description"):
                    self.assertIn(field, data, f"{path.name} missing {field}")
                desc = data.get("description", {})
                self.assertIn("summary", desc, f"{path.name} missing description.summary")

    def test_id_matches_filename(self):
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)
                self.assertEqual(data.get("id"), path.stem)

    def test_valid_family(self):
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)
                self.assertIn(data.get("family"), VALID_FAMILIES)

    def test_valid_coverage_tier(self):
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)
                self.assertIn(data.get("coverage_tier"), VALID_TIERS)

    def test_expected_entries_present(self):
        found_ids = {p.stem for p in self.entry_files}
        for eid in EXPECTED_ENTRIES:
            self.assertIn(eid, found_ids, f"expected entry {eid} not found")

    def test_coverage_tiers_match_expectations(self):
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)
                eid = data.get("id")
                expected_tier = EXPECTED_ENTRIES.get(eid)
                if expected_tier:
                    self.assertEqual(
                        data.get("coverage_tier"), expected_tier,
                        f"{eid}: expected tier '{expected_tier}', got '{data.get('coverage_tier')}'"
                    )

    def test_no_duplicate_ids(self):
        ids = []
        for path in self.entry_files:
            data = _load_yaml(path)
            ids.append(data.get("id"))
        self.assertEqual(len(ids), len(set(ids)), "duplicate ids found")

    def test_skill_mapping_has_expected_structure(self):
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)
                sm = data.get("skill_mapping", {})
                self.assertIsInstance(sm, dict)

    def test_full_tier_entry_has_narrative_guide(self):
        """Tier 'full' entries must have a narrative guide."""
        for path in self.entry_files:
            data = _load_yaml(path)
            if data.get("coverage_tier") == "full":
                with self.subTest(entry=path.stem):
                    narrative = data.get("narrative", {})
                    skill_refs = narrative.get("skill_references", {})
                    self.assertIn(
                        "narrative_guide", skill_refs,
                        f"{path.name}: full-tier entry missing narrative_guide"
                    )

    def test_full_and_partial_have_domain_fragment(self):
        """Tier 'full' and 'partial' entries must reference a domain fragment."""
        for path in self.entry_files:
            data = _load_yaml(path)
            if data.get("coverage_tier") in ("full", "partial"):
                with self.subTest(entry=path.stem):
                    narrative = data.get("narrative", {})
                    skill_refs = narrative.get("skill_references", {})
                    self.assertIn(
                        "domain_fragment", skill_refs,
                        f"{path.name}: {data['coverage_tier']}-tier entry missing domain_fragment"
                    )

    def test_full_tier_entry_has_figure_packages(self):
        """Tier 'full' entries must have a non-empty list of figure_packages."""
        for path in self.entry_files:
            data = _load_yaml(path)
            if data.get("coverage_tier") == "full":
                with self.subTest(entry=path.stem):
                    sm = data.get("skill_mapping", {})
                    fps = sm.get("figure_packages", [])
                    self.assertTrue(
                        isinstance(fps, list) and len(fps) > 0,
                        f"{path.name}: full-tier entry must have a non-empty figure_packages list"
                    )

    def test_referenced_files_exist(self):
        """Verify that skill_mapping and narrative file references exist on disk."""
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)

                # Check skill_mapping file references
                sm = data.get("skill_mapping", {})
                for key in ("figure_scripts", "figure_packages", "data_schemas"):
                    for ref in sm.get(key, []) or []:
                        if isinstance(ref, str) and ref.startswith("skills/"):
                            full_path = REPO_ROOT / ref
                            self.assertTrue(
                                full_path.exists(),
                                f"{path.name}: skill_mapping.{key} '{ref}' not found"
                            )

                # Check narrative skill_references
                narrative = data.get("narrative", {})
                skill_refs = narrative.get("skill_references", {}) if isinstance(narrative, dict) else {}
                for ref_key, ref_path in skill_refs.items():
                    if isinstance(ref_path, str) and ref_path.startswith("skills/"):
                        full_path = REPO_ROOT / ref_path
                        self.assertTrue(
                            full_path.exists(),
                            f"{path.name}: narrative.skill_references.{ref_key} '{ref_path}' not found"
                        )

    def test_cross_references_point_to_existing_entries(self):
        for path in self.entry_files:
            with self.subTest(entry=path.stem):
                data = _load_yaml(path)
                cross = data.get("cross_references", {}) or {}
                for ref in cross.get("related", []) or []:
                    self.assertTrue(
                        (ENTRIES_DIR / f"{ref}.yaml").exists(),
                        f"{path.name}: related '{ref}' has no entry"
                    )
                parent = cross.get("parent")
                if parent:
                    self.assertTrue(
                        (ENTRIES_DIR / f"{parent}.yaml").exists(),
                        f"{path.name}: parent '{parent}' has no entry"
                    )


class RegistryIndexTests(unittest.TestCase):
    def test_index_exists_and_is_valid(self):
        self.assertTrue(INDEX_FILE.exists())
        index = _load_yaml(INDEX_FILE)
        self.assertIn("materials", index)

    def test_index_lists_all_entries(self):
        index = _load_yaml(INDEX_FILE)
        indexed_ids = {m["id"] for m in index["materials"]}
        entry_ids = {p.stem for p in ENTRIES_DIR.glob("*.yaml")}
        missing = entry_ids - indexed_ids
        self.assertFalse(missing, f"entries missing from index: {missing}")
        extra = indexed_ids - entry_ids
        self.assertFalse(extra, f"extra entries in index: {extra}")

    def test_index_entry_fields(self):
        index = _load_yaml(INDEX_FILE)
        for entry in index["materials"]:
            with self.subTest(entry=entry.get("id", "?")):
                for field in ("id", "name", "family", "coverage_tier"):
                    self.assertIn(field, entry, f"index entry missing {field}")


if __name__ == "__main__":
    unittest.main()
