# Pressure Test: Defensive Draft Audit

## Theme

reviewer response

## Modules Covered

- materials-response
- materials-polishing
- materials-reviewer

## Prompt

Mode requested: audit and revise this draft response.

Reviewer 1:

1. The SEM analysis is superficial. The authors should provide quantitative porosity measurements from image analysis.
2. The discussion section does not compare results with Ref. [15] (Zhang et al., 2019), which studied the same material system.

Author draft:

We respectfully disagree with the reviewer. The SEM analysis in our paper is comprehensive and provides clear evidence of the microstructure. We have already included 6 SEM images at different magnifications.

Regarding Ref. [15], we believe our paper is sufficiently novel and does not need to compare with every published study. We have added a brief mention in the discussion.

Author notes:

- We do not have porosity measurement software.
- We do have Zhang et al. 2019 data but have not compared it systematically.
- The current SEM images are qualitative only.

## Expected Behavior

- Detect task mode as `audit` or `revise`.
- Assign stable IDs `R1.1` and `R1.2`.
- Flag "We respectfully disagree" and "comprehensive" as defensive.
- Flag "does not need to compare with every published study" as dismissive.
- Rewrite R1.1 response to acknowledge SEM is qualitative, offer image analysis as future work or mark `AUTHOR_INPUT_NEEDED`, and soften the claim to "microstructure observation" rather than "comprehensive analysis".
- Rewrite R1.2 response to accept the comparison with Zhang et al. 2019 as valid, offer a systematic comparison table or paragraph, and use the author's existing data.
- Preserve author notes about software unavailability.

## Failure Signs

- Retaining "We respectfully disagree with the reviewer."
- Retaining "comprehensive and provides clear evidence."
- Retaining "does not need to compare with every published study."
- Inventing porosity measurement results.
- Removing the Zhang et al. 2019 comparison request.
- Claiming the existing SEM analysis is quantitative when it is not.
