# PPTX Generation Example: WER-EA Journal Club

This example shows how to generate a real `.pptx` deck from a Markdown outline.

## Input

A Markdown file with slide definitions. Each slide uses `## Slide Title` as
header and `- bullet` for content. Speaker notes go in `> blockquote` format.

## Example Markdown Input

```markdown
## 文献信息
- 水性环氧改性乳化沥青界面粘结性能研究
- CBM, 2025
- 与本课题的乳化沥青粘结层方向直接相关

## 研究问题
- 环氧掺量对乳化沥青粘结强度的影响规律
- 湿润条件下的粘结性能衰减机制
- 可借鉴的剂量优化方法

## 材料体系
- 基体：70# 基质沥青乳液
- 改性剂：水性环氧树脂（WER）
- 固化剂：胺类固化剂
```

## Command

```powershell
python plugins/materials-skills/skills/materials-pptx/scripts/build_materials_pptx.py `
  --input journal-club-outline.md `
  --output wer-ea-journal-club.pptx `
  --deck-type journal-club `
  --language zh
```

## Output

A `.pptx` file with:
- 8 slides following the journal-club template
- Speaker notes for each slide
- Placeholder image slots for figures
- Chinese/English bilingual support

## Quality Rules

- Each slide has at most one claim
- Speaker notes explain what to say, not what's on the slide
- Figure references use `[Figure N]` or `[Table N]` format
- No fabricated data — all claims must trace to source evidence
