# Characterization Figure Templates

Use this reference when a figure involves XRD, TG/DTG, FTIR, SEM/TEM, fluorescence microscopy, rheology, or uncertainty visualization.

## XRD Overlay

Best use: crystalline phase comparison, hydration products, mineral fillers, cementitious phases, or asphalt filler interactions.

Required data:

- `two_theta`
- intensity per sample
- baseline/normalization method
- reference phase markers and source

Caption boundary:

> XRD patterns indicate the presence or relative change of assigned crystalline phases under the tested preparation condition.

Reviewer risk:

- Do not infer chemical bonding from XRD peak shifts alone.
- Do not compare peak intensity quantitatively unless normalization and sample preparation are controlled.

## TG/DTG Curve

Best use: hydration products, polymer residue, thermal stability, moisture loss, decomposition stages.

Required data:

- temperature
- mass percentage
- derivative mass loss if DTG is shown
- atmosphere, heating rate, sample mass

Caption boundary:

> TG/DTG curves identify mass-loss regions associated with moisture removal, decomposition, or hydration product changes; assignments should be supported by literature or complementary tests.

Reviewer risk:

- Do not call a mass-loss event a specific reaction without assignment evidence.
- State heating rate and atmosphere; otherwise curves are not comparable.

## FTIR Overlay and Peak Labels

Best use: functional group tracking, epoxy curing, asphalt-emulsion residue comparison, possible interactions.

Required data:

- wavenumber
- absorbance or transmittance
- sample labels
- peak assignment table
- preprocessing method, such as baseline correction or normalization

Caption boundary:

> FTIR spectra show changes in assigned functional-group bands; mechanism claims require consistent peak assignment and, ideally, complementary morphology or rheology evidence.

Reviewer risk:

- Avoid writing `new chemical bond was formed` from weak shifts alone.
- Do not over-label every peak; label only claim-relevant peaks.

## SEM/TEM Annotation

Best use: morphology, phase distribution, interface defects, hydration products, fracture surfaces.

Required image metadata:

- magnification or scale bar
- sample preparation/drying/coating method
- imaging mode and voltage if available
- annotation legend

Caption boundary:

> SEM/TEM images illustrate morphology or interface features in representative fields of view; quantitative image analysis is needed for statistical claims.

Reviewer risk:

- Do not generalize from one attractive micrograph.
- Do not infer durability or bonding mechanism unless linked to performance data.

## Error Bars, Boxplots, and Scatter

Choose:

- mean + SD for engineering replicate spread.
- mean + SE only when discussing uncertainty of the mean.
- 95% CI for inferential comparison.
- boxplot or violin plot when sample size is large enough to show distribution.
- all individual points when `n <= 5`.

Caption boundary:

> Error bars represent [SD/SE/95% CI]; statistical tests and replicate counts are reported in the caption or methods.

Reviewer risk:

- Never leave error bars undefined.
- Do not use a bar chart alone when distribution shape or outliers matter.
