# Figure Stance

> **Domain context**: The `domain` axis has loaded domain-specific figure guidance for [detected domain]. The stance below is general; the domain guide lists domain-specific figure types, panel structures, and reviewer pitfalls.

## Contract-First Stance

Contract-first is the core stance of materials-figure. Every figure has a
contract before it has code.

- Any figure starts with `figure_contract.md` whose seven points hold
  substantive content, then passes `check_figure_contract.py` before any
  plotting code, data generation, preview, or rendered figure.
- No contract, no code. If the contract is unwritten, template-only, or fails
  validation, stop and revise it; do not plot.
- The automatic table-plotting loop obeys the same blocking gate. It may draft
  the contract from the source table and goal, but the draft must be confirmed
  and pass validation before any plotting script runs. Zero-interaction
  auto-plotting without a validated contract is not allowed.
- This overrides general autonomy/default-execution behavior for figure tasks.

## Operating Stance

- Treat every figure as a visual argument with a visible claim boundary.
- Prefer clear evidence hierarchy over visual decoration.
- Keep source data and source anchors close to the panel that uses them.
- Make reviewer-safe uncertainty visible: missing controls, missing replicates, incompatible test methods, lab-only durability, or inferred mechanism.
- Use restrained palettes and direct labels when they reduce cognitive load.
- Keep units, test conditions, and material-system boundaries visible.

## Materials Science Priorities

Refer to the auto-loaded domain figure guide for domain-specific figure types, multi-panel structures, and caption patterns. The domain guide covers: civil, polymers, metals, ceramics, functional, and nanomaterials.

- For SEM/TEM/fluorescence panels, preserve scale bars and image provenance.
- For FTIR/XRD/TG/DSR spectra, do not overstate chemistry or field durability from a single evidence layer.
- For review figures, link panels to a table-system row or `source_map.json` anchor when available.

## Reviewer-Safe Defaults

- Show measured evidence and inferred links with different visual encodings.
- Use captions that state what the data support and what they do not prove.
- Deliver figure packages with source data, script, exports, caption, QA report, and asset manifest when the user asks for a journal-ready figure.
