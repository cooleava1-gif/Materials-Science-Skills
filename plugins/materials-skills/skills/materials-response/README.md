# materials-response

**Version:** 1.2.0

**What it does** — Drafts point-by-point reviewer replies after the comments
arrive, keeping the response letter tied to actual manuscript changes instead
of vague promises. It separates response tone from manuscript action, maps
each comment to a concrete action, and prevents unsupported promises or
fabricated experiments. Feed it the reviewer comments or editor decision
letter, the current revision notes, and the figure/data/text changes that can
prove what was fixed; name the target journal when relevant. The deliverable
is a response package, rebuttal letter, revision summary, or resubmission
note set for a materials manuscript.

**Built from** — A response-strategy system with tone, pattern, and language
layers:

- `references/response-strategy.md` — point-by-point strategy and structure
- `references/response-patterns.md` — high-frequency comment patterns
  (language, references, novelty, sample size, error bars, conflicting
  reviewers)
- `references/reviewer-strategy-library.md` — strategic responses for complex
  reviewer challenges (novelty, method, scope, conflicting reviewers)
- `references/experiment-remediation-plans.md` — concrete experiment proposals
  for mechanism, performance, statistical, and characterization evidence
- `references/reviewer-comment-patterns.md` — common reviewer comment patterns
  with underlying concerns and response strategies
- `references/experiment-revision.md` — mechanism/performance revision plans
- `references/response-document-format.md` — author response, tracked
  changes, cover letter format
- `references/language-bank.md` — rebuttal tone and phrasing
- `references/response-risk-checklist.md` — reject / major-revision risk
- `static/fragments/tone/` — academic and firm tone fragments
- `static/fragments/domain/` — 6 material-domain routing fragments
- `assets/templates/` — response-package and response-table templates
- `scripts/build_response_package.py` — assembles the response package
- `tests/pressure-tests/` — 10 difficult-case regressions

**Key rules enforced**

- Preserve the reviewer comment verbatim; never paraphrase it away.
- Answer every comment or mark it `unresolved` — no silent drops.
- Map each comment to an action (see below); never leave a reply actionless.
- Never invent experiments, supplementary figures, citations, or line
  numbers; proof-of-change must point at real revisions.
- Responses must stand alone without the reviewer re-reading the manuscript.
- Separate tone management from technical repair; a firm reply still needs a
  real fix or an honest scope boundary.
- Use experiment remediation plans for concrete, actionable experiment proposals.
- Apply reviewer strategy library for complex or challenging reviewer comments.
- Recognize common comment patterns to prepare appropriate responses.

**Action mapping** — Each reviewer comment is mapped to one of:

| Action | Meaning |
|---|---|
| `ACCEPT_TEXT` | Accept the wording change; quote the revised text. |
| `ACCEPT_ANALYSIS` | Accept the analysis/method change; cite the new result. |
| `SOFTEN_CLAIM` | Narrow the claim to match the evidence. |
| `DISAGREE` | Decline with evidence and a scope boundary. |
| `AUTHOR_INPUT_NEEDED` | Flag unresolved; needs author decision or new work. |

**What it returns** — A point-by-point response with stable comment IDs,
proof-of-change language keyed to revision locations, a routed weakness list
for writing / figure / data / reader fixes, and a cleaner split between tone
management and technical repair.

**Enhanced capabilities (v1.2.0)**

- **Reviewer Strategy Library**: Strategic responses for novelty challenges,
  method justification, scope boundaries, conflicting reviewers, data
  reproducibility, and ethics concerns.
- **Experiment Remediation Plans**: Concrete experiment proposals for FTIR,
  SEM, XRD, TG/DTG, mechanical testing, durability testing, bonding/adhesion
  testing, rheological testing, replicate testing, DOE, particle size
  distribution, BET, and spectroscopic characterization. Includes decision
  framework and response templates.
- **Reviewer Comment Patterns**: Common patterns for novelty, method, writing,
  scope, and domain-specific concerns. Each pattern includes typical wording,
  underlying concern, and response strategy.

**Reference files**

```text
skills/materials-response/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   └── build_response_package.py        assembles point-by-point response package
├── assets/
│   └── templates/
│       ├── response-package-template.md response letter scaffold
│       └── response-table-template.csv  point-by-point table scaffold
├── static/
│   ├── core/                            contract, response-contract, workflow
│   └── fragments/
│       ├── domain/                      6 material-domain routing fragments
│       └── tone/                        academic and firm tone fragments
└── references/
    ├── response-strategy.md             point-by-point strategy and structure
    ├── response-patterns.md             high-frequency comment patterns
    ├── reviewer-strategy-library.md     strategic responses for complex challenges
    ├── experiment-remediation-plans.md  concrete experiment proposals
    ├── reviewer-comment-patterns.md     common comment patterns with strategies
    ├── experiment-revision.md           mechanism/performance revision plans
    ├── response-document-format.md      author response, tracked changes format
    ├── language-bank.md                 rebuttal tone and phrasing
    └── response-risk-checklist.md       reject / major-revision risk
```

**Validation**

- Core regression test:
  `plugins/materials-skills/skills/materials-response/tests/test_response_examples.py`
- Pressure tests:
  `plugins/materials-skills/skills/materials-response/tests/pressure-tests/`
  (10 difficult-case regressions including
  `aggressive-reviewer-mechanism-request.md`)
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## When To Use

Use `materials-response` when the user request matches this skill's production surface and the needed inputs are available or can be explicitly marked as missing.

## Inputs

Typical inputs are the user prompt, material direction/profile, target journal or task mode when relevant, and any source text, data, figures, reviewer comments, or package artifacts needed by the skill.

## Outputs

Outputs are structured handoffs or artifacts described above in this README. Missing evidence, author input needs, and unsupported claims stay visible instead of being hidden in fluent prose.

## Example

```text
Draft point-by-point replies from reviewer comments and action notes.
```

## Validation

Run the skill-specific scripts or tests listed above when they apply, then run the bundle gate from the repository root:

```powershell
python .\scripts\run_release_checks.py --json
```

## Boundaries

This skill does not invent experiments, citations, measurements, journal facts, private file paths, or completed actions. Time-sensitive journal or legal facts should be checked against official sources before submission or filing.
