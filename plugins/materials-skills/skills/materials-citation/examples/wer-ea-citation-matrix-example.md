# Citation Matrix Example: WER-EA Mini-Review

This example shows a claim-citation matrix for a waterborne epoxy modified
emulsified asphalt (WER-EA) mini-review targeting CBM.

## Input

- **Topic**: waterborne epoxy modified emulsified asphalt tack coat
- **Journals**: CBM, JBE, RMPD
- **Claims**: 5 default claims from `build_citation_matrix.py`

## Command

```powershell
python skills/materials-citation/scripts/build_citation_matrix.py `
  --topic "waterborne epoxy emulsified asphalt tack coat" `
  --journals "CBM,JBE,RMPD" `
  --output wer-ea-citation-matrix.csv
```

## Output Fields

| Field | Purpose |
|---|---|
| `claim_id` | Sequential ID (CIT-001, CIT-002, ...) |
| `evidence_layer` | Classified evidence layer (bonding, mechanism, durability, etc.) |
| `source_role` | primary experimental evidence / review evidence |
| `reviewer_risk` | must-fix / strengthen / monitor |
| `search_query` | Auto-generated PubMed/Crossref query |

## Claim-Evidence Mapping

| Claim | Evidence Layer | Source Role |
|---|---|---|
| Research gap and novelty | review_background | review evidence |
| Material design rationale | material_formulation | primary experimental evidence |
| Performance improvement | bonding_interface_performance | primary experimental evidence |
| Mechanism explanation | microstructure_chemistry | primary experimental evidence |
| Durability or service-condition relevance | moisture_aging_durability | primary experimental evidence |

## Reviewer-Safe Usage

- Each claim row includes a `reviewer_risk` flag
- `risk_note` reminds the writer not to overclaim without mapped sources
- The matrix hands off to `materials-reader` for evidence-chain extraction
