---
name: materials-submission
version: "1.1.0"
stability: beta
description: Use when assembling a journal submission package for the supported materials journals declared in journal-templates.
---

# Materials Submission Router

Read `manifest.yaml`, then load the selected journal template and supporting guidance for the `task`, `journal`, and `article_type` axes. The package consumes manuscript, figure, FAIR-data, and reviewer artifacts; it emits the cover letter, journal checklist, declarations, source-tracing stubs, and `submission-package.yaml`.

Rules:

- The selected journal template controls accepted article types and required artifacts; do not substitute a generic checklist when a journal route is selected.
- Do not fabricate funding, conflicts, reviewers, data availability, code availability, submission IDs, or live upload success.
- Preserve live-verification markers until the current publisher guide is verified. Keep initial-submission and revision artifacts as separate checklist stages.
- Missing manuscript, figure, data, declaration, or handoff artifacts produce a dry-run/missing state, not a complete package.

Route manuscript prose to `materials-writing`, figures/graphical abstracts to `materials-figure`, FAIR packages to `materials-data`, and reviewer simulation to `materials-reviewer`. Return artifact paths, article type, template/schema result, checklist status, and unresolved inputs; do not claim that an external submission occurred.
