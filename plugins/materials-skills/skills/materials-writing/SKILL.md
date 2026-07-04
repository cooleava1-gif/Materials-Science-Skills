---
name: materials-writing
version: "1.2.0"
description: Use when drafting, restructuring, or auditing manuscripts for materials science and engineering research.
---

# Materials Science Writing

Turn claims, results, notes, and outlines into bounded manuscript prose.

`materials-writing` is an evidence-first drafting engine. It does not generate freeform prose from prompts. It runs a staged workflow that locks terminology, writes a one-sentence argument, maps paragraph messages, passes a confirmation gate, and only then drafts prose that can be traced back to evidence. Missing evidence stays visible as placeholders rather than being hidden in fluent sentences.

## What the skill does

- Drafts section-level prose (abstract, introduction, methods, results/discussion, conclusion) and review synthesis outlines.
- Builds a claim-evidence-boundary table before drafting so every paragraph is anchored.
- Surfaces missing inputs as `[TO CONFIRM: ...]` placeholders and `Assumptions` entries.
- Produces handoff-ready artifacts for companion skills: `reader-package`, `citation` matrices, `doe-handoff`, and polishing/reviewer loops.

## Layered architecture

This skill is split into two layers that work as one engine:

- **Static layer** under `static/` — versioned, reusable content fragments. These include core stance, workflow, output format, section drafting rules, paper-type playbooks, domain rules, journal framing, and language guidance. Static fragments carry the actual drafting logic.
- **Dynamic layer** — this file plus [manifest.yaml](manifest.yaml). The router detects the seven axes declared in the manifest, loads only the fragments needed for the current job, and runs the shared workflow end-to-end. The router does not re-encode drafting logic that already lives in fragments.

### Why this split

- Materials manuscripts span many families and domains; loading every rule would bloat context with irrelevant guidance.
- The static layer is versioned and reviewable. Adding a new journal style, material family, or section pattern is one new file plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft enter context.
- The router stays short. Update fragments, not this file, when adding scope.

## Routing protocol

Follow these steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares seven axes — `paper_type`, `section`, `language`, `journal_family`, `material_family`, `domain`, `input_source` — the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance, writing workflow, evidence contract, claim-strength ladder, terminology ledger, output format, and ethics that apply to every drafting job.

### 2. Apply profile-first routing

Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally. This sets the default `material_family` and `domain` before axis detection.

### 2b. Load experiment record if provided

If the user provides `experiment-record.yaml`, load it and seed the terminology ledger and evidence audit table before detecting sections. Route missing or ambiguous record fields through the confirmation gate as placeholders.

### 3. Detect the seven axis values

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input:

- `paper_type` — experimental-manuscript / review-paper / methods-paper. Default: experimental-manuscript.
- `section` — abstract / introduction / methods / results-discussion / conclusion / full-argument / cover-letter / highlights / methods-from-record / results-from-record / discussion-mechanism. May be multiple. Ask the user if it is ambiguous and matters for the draft.
- `language` — en or zh-to-en. Detect from the user's notes themselves.
- `journal_family` — CBM / CCC / RMPD / JBE / materials. Default: materials.
- `material_family` — neutral / civil / polymers / metals / ceramics / functional / nano. Default: neutral (or the saved profile value).
- `domain` — general / civil / polymers / metals / ceramics / functional / nano. Default: general (or the saved profile value).
- `input_source` — manual / experiment-record. Default: manual.

State the detected axis values in one short line to the user before drafting, so they can correct you cheaply.

### 4. Load the matching fragments

For each axis value, read the file mapped in the manifest. Skip the `section` axis only when the user has explicitly asked for a free-floating argument paragraph with no section context.

Do **not** read every fragment in `static/`. Load only what step 3 selected.

### 5. Apply fragments in priority order and run the staged workflow

Apply the loaded fragments in this priority order:

1. Core stance ([../_shared/core/stance.md](../_shared/core/stance.md)) — surface missing claim / evidence / boundary before drafting.
2. `paper_type` playbook — argument chain and drafting order (e.g., experimental-manuscript drafts Results → Introduction → Conclusion → Methods → Abstract).
3. `section` drafting rules and structure.
4. `domain` rules — material-system-specific evidence norms and red flags.
5. `material_family` rules — family-level framing and test conventions.
6. `journal_family` framing and constraints.
7. `language` sentence and paragraph rules (apply last).

Then run the 5-stage workflow in [static/core/workflow.md](static/core/workflow.md) end-to-end:

1. Identify the job and lock terminology.
2. Write the one-sentence argument.
3. Map section architecture and paragraph messages.
4. Ask for confirmation before full prose.
5. Draft, calibrate, and revise.

Do not skip the planning steps (1-4) just because the user asked for prose immediately. Write the one-sentence argument and pass the confirmation gate first. If essential evidence or boundary is missing, write a placeholder and list it under `Assumptions` instead of inventing content.

### 6. Reach for references only when needed

The files under `references/` are deep references and the example library, not defaults. Open them on demand per the `references.on_demand` table in the manifest. Typical triggers:

- The user needs paper logic, contribution chain, or section-to-section flow → [references/argument-chain.md](references/argument-chain.md) or [references/article-architecture.md](references/article-architecture.md).
- The manuscript concerns waterborne epoxy modified emulsified asphalt → [references/waterborne-epoxy-narrative.md](references/waterborne-epoxy-narrative.md).
- The task is a mini-review, small review, or literature review → [references/review-paper-strategy.md](references/review-paper-strategy.md) and [references/section-patterns/review-synthesis-patterns.md](references/section-patterns/review-synthesis-patterns.md).
- The draft needs overclaim, missing-evidence, or journal-fit risk checking → [references/reviewer-risk-writing.md](references/reviewer-risk-writing.md).
- The user needs writing patterns or sentence templates from real materials papers → [references/published-article-patterns.md](references/published-article-patterns.md).
- The user needs paragraph-level flow, topic sentences, or inter-paragraph transitions → [references/paragraph-flow.md](references/paragraph-flow.md).

## Handoffs

Produce handoff-ready writing artifacts for companion skills when they are the next logical step:

- **materials-reader** — when the user needs source-paper intensive reading, route to `materials-reader` and consume its `reader-package` / `source_map`.
- **materials-citation** — emit a `claim-evidence-boundary` table so `materials-citation` can build the citation matrix without re-reading the draft.
- **materials-doe** — when the user needs an experiment matrix, route to `materials-doe` and consume its `doe-handoff` to align test variables with claims.
- **materials-polishing** — pass the section draft, claim-evidence map, and terminology ledger for language polishing without losing evidence boundaries.

If any handoff artifact is missing, mark the missing input and route the weakness through [../_shared/paper-production/weakness-routing.md](../_shared/paper-production/weakness-routing.md) instead of inventing evidence.

## Gates

- Claims must match the evidence contract: no overclaim, no speculation presented as fact.
- Lock terminology before drafting; never let a draft reintroduce a variant of a locked term.
- Use the claim-strength ladder to calibrate causal vs. associative language.
- One paragraph carries one message; every paragraph must be easy to reverse-outline.
- Pass the confirmation gate before producing full section output unless the claim, evidence, and boundary are all clearly given and unambiguous.
- For WER-EA manuscripts: follow the mini-review pipeline if this is a review-style paper.

This structure mirrors the other materials-* skills so shared content can be lifted into the `_shared/` layer used by all of them.
