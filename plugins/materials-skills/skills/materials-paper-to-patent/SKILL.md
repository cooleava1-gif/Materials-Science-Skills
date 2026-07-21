---
name: materials-paper-to-patent
description: Convert materials science papers, theses, technical reports, figures, or research manuscripts into evidence-grounded Chinese invention patent drafts. Use when extracting patentable contributions, mapping claimed features to source evidence, preserving formulas and ranges, generating claim-aligned figures, validating claims against patent_kb.yaml, auditing support, or delivering separate Chinese DOCX artifacts. Default invention type is process-material.
---

# Materials Paper to Chinese Patent Router

Read `manifest.yaml` and its `always_load` files. Apply profile-first routing, detect `source_format`, `task_mode`, and `invention_type`, state the values, and load only selected fragments and keyed references.

Evidence boundary:

- Inspect the complete substantive source; stop if it cannot be inspected. Create stable P/E/F/C source IDs and use only `explicit`, `inherent`, `needs-confirmation`, or `unsupported` support states.
- Unsupported features never enter formal claims. Convert needs-confirmation features into inventor questions outside claims; never invent legal, inventor, jurisdiction, or experimental facts.
- Unresolved confirmation items force overall status `incomplete-draft`; never label the package `review-draft` or complete.
- Formal claims, specification, abstract, figure labels, and descriptions are Chinese. Preserve source-supported formulas as editable Office Math, disclosed ranges/units, claim-aligned figures, and claim-to-source mappings.

Algorithm/software gate:

- A pure algorithm/software prediction claim (`纯算法/软件预测`) is an Article 25 subject-matter risk under `《专利法》第二十五条`; model accuracy alone is not a patentable technical contribution.
- Before formal claims, require a disclosed concrete technical feature such as a manufacturing/process step, sensor-controller loop, apparatus, or measurable technical effect. Otherwise block the claim and mark the feature `needs-confirmation`.
- A quality-control or technical-process reframing is only a suggestion; never add undisclosed sensors, actuators, manufacturing steps, or effects.

Route requirements:

- `disclosure-analysis`: source map, inventories, and evidence ledger only; do not load formal claim output.
- `claim-set`: load `patent-kb`, `stage-gates`, `claim-checklist`, and `cn-drafting-guide` before formal claims.
- `full-draft`: additionally load `output-contract` and `draft-schema`; consume `reader-package` and `figure-handoff` only when supplied.
- `paper-patent-audit`: load `corpus-pair-audit` and the formal-claim references when claims are audited.

Run `validate_patent_draft.py`, `validate_patent_claims.py` for the detected invention type, and `build_patent_package.py`. Resolve every `ERROR`, review warnings against the source, label gaps `incomplete-draft`, and emit `patent-draft-handoff` to `materials-research` with validated artifact paths and status. This is a drafting aid, not a legal opinion or filing guarantee.
