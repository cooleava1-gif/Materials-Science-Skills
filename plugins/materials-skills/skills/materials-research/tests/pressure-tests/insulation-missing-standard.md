# Pressure test: Thermal insulation — reporting conductivity without standard or temperature

## Prompt
An aerogel insulation sample has thermal conductivity of 0.028 W/(m.K). The user says this was measured "at room temperature" with a "thermal conductivity tester." Draft the Methods section.

## Expected Behavior
- Flag that the measurement standard (ASTM C518, ISO 8301, etc.) is missing.
- Flag that mean temperature is not reported.
- Ask whether the sample was conditioned at a specific humidity.
- Recommend reporting all three: standard, mean temperature, specimen conditioning.

## Failure Signs
- Accepting "room temperature" as adequate.
- Not asking for the test standard.
- Reporting conductivity without questioning measurement conditions.
