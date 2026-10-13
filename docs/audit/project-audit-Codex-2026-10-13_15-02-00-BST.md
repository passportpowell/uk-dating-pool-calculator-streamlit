# UK Dating Statistic Calculator — full project audit

Auditor: Codex. Timestamp: 13 October 2026, 15:02 BST (14:02 UTC). Reviewed working tree on `main`, HEAD `954e2dd`; substantial uncommitted migration and subsequent changes are present.

## Verdict

The application has a functioning calculation suite, but its current results cannot be described as a verified count of UK adults meeting all requirements. Several filters contain unverified distributions, the uncertainty interval is not a statistically derived confidence interval, and aggregation produces demonstrable inconsistencies. A normal Git staging operation would omit the calculation engine because `src/lib` is ignored.

Release recommendation: **hold publication of accuracy claims and the current confidence intervals** until the critical findings below are resolved. Preserve the current implementation and archived evidence while repairing it. No application fixes, commits, pushes, or deployments were performed for this audit.

## Scope and method

- Read the base bundle's `00-START-HERE.md`, `BOOT.md`, and `local-routing/README.md`, together with project `AGENTS.md`, `docs/HANDOFF.md`, `docs/ACTIVE.md`, and the earlier adversarial audit.
- JEV was available and recommended inline work (execution confidence 0.43; worker recommendation Luna medium, confidence 0.35). Used inline review in the current session; the low-confidence recommendation was treated as guidance. No subagents were used.
- Inspected all active application areas: calculation/data/test modules, main calculator, regional/marriage/fertility components, methodology page, layout/styles, package/TypeScript/lint/Vercel configuration, Git ignore rules, deployment-related documentation, and income-generation scripts.
- Inspected archived directory presence and the archived V3 evidence role. Archived prototypes were not executed or modified; not every historical narrative claim was revalidated.
- Ran the existing unit suite and independent edge-case probes. Reviewed selected official HMRC, ONS, and HFEA publications live. Source checks are targeted verification, not certification of every number in the repository.
- Added `audit-probes-Codex-2026-10-13.ts` alongside this report. Reproduce with `npx --no-install tsx docs/audit/audit-probes-Codex-2026-10-13.ts`.

## Verification results

- **PASS:** `npm test` — 56 tests, 17 suites, zero failures.
- **PASS:** audit probe execution, using both `npx --no-install tsx` and direct `node node_modules/tsx/dist/cli.mjs`; the probes expose defects rather than assert that the application is correct.
- **PASS:** `npx --no-install tsc --noEmit`, exit 0; independent `node node_modules/typescript/bin/tsc --noEmit --incremental false`, exit 0.
- **PENDING / NOT VERIFIED:** lint and production-build commands were launched but did not return a completed result during the main review. Silence is not a pass; see any final verification addendum below.
- **SKIPPED:** browser-rendered desktop/mobile, light/dark contrast measurements, assistive-technology interaction, and live Vercel deployment verification. Static UI findings below are explicitly distinguished from observed browser behavior.
- **SKIPPED:** vulnerability advisory certification and exhaustive secret scanning. No secret values were read or printed. No claim is made that dependencies or the repository are vulnerability-free.

## P0 — release-blocking findings

### A01. Git ignores the calculation engine

Evidence: `.gitignore:16` contains `lib/`. `git check-ignore -v src/lib/calc.ts src/lib/data.ts src/lib/calc.test.ts` identifies that rule for all three files. `git ls-files src/lib` returns no tracked files. The Next application is still untracked in this working tree, while the legacy files appear deleted after archiving.

Impact: a normal `git add`/push of this migration omits imports required by the application, causing a missing-module build failure. The ignored `archive/` also means retained source workbooks are not part of the new repository snapshot unless deliberately preserved elsewhere.

Action: narrow the Python-specific ignore rule or explicitly unignore `src/lib/`; verify the staged file list contains all three modules and any required provenance assets. Review the migration's deletions and additions explicitly before committing. Do not blanket-stage this dirty tree.

### A02. The “90% CI” is an invented error model

Evidence: `src/lib/calc.ts:553` (`calculateConfidenceInterval`) sets variance using `activeFilterCount * 0.0018`, a fixed tail variance, and a normal quantile. It receives no survey sample sizes, standard errors, covariance matrices, weights, measured coverage, or source-specific confidence limits. `src/app/page.tsx:921` nevertheless claims it accounts for ONS/HMRC/HSE sampling error.

Impact: the 90% label implies calibrated statistical coverage that has not been established. It excludes major model uncertainty, unsupported child/marriage rates, geographic proxies, and income seed assumptions. A broad male-target probe returns an upper bound of **29,863,000**, exceeding the entire male target population of **26,625,856**. Integer rounding also turns small nonzero expected counts into zero before uncertainty is calculated.

Action: remove the statistical confidence claim. If a model sensitivity range is wanted, identify its assumptions and avoid a coverage percentage. A genuine confidence interval requires a defensible estimator and variance method, plus validation and population bounds.

### A03. Children counts still use unverified rates

Evidence: `src/lib/data.ts:582` explicitly says “Provenance weak” and supplies 0.43/0.18/0.24/0.15 for no/one/two/three-plus children. `childrenProbability` applies these equally to every sex, age, relationship state, and region. Selecting “No children” in the probe retains approximately **43%** of the previous pool.

Impact: a vitally important preference changes the result using a distribution that is not established as an adult-level UK parenthood measure. The implementation does not distinguish household children, dependent children, grown-up children, adopted children, or children living elsewhere. No co-parent-count measure is implemented.

Official context: [ONS Families and households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022) describes families and households; those denominators cannot automatically be relabelled as all adult parents. The user's household-only fallback is acceptable only when labelled as that narrower measure.

Action: replace these rates with a traceable adult-level table, including age/sex where available. Until then, exclude this multiplier and say which selected requirements are not accounted for. If only household data is usable, label it “dependent children living in the household”; never claim that its complement proves someone has no children.

### A04. Income-by-age tables are modelled, not observed joint distributions

Evidence: `scratch/generate_age_income.py` estimates log-normal distributions from manually transcribed taxpayer counts, means, and weighted averages of subgroup medians. It assumes a £12,570 truncation and puts non-taxpayers in the lowest band. `scratch/run_ras.py` calibrates this seed to national columns. These scripts and their inputs are ignored. `src/lib/data.ts:259` describes the result as eliminating confounding; the UI says it eliminates independence distortions.

Official context: [HMRC SPI 2023/24 commentary, sections 1–4](https://www.gov.uk/government/statistics/personal-incomes-statistics-for-the-tax-year-2023-to-2024/personal-incomes-statistics-2023-to-2024-commentary) confirms Table 3.2 contains age/sex counts and mean/median income, while Table 3.3 contains sex-by-income-band counts. These do not directly identify the age-by-income tails. Most tables exclude non-taxpayers.

Impact: fitting margins does not verify rare high-income age cells. An average of subgroup medians is not generally the pooled median. The resulting young high-earner figure may be plausible, but a claimed “20x correction” cannot be established from these inputs alone. RAS female target columns also differ from the active female national marginal in the highest two bands.

Action: retain the scripts and exact source cells in reproducible, versioned provenance; describe these as calibrated model estimates. Validate observed cells where available, preserve genuinely joint public data, and test sensitivity to seed distribution, truncation, and non-taxpayer treatment. Do not present a hardcoded tail as a direct HMRC observation.

### A05. Fertility and IVF display mixes incompatible measures

Evidence: `src/components/FertilityStatsTab.tsx` labels IVF figures “per cycle” and states 32% for under 35. Its source metadata groups ONS/HFEA/NHS/MBRRACE together without individual table references. `FERTILITY_AND_BIRTH_DATA` assigns one IVF rate to an open-ended 40+ category and includes 68,700 annual cycles without a precise period/definition.

Official comparison: [HFEA's 2022 preliminary report](https://www.hfea.gov.uk/about-us/publications/research-and-data/fertility-treatment-2022-preliminary-trends-and-figures/) reports about **77,000 fresh and frozen IVF cycles**, and **35% births per fresh embryo transferred** for patients aged 18–34 using their own eggs. It distinguishes ages 35–37, 38–39, 40–42, and 43–44 and identifies preliminary data. “Per embryo transferred” is not “per cycle”.

Impact: clinical statistics can materially mislead when age bands, treatment type, denominator, source year, and preliminary status are lost. Miscarriage/chromosomal/maternal mortality figures also lack claim-level source evidence; they were not fully validated in this audit.

Action: verify or remove each medical statistic independently, retain its denominator and clinical definition, and use the original age bands. Do not publish a mixed medical risk matrix under a generic official-source badge.

## P1 — calculation and product correctness

### A06. Product of averaged factors is not a stratified joint estimate

Evidence: `calculateDatingPool` separately averages income, education, height, and single-status factors across the selected ages, then multiplies their averages. For `lookingFor: 'Any'`, it also averages each factor across genders separately.

Impact: this introduces combinations of characteristics from different ages or genders. A probe with a bisexual female user, ages 25–35, income £75k+, height 180–190 cm returns **33,198** for Any, versus **90,586** from the male and female estimates added together. Part of this disagreement is the orientation function's Any branch; the factor-wise gender mixing is an additional independent mathematical problem.

Action: calculate each sex/age stratum's count and multiply applicable conditional rates inside that stratum before summing. Use measured joint tables when available. Require Any = Male + Female for an identical, consistent target-compatibility definition. Residual independence assumptions must still be disclosed after stratification.

### A07. Age selection mishandles the 90+ group

Evidence: `ageProbability` includes all of the 90+ cell whenever the upper bound reaches 90, without checking the lower bound against it. `getIncomeDistributionForAge` and `getEducationDistributionForAge` reuse the entire 90+ weight for each age 90 through 99.

Probe: ages **90–90**, **99–99**, and the invalid **100–100** each return **0.01136332967** of adults. This repeats the same open-ended population as if it were a single-year count.

Action: expose a single 90+ option, or obtain a genuine older single-year breakdown. Include the grouped count once; reject out-of-domain ages. Test boundary selections and weighted aggregation explicitly.

### A08. Age weights ignore target-sex populations; some weights are uniform by year

Evidence: age selection and income/education age averaging use the all-person age distribution. Height and single-status functions weight bands by overlapping years rather than population counts. Height averages means and then applies one normal curve, which is not a mixture of the age-band distributions.

Impact: exact age shares of men and women differ, especially at older ages. Broad age ranges can be biased even when their individual source means are correct.

Action: use the retained ONS sex-by-age population counts as the weighting base and integrate each age/band's filter rate. Restore the sex-specific evidence already present in the archived V3 datasets where appropriate.

### A09. Correlation boost is unsourced and headline/funnel diverge

Evidence: `calc.ts` applies constants 1.15, 1.35, and 1.65 based on income/degree selections. No study or fitted joint table justifies those constants. The cumulative funnel is calculated before this adjustment; the headline is calculated afterward.

Probe: male target, £100k+, undergraduate minimum, correlation enabled: headline **596,204**, final funnel **361,335**, boost **1.65**.

Action: replace the heuristic with validated joint counts/conditional rates or remove it. Every displayed breakdown must reconcile with the final result; a gender-population cap does not ensure all tighter filter intersection bounds are respected.

### A10. Relationship conditioning is still conceptually incorrect

Evidence: `marriageProbability` renormalizes legal marital categories over unmarried adults when the other filter is “not living in a couple”. It also chooses fixed opposite-sex/same-sex marriage-history distributions based on the user's orientation. Annual marriage-event statistics do not establish individual adult marital-history shares.

Impact: correcting the original blanket double-count does not establish the correct joint distribution. Legally married people can live apart; divorced or never-married people can cohabit. Legal marital history is not partitioned by the desired future partner's sex. The present fixed categories lack age/sex conditioning and civil-partnership detail.

Action: use the ONS cross-tabulation of legal status and living arrangements by age/sex, with an explicit supported definition of Single. Restore the requested five clear choices and avoid a separate incompatible availability multiplier.

### A11. Education mapping invents precision and loses Census categories

Evidence: active data divides Level 4+ into undergraduate and postgraduate shares, includes a generic APS approximation, folds apprenticeships into GCSE and unknown-level qualifications into A-level, and labels age-band splits empirical without retained query outputs/cells.

Official comparison: [ONS Census 2021 education, section 3](https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare/bulletins/educationenglandandwales/census2021#highest-level-of-qualification) groups HNC/HND/degrees/postgraduate qualifications together at Level 4+, with apprenticeships and unknown-level qualifications separate.

Probe: integrating age-specific postgraduate rates gives **9.9702%**, while requesting the full 18–99 range bypasses that integration and returns **11.4%**. The full-range unit test therefore does not establish reconciliation of the conditional tables.

Action: use actual Census classification labels, preserve unclassified levels, and only offer degree/postgraduate distinctions with separately suitable evidence. Aggregate conditional tables to verify margins instead of bypassing the calculation at the full range.

### A12. Regional results are proportional allocations, not local demographics

Evidence: `calculateRegionalPool` applies one national probability to every region, using rounded regional adult baselines and a scaling constant. The map's “density” tier is based on adult population count, not area or population density.

Impact: local ethnicity, age, education, income, and sex differences are ignored. London remains the same demographic mix as Wales or Northern Ireland; reconciliation only proves arithmetic allocation. Selecting a region changes the count but not the national pass rate. Per-region rounding can fail exact reconciliation for tiny pools.

Action: label these as national estimates allocated by population until real regional conditional rates are used. Use period-specific adult/sex populations, rename density tiers, and test small pools plus count/percentage consistency in selected regions.

### A13. Orientation silently redistributes excluded responses

Evidence: `orientationProbability` divides 0.934, 0.021, and 0.016 by their sum (0.971), discarding Other/nonresponse and renormalizing to 100%. The straight-plus-bi probe returns **97.8373%**, compared with the source marginals' combined **95.0%**.

Impact: targets are assigned identities they did not report, and self-reported identity is treated as a direct compatibility measurement. Any plus a non-bisexual user can collapse the target rate to bisexual-only for reasons not dictated by target identity.

Action: use the reported shares without redistributing unknown responses and define target compatibility consistently by user sex and target sex. Where identity is a proxy, explain it. Restore the age/sex orientation source table already retained in archived V3 rather than reverting to one national marginal.

### A14. Engine validation permits impossible results

Evidence: the public calculation function lacks runtime validation and deduplication. Arrays are summed directly; height ordering and finite values are assumed.

Probe: ten copies of White British produce an ethnicity factor **7.71878** and a funnel of **203,183,761** adults. Reversed 200–150 cm bounds produce **−25,742,929** matches. Education supplied as an unknown URL value falls back to Any instead of an error.

Action: validate finite numeric ranges, supported enums, known region keys, nonduplicate selections, and nonnegative probabilities at the calculation boundary. These malformed engine probes are not evidence that normal checkbox interaction generates duplicates; they identify absent validation that callers and future URL imports can bypass.

### A15. Shared links lose important criteria

Evidence: page URL synchronization serializes gender, orientation, age, height, income, education, single state, baldness, correlation, and region. Ethnicity, BMI, children, and marital-history selections are neither serialized nor restored.

Impact: sharing/reloading a strict scenario resets these four filters to all options, generating a different result while appearing to be the same scenario.

Action: serialize all canonical criteria with validation and a schema/version; add browser tests comparing state and result before/after share/reload. Back/forward navigation should also restore state rather than relying only on initial state creation.

### A16. Trade-off previews can disagree with Apply

Evidence: engine `INCOME_TIERS` includes 11,440 and 37,430; UI options include 24,785 and 34,963. The engine and `applyTradeOff` each independently choose a lower threshold. Engine trade-offs use national counts even when the main result is scoped to a region.

Impact: applying the offered change can produce a different threshold/count from the preview, or show nationwide gains alongside a regional headline.

Action: use one canonical threshold list and return the exact criteria patch with each trade-off. Evaluate both preview and Apply against the same scoped population.

## P2 — presentation, accessibility, evidence, and maintenance

### A17. Earlier requested filter behavior regressed

Static evidence: ethnicity/BMI/children/marital controls start collapsed; the height checkbox still hides its inputs. Feet/inches are displayed as helper text but cannot be entered directly. The helper can return **4 feet 12 inches** for 152.3 cm because rounding does not carry inches into feet.

The user previously requested all filters visible, no activation checkbox, direct feet/inches input, five relationship choices, a separate statistics explorer page, and simple explanation/source links under each requirement. Those are not all present in the current root migration. Audit these requirements against the archived V3 implementation before calling parity complete.

### A18. Evidence library is not sufficient to trace an individual result

`Sourced<T>` contains a source-name string but no required URL, exact table/cell/query, extracted denominator, evidence hash, or checked date. Methodology cards print those strings as text; links are in a separate generic list. The new income/education conditional tables are absent from the card wiring. Children/baldness/medical claims lack dedicated supporting links.

Marriage badges say “ONS Verified” across numerous exact ethnicity/pairing figures that are not individually substantiated here. Numerical normalization and agreement of one marriage total do not verify all these claims. The existing report's “READY & VERIFIED” wording exceeds the checks recorded there.

Action: preserve source files/API responses outside the ignored historical tree and attach claim-level provenance. Present plain explanations and clickable original table links at the filter stage. Date every reference period and proxy clearly.

### A19. Accessibility problems visible in source

- Region SVG groups have click handlers but no keyboard focus, button role, or keyboard activation. Table-row region selection also uses click-only handlers.
- Accordion toggles omit `aria-expanded` and `aria-controls`.
- Tabs have role/selection attributes but lack panel associations, roving focus, and arrow-key behavior.
- General `Field` labels require review for actual input association; numeric controls use wrapping labels, but not every selector is explicitly associated.
- Dark zinc text/background classes coexist with a light system-theme palette. Contrast failures are a risk requiring browser measurement; they are not asserted as measured failures.

Action: verify keyboard use and accessible names in an actual browser, then fix the demonstrated gaps. Test system light/dark preferences and reduced-motion behavior.

### A20. Output precision and language overstate knowledge

Headline percentages use four decimals and exact integer headcounts; the share text starts “According to official UK demographics”. UI wording about “eliminating independence distortions” and the confidence tooltip imply stronger validation than the model supports. “Millionaire” refers to wealth, whereas the filter selects annual income.

Action: round to appropriate significant figures, distinguish observed inputs from modelled overlap, and use short plain language. Preserve the user's intended question: share of selected adults meeting preferences, not a personal probability of meeting or forming a relationship.

### A21. Test suite verifies internal assumptions more than external accuracy

Strengths: pure-engine tests, normalized distributions, empty selections, target denominator, regional scaling, and recursion prevention are useful. The 56-test run passed.

Gaps: source extraction and specific table cells are not validated; tests assert invented young-income limits, a positive correlation boost, and the presence of CI bounds. Full-range income/education tests take special-case paths. They do not detect omitted share filters, ignored engine files, clinical denominator mismatch, sex/age additivity, 90+ duplication, or headline/funnel disagreement. Existing model tests are no substitute for browser/source QA.

Action: add invariants around additivity, bounded/nonnegative outputs, duplicate/invalid input rejection, zero/small pools, URL round-trips, exact trade-off application, and staged production files. Link factual fixtures to retained evidence rather than to the constants under test.

### A22. Deployment and project continuity remain unverified

Current `vercel.json` selects Next.js at root. The historical Vercel root-directory failure cannot be declared solved without inspecting the actual Vercel project setting. Current Next migration and package lock are untracked, while HEAD remains the old V3 routing commit.

`ACTIVE.md` still marks largely implemented work unclaimed; HANDOFF says all audit work is implemented/verified and recommends committing despite unresolved accuracy problems. README still claims 21 tests and contains broader empirical/source claims than the active data supports. The required footer GitHub-icon/card link and local Tailscale access documentation were not found in the active application; applicability to the eventual hosted footer should be confirmed during UI work.

Action: update current-state docs after checks, reconcile the requested feature list, review precisely what will be committed, and verify a real preview/production build before deployment. Do not assume the local workspace equals GitHub or production.

## Recommended work order and acceptance gates

1. **Release integrity:** fix the ignore rule, preserve provenance, and verify a complete staged snapshot. Acceptance: clean checkout contains all imported modules and builds.
2. **Remove unsupported certainty:** replace the CI claim, disable unsourced correlation, replace/exclude unverified children/clinical figures. Acceptance: every active numerical input has traceable evidence or is prominently identified as a modelling assumption.
3. **Repair calculation structure:** integrate by sex/age, fix 90+ handling, legal/cohabitation conditioning, and runtime validation. Acceptance: additive strata; bounded outputs; consistent denominators and reconciled funnel/headline.
4. **Repair scenario behavior:** complete URL persistence, exact trade-off patches, regional scope, all-visible preferences, and feet/inches input. Acceptance: browser round-trip reproduces criteria/result and previews equal applied changes.
5. **Source and UI QA:** per-filter evidence, official table links, consistent geographic labels, clinical denominator review, keyboard navigation, responsive/light/dark checks. Acceptance: documented observed checks, not a badge based only on unit tests.
6. **Release verification:** run tests/typecheck/lint/build, inspect Git diff and staged contents, validate Vercel settings and actual deployment, then refresh HANDOFF/ACTIVE/README. Committing or deploying remains a separate user-authorized action.

## Audit limits

This is a code/data/provenance audit with reproducible numerical probes. It does not certify medical guidance, re-estimate the complete UK joint demographic distribution, or establish statistical coverage for an alternative uncertainty range. Unsupported values are reported as unverified unless an explicit contradictory source or reproducible failure is documented above. The application's active source was preserved.
