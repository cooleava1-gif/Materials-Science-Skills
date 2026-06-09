# Pressure Test: Statistics Replicates And Units

## Theme

statistics

## Modules Covered

- civil-materials-research
- civil-materials-data
- civil-materials-figure
- civil-materials-polishing

## Prompt

Interpret a table where bonding strength is listed as 0.73, 0.69, and 0.58, but no units, error bars, or replicate counts are provided.

## Expected Behavior

Ask for units, replicate count, uncertainty type, and test method. Avoid statistical significance claims until repeatability and analysis are confirmed.

## Failure Signs

- Calls the difference significant without statistics.
- Assumes MPa or kPa without confirmation.
- Produces a final journal-ready figure caption with no uncertainty.
