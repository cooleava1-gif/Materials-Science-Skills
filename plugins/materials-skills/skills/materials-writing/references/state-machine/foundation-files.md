# Foundation Files

Use foundation files only when a writing task needs continuity across drafting,
revision, or QA rounds. They are project artifacts, not active state in this
skill package.

## Expected Project Files

| File | Role |
|---|---|
| `00_scope.md` | Task, audience, material system, deliverable, and boundaries. |
| `01_research_canon.md` | Facts, terminology, forbidden claims, and open decisions. |
| `02_evidence_table.md` | Claims, sources, evidence strength, section use, risk, and status. |
| `03_argument_map.md` | Scientific tension, research question, one-sentence argument, and rivals. |
| `04_section_contracts.md` | Required, allowed, and forbidden claims for each target section. |
| `05_style_guide.md` | Terminology, claim strength, and reviewer-safe language rules. |
| `state.json` | Writing mode, round, scores, debts, stop status, and artifacts. |

Before drafting or QA, check only the files relevant to the requested mode.
If they are missing, report the gap or return a state patch for the user's
project. Do not silently invent project state.
