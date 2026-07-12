# Submission Package Workflow

The workflow follows Route C of the paper-production orchestrator.

## Phase 1: Journal fit confirmation

Load `_shared/journal-formats/<journal>.md` and
`_shared/journal-templates/<journal>.yaml`. Emit a journal-fit note and
mark every `live_verification_fields` entry with a placeholder.

## Phase 2: Manuscript package audit

If `writing_state_path` is set, read `state.json` and the foundation files
referenced by it. Pre-fill title, abstract, authors, and keywords. Emit
`manuscript/SOURCE.md` with the source path and status. If the writing
state is missing, ask the user to fill title, abstract, and authors in the
manifest.

## Phase 3: Figure and graphical abstract intake

If `figure_package_path` is set, read the figure package manifest. Record
figure status and caption_boundary state. Emit `figures/SOURCE.md` plus a
graphical-abstract concept note. If the path is missing, record the
artifact as `not_applicable`.

## Phase 4: Data and declaration boundary

If `fair_package_path` is set, read the FAIR package manifest. Record data
availability status. Emit `data/SOURCE.md` and `declarations.md` from the
manifest fields. Empty declaration fields stay as
`[LIVE-VERIFICATION: ...]` placeholders.

## Phase 5: Reviewer-risk regression

If `weakness_routing_path` is set, read the weakness-routing CSV. Compute
G6 (Reviewer Simulation) and G7 (Submission Fit) regression status. Emit
`reviewer-risk-regression.md`. If the path is missing, record G6/G7 as
`not_applicable` with a note that reviewer simulation has not been run.

## Phase 6: Final assembly

Run `build_submission_package.py`. The script creates the
`submission-package/` directory, writes `MANIFEST.md`, calls the three
generator scripts, writes `SOURCE.md` stubs, and writes
`reviewer-risk-regression.md`. Use `--dry-run` to validate the manifest
before final assembly.
