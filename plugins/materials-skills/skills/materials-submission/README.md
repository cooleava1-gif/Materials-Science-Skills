# materials-submission

Version: 1.0.0

`materials-submission` assembles a journal submission package for four
pilot Elsevier journals: CBM, CCC, RMPD, JBE. It reads artifacts from
sibling skills, fills a manifest, and produces a `submission-package/`
directory with cover letter, highlights, checklist, declarations, and
source-tracing stubs.

## When to use

- Assemble a submission package for a civil/construction materials paper.
- Draft a cover letter from manuscript metadata and journal fit.
- Generate Elsevier highlights from an abstract.
- Produce a journal-specific submission checklist.

## Core outputs

| Output | Purpose |
|---|---|
| `submission-package/MANIFEST.md` | Package manifest with source paths and statuses |
| `submission-package/cover-letter.md` | 7-paragraph cover letter skeleton |
| `submission-package/highlights.md` | 3-5 highlights, ≤85 characters each |
| `submission-package/keywords.md` | Keywords from manifest or writing state |
| `submission-package/declarations.md` | Declaration checklist with live-verification placeholders |
| `submission-package/submission-checklist.md` | Journal-specific submission checklist |
| `submission-package/manuscript/SOURCE.md` | Manuscript source stub |
| `submission-package/figures/SOURCE.md` | Figure package source stub |
| `submission-package/data/SOURCE.md` | FAIR package source stub |
| `submission-package/reviewer-risk-regression.md` | G6/G7 regression status |

## Boundaries

- The skill does not ship `.tex` or `.docx` template files. It points to
  the publisher's official template and fills metadata.
- The skill does not upload to Editorial Manager. It produces a package.
- The skill does not fabricate declarations, suggested reviewers, funding,
  or conflicts. Empty fields stay as live-verification placeholders.
- The skill does not rewrite manuscript text, regenerate figures, or
  rebuild the FAIR package. It records source paths.

## Pilot journals

| Journal | Publisher | Official class |
|---|---|---|
| CBM (Construction and Building Materials) | Elsevier | `elsarticle.cls` |
| CCC (Cement and Concrete Composites) | Elsevier | `elsarticle.cls` |
| RMPD (Road Materials and Pavement Design) | Taylor & Francis | `interact.cls` |
| JBE (Journal of Building Engineering) | Elsevier | `elsarticle.cls` |

## Operational references

| Reference | Use |
|---|---|
| `references/submission-package-protocol.md` | Assembly protocol and refusal conditions |
| `references/cover-letter-strategy.md` | Cover letter generation strategy |
| `references/highlights-strategy.md` | Highlights generation strategy |
| `references/declaration-boundary.md` | No-fabrication declaration boundary |
| `references/live-verification.md` | Live-verification placeholder rules |
