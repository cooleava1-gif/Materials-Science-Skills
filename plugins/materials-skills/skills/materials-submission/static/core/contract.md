# Submission Package Contract

`materials-submission` produces a submission package directory. It is not a
replacement for manuscript writing, figure production, or FAIR packaging.

## Inputs

- `submission-manifest.yaml` (required): target journal, article type,
  title, authors, corresponding author, funding, conflicts, data
  availability status, optional source paths, `live_verification_acknowledged`.
- Optional `materials-writing/state.json` + foundation files.
- Optional `materials-figure` figure package manifest.
- Optional `materials-data` FAIR package manifest.
- Optional `materials-reviewer` weakness-routing CSV.
- `_shared/journal-formats/<journal>.md` fact sheet.
- `_shared/journal-templates/<journal>.yaml` + `.md` guidance.

## Outputs

- `submission-package/MANIFEST.md`
- `submission-package/cover-letter.md`
- `submission-package/highlights.md` (when `highlights_required` is true)
- `submission-package/keywords.md`
- `submission-package/declarations.md`
- `submission-package/submission-checklist.md`
- `submission-package/manuscript/SOURCE.md`
- `submission-package/figures/SOURCE.md`
- `submission-package/data/SOURCE.md`
- `submission-package/reviewer-risk-regression.md`

## Refusal conditions

The script refuses to write a final package and emits a dry-run manifest
when:

- `live_verification_acknowledged` is false
- `target_journal` is not one of the pilot journals (cbm, ccc, rmpd, jbe)
- `data_availability_status` is `pending` and no FAIR package path is set
- `title` or `corresponding_author` is missing

## Evidence boundary

The skill records source paths in `SOURCE.md` stubs. It does not copy
manuscript text, figures, or data into the package. Cover letter and
highlights placeholders must be filled by the LLM using only the prepared
inputs; declarations must not be fabricated.
