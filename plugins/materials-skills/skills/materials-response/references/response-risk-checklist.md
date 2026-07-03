# Response Risk Audit Guide

A risk assessment and compliance guide for peer-review rebuttal packages in materials science and engineering. Use this guide to audit response drafts before resubmission.

---

## 1. Risk Severity Matrix

| Risk Level | Impact | Common Root Causes | Action Needed |
|---|---|---|---|
| **High** (Showstopper) | Desk reject, immediate rejection by editor, or harsh second-round rejection. | Tone defensiveness, empty promises, fabricated data, ignored comments. | Stop resubmission; rewrite replies; acquire verified raw data. |
| **Medium** (Revision Loop) | Triggers another major/minor revision round; delays publication by months. | Missing page/line numbers, unaligned text/figure updates, weak control benchmarking. | Add concrete line links; synchronize manuscript edits; clarify control choices. |
| **Low** (Polishing) | minor delays; reviewer annoyance; editor requests quick formatting patch. | Typos, inconsistent unit aliases, formatting deviations. | Run final proofread; align unit symbols. |

---

## 2. High-Risk Flags & Audit Protocols

### 2.1 Tone Defensiveness
- **Risk**: Criticizing the reviewer's intelligence, reading comprehension, or fairness. Using defensive adjectives.
- **Audit Protocol**: Search the response draft for defensive trigger words:
  - `clearly`, `obviously`, `manifestly`, `of course` (these imply the reviewer is blind/dense).
  - `as already stated`, `as mentioned in the paper` (these suggest the reviewer did not read carefully).
  - `wrong`, `incorrect`, `misunderstood`.
- **Remediation**: Rephrase to place the blame on the manuscript's original clarity rather than the reviewer.
  - *Bad*: "Obviously, this test was already done as stated in Section 2."
  - *Good*: "We apologize for the lack of clarity in our original draft. We have revised Section 2 (Page 4, Line 12) to explicitly state that the test was conducted..."

### 2.2 Fabricated / Unsupported Promises
- **Risk**: Saying a test was completed or will be completed when the raw data is not in the resubmission package. Promising future studies that cannot be verified.
- **Audit Protocol**: Check all verbs in the response: `will perform`, `has scheduled`, `is compiling`. Verify if the corresponding figures/tables have been added to the tracked-changes manuscript.
- **Remediation**: If data is missing, flag as `[AUTHOR_INPUT_NEEDED]` and frame the lack of data as a scientific limitation. Never claim an experiment is complete unless the user confirms and provides data.

### 2.3 The "Silent Drop" (Incomplete Response)
- **Risk**: Responding to only the first half of a compound reviewer comment, hoping they will not notice the missing part.
- **Audit Protocol**: For every comment, map each clause containing a question mark or a suggestion to a sub-action in the response. If a comment contains three distinct queries, verify that the reply has three corresponding parts (e.g., R1.1a, R1.1b, R1.1c).
- **Remediation**: Use bullet points in the reply to address each sub-question individually.

---

## 3. Medium-Risk Flags & Audit Protocols

### 3.1 Unverifiable Revisions (Actionless Replies)
- **Risk**: Writing "We have revised the paper accordingly" without citing the exact section, page, or line numbers of the change.
- **Audit Protocol**: Ensure every reply that claims a change contains a page/line reference in the format `Page X, Lines Y-Z` or `Section A.B`.
- **Remediation**: Open the tracked draft, find the exact lines of the change, and copy them directly into the response letter as a quoted block or a diff.

### 3.2 Inconsistent Evidence Claims
- **Risk**: Figures in the response letter show different values or trends compared to the figures in the revised manuscript.
- **Audit Protocol**: Cross-check data values (e.g., strength in MPa, viscosity in Pa·s, peaks in cm⁻¹) cited in the response letter against the updated tables and figures in the manuscript draft.
- **Remediation**: Harmonize the values; verify that any changes made to figure captions in the manuscript are mirrored in the response letter.

---

## 4. Rebuttal Language Audit Table

Use this table to audit vocabulary choices:

| Taboo Word/Phrase | Risk Level | Reason | Preferred Academic Alternative |
|---|---|---|---|
| "The reviewer is wrong..." | **High** | Insulting and defensive. | "We respectfully clarify that..." (supported by data/standards) |
| "Obviously/Clearly, the data show..." | **High** | Condescending tone. | "The data presented in Figure X indicate..." |
| "We will do this in a future paper..." | **High** | Often perceived as dodging an essential revision. | "We agree that this is a critical aspect. Due to [scientific reason], it is beyond the scope of this work and is now discussed as a limitation in Section X..." |
| "We have revised the text accordingly." | **Medium** | Vague and actionless. | "We have rephrased Section X (Page Y, Lines Z-W) to clarify this point: [Insert Quote]" |
| "It is impossible to test this..." | **Medium** | Sounds like an excuse. | "Performing this test is constrained by [material constraint / standard limitation] as explained in Section X..." |

---

## 5. Pre-Flight Checklist

Before resubmission, verify:
- [ ] 1. Every comment is preserved verbatim (no paraphrasing).
- [ ] 2. Tone is polite, professional, and free of defensive adverbs.
- [ ] 3. Every reply maps to a concrete line range or figure/table index.
- [ ] 4. Any experiment claimed as "completed" has its raw data plotted and integrated.
- [ ] 5. All placeholders (e.g., `[insert page number]`) have been replaced with real numbers.
