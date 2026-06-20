# Paper to presentation

## Route Summary

Converts a paper package or reader notes into a journal-club slide outline and
then a real `.pptx` deck.

## Demo Prompt

```text
Turn this paper package into a journal-club slide outline and then a real PPTX.
```

## Workflow Steps

1. `materials-paper2ppt` extracts story arc, slide titles, and speaker notes.
2. `materials-figure` supplies figure-placement or redrawing guidance when needed.
3. `materials-pptx` renders the structured slide spec into a `.pptx` file.

## Expected Artifacts

- Slide-ready Markdown or JSON slide spec.
- Figure placement notes.
- Real PowerPoint deck with notes.

## What Good Looks Like

The deck follows the paper's evidence chain, keeps slide claims short, and
separates author results from the presenter's interpretation.
