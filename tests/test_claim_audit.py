"""Tests for the Claim Strength Audit engine.

Tests:
- Overclaim detection (proves, confirms, significantly, etc.)
- Missing evidence marker detection
- Downgrade suggestions
- Registry cross-reference (when material_id is provided)
- Score computation
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "claim_strength_audit.py"


def _run(text: str, *args: str) -> dict:
    """Run the audit engine and return parsed JSON."""
    cmd = [sys.executable, str(AUDIT_SCRIPT), "--text", text, "--json", *args]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


class ClaimStrengthAuditOverclaimTests(unittest.TestCase):
    """Verify that overclaim patterns are detected."""

    def test_detects_proves(self):
        result = _run("This proves the mechanism.")
        self.assertGreaterEqual(result["total_issues"], 1)
        self.assertTrue(any("proves" in f.get("pattern", "") for f in result["findings"]))

    def test_detects_confirms(self):
        result = _run("FTIR confirms the curing reaction.")
        issues = [f for f in result["findings"] if f["type"] == "overclaim"]
        self.assertTrue(any("confirmed" in f["pattern"] or "confirms" in f["pattern"] for f in issues))

    def test_detects_significantly_without_pvalue(self):
        result = _run("The material significantly improves bonding strength.")
        self.assertTrue(
            any("significantly" in f.get("pattern", "") for f in result["findings"])
        )

    def test_detects_green_unqualified(self):
        result = _run("This is a green material for construction.")
        self.assertTrue(
            any("green" in f.get("pattern", "") for f in result["findings"])
        )

    def test_detects_field_ready_unqualified(self):
        result = _run("The material is suitable for field application.")
        self.assertTrue(
            any("field-ready" in f.get("pattern", "") or "field" in f.get("pattern", "").lower()
                for f in result["findings"])
        )

    def test_empty_for_safe_language(self):
        result = _run(
            "The increase in bond strength may be attributed to epoxy crosslinking. "
            "FTIR suggests the formation of C-O-C ether bonds."
        )
        self.assertEqual(result["total_issues"], 0)
        self.assertEqual(result["score"]["level"], "excellent")


class MissingEvidenceTests(unittest.TestCase):
    def test_detects_needs_quantitative_result(self):
        result = _run("The bonding improved significantly. [needs quantitative result]")
        self.assertTrue(
            any("needs quantitative" in f.get("pattern", "") for f in result["findings"])
        )

    def test_detects_needs_mechanism_evidence(self):
        result = _run("The mechanism involves crosslinking. [needs mechanism evidence]")
        self.assertTrue(
            any("mechanism evidence" in f.get("pattern", "") for f in result["findings"])
        )


class ScoreComputationTests(unittest.TestCase):
    def test_score_drops_with_overclaim(self):
        safe = _run(
            "The increase may be attributed to A. XRD indicates phase B."
        )
        risky = _run(
            "This proves the mechanism. This green material significantly improves everything."
        )
        self.assertGreater(safe["score"]["score"], risky["score"]["score"])

    def test_excellent_level_at_zero_issues(self):
        result = _run("The data are consistent with the proposed mechanism.")
        self.assertEqual(result["score"]["level"], "excellent")


class DowngradeSuggestionsTests(unittest.TestCase):
    def test_proves_suggests_downgrade(self):
        result = _run("This proves the concept.")
        downgrades = [f for f in result["findings"] if f["type"] == "downgrade"]
        self.assertTrue(any("proves" in str(f) or "suggests" in f.get("suggestion", "").lower()
                          for f in downgrades))


class JSONOutputTests(unittest.TestCase):
    def test_json_contains_expected_fields(self):
        result = _run("This proves the mechanism. [needs evidence]")
        for field in ("text_length", "sentence_count", "total_issues",
                      "high_severity", "findings", "score"):
            self.assertIn(field, result, f"missing {field}")
        self.assertIn("score", result.get("score", {}))
        self.assertIn("level", result.get("score", {}))


if __name__ == "__main__":
    unittest.main()
