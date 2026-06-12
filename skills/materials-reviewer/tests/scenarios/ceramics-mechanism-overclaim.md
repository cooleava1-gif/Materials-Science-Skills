# Test: Ceramics — mechanism overclaim from limited characterization

## Skill
materials-reviewer

## Input
A ceramics manuscript claims: "The addition of Y2O3 stabilizes the tetragonal phase of ZrO2, enhancing the fracture toughness through transformation toughening." The only characterization is XRD showing tetragonal/monoclinic ratio. No fracture toughness data (no SENB, SEVNB, or indentation) are reported. The paper targets JACerS.

## Expected Behavior
- Note that transformation toughening requires fracture toughness evidence, not just phase ratio.
- Flag missing fracture toughness testing as a major gap.
- Distinguish the phase composition evidence from the mechanism claim.
- Assess journal fit (JACerS expects clear processing-structure-property linkage).

## Forbidden Behavior
- Accepting the mechanism claim based on XRD alone.
- Not flagging the missing mechanical testing.
- Recommending acceptance without addressing the evidence gap.

## Checklist
- [ ] Mechanism claim flagged as unsupported.
- [ ] Fracture toughness testing recommended.
- [ ] Phase ratio vs mechanical property distinction made.
- [ ] Journal fit assessed.
