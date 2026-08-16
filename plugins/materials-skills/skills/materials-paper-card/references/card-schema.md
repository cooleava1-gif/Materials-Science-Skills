# Card Schema Reference

Machine-checkable shape of the final `paper-card.md` (used for delivery QA
and by downstream skills that consume cards).

## Header block

- `Source:` required — citation, DOI, or file path.
- `Locator mode:` one of `page-grounded`, `structure-grounded`,
  `source-limited` (definitions in the core contract).
- `Context mode:` one of `paper-only`, `targeted external check`,
  `externally verified`.
- `Evidence base:` supplied text description or the reader-package
  identifier whose evidence IDs the card reuses.

## Section rules

- Exactly the headings `## 01` … `## 16` from the output format, in order,
  each with its bilingual title. No extra top-level sections; extra
  subsections are allowed inside a numbered section.
- Evidence citations: `[S:<source-id>]` for supplied-text spans,
  `[E:<evidence-id>]` for reader-package tuples, `[p. N]` only in
  page-grounded mode.
- `Not assessable from supplied material: <reason>` is the only allowed
  placeholder and must be justified in-line.
- Reported-not-verified marking: characterization values and performance
  numbers taken from the paper are cited; the card never re-measures.

## QA checklist (run before delivery)

1. 16/16 sections present, ordered, numbered.
2. Every `Not assessable` has a reason.
3. Every `[E:...]` ID resolves in the evidence base; every `[p. N]` is
   page-grounded mode only.
4. Section 11 wording passes the claim-strength ladder (no causal upgrade
   of correlational evidence).
5. Section 16 ideas each carry gap → experiment sketch → boundary.
6. No reviewer-grade language (accept/reject/score) anywhere.
