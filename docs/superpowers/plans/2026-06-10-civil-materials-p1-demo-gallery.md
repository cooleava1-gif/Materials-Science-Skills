# Civil Materials P1 Demo And Gallery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the new productized entry surface into a stronger first-use experience by adding clickable workflow demos and a screenshot-driven gallery around the existing WER-EA, reader-package, and PPT handoff assets.

**Architecture:** Keep the new root README and install guide as the front door, then add two supporting document layers: `docs/workflows/` for guided demo routes and `docs/gallery/` for visual proof. Lock both with product contract tests and release-check markers so the showcase stays aligned with the repo's real assets.

**Tech Stack:** Markdown, Python `unittest`, existing release-check scripts

---

### Task 1: Add Failing Workflow And Gallery Contract Tests

**Files:**
- Modify: `tests/test_product_docs_contract.py`

- [ ] **Step 1: Write failing workflow demo assertions**

```python
for slug in ["wer-ea-mini-review", "experimental-manuscript", "revision-loop", "paper-to-presentation"]:
    self.assertTrue((ROOT / "docs" / "workflows" / f"{slug}.md").is_file())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: FAIL because `docs/workflows/` and `docs/gallery/` do not exist yet.

- [ ] **Step 3: Add gallery-level assertions**

```python
self.assertIn("## Screenshot Gallery", gallery_text)
self.assertIn("wer_ea_mechanism_map.png", gallery_text)
```

- [ ] **Step 4: Re-run the same test target**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: FAIL only on missing workflow/gallery docs, not on syntax or imports.

- [ ] **Step 5: Commit**

```bash
git add tests/test_product_docs_contract.py
git commit -m "test: require workflow demos and gallery docs"
```

### Task 2: Create Workflow Demo Documents

**Files:**
- Create: `docs/workflows/README.md`
- Create: `docs/workflows/wer-ea-mini-review.md`
- Create: `docs/workflows/experimental-manuscript.md`
- Create: `docs/workflows/revision-loop.md`
- Create: `docs/workflows/paper-to-presentation.md`

- [ ] **Step 1: Add a workflow hub**

```markdown
## Workflow Index

1. WER-EA mini-review
2. Experimental manuscript
3. Revision loop
4. Paper to presentation
```

- [ ] **Step 2: Give each route one consistent structure**

```markdown
## Route Summary
## Demo Prompt
## Workflow Steps
## Expected Artifacts
## What Good Looks Like
```

- [ ] **Step 3: Make the content concrete**

```markdown
Step 1: Start with `civil-materials-research` and route by `paper_stage=screening`.
```

- [ ] **Step 4: Re-run the product docs contract test**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: workflow assertions pass; gallery assertions may still fail.

- [ ] **Step 5: Commit**

```bash
git add docs/workflows
git commit -m "docs: add guided workflow demos"
```

### Task 3: Create The Screenshot-Driven Gallery

**Files:**
- Create: `docs/gallery/README.md`
- Modify: `README.md`
- Modify: `install.md`

- [ ] **Step 1: Build a gallery page from real assets**

```markdown
## Screenshot Gallery
## Workflow Proof
## Artifact Deep Dives
```

- [ ] **Step 2: Link gallery and workflow docs from the front door**

```markdown
## Guided Demos
## Visual Gallery
```

- [ ] **Step 3: Use real repo assets, not placeholders**

```markdown
![WER-EA mechanism map](../skills/civil-materials-figure/assets/wer-ea-atlas/generated/wer_ea_mechanism_map.png)
```

- [ ] **Step 4: Re-run the product docs contract test**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add README.md install.md docs/gallery/README.md
git commit -m "docs: add gallery-driven entry experience"
```

### Task 4: Extend Release Checks And Final Verification

**Files:**
- Modify: `scripts/run_release_checks.py`

- [ ] **Step 1: Add release markers for workflow and gallery docs**

```python
if "## Guided Demos" not in readme_text:
    issues["skills_index"].append("README.md missing guided demos section")
```

- [ ] **Step 2: Re-run targeted tests**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: PASS

- [ ] **Step 3: Reinstall and run release checks**

Run: `.\scripts\install.ps1`
Expected: installed skill directories refreshed.

- [ ] **Step 4: Run full verification**

Run: `python .\scripts\run_release_checks.py --json`
Expected: top-level final JSON `status` is `pass`.

- [ ] **Step 5: Commit**

```bash
git add scripts/run_release_checks.py
git commit -m "test: lock workflow demos and gallery release surface"
```
