# Test: Paragraph flow regression — one paragraph, one message

## Skill

materials-writing

## Input

The user asks: "Fix the flow of this results/discussion paragraph."

The user provides:

> The bonding strength of WER-EA tack coat increased from 0.43 MPa to 0.55 MPa at 10% epoxy content. This improvement is due to the oxirane groups reacting with the asphalt interface, forming a more continuous interfacial morphology that improves load transfer. The moisture conditioning retained 75% of the dry strength. Storage stability was acceptable for 7 days.

## Expected behavior

- Identify that the original paragraph carries multiple messages (result, mechanism, durability, storage stability).
- Split the paragraph so each new paragraph carries one message only.
- Ensure the first sentence of each paragraph forecasts its message.
- Add transitions that carry the argument forward, not just the topic.
- Preserve the evidence strength: do not upgrade "due to" to a mechanism claim without cross-validating evidence.
- Return the revised draft plus a section outline showing the paragraph-message map.

Example of an acceptable revision:

> **Result**: The bonding strength of WER-EA tack coat increased from 0.43 MPa to 0.55 MPa at 10% epoxy content under dry conditions at 25 °C.
>
> **Mechanism interpretation**: This strength increase is consistent with a more continuous interfacial morphology. FTIR shows the oxirane peak at 915 cm⁻¹ decreases with curing time, and SEM images show fewer voids at the interface at 10% epoxy than in the control.
>
> **Durability**: After moisture conditioning, the 10% epoxy formulation retained 75% of its dry bonding strength, indicating that the improved interface is partially preserved under wet conditions.
>
> **Workability boundary**: Storage stability remained acceptable for 7 days, suggesting that the 10% epoxy content does not compromise short-term constructability.

## Forbidden behavior

- Do not leave the multi-message paragraph intact.
- Do not split paragraphs so that a single paragraph still mixes result and mechanism.
- Do not add transitions that merely repeat the topic without advancing the argument.
- Do not invent additional characterization data (e.g., new FTIR peaks, SEM descriptions not in the record).

## Pass/fail checklist

- [ ] The original multi-message paragraph is split into single-message paragraphs.
- [ ] Each paragraph's first sentence forecasts its message.
- [ ] Transitions advance the argument rather than just continuing the topic.
- [ ] The paragraph-message map is shown in the section outline.
- [ ] No fabricated evidence is introduced.
