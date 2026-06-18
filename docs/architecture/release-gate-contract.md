# Release Gate Contract

Release gates prove that the skill package is structurally coherent and that
declared automation surfaces still run. They do not prove scientific truth,
paper-level evidence quality, or that a generated manuscript, figure, citation
matrix, or slide deck is publication-ready without expert review.

## Buckets

`skill_architecture` proves that each `materials-*` skill has router
files, manifest metadata, static core files, and declared paths. It does not
prove that every reference is scientifically complete.

`manifest_routes` proves that `always_load` and `axes.*.values.*.path` entries
resolve to files. It does not prove that every possible user request chooses the
best route.

`all_skill_mojibake` proves that checked trigger strings and selected text
surfaces do not contain known mojibake markers. It does not prove translation
quality or domain wording quality.

`reader_standard_package` proves that the reader package contract, scaffold
builder, auditor, validator, and required templates can produce and inspect a
package shape. It does not prove that extracted evidence is sufficient for a
review claim.

`academic_search_expanded_sources` proves that source adapters, identifier
normalizers, citation import/export helpers, and mocked API parsing behave as
specified. It does not prove live database availability, API quota health, or
that search results are deep-read evidence.

`wer_ea_asset_library` proves that WER-EA atlas specs, data templates, scripts,
and generated example assets exist and pass structural QA. It does not prove
that example figures are experimental findings.

`paper2ppt_pptx_smoke_or_exemption` proves that slide handoff and PPTX skills
either have smoke coverage or a documented release exemption. It does not prove
visual polish for every future deck.

Existing buckets such as `coverage`, `skill_assets`, `generated_artifacts`, and
`mojibake` remain valid compatibility surfaces. They should continue to report
machine-readable JSON with top-level `status`, `coverage`, `issues`, and test
summaries.

## Plugin Package Layout

The release gate validates the package under:

```text
plugins/materials-skills/skills/<skill>/
```

There is no separate root skill tree. All skill assets, references, scripts,
tests, and manifests must be present inside the plugin package.

## Interpreting Results

Hard failures mean the package is structurally unsafe to release: missing router
files, broken manifest paths, unreadable manifests, or required script/test
failures.

Warnings mean the package is inspectable but not fully normalized. Examples
include missing standard manifest blocks during migration, compatible but
non-normalized static core contract filenames, or mojibake trigger text that has
not yet been repaired.

No release bucket replaces source-grounded reading. Search records, generated
figures, package scaffolds, and citation matrices are handoff artifacts until
they are checked against paper text, figures, tables, and reviewer-safe evidence
boundaries.
