---
name: materials-html-deck
version: "3.0.0"
stability: beta
description: Use when generating browser-native HTML academic decks from materials science papers, notes, figures, data, or slide outlines.
---

# Materials HTML Deck Router

Read `manifest.yaml` and all declared `always_load` files. Apply profile-first routing, then detect `deck_type`, `paper_type`, `task`, `output_format`, `verification_level`, `academic_style`, `source_type`, `domain`, `material_family`, and `template`; load only selected fragments.

The source artifact is a browser-native deck: `index.html`, independent `slides/*.html`, shared style tokens, screenshots, speaker notes, QA report, and an asset manifest. A JSON outline may use `scripts/build_deck.mjs`; paper, notes, text, or data require source extraction and a slide-by-slide evidence plan before the same build path.

Hard stops:

- Keep every slide claim tied to a supplied figure, table, test, or source paper; separate measured results from inferred mechanisms.
- Do not fabricate numbers, figure details, unsupported implications, or missing assets. Do not crop away data labels, axes, legends, or scale bars.
- Run strict Playwright verification on every slide. If Playwright is missing, fail with the exact installation blocker rather than claiming visual QA.
- Deliver screenshots, speaker notes, QA report, and asset manifest with the HTML deck; missing required artifacts keep the package incomplete.

Use Chinese slide titles by default unless English is requested. Route static scientific figure production to `materials-figure`, manuscript prose to `materials-writing`, and Office/document export outside this Skill. Run `scripts/verify_deck_html.mjs` and report page errors, console errors, missing media, blank slides, and screenshot status.
