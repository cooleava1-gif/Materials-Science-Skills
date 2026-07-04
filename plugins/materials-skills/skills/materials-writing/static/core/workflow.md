# Writing Workflow

Run this 5-stage loop for every drafting or restructuring task. Do not skip stages 1-4 just because the user asked for prose immediately.

## Stage 1: Identify the job and lock terminology

Identify the target section, paper type, journal family, material family, domain, and input source from the user's input and the loaded fragments. On first contact with the material, extract the recurring terms — materials, binders, modifiers, test methods, standards, units, abbreviations — into a Terminology Ledger and lock the canonical forms before drafting any prose. See [../../_shared/core/terminology-ledger.md](../../_shared/core/terminology-ledger.md).

If the user provides `experiment-record.yaml`, seed the ledger from the record's `materials`, `methods`, and `measurements` blocks. Flag any record field that is missing, ambiguous, or conflicts with the prompt.

## Stage 2: Write the one-sentence argument

Reduce the draft to one sentence:

> In [engineering problem], we [advance] using [material/approach], supported by [evidence], with [boundary].

Force every section to serve this sentence. If the sentence cannot be written, the paper does not yet have an argument — surface that to the user and stop for clarification.

Then build a claim-evidence-boundary table: each claim, the evidence that supports it, and where the claim stops. Do not draft prose until the table is at least sketched.

## Stage 3: Map section architecture and paragraph messages

Pick the section structure from the relevant `section/*.md` fragment. The `paper_type` decides drafting order:

- **experimental-manuscript**: Results → Introduction → Conclusion → Methods → Abstract.
- **review-paper**: synthesis axes → gap → trend → outlook.
- **methods-paper**: protocol → validation → boundary.

Pull deeper patterns from [../../references/argument-chain.md](../../references/argument-chain.md) or [../../references/article-architecture.md](../../references/article-architecture.md) when needed.

Map every paragraph to one message only. Allowed paragraph messages:

- context
- gap
- approach
- result
- comparison
- mechanism
- implication
- limitation

If a paragraph carries two messages, split it before drafting. Every paragraph must be easy to reverse-outline: a reader should be able to write its one-sentence summary from the first sentence alone.

## Stage 4: Confirmation gate — align before drafting

Drafting a full section on a wrong assumed premise wastes the whole draft and is the main reason output "does not match what I meant". Before writing full prose, show the user a short alignment block and **stop for confirmation**:

- **One-sentence argument** (from stage 2) — echo it back in plain language.
- **Plan**: detected paper type, section(s), journal family, material family, domain, and the paragraph map from stage 3 as a short bullet list.
- **Terminology lock**: the canonical forms from stage 1 for the main materials, modifiers, test methods, and standards.
- **Key assumptions**: anything inferred rather than told — especially the core contribution, the leading result, and the mechanism evidence. Mark each clearly as an assumption.
- **At most 2-3 targeted questions**, only on genuinely ambiguous, high-leverage points. Do not pad the list.

Skip the gate only when the core claim, evidence, and boundary are all clearly given and there is no real ambiguity. In that case, state the one-sentence argument in one line and proceed.

## Stage 5: Draft, calibrate, and revise

### 5a. Draft from evidence outward

Draft per the confirmed plan. Keep claims near the data that support them — do not stack claims at the top of a section and leave evidence at the bottom. Each paragraph annotates its evidence source (user data, figure, table, citation, or `[TO CONFIRM: ...]` placeholder). Do not invent results, dosage ranges, mechanisms, or statistics.

### 5b. Calibrate verbs to evidence strength

Strong direct evidence earns `show` / `demonstrate`. Trend-level or indirect evidence earns `suggest` / `indicate`. Plausible but unverified mechanisms earn `may` / `could`. See [../../_shared/core/claim-strength-ladder.md](../../_shared/core/claim-strength-ladder.md).

### 5c. Remove unsupported overclaims

Sweep for `first`, `novel`, `unique`, `comprehensive`, `proves`, `significantly improves`, `environmentally friendly`, `confirmed mechanism`. Apply the downgrade rules in [../../_shared/core/claim-strength-ladder.md](../../_shared/core/claim-strength-ladder.md): `proves` → `suggests`, `significantly improves` → `improves` (without stats), `confirmed` → `inferred` (without mechanism evidence), `first`/`novel` → a precise gap.

### 5d. Run a paragraph-flow check

- One paragraph, one message.
- The first sentence is the topic / claim.
- Each subsequent sentence has an explicit relation to the previous one (cause, comparison, restriction, example).
- Inter-paragraph transitions carry the argument forward, not just the topic.
- Every paragraph must be easy to reverse-outline.

### 5e. Output

Return the section draft plus notes in the six-part format defined in [output-format.md](output-format.md): Draft, Section outline, Assumptions, Claim-evidence map, Why this structure, To redirect me.

### 5f. Revise by targeted edit, not full rewrite

When the user reacts to a draft, "this is not what I meant" is usually local — a wrong claim, a mis-framed paragraph, the wrong result leading. Do not silently re-draft the whole section: a full rewrite breaks the paragraphs that were already right and forces the user to re-check everything.

- Change **only** the paragraphs or claims the user flagged; keep the rest verbatim.
- If a requested fix forces a structural change (reordering sections, moving a claim across paragraphs), say so and confirm the new structure before applying it.
- Keep the Terminology Ledger (stage 1) stable across revisions unless the user renames a term; never let a revision reintroduce a variant of a locked term.
- After revising, re-run only the checks relevant to what changed (5b-5d), not the whole workflow.
- If the user's redirection reveals the original premise was wrong, return to the confirmation gate (stage 4) instead of patching prose on a broken premise.

## Handoffs

Honor the promises and refusals in [contract.md](contract.md). When a companion skill is the better continuation point, produce handoff-ready outputs:

- **reader handoff** — when the user needs source-paper intensive reading, route to `materials-reader` and consume its `reader-package` / `source_map`.
- **citation handoff** — emit a `claim-evidence-boundary` table so `materials-citation` can build the citation matrix without re-reading the draft.
- **doe handoff** — when the user needs an experiment matrix, route to `materials-doe` and consume its `doe-handoff` to align test variables with claims.

If any handoff artifact is missing, mark the missing input and route the weakness through [../../_shared/paper-production/weakness-routing.md](../../_shared/paper-production/weakness-routing.md) instead of inventing evidence.
