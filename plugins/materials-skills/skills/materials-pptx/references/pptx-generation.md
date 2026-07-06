# PPTX Generation

Use `scripts/build_materials_pptx.py`.

Common commands:

```bash
python scripts/build_materials_pptx.py --title "Waterborne epoxy modified emulsified asphalt" --presenter "种浩然" --output deck.pptx
```

With a Markdown outline:

```bash
python scripts/build_materials_pptx.py --input outline.md --output deck.pptx
```

With a JSON outline:

```bash
python scripts/build_materials_pptx.py --input outline.json --output deck.pptx
```

With a preset:

```bash
python scripts/build_materials_pptx.py --deck-type journal-club --language zh --title "Paper title" --output deck.pptx
```

With one command-line image and crop:

```bash
python scripts/build_materials_pptx.py --title "Bonding performance" --image figure.png --image-slide 5 --crop 4,0,4,8 --output deck.pptx
```

With per-slide images and speaker notes:

```json
{
  "slides": [
    {
      "title": "关键结果",
      "bullets": ["Claim: bonding strength improved", "Evidence: pull-off test"],
      "notes": ["Explain the control group and dosage range.", "Do not overstate durability."],
      "images": [
        {
          "path": "figures/evidence-map.png",
          "alt": "Evidence map figure",
          "crop": {"left": 3, "top": 0, "right": 3, "bottom": 6}
        }
      ]
    }
  ]
}
```

Accepted Markdown shape:

```markdown
## Slide 1 - Title
- Topic
- Presenter

## Slide 2 - Engineering Problem
- Claim
- Evidence
Speaker note:
- Explain what the figure supports.
![Evidence map figure](figures/evidence-map.png)
```

The script is dependency-light and writes Office Open XML directly using Python standard libraries. It supports PNG/JPEG images, source-rectangle cropping, and speaker notes.
