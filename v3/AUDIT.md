# Project review — 9 September 2026

## Scope and working-tree state

Reviewed the present Streamlit entry point, calculation/data modules, sidebar/results/map/styles, marriage and child-health content structure and citations, dependency list, architecture/quick-start/refactoring documentation, regional CSV and shared project notes. Checked the local Git tree and recent history. The old Next.js app is deleted in this working tree and the recorded commit omits its calculation library. Prior deployment claims in shared notes were treated as history, not verification of a currently available implementation. No cloud deployment, Git history rewrite, restoration of deleted files or credential access was performed.

The working tree already contained many edits and deletions before this work. The redesign lives in `v3/`; legacy modules are unchanged. The root README now directs local development to V3, while retaining its previous documentation as historical material.

## Findings and treatment

| Component | Finding | V3 treatment |
| --- | --- | --- |
| app.py | Independent multiplication of 12 filters produces precise “matches”. A flat sex split is combined with age-independent marginals. Source guidance points at a deleted Python file. | Replaced calculation engine and interface in V3. Results are directly summed demographic estimates with visible denominator and caveat. |
| data.py / age | 54.2m adult base and broad, interpolated age groups; 65+ treated as uniform over 65–99. | Import original MYE2 sex-specific single-year counts and retain the actual 90+ terminal group. Verified 55,022,253 adults in the pinned UK snapshot. |
| data.py / income | Hand-built distributions are normalised; mixes ASHE employee and HMRC taxpayer concepts with all adults. | Excluded until values and compatible denominators can be extracted and verified. |
| data.py / ethnicity | England-and-Wales Census distribution is labelled adjusted for the whole UK, then normalised. | Excluded; no unsupported harmonisation. |
| calculations.py / orientation | Removes nonresponse and “other” from the denominator, redistributes shares, and equates identity with compatible interest. | No orientation-compatibility multiplier. |
| calculations.py / relationship | A flat 35% “single” rate is combined with legal marital-history distributions; these measure different things. Same-sex/opposite-sex distributions are not a valid classification of all people's marital histories. | Direct ONS living-arrangement or legal-status tables, kept separate. |
| height / BMI / baldness | Assumed height spread and broad prevalence are not joint distributions of the selected UK age group. BMI categories are labelled body types. | Excluded from calculated results; evidence gap described in the interface. |
| children / education | Generic source labels do not identify exact cells or justify the hand-coded distributions. | Excluded until traceable and definition-compatible. |
| map_visualization.py / ui_results.py | Applies a constant national probability to estimated region populations, then claims consistent local chances. | Geography uses the selected region's actual source age/sex counts. No invented regional match map. |
| ui_marriage_stats.py / ui_marriage_stats_content.py | Large overlapping content modules, dated freshness claims, mojibake and mixtures of estimates/projections with blanket assertions of official accuracy. Annual marriage events are not a stock of available partners. | Replaced active relationship content with direct 2025 status/living-arrangement records. Legacy narrative claims have not been certified. |
| ui_baby_stats_content.py / BABY_HEALTH_DATA | Medical tables and broad citations require a separate claim-level audit; units and populations are not consistently established by the code. | No legacy medical numbers are displayed in V3. They remain in the preserved original files. |
| styles/sidebar | Dense sidebar, oversized result tabs, styling applied broadly to div/span elements. | New responsive layout, native labelled controls, keyboard tabs, visible focus and bounded tables. |
| documentation | References deleted modules and an old deployment; “all sourced” claims exceed evidence. | New V3 documentation plus an explicit historical boundary at the top of the original README. |

This was a review of all project areas, not a certification of every legacy statistic. The supported V3 dataset is independently extracted and checked; unsupported legacy claims remain excluded.

## Source controls

1. Original binary workbooks retained; SHA-256 hashes recorded and tested.
2. Source-table headers, numeric types and worksheet addresses checked by extraction.
3. UK all-age total independently reconciles to 69,281,437 and age-18+ total to 55,022,253; male and female adult totals reconcile to 26,625,856 and 28,396,397.
4. Every population age cell reconciles across sexes and constituent countries.
5. Relationship estimates, CV flags and CI margins copied directly, without reweighting, geographic projection or partial age-band interpolation.
6. Suppressed and unavailable values remain nonnumeric; dependent totals are withheld. CV d values are visibly flagged. Individual margins are not combined without covariance information.
7. Reference year and geography are attached to results, comparisons and downloads. The 2025 relationship source is separate from the pinned mid-2024 population snapshot.

## Acceptance checks

- Unit suite: nine tests passed, covering aggregate reconciliation, bounds, missing values, direct-cell relationship estimates, supported combinations, source fingerprints and export provenance.
- Chromium: interaction, comparisons, JSON download, suppression, invalid ages, keyboard tabs, shared URL reload, failed-data handling and absence of JavaScript errors passed.
- Responsive checks: 390px, 430px and 768px without page overflow; desktop and mobile screenshots visually inspected.
- Fresh process binds only to localhost on an OS-assigned random port. Root and health endpoint return HTTP 200; `.env` and legacy source paths return 404.

The supported results remain statistical estimates with source limitations. No claim is made about a person's likelihood of finding a partner. No changes were published externally.

## V3.1 clarification — requirements calculator restored

The user clarified that the original dating-calculator workflow must remain primary. `/` now serves the requirements calculator; `/index.html` retains V3.0's direct-source explorer. Newly extracted NHS and HMRC marginals and verified ONS publication shares are combined only as a labelled model. The V3.0 review above remains a record of legacy-data findings, not a description of the new default page. Combining source-backed marginal inputs does not produce an officially verified joint count. Refer to the active calculator's per-result assumptions and JSON exports. Height spread is a user-set assumption; no source validity is claimed for it. All 18 engine/data tests and the requirements-calculator browser suite passed.
