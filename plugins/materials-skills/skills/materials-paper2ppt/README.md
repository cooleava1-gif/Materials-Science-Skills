# materials-paper2ppt

**What it does** — Converts papers, reading notes, review matrices, and
research outlines into slide-ready Markdown for civil engineering and
construction materials presentations. It is the handoff layer before real
PowerPoint generation: it structures the talk around the evidence chain rather
than manuscript section order, emits a slide-by-slide Markdown outline with
Chinese titles, pacing, figure placement, and speaker notes, then hands off to
`materials-pptx` for the actual `.pptx` file.

**Built from** — Journal-club and group-meeting practice with evidence-first
slide design:

- `references/` — 5 deck-type arcs (journal-club, project-report, review-talk,
  mechanism, materials-experiment-arc) plus a pptx-handoff guide
- `static/core/` — contract, ppt-contract, and the 7-step workflow
- `static/fragments/task/` — slide-outline and pptx-deck task fragments
- `static/fragments/domain/` — domain-context fragment for materials routing
- `scripts/build_ppt_markdown.py` — fast Markdown scaffold, with optional
  `--pptx-output` for a quick `.pptx`
- `assets/templates/materials-ppt-template.md` — slide Markdown template

**Presentation logic** — A 7-step arc drives every deck:

1. Classify the paper or project.
2. Write a one-sentence presentation thesis.
3. Select 3-6 evidence points.
4. Assign one slide purpose per slide.
5. Place figures only where they prove the slide claim.
6. Add Chinese takeaways and speaker notes.
7. Run a final check for overcrowding, unsupported claims, and missing
   limitations.

**Default output package** — A slide-ready Markdown outline handed off to
`materials-pptx`:

```text
paper2ppt-output/
  slides.md          slide-by-slide outline (## Slide N - Title)
```

Each slide carries 3-5 bullets where the first bullet is the slide message and
the second is the evidence source, followed by a speaker-note block and figure
references:

```markdown
## Slide N - Title
- Slide message (one-sentence claim)
- Evidence source (figure, table, or citation)
- Supporting bullets
Speaker note:
- Talking points and caveats
![figure](path/to/figure.svg)
```

**Key rules enforced**

- Structures the talk only; does not by itself produce a final `.pptx`. Use
  `materials-pptx` for real deck generation, or
  `build_ppt_markdown.py --pptx-output` for a fast scaffold.
- Chinese slide titles by default; English only when requested.
- Each figure must stay tied to a claim; no fabricated figures, numbers,
  mechanisms, or paper conclusions.
- One slide purpose per slide; avoid crowded text.
- Every deck ends with limitations and borrowable ideas.

**Reference files**

```text
skills/materials-paper2ppt/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   └── build_ppt_markdown.py   slide Markdown builder, optional --pptx-output
├── assets/
│   └── templates/
│       └── materials-ppt-template.md   slide Markdown template
├── static/
│   ├── core/
│   │   ├── contract.md        evidence contract
│   │   ├── ppt-contract.md    deck rules and claim discipline
│   │   └── workflow.md        7-step presentation arc
│   └── fragments/
│       ├── task/
│       │   ├── slide-outline.md   slide outline task fragment
│       │   └── pptx-deck.md       pptx-deck task fragment
│       └── domain/
│           └── domain-context.md  materials domain routing
└── references/
    ├── journal-club-deck.md        journal-club deck arc
    ├── project-report-deck.md      project/thesis report deck arc
    ├── review-talk-deck.md         review/progress talk deck arc
    ├── mechanism-deck.md           mechanism-focused deck arc
    ├── materials-experiment-arc.md experiment story arc
    └── pptx-handoff.md             handoff logic to materials-pptx
```

**Validation**

- Bundle verification: `python .\scripts\run_release_checks.py --json`
- Architecture check: `python .\scripts\check_skill_architecture.py --json`
