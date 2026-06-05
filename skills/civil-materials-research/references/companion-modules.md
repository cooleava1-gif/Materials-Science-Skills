# Companion Modules

`civil-materials-research` is the strategic router. Use companion skills for production-heavy work.

| Need | Companion skill | Use when |
|---|---|---|
| Full paper reading | `civil-materials-reader` | reading PDFs, pasted papers, DOI/HTML, evidence-chain audits, literature matrices, journal-club notes |
| Literature search and citation mapping | `civil-materials-citation` | building search strategies, citation matrices, reference gap audits, claim-source maps |
| English polishing | `civil-materials-polishing` | polishing abstracts, introductions, results/discussions, cover letters, Chinese-to-English text, claim-strength audits |
| Reviewer response | `civil-materials-response` | major/minor revision responses, rebuttal letters, response tables, revision summaries |
| PPT outlines and slide logic | `civil-materials-paper2ppt` | group meeting decks, journal-club slides, thesis/project reports, review talks, slide-ready Markdown |
| Real PPTX generation | `civil-materials-pptx` | one-click `.pptx` generation, Markdown/JSON-to-PPTX conversion, PowerPoint deck scaffolds |
| Figures | `civil-materials-figure` | figure plans, SVG plots, figure packages, data-to-caption work |
| Data and FAIR | `civil-materials-data` | raw/processed data organization, metadata, FAIR audits, dataset packages, data availability statements |

Routing rule:

1. Use `civil-materials-research` first when the user needs topic strategy, evidence-chain judgment, journal targeting, or experiment design.
2. Use a companion skill when the output format is already clear.
3. Return to `civil-materials-research` for final reviewer-risk audit before submission.

Preferred handoff sequence for a full manuscript cycle:

1. `civil-materials-reader` for source notes.
2. `civil-materials-citation` for claim-source mapping.
3. `civil-materials-research` for manuscript logic and journal fit.
4. `civil-materials-polishing` for English.
5. `civil-materials-data` for FAIR packaging and data availability statements.
6. `civil-materials-figure` and `civil-materials-pptx` for visual outputs.
7. `civil-materials-response` after peer review.
