# OpenRouter Image Generation (GPT Image 2 and OpenAI-compatible endpoints)

Provider reference for the AI-schematic route. Adapted from nature-skills
(Apache-2.0). Output is always a **draft**, never a data panel.

## When to use

The user explicitly asks for OpenRouter, GPT Image 2, an image-generation
API, an AI-generated mechanism schematic, graphical abstract, concept
illustration, or 示意图/图形摘要/机制图（AI 生成）. Planning- or audit-only
requests read [ai-schematic-workflow.md](ai-schematic-workflow.md) and do not
call the API at all.

## Setup

- API key: `OPENROUTER_API_KEY` environment variable (default
  `--api-key-env`; change for other providers).
- Model: `openai/gpt-image-2` by default, override with `--model` or
  `OPENROUTER_IMAGE_MODEL`.
- Any OpenAI-compatible images endpoint works via `--api-url` (default
  `https://openrouter.ai/api/v1/images`).
- Optional attribution headers: `OPENROUTER_SITE_URL`,
  `OPENROUTER_APP_NAME`.

## Running

```bash
# Compose and review the payload first — no key needed:
python scripts/generate_openrouter_schematic.py \
  --title "Waterborne epoxy modified emulsified asphalt" \
  --abstract-file abstract.txt \
  --panel-map "1) emulsified asphalt droplets + epoxy resin -> 2) co-curing interface -> 3) crosslinked network bonding aggregate" \
  --dry-run

# Real call:
python scripts/generate_openrouter_schematic.py \
  --title "Waterborne epoxy modified emulsified asphalt" \
  --abstract-file abstract.txt --panel-map "..." \
  --outdir ai_schematic --basename mechanism_draft_v1
```

Inputs: `--title`, `--abstract`/`--abstract-file`, `--panel-map`,
`--prompt`/`--prompt-file`, `--style`, `--raw`, `--reference-image` (path /
URL / data URL for image-to-image guidance), geometry options
(`--aspect-ratio 16:9`, `--resolution 2K`, `--quality high`,
`--output-format png`, `--background`, `--n`).

Outputs land in `--outdir` (default `ai_schematic/`): the image plus
`<basename>_request_metadata.json` holding the full request payload,
response usage, and saved-file list — the provenance record the AI-schematic
workflow requires.

## Hard rules

- No invented quantitative values, fake micrographs or spectra, p-values,
  institutional logos, journal marks, or unsupported mechanisms — the
  script's scaffold enforces this wording into every composed prompt;
  `--raw` bypasses the scaffold and is the caller's responsibility.
- Treat outputs as internal drafts until the journal policy gate clears
  them; add the disclosure line when submitting.
- Never route measured data through the image API; plotting goes through the
  backend gate.
- Costs and rate limits are the caller's; `--n` and `--quality` multiply
  cost.
