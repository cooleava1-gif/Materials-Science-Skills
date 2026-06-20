# Materials Paper to Chinese Patent

Convert materials science papers into evidence-grounded Chinese invention
patent drafts. Default invention type is **process-material**; switch via
`manifest.yaml` axes for algorithm or apparatus inventions.

## Pipeline

1. Detect source format, task mode, and invention type.
2. Build source map, terminology ledger, evidence ledger.
3. Draft claims with claim-feature map.
4. Validate via `validate_patent_draft.py` + `validate_patent_claims.py`.
5. Build DOCX package via `build_patent_package.py`.

## Scripts

| Script | Purpose |
|---|---|
| `extract_pdf_text.py` | Extract text from selectable PDFs |
| `init_patent_project.py` | Initialize project + draft.json template |
| `audit_claims.py` | Audit claim-to-source mapping |
| `validate_patent_draft.py` | Validate draft.json structure |
| `validate_patent_claims.py` | **Civil:** KB-driven claims content check |
| `build_patent_package.py` | Render 4 DOCX files + figures |
| `render_patent_docx.py` | DOCX rendering engine |
| `render_flowchart_svg.py` | Main flowchart SVG |
| `math_to_omml.py` | LaTeX → Office Math (OMML) |

## References

See `references/` for drafting guide, draft schema, corpus patterns,
audit method, and civil claims checklist.

## Verification

Run the release check after any structural change:

```bash
python scripts/run_release_checks.py --json
```
