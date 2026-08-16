# AI-Assisted Schematic Workflow (Graphical Abstracts, Mechanism Drafts)

Use this reference whenever a task involves planning, generating, revising,
or auditing an AI-assisted graphical abstract, mechanism schematic, concept
illustration, or process diagram for a materials manuscript. Apply it before
any provider-specific image-generation instructions.

Adapted from the nature-skills AI graphical-abstract workflow (Apache-2.0),
retargeted to materials figure contracts.

## Authority boundary and policy gate

- Before generating a submission candidate, verify the target journal's
  current graphical-abstract, AI-generated-image, image-integrity, copyright,
  and disclosure rules on official pages. Record journal, URL, and access
  date in the provenance record.
- If journal clearance is unknown, label the output
  **internal design draft — submission eligibility unverified**. Never call
  it submission-ready.
- Keep two decisions separate: whether a draft is useful internally and
  whether the final asset is submission-eligible.
- Materials journals commonly restrict AI-generated artwork in submitted
  figures; data-derived panels are never AI-generated.

## 1. Define the communication target

1. The single sentence the reader should remember (the core conclusion from
   the figure contract).
2. Figure type: mechanism (e.g., curing, interface bonding, corrosion,
   degradation), process route, experimental setup, workflow, comparison,
   or structure–property map.
3. Audience vocabulary (materials / civil / chemistry readers).
4. Evidence boundary: what the study demonstrates, what is contextual, and
   what must not be implied.
5. Details to omit because they do not support the central message.

## 2. Build a visual brief

- Choose an explicit reading path: left-to-right, top-to-bottom, cycle, or
  split comparison; arrows and grouping only where they clarify that path.
- Limited, high-contrast, color-accessible palette; assign color by
  scientific meaning (phase, phase change, driving force), not decoration.
- Reserve the strongest accent for the central causal step or principal
  result.
- Panel captions stay out of the image; short redrawable labels only.

## 3. Assign the AI a bounded role

- Preferred: AI drafts the composition; the author redraws in vector form
  for submission.
- Acceptable: AI generates the full draft with the prompt written as a
  figure contract (below), then human scientific review.
- Never: AI invents quantitative values, fake micrographs, spectra, p-values,
  institutional marks, or journal logos; AI output presented as experimental
  data.

## 4. Write the prompt as a figure contract

Mirror the plotting figure contract: core conclusion, entities and phases
named exactly as in the manuscript, process steps in order, claim boundary,
and style constraints. Run
[scripts/generate_openrouter_schematic.py](../scripts/generate_openrouter_schematic.py)
in `--dry-run` first to review the assembled payload.

## 5. Human scientific and publication QA

- Scientific accuracy: every entity, arrow, and step defensible from the
  manuscript; no invented mechanism.
- Completeness: central message readable in under 30 seconds.
- Provenance: record tool, model, prompt, date, and human-reviewer name in
  `ai_schematic/<basename>_request_metadata.json` plus a one-line disclosure
  sentence drafted for the methods/acknowledgements if the journal allows
  AI-assisted graphics.
- Redraw boundary: for submission-required vector output, treat the AI draft
  as the composition reference, not the final asset.

## Route boundaries

- Data-driven panels (XRD, FTIR, SEM plates, performance curves) always go
  through the plotting pipeline and its Python/R backend gate, never through
  the image API.
- This route (standalone draft) skips the backend gate because no data are
  plotted.
- Mixing: an AI mechanism draft may sit beside plotted panels only if each
  panel's origin (plotted vs AI draft) is stated in the caption.
- **Asset mode → hybrid composition**: when the goal is a publication-grade
  composite (not a draft), AI generates decoration assets only (icons,
  gradients, shadows, translucent blocks) and R draws every semantic
  element. Switch to
  [hybrid-composition.md](hybrid-composition.md) and drive generation with
  `--asset-mode`; the bounded role below tightens to "decoration only, no
  text, no arrows, no borders in the AI image".
