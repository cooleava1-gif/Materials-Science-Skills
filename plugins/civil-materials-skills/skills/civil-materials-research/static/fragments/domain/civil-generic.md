# Domain: Civil Materials Generic

Use this when the user has not specified a material family.

Ask or infer:

- Material system.
- Engineering use case.
- Main performance target.
- Available evidence.
- Target output.

If the user mentions asphalt, cement, concrete, durability, low carbon, or a target journal, switch to the more specific fragment.

## Broader Civil-Materials Triage

When the topic is outside asphalt and cement/concrete, keep the answer useful but explicit about evidence limits.

| Subdomain | Typical material systems | Evidence to request first | Reviewer-risk boundary |
|---|---|---|---|
| steel and metallic structures | steel corrosion protection, weld repair, coatings, FRP-steel bonding | corrosion environment, surface preparation, adhesion, fatigue, electrochemical data | Do not infer long-term corrosion resistance from short immersion tests alone. |
| geotechnical and rock-soil materials | stabilized soil, cement-treated soil, expansive soil, rock reinforcement, grouting | gradation, Atterberg limits, compaction, UCS/CBR, wet-dry/freeze-thaw, curing | Do not transfer concrete hydration logic directly to soil without mineralogy and water-content context. |
| timber and bio-based materials | engineered wood, bamboo, timber adhesive, moisture protection | species, density, moisture content, adhesive system, bending/shear, fungal/aging exposure | Do not claim durability without humidity, biological, or weathering evidence. |
| masonry and repair materials | brick, block, mortar repair, tile adhesive, heritage repair | substrate condition, bond strength, compatibility, shrinkage, salt/freeze exposure | Do not discuss repair compatibility without substrate and exposure details. |
| waterproofing and sealants | membranes, coatings, sealants, polymer-modified repair layers | tensile/tear strength, elongation, adhesion, water pressure, aging, UV/thermal cycling | Do not call a system field-ready without installation and aging constraints. |

## Output Rule

If a non-asphalt/non-concrete topic appears, state:

`Domain note: this bundle has strongest built-in depth for asphalt and cement/concrete. For [subdomain], use the generic evidence contract and request standards, exposure condition, substrate/specimen details, and durability data before making strong claims.`

Then produce the requested output using the same claim-evidence-mechanism-boundary logic.
