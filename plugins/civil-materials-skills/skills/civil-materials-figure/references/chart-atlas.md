# Civil Materials Chart Atlas

Use this atlas when choosing a production figure family before coding. Each chart type links a civil-materials claim to a safe code pattern.

| Chart family | Best use | Code pattern | Reviewer risk |
|---|---|---|---|
| bonding strength grouped bar | Control vs. modified tack coat under dry/wet states | `make_grouped_bar()` with SD bars | Missing replicate count or test condition |
| dosage-performance curve | Optimization trend across epoxy dosage | `make_line_trend()` with highlighted candidate range | Calling one dosage "optimal" without durability |
| FTIR overlay | curing or chemical-change evidence | `make_ftir_overlay()` with peak labels | Claiming full mechanism from FTIR alone |
| XRD stacked pattern | hydration or crystalline phase comparison | `make_xrd_pattern()` with offset traces | Unassigned peaks or no baseline correction |
| durability retention bar | Moisture, aging, freeze-thaw screening | grouped retention bars with raw baseline noted | Retention without original strength values |
| mechanical radar | Multi-index comparison for screening | `make_radar()` on normalized indices | Hiding weak raw indicators |
| SEM/fluorescence plate | morphology and phase distribution | assembled panel with scale bar | Representative image without field count |
| TG/DTG paired plot | thermal stability and decomposition | aligned mass-loss and derivative axes | Overinterpreting small peak shifts |
| box/violin plot | replicate-rich performance datasets | raw points plus distribution shape | Using distribution plots for n < 5 |
| mechanism schematic | Evidence-chain summary | solid/dashed arrows by evidence confidence | Drawing unsupported causal links |

Start with the claim, then choose the chart. Do not start with the prettiest chart and retrofit a claim.
