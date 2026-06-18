# materials-doe

Design-of-experiments planning and matrix generation for civil engineering
and construction materials research. Supports classical factorial, Taguchi
orthogonal array, and mixture/simplex designs with factor screening and
response surface extensions.

## When To Use

Use this skill when the user needs an experimental matrix, factor screening
plan, Taguchi orthogonal array, mixture design, response surface plan, or
guidance on sample size and replication for materials testing.

## Inputs

- material system and domain (asphalt, cement-concrete, general materials)
- factors, levels, and any known constraints
- design mode preference: classical, orthogonal, or mix-design
- target output: test matrix, summary plan, or figure

## Outputs

| Output | Description |
|---|---|
| Test matrix | Factor-level table in CSV or markdown |
| Analysis strategy | Notes on ANOVA, S/N ratio, or RSM approach |
| Doe handoff | Structured handoff for downstream skills |

## Usage Examples

- "Design an L9 orthogonal array for asphalt modifier dosage, curing time, and temperature"
- "Generate a mix design matrix for three-component mortar system"
- "Plan a factorial experiment for concrete durability factors"

## Validation

- Core tests live under `plugins/materials-skills/skills/materials-doe/tests/`
- Bundle verification: `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill plans experiments and generates matrices. It does not execute
tests, analyze collected data, or produce manuscript text. For data analysis
or figure production, hand off to materials-data or materials-figure.
