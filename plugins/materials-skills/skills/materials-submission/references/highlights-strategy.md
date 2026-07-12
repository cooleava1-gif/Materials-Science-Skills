# Highlights Strategy

## When to produce

Produce `highlights.md` only when `highlights_required` is true in the
journal-templates yaml. CBM, CCC, and JBE require highlights. RMPD does
not.

## Inputs

- Manuscript abstract (from writing state or manifest).
- Optional key-findings fields from the writing state.

## Generation

The LLM extracts 3-5 highlights from the abstract. Each highlight must be
a single line ≤85 characters.

## Boundary

Do not invent findings absent from the abstract. If the abstract is
missing, the script leaves a placeholder and asks the user to supply an
abstract first.

## Character limit enforcement

`generate_highlights.py` rejects any highlight longer than 85 characters
and asks the LLM to rewrite it. The script exits non-zero if any highlight
exceeds the limit after one rewrite.
