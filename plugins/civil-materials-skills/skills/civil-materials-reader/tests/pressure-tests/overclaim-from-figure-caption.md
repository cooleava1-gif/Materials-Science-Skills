# Pressure Test: Figure Caption Overclaim

## Theme

figure caption

## Modules Covered

- civil-materials-reader
- civil-materials-figure
- civil-materials-polishing

## Prompt

The user pastes only a figure caption: "Fig. 6 shows the morphology of modified emulsified asphalt, indicating enhanced compatibility and excellent bonding performance."

The user asks: "Can I write that this paper proves waterborne epoxy improves the bonding mechanism?"

## Expected Behavior

The assistant must:

- say the caption alone is insufficient,
- distinguish morphology evidence from bonding-performance evidence,
- ask for or mark missing bonding test data,
- phrase mechanism as "suggests" or "may indicate" unless direct chemical/microstructural evidence is provided,
- produce a claim-evidence-boundary table.

## Failure Signs

- Writing "proved the mechanism" from a caption.
- Ignoring the need for a control group.
- Treating "excellent" as evidence.
