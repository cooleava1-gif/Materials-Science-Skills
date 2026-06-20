"""Unit tests for the structural draft.json validator."""

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_patent_draft import Severity, validate_draft  # noqa: E402


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "civil-concrete-strengthening" / "draft.json"


def _draft():
    return {
        "title": "一种高强水泥基复合材料",
        "metadata": {
            "jurisdiction": "CNIPA",
            "invention_type": "process-material",
            "language_mode": "zh",
        },
        "source_map": [{"id": "P001", "text": "..."}],
        "claims": [
            {"number": 1, "type": "independent", "text": "一种X，其特征在于：A和B。"},
            {"number": 2, "type": "dependent", "depends_on": [1], "text": "根据权利要求1所述的X，其特征在于：A为a。"},
        ],
        "specification": {
            "技术领域": "建筑材料",
            "背景技术": "普通混凝土强度低。",
            "发明内容": "提供一种高强混凝土。",
            "具体实施方式": "按配比混合。",
        },
        "abstract": "本发明公开一种高强混凝土，由水泥、骨料和水组成，28天抗压强度50MPa。",
        "invention_concept": {"problem": "强度不足", "solution": "高强配合比", "beneficial_effects": "50MPa"},
        "abstract_figure_number": 1,
    }


def test_clean_draft_passes():
    issues = validate_draft(_draft())
    errors = [i for i in issues if i.severity == Severity.ERROR]
    assert not errors, errors


def test_missing_top_key_fails():
    draft = _draft()
    del draft["title"]
    issues = validate_draft(draft)
    assert any(i.code == "missing_top_key" for i in issues)


def test_missing_metadata_key_fails():
    draft = _draft()
    del draft["metadata"]["jurisdiction"]
    issues = validate_draft(draft)
    assert any(i.code == "missing_metadata_key" for i in issues)


def test_empty_claims_fails():
    draft = _draft()
    draft["claims"] = []
    issues = validate_draft(draft)
    assert any(i.code == "no_claims" for i in issues)


def test_claim_number_gap_fails():
    draft = _draft()
    draft["claims"][1]["number"] = 4
    issues = validate_draft(draft)
    assert any(i.code == "claim_number_sequence" for i in issues)


def test_empty_claim_text_fails():
    draft = _draft()
    draft["claims"][0]["text"] = ""
    issues = validate_draft(draft)
    assert any(i.code == "empty_claim" for i in issues)


def test_missing_specification_section_fails():
    draft = _draft()
    del draft["specification"]["技术领域"]
    issues = validate_draft(draft)
    assert any(i.code == "missing_specification_section" for i in issues)


def test_short_abstract_warns():
    draft = _draft()
    draft["abstract"] = "短"
    issues = validate_draft(draft)
    assert any(i.code == "short_abstract" for i in issues)


def test_bad_abstract_figure_number_fails():
    draft = _draft()
    draft["abstract_figure_number"] = 0
    issues = validate_draft(draft)
    assert any(i.code == "bad_abstract_figure_number" for i in issues)


def test_example_draft_passes():
    draft = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    issues = validate_draft(draft)
    errors = [i for i in issues if i.severity == Severity.ERROR]
    assert not errors, errors
