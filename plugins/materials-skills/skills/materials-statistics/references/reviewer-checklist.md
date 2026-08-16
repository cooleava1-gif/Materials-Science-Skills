# Reviewer Checklist

Run before delivering any statistics audit, revision, or draft.

## Severity labels

- **P0** — the claimed inference is not supported as reported (invalid n,
  missing correction across a family, interaction claim without the
  interaction test, pseudoreplication).
- **P1** — defensible but reviewer-visible (assumption checks missing,
  SEM/SD ambiguity, significance-only wording, software version absent).
- **P2** — hygiene (precision inconsistencies, caption/methods n mismatch,
  unit-basis drift).

## Final delivery checks

1. Every claim table row has: test, n as independent units, correction,
   effect estimate with uncertainty, and software — or `AUTHOR_INPUT_NEEDED`.
2. No invented values anywhere; repairs are wording-level only.
3. Ready-to-paste text uses past tense for what was done, present for the
   reporting policy; hedged language for inferred mechanisms.
4. The output format's sections are all present, including the
   reviewer-risk note.
5. Handoffs proposed, not silently executed: design changes →
   `materials-doe`; re-plotting → `materials-figure`; wording →
   `materials-polishing`; response assembly → `materials-response`.

## Reviewer-risk statements (typical)

- "A statistical reviewer will ask what the error term is in the Taguchi
  ANOVA; pool-and-report or replicate."
- "The 15-reading n will be challenged; the design supports n = 3 per mix —
  restate or add specimens."
- "Pairwise stars without a named correction invite a methods comment;
  Tukey or Holm naming fixes it cheaply."

## Escalation boundaries

- Raw-data reanalysis beyond summary arithmetic: only with user data and an
  explicit request; otherwise propose the analysis plan.
- Clinical, regulatory, or safety-critical statistics: out of scope; state
  the boundary.
- Standard-specific precision statements (ASTM repeatability): defer to the
  invoked standard and quote it.
