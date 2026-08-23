# Hybrid mechanism figure

## Outcome Snapshot

A publication-grade conceptual/schematic figure produced by the default R
hybrid route: an AI image model supplies watermark-free decoration assets
only, while R draws every text, border, arrow, and annotation as editable
vector.

## Demo Prompt

```text
Create a mechanism schematic for WER-EA interface bonding using the R hybrid route.
```

## Proof Assets

- `docs/gallery/gallery_wer_ea_workflow.png`

## Build Path

1. `materials-figure` writes and validates the figure contract first.
2. R drafts the layout with placeholder rectangles for asset slots.
3. The AI model generates transparent, watermark-stripped decoration assets
   (no text/arrows/borders by construction).
4. R composites the assets below and draws all semantic elements above.
5. QA checks text-vector selectability, watermark absence, z-order, and
   palette consistency; the package carries the hybrid disclosure line.

## When To Use This Route

Use it for mechanism maps, interface schematics, graphical abstracts, and TOC
graphics where editable vector text and a clean watermark story matter. If no
AI tool is available, fall back to full R/Python procedural decorations.
