# Pressure test: Thermal insulation — ignoring moisture effect on conductivity

## Theme

missing experimental conditions

## Modules Covered

- materials-research
- materials-data
- materials-figure

## Prompt
An insulation paper claims: "The aerogel maintains lambda = 0.028 W/(m.K)." All measurements were done under dry conditions at 25 C. The paper targets building insulation applications.

## Expected Behavior
- Flag that in-service humidity will increase conductivity.
- Recommend reporting conductivity at relevant RH levels (50%, 80%).
- Suggest hygrothermal aging test if long-term performance is claimed.
- Note that dry-room-temperature data alone is insufficient for building applications.

## Failure Signs
- Accepting dry-only data as sufficient for building claims.
- Not flagging the humidity gap.
