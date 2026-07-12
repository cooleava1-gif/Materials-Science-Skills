# Submission Package Protocol

## Assembly steps

1. Read `submission-manifest.yaml`.
2. Check refusal conditions. If any fail, emit a dry-run manifest and stop.
3. Load journal-formats fact sheet and journal-templates yaml.
4. If `writing_state_path` is set, read `state.json` and pre-fill title,
   abstract, authors, keywords.
5. If `figure_package_path` is set, read the figure package manifest.
6. If `fair_package_path` is set, read the FAIR package manifest.
7. If `weakness_routing_path` is set, read the weakness-routing CSV.
8. Create `submission-package/`.
9. Write `MANIFEST.md`.
10. Call `generate_cover_letter.py` to produce `cover-letter.md`.
11. If `highlights_required` is true, call `generate_highlights.py` to
    produce `highlights.md`.
12. Write `keywords.md` from manifest or writing state.
13. Write `declarations.md` from manifest fields plus live-verification
    placeholders.
14. Call `generate_checklist.py` to produce `submission-checklist.md`.
15. Write `manuscript/SOURCE.md`, `figures/SOURCE.md`, `data/SOURCE.md`.
16. Write `reviewer-risk-regression.md` from weakness-routing rows.

## Dry-run mode

`--dry-run` prints the intended `MANIFEST.md` and the list of files that
would be written, without creating the directory.

## Source tracing

`SOURCE.md` stubs record the source path and status of each artifact. The
package never copies manuscript text, figures, or data. This keeps the
package traceable and avoids stale content.
