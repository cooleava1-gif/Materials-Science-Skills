# materials-pptx

**What it does** — Turns structured Markdown or JSON slide specs into a real
`.pptx` deck for civil engineering and construction materials presentations,
with speaker notes and image placement. It is the generation layer after the
talk story and slide logic are already decided: it reads a slide outline,
embeds PNG/JPEG figures with source-rectangle cropping, attaches per-slide
speaker notes, and writes a valid Office Open XML `.pptx` file. Use it for
journal clubs, group meetings, thesis reports, and paper presentations.

**Built from** — A dependency-light OOXML writer plus deck and style guides:

- `scripts/build_materials_pptx.py` — writes `.pptx` directly with Python
  standard libraries (no python-pptx dependency); supports Markdown/JSON input,
  presets, per-slide images, cropping, and speaker notes
- `references/deck-structures.md` — deck-type structures (paper-reading,
  research-report, review-talk)
- `references/visual-style.md` — mechanism-deck visual style
- `references/pptx-generation.md` — command examples and accepted input shapes
- `static/core/` — contract, pptx-contract, and workflow
- `static/fragments/template/` — academic, defense, and journal-club templates
- `static/fragments/domain/` — domain-context fragment for materials routing
- `assets/templates/` — deck-outline templates in Markdown and JSON

**Default output package** — A real `.pptx` file with embedded media and notes:

```text
deck.pptx
  ppt/slides/          one slide per slide spec
  ppt/notesSlides/     speaker notes linked to each slide
  ppt/media/           embedded PNG/JPEG figures
```

A generated deck includes a title slide, engineering problem, material design
or paper identity, experiment/evidence chain, key results, mechanism or
interpretation, limitations, and next steps. Missing information stays as a
visible placeholder rather than invented content.

**Key rules enforced**

- Generates the file only; it does not design the talk logic. If the slide
  structure is not ready, start with `materials-paper2ppt`.
- Speaker notes are required on note-bearing slides; do not ship silent decks.
- One main message per slide; Chinese titles by default, English only when
  requested.
- Image cropping must preserve axes, legends, labels, and scale bars; never
  crop away data.
- Separate measured results from inferred mechanisms; keep claims tied to
  figures, tests, or source papers.
- If information is missing, keep the placeholder visible rather than inventing
  content.

**Reference files**

```text
skills/materials-pptx/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   └── build_materials_pptx.py   OOXML .pptx writer (stdlib, no python-pptx)
├── assets/
│   └── templates/
│       ├── deck-outline-template.md    Markdown slide outline template
│       └── deck-outline-template.json  JSON slide outline template
├── static/
│   ├── core/
│   │   ├── contract.md        evidence contract
│   │   ├── pptx-contract.md   required slides and media/notes rules
│   │   └── workflow.md        6-step generation workflow
│   └── fragments/
│       ├── template/
│       │   ├── academic.md      academic/conference template
│       │   ├── defense.md       thesis defense template
│       │   └── journal-club.md  journal-club template
│       └── domain/
│           └── domain-context.md  materials domain routing
└── references/
    ├── deck-structures.md    deck-type structures
    ├── visual-style.md       mechanism-deck visual style
    └── pptx-generation.md    command examples and input shapes
```

**Validation**

- Bundle verification: `python .\scripts\run_release_checks.py --json`
- Architecture check: `python .\scripts\check_skill_architecture.py --json`

## When To Use

Use `materials-pptx` when the user request matches this skill's production surface and the needed inputs are available or can be explicitly marked as missing.

## Inputs

Typical inputs are the user prompt, material direction/profile, target journal or task mode when relevant, and any source text, data, figures, reviewer comments, or package artifacts needed by the skill.

## Outputs

Outputs are structured handoffs or artifacts described above in this README. Missing evidence, author input needs, and unsupported claims stay visible instead of being hidden in fluent prose.

## Example

```text
Render a structured slide spec into a real PowerPoint deck.
```

## Validation

Run the skill-specific scripts or tests listed above when they apply, then run the bundle gate from the repository root:

```powershell
python .\scripts\run_release_checks.py --json
```

## Boundaries

This skill does not invent experiments, citations, measurements, journal facts, private file paths, or completed actions. Time-sensitive journal or legal facts should be checked against official sources before submission or filing.
