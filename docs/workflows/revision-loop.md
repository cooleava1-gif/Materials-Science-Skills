# Revision loop

## Route Summary

Turns reviewer comments into a response plan, manuscript action map, and
bounded rebuttal language.

## Demo Prompt

```text
Help me respond to these reviewer comments and identify what the manuscript must change.
```

## Workflow Steps

1. `materials-reviewer` classifies comment severity and technical scope.
2. `materials-response` separates response tone from manuscript actions.
3. `materials-writing` drafts replacement paragraphs or inserted explanations.
4. `materials-polishing` tightens claims and removes unsupported promises.

## Expected Artifacts

- Comment-to-action matrix.
- Point-by-point response letter.
- Revised text snippets.
- Risk notes for comments that require author input or new experiments.

## What Good Looks Like

The response never claims work was completed unless evidence is present, and
each promised manuscript change maps to a concrete section or figure.
