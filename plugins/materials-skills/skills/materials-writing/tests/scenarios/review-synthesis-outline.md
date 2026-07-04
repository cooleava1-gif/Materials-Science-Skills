# Test: Review synthesis outline — axes, not paper list

## Skill

materials-writing

## Input

The user asks: "I have 15 papers on epoxy-modified asphalt for pavement applications. Help me outline a mini-review."

Available information:
- 15 papers cover: epoxy types, curing agents, emulsification methods, bonding tests, moisture conditioning, and field case studies.
- No synthesis structure is provided by the user.

## Expected behavior

- Detect `paper_type` as `review-paper`.
- Propose a synthesis-axes structure for the review outline:
  - mechanism (curing, crosslinking, interfacial bonding),
  - material design (epoxy type, dosage, emulsification route),
  - performance trade-off (bonding gain vs. viscosity/storage-stability cost),
  - research agenda (wet-condition validation, standardization, field gaps).
- Explain why each axis is chosen and how the 15 papers map to the axes.
- Identify explicit evidence gaps in the literature (e.g., limited wet-bonding data, inconsistent test standards).
- Output a structured outline in the six-part writing format, with the outline itself organized by synthesis axes.

## Forbidden behavior

- Do not produce a paper-by-paper annotated bibliography.
- Do not list papers as the top-level outline headings.
- Do not omit the evidence-gap and research-agenda sections.
- Do not let the user infer the synthesis structure rather than stating it explicitly.

## Pass/fail checklist

- [ ] The outline is organized by synthesis axes, not by paper-by-paper summaries.
- [ ] The chosen axes are justified in the output.
- [ ] Evidence gaps in the literature are explicitly called out.
- [ ] A research agenda is proposed.
- [ ] The 15 papers are mapped to the axes rather than listed sequentially.
