# Polishing Workflow — 12 Steps

Use this workflow for every polishing pass. Execute steps in order; each step
depends on the previous one's output.

---

## Step 1: Sentence Split

Scan every sentence. If a sentence exceeds 30 words, split it. Hard ceiling:
35 words. Put the material, test, result, and interpretation in logical order.

### Splitting rules

| Pattern | Split strategy |
|---|---|
| Two independent clauses joined by comma | Period or semicolon |
| Three causal links stacked | Break into 2–3 sentences |
| Long relative clause mid-sentence | Extract to separate sentence |
| Parenthetical test condition | Move to its own clause or sentence |
| Multiple specimens compared | One sentence per comparison |

### Example

Before (49 words):
> The WER modified emulsified asphalt, which was prepared with 20% WER content
> and cured at 60°C for 24 h, showed a bonding strength of 0.41 MPa that was
> 73.2% higher than the base asphalt measured under the same conditions using
> the pull-off test according to ASTM D7234.

After (2 sentences, 35 words max):
> The WER-EA with 20% WER content showed a bonding strength of 0.41 MPa after
> curing at 60°C for 24 h (ASTM D7234 pull-off test). This was 73.2% higher
> than the base asphalt.

---

## Step 2: Section Identification

Identify the manuscript section for each paragraph. This determines tense,
voice, and hedging rules for subsequent steps.

| Section | Primary tense | Purpose |
|---|---|---|
| Abstract | Past (methods/results), present (implication) | Compress the study |
| Introduction | Present (known facts), past (prior studies) | Build the gap |
| Methods | Past | Describe procedures |
| Results | Past | Report observations |
| Discussion | Present (interpretation), past/present (comparison) | Explain and contextualize |
| Conclusions | Present (general), past (specific findings) | Close the argument |

Tag each paragraph with its section before proceeding.

---

## Step 3: Hourglass Check

Verify that the section follows the correct information flow shape.

### Introduction — Narrowing funnel

```
Broad engineering problem
  → Specific material system
    → Unresolved bottleneck
      → Study objective
        → Evidence plan
```

The introduction must **narrow** from broad to specific. If it widens again
after stating the gap, restructure.

### Discussion — Widening funnel

```
Key result (what happened)
  → Mechanism explanation (why)
    → Comparison with literature (context)
      → Engineering implication (so what)
        → Limitation and future work (boundary)
```

The discussion must **widen** from specific result to broader implication.
If it narrows to new data or methods, move that content to Results.

### Results — Evidence ladder

```
Data trend → Comparison with control → Statistical significance → Mechanism evidence → Boundary
```

### Conclusions — Closing triangle

```
Specific finding → General implication → Bounded recommendation
```

For each section, verify the shape is correct. If not, flag for restructuring
rather than polishing misordered content.

See `hourglass-structure.md` for detailed per-section patterns.

---

## Step 4: Tense Audit

Check every sentence against the tense rules for its section.

### Key rules

| Section | Rule | Violation example | Fix |
|---|---|---|---|
| Methods | Past tense for all procedures | `Samples are prepared...` | `Samples were prepared...` |
| Results | Past tense for observations | `Figure 1 shows...` | `Figure 1 shows...` (present OK for figure references) |
| Discussion (interpretation) | Present for mechanism | `The improvement was attributed to...` | `The improvement may be attributed to...` |
| Discussion (comparison) | Past or present | `Our results agreed with...` | `Our results are consistent with...` |
| Conclusions (general) | Present tense | `WER improved bonding...` | `WER improves bonding...` |
| Conclusions (specific) | Past tense | `The optimal dosage is 15%...` | `The optimal dosage was 15%...` |

### Common violations

- Mixing past and present within a single paragraph without justification.
- Using present tense in Methods (`Specimens are cut...` → `Specimens were cut...`).
- Using past tense in Discussion interpretation (`This was attributed to...` → `This may be attributed to...`).
- Using passive voice where active is clearer (`It was found that...` → delete).

See `language-rulebook.md` for the complete tense rules table.

---

## Step 5: Sentence Edit

For each sentence, apply:

1. **One main proposition** per sentence.
2. **Subject-verb proximity**: keep the verb close to its subject.
3. **Old information first, new information last**: known context before new result.
4. **No comma splices**: two independent clauses need a period, semicolon, or
   conjunction.
5. **No stacked modifiers**: break `the WER-modified emulsified asphalt
   bonding strength improvement` into `the improvement in bonding strength
   of WER-EA`.

### Clause order

Prefer: Subject → Verb → Object → Condition → Source

> The modified emulsion showed higher bond strength than the control after
> 7 d curing (ASTM D7234).

Not: > Under the condition of 7 d curing according to ASTM D7234, the bond
strength of the modified emulsion was higher than the control.

---

## Step 6: Vocabulary Upgrade

Replace weak or imprecise words with evidence-calibrated alternatives.

See `vocabulary-upgrade.md` for the complete replacement table.

### Core principle

The verb must match the evidence level:

| Evidence level | Safe verbs |
|---|---|
| Direct measurement | showed, exhibited, increased, decreased, reached |
| Supported conclusion | demonstrated, confirmed, revealed |
| Mechanism inference | suggested, indicated, may be attributed to |
| Engineering implication | has potential to, is expected to, shows promise for |

### Common upgrades

| Weak / vague | Stronger / precise |
|---|---|
| `good` | `higher`, `improved`, `within the target range` |
| `better` | `higher than the control by X%` |
| `excellent` | remove, or state measured criterion |
| `a lot` | `substantially`, or quantify |
| `very` | remove (usually adds nothing) |
| `nice` | remove (not academic) |
| `huge` | `significant` (only with statistics) |
| `important` | `critical`, `essential`, or state why |

---

## Step 7: Template Check

Verify the paragraph follows the standard academic template for its section.

### Introduction template

1. Broad context (1–2 sentences).
2. Specific material system (1–2 sentences).
3. Unresolved bottleneck (2–3 sentences).
4. Study objective (1 sentence).
5. Evidence plan (1 sentence, optional).

### Results template

1. Lead with the trend or observation.
2. Quantify with value, condition, and test standard.
3. Compare with control or baseline.
4. Add mechanism evidence if available.
5. State limitation or boundary.

### Discussion template

1. Restate key finding (1 sentence).
2. Explain mechanism (2–3 sentences).
3. Compare with literature (2–3 sentences).
4. Engineering implication (1–2 sentences).
5. Limitation and future work (1–2 sentences).

### Conclusions template

1. Specific finding (1–2 sentences).
2. General implication (1 sentence).
3. Bounded recommendation or future direction (1 sentence).

---

## Step 8: Citation Audit

Check every citation against the rules in `citation-integrity.md`.

### Four attribution types

| Type | When to use | Example |
|---|---|---|
| Direct attribution | Citing a specific finding | `Kong et al. (2024) reported that...` |
| Supporting attribution | Citing a method or standard | `according to ASTM D7234` |
| Contextual attribution | Citing background knowledge | `Emulsified asphalt is widely used in pavement maintenance (Zhang et al., 2017)` |
| Comparative attribution | Citing a contrasting result | `Unlike the findings of Li et al. (2023), our results suggest...` |

### Citation rules

- Cite only sources you have personally read and verified.
- Do not cite a review paper for a specific experimental finding — cite the
  original study.
- Do not cite a source for a claim it does not support.
- Verify that cited page numbers, figures, and tables are correct.
- Keep citation count reasonable: 3–5 per paragraph in Introduction, 2–3 in
  Discussion.

---

## Step 9: House Style Check

Apply journal-specific and British English rules.

### British English (for most UK/European journals)

| American | British |
|---|---|
| behavior | behaviour |
| color | colour |
| analyze | analyse |
| program (computing) | programme |
| modeling | modelling |
| signaling | signalling |
| favor | favour |
| center | centre |
| fiber | fibre |
| liter | litre |

See `british-english.md` for the complete list.

### Journal-specific checks

| Journal | Key style points |
|---|---|
| CBM | Elsevier style; SI units; ≤35 words/sentence |
| CCC | Elsevier style; cement terminology; ASTM/EN standards |
| RMPD | Taylor & Francis; pavement language; AASHTO/JTG standards |
| JBE | Elsevier; building engineering scope; sustainability framing |
| JACERS | Wiley; ceramics terminology; ASTM C-series standards |

---

## Step 10: Overclaim Detection

Scan for overclaim patterns. See the claim-strength ladder in
`_shared/core/claim-strength-ladder.md`.

### Red flag words

| Flag word | Why it's risky | Replacement |
|---|---|---|
| `prove` / `proves` | Implies definitive evidence | `show`, `demonstrate`, `suggest` |
| `significant` | Requires statistical test | State p-value or remove |
| `first` / `novel` | Requires exhaustive literature check | `to our knowledge, the first` |
| `green` / `sustainable` | Requires LCA or emission data | `potentially sustainable`, state boundary |
| `excellent` | Subjective, no criterion | Remove, or state measured value |
| `completely` | Overstates certainty | Remove or qualify |
| `unprecedented` | Requires exhaustive check | `to our knowledge, not previously reported` |
| `best` | Requires comprehensive comparison | `among the highest`, `optimal within the tested range` |
| `field-ready` | Requires field validation | `shows promise for field application` |
| `always` / `never` | Absolute, rarely true | `under the tested conditions` / `was not observed` |

### Sustainability claims

Do not use "green," "low-carbon," or "sustainable" from waterborne chemistry,
waste use, or recycled content alone:

- If no complete LCA exists: label any estimate as a screening calculation and
  define the functional unit.
- If only durability or bonding data exist: phrase environmental value as a
  service-life hypothesis requiring verification.

---

## Step 11: Proofreading

Final mechanical checks:

| Check | Rule |
|---|---|
| Spelling | Use journal-standard English (British or American consistently) |
| Abbreviations | Defined at first use: `waterborne epoxy resin (WER)` |
| Numbers | Numerals for measurements, spell out at sentence start |
| Units | Space between value and unit: `25 cm` not `25cm` |
| Ranges | En dash: `10–20%` not `10-20%` or `10 to 20%` |
| Figures/Tables | Present tense: `Figure 1 shows...`, `Table 3 lists...` |
| Parallel structure | Lists and series use the same grammatical form |
| Double spaces | Remove (one space after period) |
| Hyphenation | Compound modifiers before noun: `water-based coating`, `high-temperature test` |

### Checklist

- [ ] No sentence exceeds 35 words.
- [ ] All abbreviations defined at first use.
- [ ] Units use SI with proper spacing.
- [ ] Figure/Table references in present tense.
- [ ] No double spaces.
- [ ] Consistent British/American English throughout.
- [ ] All references verified against source.
- [ ] All quantitative values match the data.

---

## Step 12: Output

Return:

1. **Polished text** — the cleaned manuscript section.
2. **Risk note** — a compact summary of flagged issues:

```
## Claim Risk Note

- [OVERCLAIM] Line 12: "significantly improved" → needs p-value or change
  to "showed higher mean strength"
- [TENSE] Line 27: Methods section uses present tense → changed to past
- [BOUNDARY] Line 35: "optimal dosage" claimed without durability data →
  added "within the tested mechanical range"
- [CITATION] Line 42: Review paper cited for specific finding → recommend
  citing original study
```

3. **Change log** (optional) — for revision rounds, track what changed.

---

## Summary

| Step | Focus | Output |
|---|---|---|
| 1. Sentence Split | Break long sentences | All sentences ≤ 35 words |
| 2. Section ID | Tag paragraphs by section | Section labels |
| 3. Hourglass Check | Verify information flow | Restructure flags |
| 4. Tense Audit | Match tense to section | Tense corrections |
| 5. Sentence Edit | Clarity and structure | Edited sentences |
| 6. Vocabulary Upgrade | Evidence-calibrated verbs | Word replacements |
| 7. Template Check | Section template compliance | Restructure notes |
| 8. Citation Audit | Attribution integrity | Citation corrections |
| 9. House Style | Journal + British English | Style fixes |
| 10. Overclaim Detection | Claim-strength audit | Overclaim flags |
| 11. Proofreading | Mechanical correctness | Typo/format fixes |
| 12. Output | Deliverable | Polished text + risk note |
