# Hybrid Composition Reference (default route for conceptual/schematic figures)

Layer-split composition is the **default** way `materials-figure` produces
conceptual/schematic figures — mechanism schematics, interface/molecular
illustrations, graphical abstracts, process diagrams, and TOC graphics:

- **AI layer (user-provided image model)** generates *decoration assets
  only*: pseudo-3D gradient spheres, icons, gradients, shadows, and
  semi-transparent color blocks — always watermark-stripped, transparent
  background, never text or structure.
- **R layer** draws *everything semantic*: all text, panel borders, arrows,
  dashed boxes, dimension marks, captions, and scientific annotations —
  crisp, editable vector output.

R stays the sole drawing backend (the exclusivity rule is preserved: AI
assets are *inputs*, not a backend). Data panels are never part of this
route.

A standalone AI draft (the model draws an entire schematic in one image) is
used only when the user explicitly asks for a quick draft; the hybrid route
remains the default even then unless stated otherwise.

## AI tool requirement and fallback / 工具前置与兜底

Hybrid composition requires the **user to provide an AI image model** —
GPT Image 2 (OpenRouter or any OpenAI-compatible endpoint via
`--api-url`), nanobanana / Gemini image models, or any tool the user can
run. Check availability before promising a hybrid figure; if no tool is
available, say so explicitly and offer the fallback below — never
fabricate "AI-generated" assets or silently drop the decoration layer.

| Situation | Action |
|---|---|
| API access provided (key/endpoint) | Generate assets with `generate_openrouter_schematic.py --asset-mode` (dry-run payload first); record provenance from `*_request_metadata.json` |
| User generates assets themselves (e.g., nanobanana in their own UI) | Hand over `fig4_asset_prompt.txt`-style decoration prompts; user drops the PNGs into `assets/`; record tool + model + date manually in `asset_manifest.yaml`; the layer contract (no text/arrows/borders, no watermark) still applies |
| No AI tool at all | Explain that hybrid needs a user-provided image model, then fall back to full R/Python drawing: procedural decoration approximations (soft radial-gradient discs via raster math or layered translucent circles, tint fills, simulated shadows) — same semantics, same export bundle; mark the figure R/Python-drawn, no AI disclosure needed |

The fallback is a first-class path, not a degraded error: procedural
decorations in R/Python keep the figure complete and submission-safe with
zero policy gate. When a tool later becomes available, re-run only the
asset step and swap the decoration layer via the placement map.

## Watermark policy 去水印（默认强制）

- AI image providers embed provenance marks (e.g. C2PA manifest blocks and
  pixel-level model watermarks). **Assets entering a composite figure must
  be stripped of the manifest block** before placement; the generation
  script's default behavior should already remove it for PNG output — never
  request the provider to keep provenance markers.
- Generate hybrid assets as **PNG + transparent background**; formats that
  do not auto-strip provenance blocks (e.g. JPEG/WebP on some providers)
  should be avoided for composite assets.
- Pixel-level model watermarks cannot be removed losslessly from the raster
  itself, but because the AI layer is decoration-only (no semantics) and
  the semantic content is R-drawn vector, the residual mark does not affect
  text legibility or print quality. State "raster layer carries
  model-level watermark residue; semantic layer is vector" in the QA
  report.

## Layer contract 图层契约

| Element | Layer | Rule |
|---|---|---|
| Icons, gradients, shadows, translucent blocks | AI | decoration only; no meaning-carrying content; watermark-stripped PNG with transparent background |
| All text, numbers, letters | R | never rasterised into the AI image |
| Borders, frames, dashed boxes | R | precise geometry and alignment |
| Arrows, dimension marks, leader lines | R | direction and length are semantics |
| Scientific annotations (phase names, conditions, units) | R | must stay editable vector |
| Colour palette | shared | AI prompts reuse the R palette hex values |

An element that carries scientific meaning never enters the AI image; an
element that is purely decorative never needs hand-drawing in R.

## Workflow

1. **Figure contract first** — unchanged (`static/core/contract.md`): core
   conclusion, panel map, journal/export contract. Add one block: the
   asset list (which decorations exist, their target panels).
2. **Draft the layout in R** first with placeholder rectangles for asset
   slots (paper units, mm). This fixes geometry before any generation.
3. **Generate assets** with
   [scripts/generate_openrouter_schematic.py](../scripts/generate_openrouter_schematic.py)
   `--asset-mode --dry-run` first; real call with `--background
   transparent --output-format png`. One asset sheet or per-asset images;
   no text in any prompt or output.
4. **Self-check each asset** with an image-understanding tool: no text, no
   watermark residue, transparent background, palette matches the declared
   hex values. Regenerate on failure (max 3 rounds), then fall back to
   procedural decorations.
5. **Record the placement map** in `asset_manifest.yaml` (below) next to
   the figure contract.
6. **Composite in R** — AI raster below, R semantics above:

```r
library(png); library(grid); library(ggplot2)
decor <- rasterGrob(readPNG("assets/icon_layer.png"),
                    x = unit(38, "mm"), y = unit(120, "mm"),   # slot centre
                    width = unit(24, "mm"),                    # slot size
                    interpolate = TRUE)
ggplot() + annotation_custom(decor, xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = Inf) +
  # semantics drawn after: geom_segment arrows, geom_text, dashed rects ...
```

   Use `magick::image_composite` when pixel-level blending (shadow over
   gradient) is needed before placement. `patchwork::inset_element` works
   for per-panel asset slots.
7. **Export** with the standard 4-format bundle (svglite / cairo_pdf keep
   the R layer's text as editable vector; AI layers stay raster — state
   raster DPI and the watermark-residue note in the QA report).
8. **QA additions** (on top of `references/figure-qa-contract.md`):
   - text vector check: SVG/PDF text selectable, no rasterised text;
   - watermark check: asset image has no provenance block residue, no
     visible mark/logo;
   - z-order: no AI pixel covers an R semantic element;
   - alignment: each asset sits inside its declared placement slot;
   - palette consistency: AI colours match the declared hex values;
   - policy gate + disclosure line recorded (below).

## asset_manifest.yaml

```yaml
figure: fig3_mechanism
hybrid_mode: true
palette: ["#2F5A72", "#C4622D", "#7A8B52"]
assets:
  - file: assets/icon_layer.png
    prompt_id: openrouter_schematic_20260816_1432   # from request metadata
    content: [gradient background block, droplet icons, soft shadows]
    slot: {panel: c, x_mm: 38, y_mm: 120, w_mm: 24, h_mm: 18}
    dpi: 600
    watermark_status: stripped_provenance_block   # or procedural (no AI), or model_level_residual_only
disclosure: "Decorative elements generated with openai/gpt-image-2 (OpenRouter);
  all text, annotations, and structural lines drawn in R (ggplot2)."
policy_check: {journal: CBM, verified: false, url: null, date: null}
```

The `*_request_metadata.json` written by the generation script is the
provenance record; `asset_manifest.yaml` ties assets to slots.

## Policy and disclosure

- AI decoration in a submitted figure still requires the journal's current
  AI-image policy check (record journal, URL, date) and the disclosure
  line in methods/acknowledgements. Until verified, the package is
  labelled **submission eligibility unverified**.
- The disclosure is stronger than the standalone route's: decorative
  elements AI-generated, all scientific content vector-drawn in R.
- Reviewers may still ask for AI-free versions: keep the R script able to
  render with assets replaced by plain rectangles (`--no-assets` mode in
  the plot script is good practice).

## Failure modes

- Text baked into the AI asset (usually from a sloppy prompt) — regenerate
  the asset; never overlay-correct in image editing.
- Provenance block still present in the asset — re-export as PNG with
  stripping enabled; never ship it into the composite.
- Asset DPI below the R export DPI → visible blur at print size; render
  2K+ or regenerate at target size.
- Gradient colour drift vs palette — constrain hex values in the prompt
  and re-check in QA.
- Asset obscures an annotation — fix the placement map, not the annotation
  position.
