"""Unit tests for the civil claims validation engine."""

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_patent_claims import (  # noqa: E402
    Severity,
    check_independent_claim_technical_features,
    check_dependent_claim_references,
    check_support_in_specification,
    check_anti_patterns,
    check_unit_consistency,
    check_invention_type_alignment,
    check_claim_count_limits,
    load_kb,
    validate,
)


KB = load_kb(Path(__file__).resolve().parents[1] / "static" / "core" / "patent_kb.yaml")


def _base_draft():
    return {
        "claims": [
            {
                "number": 1,
                "type": "independent",
                "text": "一种水泥基复合材料，其特征在于：包括水泥、骨料和水；w/b为0.35；抗压强度为50MPa。",
                "feature_map": ["P001", "P002", "P003"],
            }
        ],
        "specification": {
            "技术领域": "本发明涉及建筑材料领域，具体涉及一种水泥基复合材料及其制备方法。",
            "背景技术": "普通混凝土水泥含量低，水灰比高，骨料通常采用卵石，强度不足。",
            "发明内容": "提供一种高强水泥基复合材料，包括水泥、骨料和水，骨料选用碎石。",
            "具体实施方式": "将水泥、骨料和水按比例混合，水灰比w/b为0.35，骨料为碎石，标准养护28天，测得抗压强度50MPa。",
        },
        "evidence_ledger": [
            {"id": "EV001", "source_ids": ["P001", "P002", "P003"], "support_status": "explicit"},
        ],
    }


def test_independent_claim_with_特征在于_passes():
    issues = check_independent_claim_technical_features(_base_draft()["claims"], KB)
    assert all(i.severity != Severity.ERROR for i in issues), issues


def test_independent_claim_without_特征在于_fails():
    draft = _base_draft()
    draft["claims"][0]["text"] = "一种水泥基复合材料，包括水泥、骨料和水。"
    issues = check_independent_claim_technical_features(draft["claims"], KB)
    assert any(i.severity == Severity.ERROR for i in issues)


def test_dependent_claim_correct_reference_passes():
    draft = _base_draft()
    draft["claims"].append({
        "number": 2,
        "type": "dependent",
        "text": "根据权利要求1所述的水泥基复合材料，其特征在于：所述骨料为碎石。",
        "feature_map": ["P004"],
    })
    issues = check_dependent_claim_references(draft["claims"], KB)
    assert all(i.severity != Severity.ERROR for i in issues), issues


def test_dependent_claim_bad_reference_fails():
    draft = _base_draft()
    draft["claims"].append({
        "number": 2,
        "type": "dependent",
        "text": "根据权利要求5所述的水泥基复合材料，其特征在于：所述骨料为碎石。",
        "feature_map": ["P004"],
    })
    issues = check_dependent_claim_references(draft["claims"], KB)
    assert any(i.severity == Severity.ERROR for i in issues)


def test_support_in_specification_passes():
    draft = _base_draft()
    issues = check_support_in_specification(draft["claims"], draft["specification"], KB)
    assert all(i.severity != Severity.ERROR for i in issues), issues


def test_support_in_specification_fails_on_unsupported_keyword():
    draft = _base_draft()
    draft["claims"][0]["text"] = "一种含纳米金刚石的复合材料，其特征在于：包括水泥和纳米金刚石。"
    issues = check_support_in_specification(draft["claims"], draft["specification"], KB)
    assert any(i.severity == Severity.ERROR for i in issues)


def test_anti_pattern_pure_functional_limitation_fails():
    draft = _base_draft()
    draft["claims"][0]["text"] = "一种用于建造高楼的装置，其特征在于：包括水泥。"
    issues = check_anti_patterns(draft["claims"], KB)
    assert any("pure_functional" in (i.code or "") for i in issues)


def test_anti_pattern_vague_result_fails():
    draft = _base_draft()
    draft["claims"][0]["text"] = "一种混凝土制备方法，其特征在于：混合、浇注，得到技术结果。"
    issues = check_anti_patterns(draft["claims"], KB)
    assert any("vague_result" in (i.code or "") for i in issues)


def test_unit_consistency_passes():
    draft = _base_draft()
    issues = check_unit_consistency(
        draft["claims"] + [{"number": 0, "text": json.dumps(draft["specification"], ensure_ascii=False)}],
        KB,
    )
    assert all(i.severity != Severity.ERROR for i in issues), issues


def test_unit_consistency_detects_aliased_strength():
    issues = check_unit_consistency([{"number": 1, "text": "抗压强度为50兆帕"}], KB)
    assert all(i.severity != Severity.ERROR for i in issues)


def test_invention_type_alignment_process_material_passes():
    issues = check_invention_type_alignment(_base_draft()["claims"], "process-material", KB)
    assert all(i.severity != Severity.ERROR for i in issues), issues


def test_invention_type_alignment_mismatch_warns():
    draft = _base_draft()
    draft["claims"][0]["text"] = "一种X，其特征在于：包括A和B。"
    issues = check_invention_type_alignment(draft["claims"], "process-material", KB)
    assert any(i.severity in (Severity.WARNING, Severity.INFO) for i in issues)


def test_claim_count_with_two_independents_passes():
    draft = _base_draft()
    draft["claims"].append({
        "number": 2,
        "type": "independent",
        "text": "一种制备方法，其特征在于：包括步骤S1、S2。",
    })
    issues = check_claim_count_limits(draft["claims"], KB)
    assert all(i.severity != Severity.ERROR for i in issues), issues


def test_claim_count_with_three_independents_fails():
    draft = _base_draft()
    draft["claims"].append({"number": 2, "type": "independent", "text": "一种制备方法，其特征在于：包括S1、S2。"})
    draft["claims"].append({"number": 3, "type": "independent", "text": "一种用途，其特征在于：用于建筑。"})
    issues = check_claim_count_limits(draft["claims"], KB)
    assert any(i.severity == Severity.ERROR for i in issues)


def test_full_validate_clean_draft_passes():
    draft = _base_draft()
    draft["claims"].append({
        "number": 2,
        "type": "dependent",
        "text": "根据权利要求1所述的水泥基复合材料，其特征在于：所述骨料为碎石。",
        "feature_map": ["P004"],
    })
    findings = validate(draft, "process-material", KB)
    errors = [f for f in findings if f.severity == Severity.ERROR]
    assert not errors, f"unexpected errors: {errors}"


def test_full_validate_dirty_draft_fails():
    draft = _base_draft()
    draft["claims"][0]["text"] = "一种用于建筑的装置，其特征在于：包括水泥。"
    findings = validate(draft, "process-material", KB)
    errors = [f for f in findings if f.severity == Severity.ERROR]
    assert errors
