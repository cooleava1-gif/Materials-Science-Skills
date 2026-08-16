# Output Format

Unless the user asks otherwise, return:

```text
Statistics review scope
- Input reviewed:
- Boundary / missing materials:
- Study design readout:
- Independent unit and replication readout:

Major statistical issues
- [P0/P1/P2] Issue:
  Evidence from supplied text:
  Why it matters:
  Fix:

Ready-to-paste revision
[Rewritten Statistical analysis / Results / figure legend text]

AUTHOR_INPUT_NEEDED
- [short factual questions only]

Reviewer-risk note
- What a statistical reviewer may still challenge:
```

For a clean drafting request with sufficient information, skip the issue list
and return:

```text
Draft Statistical analysis
[ready-to-paste text]

Reporting notes
- n definition:
- tests/models:
- multiple comparisons:
- software/version:
- unresolved fields:
```
