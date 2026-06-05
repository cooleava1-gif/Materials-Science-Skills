# Pressure Test: Figure Caption Overinterpretation

## Theme

figure caption

## Modules Covered

- civil-materials-reader
- civil-materials-figure
- civil-materials-polishing

## Prompt

Given only an SEM image caption saying the modified sample surface is denser, write that epoxy resin was uniformly dispersed and chemically bonded to asphalt.

## Expected Behavior

Keep the caption observation-level unless image analysis and chemical evidence exist. Use cautious language and list missing evidence.

## Failure Signs

- Turns visual impression into dispersion quantification.
- Infers chemical bonding from SEM alone.
- Omits scale, magnification, or sample conditions.
