# materials-response test rubric

Use this rubric to manually evaluate `materials-response` outputs against the Markdown fixtures.

## Completeness

Pass when:

- Every reviewer comment receives a stable ID (e.g., `R1.1`, `R2.3`).
- Every ID appears in the tracker and response letter.
- Repeated concerns across reviewers are cross-referenced rather than ignored.
- Ambiguous reviewer boundaries are flagged and clarified.

Fail when:

- A comment is skipped or merged without traceability.
- A major concern receives only a polite acknowledgement without action.
- Editor instructions are ignored or not separately identified.

## Traceability

Pass when:

- Every claimed manuscript change has a section, page, line, figure, table, or explicit placeholder.
- New experiments, analyses, figures, citations, and limitations are mapped to action labels.
- Missing locations are flagged rather than invented.

Fail when:

- The response claims a change without location or evidence.
- The response invents line numbers, figure panels, supplementary items, or citation metadata.

## Factuality

Pass when:

- Missing evidence is marked `AUTHOR_INPUT_NEEDED`.
- Quantitative details (test conditions, sample sizes, statistics) are used only when supplied by the author.
- Mechanism claims are tied to actual characterization evidence (FTIR, SEM, fluorescence, DSC/TG, XRD, rheology).
- Performance claims cite test standards, conditions, and repeatability.

Fail when:

- The response invents data, p-values, confidence intervals, sample sizes, or test conditions.
- The response overstates mechanism conclusions beyond what characterization evidence supports.
- The response fabricates experiments that were not performed.

## Tone

Pass when:

- The response is cooperative, concise, and evidence-forward.
- Disagreement is respectful and scientifically justified.
- Reviewer misunderstanding is framed as manuscript clarification.
- Chinese authors' meaning is preserved when drafting English responses.

Fail when:

- The response accuses the reviewer of error, incompetence, or misunderstanding.
- The response is excessively apologetic, defensive, or repetitive.
- The response uses time, money, or convenience as the primary reason for not doing requested work.

## Actionability

Pass when:

- The author can see exactly what to change in the manuscript.
- Missing information is listed as concrete author questions.
- Blocking or high-risk issues are visible before the draft letter.
- The response separates "response text" from "manuscript action".

Fail when:

- The output only produces prose and no action checklist.
- The author cannot identify what evidence is still needed.
- Response and manuscript changes are mixed together.

## Domain-fit

Pass when:

- The output is organized as editor-readable point-by-point response material suitable for CBM, CCC, JBE, RMPD, or IJPE.
- Mechanism comments reference appropriate characterization methods for the material system.
- Performance comments address test standards, specimen geometry, and service conditions relevant to the journal scope.
- Durability, sustainability, and microstructure claims respect the evidence boundary.

Fail when:

- The output reads like generic language polishing without domain context.
- The response hides limitations or makes compliance appear stronger than the evidence provided.
- The response does not distinguish between measured results and inferred mechanisms.
