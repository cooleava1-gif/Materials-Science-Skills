import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class NarrativeGuidesTest(unittest.TestCase):
    _narrative_files = [
        "asphalt-narrative.md",
        "asphalt-pavement-narrative.md",
        "cement-narrative.md",
        "cement-concrete-narrative.md",
        "ceramics-narrative.md",
        "structural-ceramics-narrative.md",
        "bioceramics-narrative.md",
        "refractories-narrative.md",
        "functional-ceramics-narrative.md",
        "ferrous-alloys-narrative.md",
        "nonferrous-alloys-narrative.md",
        "high-temperature-alloys-narrative.md",
        "additive-metals-narrative.md",
        "steel-metal-narrative.md",
        "nano-thin-films-narrative.md",
        "nanoparticles-narrative.md",
        "nanocomposites-narrative.md",
        "2d-materials-narrative.md",
        "dielectrics-piezoelectrics-narrative.md",
        "photonic-optoelectronic-narrative.md",
        "semiconductors-narrative.md",
        "thermal-insulation-narrative.md",
        "insulation-narrative.md",
        "thermoplastics-narrative.md",
        "thermosets-narrative.md",
        "rubber-elastomers-narrative.md",
        "polymer-composites-narrative.md",
        "waterborne-epoxy-narrative.md",
        "construction-materials-narrative.md",
        "civil-generic-narrative.md",
        "geotechnical-materials-narrative.md",
        "timber-masonry-narrative.md",
        "waterproofing-sealants-narrative.md",
        "sustainability-durability-narrative.md",
    ]

    def test_all_narrative_guide_files_exist(self):
        for filename in self._narrative_files:
            path = SKILL_ROOT / "references" / filename
            self.assertTrue(path.exists(), f"{filename} should exist")

    def test_each_narrative_contains_required_sections(self):
        required_sections = [
            "narrative arc",
            "Key evidence chain",
            "Common section structure",
            "Useful keywords",
            "Reviewer-safe language",
        ]
        _short_narratives = {"waterborne-epoxy-narrative.md"}
        for filename in self._narrative_files:
            with self.subTest(filename=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                if filename in _short_narratives:
                    self.assertIn("manuscript narrative", text.lower(),
                                  f"{filename} should describe the narrative")
                    self.assertIn("keywords", text.lower(),
                                  f"{filename} should contain keywords")
                else:
                    for section in required_sections:
                        self.assertIn(section, text,
                                      f"{filename} should contain '{section}'")

    def test_each_narrative_is_non_empty_with_substantial_content(self):
        for filename in self._narrative_files:
            with self.subTest(filename=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                self.assertGreater(len(text.strip()), 500,
                                   f"{filename} should have substantial content (>500 chars)")

    def test_civil_narratives_have_domain_specific_content(self):
        civil_files = [
            "asphalt-narrative.md",
            "cement-narrative.md",
            "construction-materials-narrative.md",
            "civil-generic-narrative.md",
        ]
        for filename in civil_files:
            with self.subTest(civil=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                self.assertIn("Introduction", text,
                              f"{filename} should have Introduction section structure")
                self.assertIn("standard", text.lower(),
                              f"{filename} should mention 'standard'")

    def test_metals_narratives_have_domain_specific_content(self):
        metals_files = [
            "ferrous-alloys-narrative.md",
            "nonferrous-alloys-narrative.md",
            "steel-metal-narrative.md",
        ]
        for filename in metals_files:
            with self.subTest(metals=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                self.assertIn("structure", text.lower(),
                              f"{filename} should mention 'structure'")
                self.assertIn("tensile", text.lower(),
                              f"{filename} should mention 'tensile'")

    def test_nano_narratives_have_domain_specific_content(self):
        nano_files = [
            "nanoparticles-narrative.md",
            "nanocomposites-narrative.md",
            "2d-materials-narrative.md",
            "nano-thin-films-narrative.md",
        ]
        for filename in nano_files:
            with self.subTest(nano=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                for keyword in ["size", "TEM", "surface"]:
                    self.assertIn(keyword.lower(), text.lower(),
                                  f"{filename} should mention '{keyword}'")


if __name__ == "__main__":
    unittest.main()