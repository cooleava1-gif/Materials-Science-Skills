# Skills Index

This index lists all 14 installable `materials-*` skills.

| Skill | Primary role | Typical handoff |
|---|---|---|
| `materials-research` | Router and paper-production orchestrator | All companion skills |
| `materials-reader` | Source-grounded reader package | citation, writing, figure |
| `materials-citation` | Search strategy and citation matrix | reader, writing |
| `materials-literature-pipeline` | Recurring discovery and source-depth triage | research, reader, citation |
| `materials-writing` | Stateful manuscript sections and argument chains | polishing, reviewer |
| `materials-polishing` | Claim-strength and language tightening | reviewer, response |
| `materials-figure` | Figure contracts and publication plots | writing, data |
| `materials-data` | FAIR dataset package | writing, figure |
| `materials-doe` | Experiment design matrices | data, writing |
| `materials-reviewer` | Simulated peer review and risk report | response, writing |
| `materials-response` | Point-by-point rebuttal package | writing, polishing |
| `materials-html-deck` | Slide-ready outline and verified HTML academic deck | figure |
| `materials-paper-to-patent` | Chinese invention-patent draft | figure, data |
| `materials-submission` | Route C assembly for 10 supported journal templates | research, writing, figure, data |

The bundle uses profile-first routing from `.materials/profile.yaml` when the
user has saved a local materials direction. That file is user-local and must
not be committed.
