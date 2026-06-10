# Paper to presentation

## Route Summary

Use this route when the main deliverable is a talk rather than a paper draft.
The goal is to preserve the evidence structure of the paper while converting it
into a clear speaking sequence and, if needed, a real PowerPoint file.

## Demo Prompt

```text
Turn this paper package into a journal-club slide outline and then a real PPTX.
```

## Workflow Steps

1. Start with `civil-materials-paper2ppt` to decide the audience, slide count,
   talk arc, and which figures or results deserve space.
2. Build a slide-ready Markdown or JSON outline instead of writing a loose
   narrative.
3. If figure selection is messy, borrow the relevant artifacts from the reader
   or figure workflows first, then finalize the slide order.
4. Use `civil-materials-pptx` to generate the actual `.pptx` file with notes
   and image placement.
5. If the talk is for a group meeting or thesis report, loop back once to make
   sure the deck still matches the paper's evidence boundaries.

## Expected Artifacts

- slide-ready Markdown outline
- selected figure list and narrative pacing
- real `.pptx` deck when generation is requested
- a talk structure that stays consistent with the underlying paper package

## What Good Looks Like

- each slide has a clear speaking job instead of a wall of text
- the talk preserves the paper's evidence hierarchy
- figure-heavy slides still state what is measured versus inferred
- the final deck can be presented directly or lightly polished
- the PPT path does not fabricate missing data just to fill slides
