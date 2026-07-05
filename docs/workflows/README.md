# Workflow Demos

Concrete entry routes for the Materials Science Skills bundle. Each route
starts with a user prompt, then names the companion skills and artifacts that
should appear.

## Workflow Index

| Workflow | Best use | Route |
|---|---|---|
| [WER-EA mini-review](wer-ea-mini-review.md) | Review planning for waterborne epoxy asphalt | research -> citation -> reader -> writing -> figure |
| [Experimental manuscript](experimental-manuscript.md) | Evidence-gap audit before discussion drafting | research -> data -> figure -> writing -> reviewer |
| [Experimental pipeline](experimental-pipeline.md) | Closed DOE -> record -> data -> figure loop | doe -> data -> figure |
| [Revision loop](revision-loop.md) | Reviewer comments and rebuttal planning | reviewer -> response -> writing -> polishing |
| [Paper to presentation](paper-to-presentation.md) | Journal-club outline and deck creation | paper2ppt -> pptx |
| [Ceramics Sintering Manuscript](ceramics-sintering-manuscript.md) | YSZ sintering experiment to JACerS submission pipeline | doe -> data -> citation -> reader -> writing -> figure -> reviewer -> response |

Run `python .\scripts\run_release_checks.py --json` after changing skill or
documentation files. The public GitHub package does not ship the internal
Python regression suite.
