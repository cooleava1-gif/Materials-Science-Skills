---
name: materials-writing
version: "1.1.0"
description: Use when drafting, restructuring, or auditing manuscripts for materials science and engineering research.
---

# Materials Science Writing

Draft materials manuscripts with evidence-grounded claims and journal-aware structure.

## Layered architecture

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments — core stance, workflow, output format, paper-type playbooks, per-section drafting guidance, per-material-family and per-domain rules, language-specific rules, and per-journal style.
- A **dynamic layer** (this file plus [manifest.yaml](manifest.yaml)) that detects the request's axes and loads only the fragments needed for the current job.

Do not apply drafting logic from memory or from this router. Always load fragments from disk as described below.

### Why this split

- Materials manuscripts span many material families (civil, polymers, metals, ceramics, functional, nano) and engineering domains; baking every rule into the router would bloat context with guidance irrelevant to the current draft.
- The static layer is versioned and reviewable. Adding a new journal style, material family, or section pattern is one new file plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft enter context, instead of the full multi-thousand-line reference set.
- The router itself is short on purpose. Update fragments, not this file, when adding scope.

## Routing protocol

Follow these steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares seven axes — `paper_type`, `section`, `language`, `journal_family`, `material_family`, `domain`, `input_source` — the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance, writing workflow, evidence contract, claim-strength ladder, terminology ledger, and ethics that apply to every drafting job.

### 2. Apply profile-first routing

Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally. This sets the default `material_family` and `domain` before axis detection.

### 2b. Load experiment record if provided

If the user provides `experiment-record.yaml`, load it and seed the terminology ledger and evidence audit table before detecting sections.

### 3. Detect the seven axis values

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input:

- `paper_type` — experimental-manuscript / review-paper / methods-paper. Default: experimental-manuscript.
- `section` — abstract / introduction / methods / results-discussion / conclusion / full-argument / cover-letter / highlights / methods-from-record / results-from-record / discussion-mechanism. May be multiple. Ask the user if it is ambiguous and matters for the draft.
- `language` — en or zh-to-en. Detect from the user's notes themselves.
- `journal_family` — CBM / CCC / RMPD / JBE / materials. Default: materials.
- `material_family` — neutral / civil / polymers / metals / ceramics / functional / nano. Default: neutral (or the saved profile value).
- `domain` — general / civil / polymers / metals / ceramics / functional / nano. Default: general (or the saved profile value).

State the detected axis values in one short line to the user before drafting, so they can correct you cheaply.

### 4. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section` axis only when the user has explicitly asked for a free-floating argument paragraph with no section context.

Do **not** read every fragment in `static/`. Load only what step 3 selected.

### 5. Apply fragments in priority order

Apply the loaded fragments in this priority order:

1. Core stance ([../_shared/core/stance.md](../_shared/core/stance.md)) — surface missing claim / evidence / boundary before drafting.
2. `paper_type` playbook — argument chain and drafting order (e.g., experimental-manuscript drafts Results → Introduction → Conclusion → Methods → Abstract).
3. `section` drafting rules and structure.
4. `domain` rules — material-system-specific evidence norms and red flags.
5. `material_family` rules — family-level framing and test conventions.
6. `journal_family` framing and constraints.
7. `language` sentence and paragraph rules (apply last).

Run the 11-step workflow in [static/core/workflow.md](static/core/workflow.md) end-to-end. Do not skip the planning steps (1-5) just because the user asked for prose immediately — write the one-sentence argument and pass the confirmation gate first.

If essential evidence or boundary is missing, write a placeholder and list it under `Assumptions` instead of inventing content.

### 6. Reach for references only when needed

The files under `references/` are deep references and the example library, not defaults. Open them on demand per the `references.on_demand` table in the manifest. Typical triggers:

- The user needs paper logic, contribution chain, or section-to-section flow → [references/argument-chain.md](references/argument-chain.md).
- The manuscript concerns waterborne epoxy modified emulsified asphalt → [references/waterborne-epoxy-narrative.md](references/waterborne-epoxy-narrative.md).
- The task is a mini-review, small review, or literature review → [references/review-paper-strategy.md](references/review-paper-strategy.md).
- The draft needs overclaim, missing-evidence, or journal-fit risk checking → [references/reviewer-risk-writing.md](references/reviewer-risk-writing.md).
- The user needs writing patterns or sentence templates from real materials papers → [references/published-article-patterns.md](references/published-article-patterns.md).

## Gates

- Claims must match the evidence contract: no overclaim, no speculation presented as fact.
- Use the claim-strength ladder to calibrate causal vs. associative language.
- For WER-EA manuscripts: follow the mini-review pipeline if this is a review-style paper.

This structure mirrors the other materials-* skills so shared content can be lifted into the `_shared/` layer used by all of them.
