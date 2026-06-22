---
name: materials-polishing
version: "1.2.0"
stability: stable
description: >-
  Polish, restructure, or translate academic prose for civil engineering and
  construction materials research while preserving scientific responsibility.
  Use when the user asks to polish a manuscript paragraph, abstract,
  introduction, results, discussion, conclusion, title, methods section, or
  Chinese academic draft for publication-quality English. Also trigger on
  general academic/scientific writing requests even without the word
  "materials", including academic writing, scientific writing, SCI/paper
  writing, English manuscript polishing, language editing, proofreading, and
  Chinese phrasings such as 学术写作、科研写作、论文润色、写paper、SCI写作、
  英文论文润色、语言润色、润色、改写、学术英语、英文写作、中译英、降重、
  检查语法、检查句式、修改句式.
---

# Materials Science Polishing — Router

Polish materials prose while preserving scientific responsibility.

This skill is split into two layers:

- A **static layer** under `static/` and `references/` that holds versioned,
  reusable content fragments — core stance, failure-mode diagnosis, polishing
  contract, workflow, output format, paper-type playbooks, per-section guidance,
  language-specific rules, per-journal-family style, and per-domain rules.
- A **dynamic layer** (this file plus [manifest.yaml](manifest.yaml)) that
  detects the request's axes and loads only the fragments needed for the current
  job.

Do not apply polishing logic from memory or from this router. Always load
fragments from disk as described below.

## Why this split

- Materials manuscripts span many material families (civil, polymers, metals,
  ceramics, functional, nano) and engineering domains; baking every rule into
  the router would bloat context with guidance irrelevant to the current polish.
- The static layer is versioned and reviewable. Adding a new journal style,
  material family, or section pattern is one new file plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to
  this polish enter context, instead of the full multi-thousand-line reference
  set.
- The router itself is short on purpose. Update fragments, not this file, when
  adding scope.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares six axes — `section`,
`journal_family`, `language_mode`, `paper_type`, `material_family`, `domain` —
the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance,
failure-mode diagnosis, polishing contract, workflow, output format, evidence
contract, claim-strength ladder, terminology ledger, ethics, and weakness routing
that apply to every polishing job.

### 2. Apply profile-first routing

Apply profile-first routing from `.materials/profile.yaml`; on first use, ask
for direction once and save it locally. This sets the default `material_family`
and `domain` before axis detection.

### 3. Detect the axis values for this request

For each axis in the manifest, decide the value using the manifest's `detect:`
hint and the user's input:

- `section` — abstract / introduction / results-discussion / conclusions /
  methods / title / cover-letter / generic. May be multiple. Ask the user if it
  is ambiguous and matters for the polish.
- `journal_family` — materials / pavement / cement-concrete / polymers /
  ceramics / metals / insulation / nano / functional. Default: materials.
- `language_mode` — rulebook / chinese-to-english / claim-strength. Default:
  rulebook.
- `paper_type` — research / review. Default: research.
- `material_family` — neutral / civil / polymers / metals / ceramics /
  functional / nano. Default: neutral (or the saved profile value).
- `domain` — general / civil / polymers / metals / ceramics / functional /
  nano. Default: general (or the saved profile value).

State the detected axis values in one short line to the user before proceeding,
so they can correct you cheaply.

### 4. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section`
axis only if the user has supplied free-floating prose with no section context.

Do **not** read every fragment in `static/` or `references/`. Load only what
step 3 selected.

### 5. Polish using the loaded material

Apply the loaded fragments in this priority order, matching the
`paper type -> section job -> paragraph logic -> claim/evidence/boundary ->
sentence polish` rule from `static/core/failure-modes.md`:

1. **Core stance and failure-modes** (`static/core/stance.md`,
   `static/core/failure-modes.md`) — diagnose the main structural problem
   before editing a single sentence.
2. **Paper-type playbook** (`static/fragments/paper_type/research.md` or
   `review.md`) — argument chain and polishing order.
3. **Section-specific job and failure modes** (`static/fragments/section/*.md`
   or `references/<section>.md`) — template check, tense audit, section shape.
4. **Domain rules** (`static/fragments/domain/*.md`) — material-system-specific
   evidence norms, terminology checks, and overclaim patterns.
5. **Material_family rules** (`../materials-research/static/fragments/domain/*-family.md`)
   — family-level framing and test conventions.
6. **Journal_family framing and constraints** (`references/*-language.md` or
   `references/style-guardrails.md`) — journal-specific tone and terminology.
7. **Language rules** (`static/fragments/language/*.md` or
   `references/chinese-to-english-patterns.md`) — apply last.

Run the 12-step workflow in [static/core/workflow.md](static/core/workflow.md)
end-to-end. Do not skip the diagnosis steps (sentence split, section
identification, hourglass check) just because the user asked for a quick polish
— structural problems cannot be polished away.

If a paragraph's structural problem cannot be fixed without inventing content,
flag it instead of papering over it.

### 6. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on
demand per the `references.on_demand` table in the manifest. Typical triggers:

- The user needs to verify section structure, information flow, or paragraph
  order → [references/hourglass-structure.md](references/hourglass-structure.md).
- The user needs to calibrate causal vs. associative language →
  [references/claim-strength-ladder.md](references/claim-strength-ladder.md) or
  `../_shared/core/claim-strength-ladder.md`.
- The user needs weak-word and verb calibration →
  [references/vocabulary-upgrade.md](references/vocabulary-upgrade.md).
- The user needs to audit citations, attribution, or density →
  [references/citation-integrity.md](references/citation-integrity.md).
- The user needs British English spelling and consistency →
  [references/british-english.md](references/british-english.md).
- The user needs final mechanical checks →
  [references/proofreading.md](references/proofreading.md).
- The user needs Chinese-to-English rewriting patterns →
  [references/chinese-to-english-patterns.md](references/chinese-to-english-patterns.md).

## Output format

Follow [static/core/output-format.md](static/core/output-format.md):

1. The polished text as plain prose.
2. `Revision notes:` with 3–5 short bullets on major structural and stylistic
   changes.
3. `Claim Risk Note:` when overclaim, tense, boundary, or citation issues are
   flagged (see Step 12 of `static/core/workflow.md`).

If any paragraph's structural problem could not be fixed without inventing
content, say so under `Revision notes:` instead of papering over it.

## Gates

- Do not make weak evidence sound strong.
- Limit sentences to <=35 words.
- Preserve data, units, test conditions, citation intent, uncertainty,
  limitations, and author meaning.
- Flag unsupported novelty, missing statistical evidence, vague mechanism
  claims, sustainability claims without boundary, and "significant" without
  statistical support.
- Do not invent data, experiments, citations, mechanisms, or novelty claims.
