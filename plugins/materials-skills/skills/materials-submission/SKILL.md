---
name: materials-submission
version: "1.0.0"
stability: beta
description: Use when assembling a journal submission package (cover letter, highlights, checklist, declarations) for CBM, CCC, RMPD, or JBE.
---

# Materials Submission

`materials-submission` orchestrates Route C of the paper-production
orchestrator. It reads artifacts from `materials-writing`,
`materials-figure`, `materials-data`, and `materials-reviewer`, fills a
`submission-manifest.yaml`, and assembles a `submission-package/` directory
with a cover letter, highlights, checklist, declarations, and source-tracing
stubs.

## When to use

- Assemble a submission package for CBM, CCC, RMPD, or JBE.
- Draft a cover letter from manuscript metadata and journal fit.
- Generate Elsevier highlights from an abstract.
- Produce a journal-specific submission checklist.
- Check that declarations and live-verification fields are ready.

## When not to use

- If you need manuscript prose, use `materials-writing`.
- If you need figure production, use `materials-figure`.
- If you need FAIR data packaging, use `materials-data`.
- If you need reviewer simulation, use `materials-reviewer`.

## Architecture

- **Static layer** under `static/` holds the contract, the 6-phase Route C
  workflow, and the output package shape.
- **Dynamic layer** detects `task`, `journal`, and `article_type`, then
  loads only the fragments needed for the current job.
- **Tool layer** under `scripts/` assembles the package. The LLM fills
  cover-letter and highlights paragraphs from prepared inputs; the scripts
  enforce declaration boundaries and character limits.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`.
3. Detect axes and load matching fragments.
4. Help the user fill `submission-manifest.yaml` (title, authors,
   corresponding author, funding, conflicts, data availability status,
   optional paths to writing state, figure package, FAIR package,
   weakness-routing CSV).
5. Run `scripts/build_submission_package.py --dry-run` to validate the
   manifest. Resolve any refusal condition.
6. Run `scripts/build_submission_package.py` to assemble the package.
7. Fill the `[LLM: ...]` placeholders in `cover-letter.md` and
   `highlights.md` using the prepared inputs.
8. Re-check every `live_verification_fields` entry against the current
   Guide for Authors before submission.

## Evidence contract

- Do not fabricate declarations, suggested reviewers, funding, or conflicts.
- Empty declaration fields stay as `[LIVE-VERIFICATION: ...]` placeholders.
- The package records source paths in `SOURCE.md` stubs instead of copying
  potentially stale content.
- `live_verification_acknowledged: false` blocks final assembly.
