# Companion Modules

`materials-research` is the strategic router. Use companion skills for production-heavy work.

| Need | Companion skill | Use when |
|---|---|---|
| Full paper reading | `materials-reader` | reading PDFs, pasted papers, DOI/HTML, evidence-chain audits, literature matrices, journal-club notes |
| Literature search and citation mapping | `materials-citation` | building search strategies, citation matrices, reference gap audits, claim-source maps |
| From-scratch manuscript drafting | `materials-writing` | paper argument chains, abstracts, introductions, results/discussion drafting, review-paper outlines |
| English polishing | `materials-polishing` | polishing abstracts, introductions, results/discussions, cover letters, Chinese-to-English text, claim-strength audits |
| Reviewer response | `materials-response` | major/minor revision responses, rebuttal letters, response tables, revision summaries |
| Simulated peer review | `materials-reviewer` | referee-style reports, pre-submission reviewer-risk audits, two-reviewer simulations, cross-review synthesis |
| High-fidelity HTML academic decks | `materials-html-deck` | group meeting decks, journal-club slides, thesis/project reports, review talks, Markdown/JSON-to-HTML deck generation |
| Figures | `materials-figure` | figure plans, SVG plots, figure packages, data-to-caption work |
| Data and FAIR | `materials-data` | raw/processed data organization, metadata, FAIR audits, dataset packages, data availability statements |
| Design of experiments | `materials-doe` | DOE methodology, factorial/screening designs, response surface optimization, robustness testing, orthogonal arrays, factor-level planning |

Routing rule:

1. Use `materials-research` first when the user needs topic strategy, evidence-chain judgment, journal targeting, or experiment design.
2. Use `materials-doe` when the experiment-design task requires formal DOE methodology (factorial, RSM, Taguchi, robustness).
3. Use a companion skill when the output format is already clear.
4. Return to `materials-research` for final reviewer-risk audit before submission.

Preferred handoff sequence for a full manuscript cycle:

1. `materials-reader` for source notes.
2. `materials-citation` for claim-source mapping.
3. `materials-doe` for experiment design and factor-level planning (when applicable).
4. `materials-writing` for argument chain and first complete draft.
5. `materials-research` for manuscript logic and journal fit.
6. `materials-polishing` for English.
7. `materials-data` for FAIR packaging and data availability statements.
8. `materials-figure` and `materials-html-deck` for visual outputs.
9. `materials-reviewer` for simulated peer review before submission.
10. `materials-response` after peer review.
