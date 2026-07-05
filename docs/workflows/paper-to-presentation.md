# Paper to presentation

## Route Summary

Converts a paper package or reader notes into a journal-club outline and
then a verified browser-native HTML academic deck.

## Demo Prompt

```text
Turn this paper package into a journal-club outline and verified HTML academic deck.
```

## Workflow Steps

1. `materials-html-deck` extracts the story arc, slide titles, and speaker notes.
2. `materials-figure` supplies figure-placement or redrawing guidance when needed.
3. `materials-html-deck` renders the structured slide spec into retained HTML slides and runs strict Playwright verification.

## Expected Artifacts

- Slide-ready Markdown or JSON slide spec.
- Figure placement notes.
- Retained HTML deck directory with screenshots, speaker notes, QA report, and asset manifest.

## What Good Looks Like

The deck follows the paper's evidence chain, keeps slide claims short, and
separates author results from the presenter's interpretation.
