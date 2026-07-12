# Writing Workflow

Tiered drafting loop. Job size decides how many stages run explicitly.

## Tiering

- **Local single-paragraph edit** (e.g. "polish this paragraph" with a fixed claim, evidence, and boundary): Stages 1-2 run internally, then go straight to Stage 5. Do not force a confirmation gate for a genuinely local edit.
- **Single-section, full-manuscript, or multi-section job** (e.g. "draft the Introduction", "draft the Results and Discussion", "build the full argument"): run Stages 1-5 explicitly, including the confirmation gate at Stage 4.
- **QA or multi-round revision job**: also run the state-machine preflight below.

## State-machine preflight (opt-in)

Only when `writing_mode` is `qa`, or the user explicitly asks for multi-round revision with scoring. Most drafting jobs skip this entirely.

Load `content-first-qa-pipeline` for QA or multi-round revision. If scoring or continuity is needed, check for project-provided foundation files and `state.json` before Stage 1. If they are absent, report the missing inputs or provide a state patch/init instruction for the user's project; do not create active state inside this skill package. Load the state-machine references listed under `references.on_demand` in the manifest (`foundation-files`, `stopping-rules`, `evaluation-rubric`, `validation-checklist`) when the corresponding decision is needed.

State-aware runs must carry these fields forward: `writing_mode`, `round`, `scores`, `previous_scores`, `technical_debts`, `stop_status`, and `artifacts`. If the active files cannot be edited directly, return a state patch for the user project instead of silently dropping the state update.

## Stage 1: Identify the job and lock terminology

Identify the writing mode, target section, paper type, journal family, material family, domain, and input source from the user's input and the loaded fragments. On first contact with the material, extract the recurring terms — materials, binders, modifiers, test methods, standards, units, abbreviations — into a Terminology Ledger and lock the canonical forms before drafting any prose. See [terminology-ledger](../../../_shared/core/terminology-ledger.md) (load on demand).

If the user provides `experiment-record.yaml`, seed the ledger from the record's `materials`, `methods`, and `measurements` blocks. Flag any record field that is missing, ambiguous, or conflicts with the prompt.

## Stage 2: Write the one-sentence argument

Reduce the draft to one sentence:

> In [engineering problem], we [advance] using [material/approach], supported by [evidence], with [boundary].

Force every section to serve this sentence. If the sentence cannot be written, the paper does not yet have an argument — surface that to the user and stop for clarification.

Then build a claim-evidence-boundary table: each claim, the evidence that supports it, and where the claim stops. Load [evidence-contract](../../../_shared/core/evidence-contract.md) on demand for the audit table format. Do not draft prose until the table is at least sketched.

## Stage 3: Map section architecture and paragraph messages

Pick the section structure from the relevant `section/*.md` fragment. The `paper_type` decides drafting order:

- **experimental-manuscript**: Results → Introduction → Conclusion → Methods → Abstract.
- **review-paper**: synthesis axes → gap → trend → outlook.
- **methods-paper**: protocol → validation → boundary.

Pull deeper patterns from [../../references/argument-chain.md](../../references/argument-chain.md) or [../../references/article-architecture.md](../../references/article-architecture.md) when needed.

Map every paragraph to one message only. Allowed paragraph messages: context, gap, approach, result, comparison, mechanism, implication, limitation. If a paragraph carries two messages, split it before drafting. Every paragraph must be easy to reverse-outline: a reader should be able to write its one-sentence summary from the first sentence alone.

## Stage 4: Confirmation gate — align before drafting

Drafting a full section on a wrong assumed premise wastes the whole draft. Before writing full prose, show the user a short alignment block and **stop for confirmation**:

- **One-sentence argument** (from stage 2) — echo it back in plain language.
- **Plan**: detected paper type, section(s), journal family, material family, domain, and the paragraph map from stage 3 as a short bullet list.
- **State**: detected writing mode, current round, score status, and whether foundation files are complete enough for this run.
- **Terminology lock**: the canonical forms from stage 1 for the main materials, modifiers, test methods, and standards.
- **Key assumptions**: anything inferred rather than told — especially the core contribution, the leading result, and the mechanism evidence. Mark each clearly as an assumption.
- **At most 2-3 targeted questions**, only on genuinely ambiguous, high-leverage points. Do not pad the list.

The local single-paragraph tier is the only gate exemption. A complete section still receives the alignment block; when the claim, evidence, and boundary are already clear, keep the block short rather than removing it.

## Stage 5: Draft, calibrate, and revise

### 5a. Draft from evidence outward

Draft per the confirmed plan. Keep claims near the data that support them — do not stack claims at the top of a section and leave evidence at the bottom. Each paragraph annotates its evidence source (user data, figure, table, citation, or `[TO CONFIRM: ...]` placeholder). Do not invent results, dosage ranges, mechanisms, or statistics.

### 5b. Calibrate verbs to evidence strength

Strong direct evidence earns `show` / `demonstrate`. Trend-level or indirect evidence earns `suggest` / `indicate`. Plausible but unverified mechanisms earn `may` / `could`. Load [claim-strength-ladder](../../../_shared/core/claim-strength-ladder.md) on demand for the full ladder and downgrade rules.

### 5c. Remove unsupported overclaims

Sweep for `first`, `novel`, `unique`, `comprehensive`, `proves`, `significantly improves`, `environmentally friendly`, `confirmed mechanism`. Apply the downgrade rules: `proves` → `suggests`, `significantly improves` → `improves` (without stats), `confirmed` → `inferred` (without mechanism evidence), `first`/`novel` → a precise gap.

### 5d. Run a paragraph-flow check

- One paragraph, one message.
- The first sentence is the topic / claim.
- Each subsequent sentence has an explicit relation to the previous one (cause, comparison, restriction, example).
- Inter-paragraph transitions carry the argument forward, not just the topic.
- Every paragraph must be easy to reverse-outline.

### 5e. Output

Return the section draft plus notes in the six-part format defined in [output-format.md](output-format.md): Draft, Section outline, Assumptions, Claim-evidence map, Why this structure, To redirect me.

For state-machine runs, include a compact status block with current artifact, score/status, remaining risks, stop-or-continue reason, and one next action. Apply the stopping rules before recommending another full revision loop.

### 5f. Revise by targeted edit, not full rewrite

When the user reacts to a draft, "this is not what I meant" is usually local — a wrong claim, a mis-framed paragraph, the wrong result leading. Do not silently re-draft the whole section: a full rewrite breaks the paragraphs that were already right and forces the user to re-check everything.

- Change **only** the paragraphs or claims the user flagged; keep the rest verbatim.
- If a requested fix forces a structural change (reordering sections, moving a claim across paragraphs), say so and confirm the new structure before applying it.
- Keep the Terminology Ledger (stage 1) stable across revisions unless the user renames a term; never let a revision reintroduce a variant of a locked term.
- After revising, re-run only the checks relevant to what changed (5b-5d), not the whole workflow.
- If the user's redirection reveals the original premise was wrong, return to the confirmation gate (stage 4) instead of patching prose on a broken premise.

## Gates

These gates apply to every job. They are stated once here; do not re-encode them in fragments or the router.

- **Evidence contract**: no overclaim, no speculation presented as fact. Claims must match evidence strength (5b-5c). When evidence is missing, write a placeholder — never fill the gap with confident prose.
- **Terminology lock**: once the ledger is set, every output uses canonical forms. A revision must not reintroduce a variant of a locked term.
- **Paragraph discipline**: one paragraph carries one message; every paragraph is easy to reverse-outline.
- **Confirmation gate** (complete-section, full-manuscript, and multi-section jobs): pass Stage 4 before full section output. Only a genuinely local single-paragraph edit may use the fast path.
- **State-machine gates** (QA / multi-round revision only):
  - Every response includes current artifact or revised text, score/status, remaining risks, stop-or-continue reason, and one next action.
  - Follow the content-first order: Gate 2 expert/content review, Gate 1 language/style scan, Gate 3 auto-validation, then Gate 4 score threshold.
  - Stop revision loops after any stopping rule triggers: maximum three full revision rounds, two consecutive score improvements below 0.5, missing key evidence, unresolved specialist conflict, or target threshold reached.

## Handoffs

Honor the promises and refusals in [contract.md](contract.md). When a companion skill is the better continuation point, produce handoff-ready outputs:

- **reader handoff** — when the user needs source-paper intensive reading, route to `materials-reader` and consume its `reader-package` / `source_map`.
- **citation handoff** — emit a `claim-evidence-boundary` table so `materials-citation` can build the citation matrix without re-reading the draft.
- **doe handoff** — when the user needs an experiment matrix, route to `materials-doe` and consume its `doe-handoff` to align test variables with claims.

If any handoff artifact is missing, mark the missing input and route the weakness through [weakness-routing](../../../_shared/paper-production/weakness-routing.md) instead of inventing evidence.
