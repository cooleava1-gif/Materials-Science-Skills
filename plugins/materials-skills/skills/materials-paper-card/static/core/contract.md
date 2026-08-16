# Paper Card Evidence Contract

A Paper Card is a reading artifact: every non-trivial statement resolves to
the supplied source or to an evidence tuple inherited from a
`materials-reader` package.

## Source and locator modes

| Mode | Condition | Citation rule |
|---|---|---|
| `page-grounded` | reliable PDF page indices available | cite PDF page + structural locator (section/figure/table) |
| `structure-grounded` | pages unreliable, but sections/figures/tables/equations identifiable | cite structural locators only, never page numbers |
| `source-limited` | abstract / metadata / excerpt only | cite the supplied text span; no page citations, no inferred evidence |

## Evidence rules

- Claims inherit evidence tuples (`claim-id`, `source-id`, evidence layer,
  source quality) from the reader package when supplied; new tuples must
  follow the shared evidence contract.
- Sections that the source cannot support are written `Not assessable from
  supplied material` with a one-line reason — never filled by inference.
- Characterization statements (XRD phase IDs, FTIR assignments, SEM
  morphology, mechanical values) quote the paper's own claims and mark them
  as reported, not verified.
- External verification is limited to Section 01 (bibliographic), Section 15
  (knowledge connections), and explicit novelty checks; record the context
  mode (`paper-only` / `targeted external check` / `externally verified`).

## Hard boundaries

- No invented data, mechanisms, or citations.
- The card does not grade the paper (that is peer review) and does not
  rewrite it (that is polishing); critical analysis stays analytic.
- Section 16 ideas must be testable and boundary-respecting (see
  `references/research-idea-gates.md`).
