# Submission Package Output Format

The submission package is a directory, not a single file.

## Directory shape

```text
submission-package/
  MANIFEST.md
  cover-letter.md
  highlights.md
  keywords.md              # when required by the article route
  declarations.md          # when required by the article route
  submission-checklist.md
  manuscript/SOURCE.md
  figures/SOURCE.md
  data/SOURCE.md
  reviewer-risk-regression.md
```

## MANIFEST.md

Lists every artifact in the package with its source path, status, and
live-verification flag. One row per artifact.

## Placeholder convention

- `[LLM: ...]` marks paragraphs the LLM must fill from prepared inputs.
- `[LIVE-VERIFICATION: ...]` marks fields the user must re-check against
  the current Guide for Authors before submission.

## Dry-run output

`--dry-run` prints the intended `MANIFEST.md` and the list of files that
would be written, without creating the directory.
