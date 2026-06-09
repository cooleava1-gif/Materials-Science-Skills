# PPTX Handoff

Use this when the user wants an actual PowerPoint file.

## Handoff Logic

1. Build the story arc with `civil-materials-paper2ppt`.
2. Keep each slide as `## Slide N - Title`.
3. Use 3-5 bullets per slide.
4. Make the first bullet the slide message.
5. Make the second bullet the evidence source.
6. Pass the Markdown outline to `civil-materials-pptx`.

## Script Route

Run `scripts/build_ppt_markdown.py --pptx-output deck.pptx` for a fast scaffold.

Use `civil-materials-pptx` for customized deck types, JSON input, or final PowerPoint generation.
