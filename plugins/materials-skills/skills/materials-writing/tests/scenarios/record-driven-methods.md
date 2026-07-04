# Test: Record-driven Methods — consume experiment record without inventing details

## Skill

materials-writing

## Input

The user asks: "Draft the Methods section from my experiment record."

Available information:
- An `experiment-record.yaml` is provided.
- Record contains: material sources, mixing sequence, test standard references, and partial curing-condition notes.
- Record is missing: emulsifier dosage, replicate count, and exact specimen dimensions.

The user provides this experiment record excerpt:

```yaml
materials:
  base_asphalt: 70/100 penetration grade
  emulsifier: cationic slow-setting
  modifier: waterborne epoxy resin
methods:
  preparation: shear mixing at 60 C, 2000 rpm, 30 min
  curing: 25 C, 60% RH
  test_standard: ASTM D4541 (pull-off bonding)
measurements:
  bonding_strength:
    unit: MPa
    temperatures: [25]
  viscosity:
    unit: mPa.s
```

## Expected behavior

- Load and consume the experiment record as the primary input source.
- Lock terminology from the record (e.g., "waterborne epoxy resin", "cationic slow-setting emulsifier", "ASTM D4541").
- Draft the Methods section from the record fields.
- Insert `[TO CONFIRM: emulsifier dosage]`, `[TO CONFIRM: replicate count]`, and `[TO CONFIRM: specimen dimensions]` placeholders where the record is missing required details.
- List the missing fields under `Assumptions`.
- Do not invent values for missing fields.

## Forbidden behavior

- Do not ignore the experiment record and draft from general knowledge.
- Do not invent an emulsifier dosage, replicate count, or specimen dimensions.
- Do not omit the curing condition or test standard that are present in the record.
- Do not add unrecorded steps (e.g., sonication, vacuum drying) without marking them as unverified.

## Pass/fail checklist

- [ ] The Methods section is clearly derived from the experiment record.
- [ ] Locked terminology matches the record rather than inventing synonyms.
- [ ] Missing record fields are surfaced as `[TO CONFIRM: ...]` placeholders.
- [ ] `Assumptions` lists the missing experimental inputs.
- [ ] No fabricated material or method details appear in the draft.
