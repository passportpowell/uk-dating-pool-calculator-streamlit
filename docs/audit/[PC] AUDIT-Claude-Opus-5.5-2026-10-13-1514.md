# Project Audit — UK Dating Statistic Calculator

- **Auditor:** Claude Opus 5.5 (Claude Code, desktop app)
- **Date:** 2026-10-13 15:14 BST (14:14 UTC)
- **Scope:** Whole project at `N:\Otis Projects\UK dating statistic calculator`: engine (`src/lib`), UI (`src/app`, `src/components`), data provenance, tests, repo/deploy state, and compliance with the `- Base Prompts and Skill` protocol (`00-START-HERE.md`, `BOOT.md`) and project `AGENTS.md`.
- **Mode:** Read-only. I changed no code. The only file I wrote is this report.
- **Note:** `docs/audit/audit-probes-Codex-2026-10-13.ts` was already here, so Codex appears to be auditing in parallel. I reused that probe script (I ran it but did not edit it). The numbers below come from my own run of it.

---

## 1. Verification run

| Check | Result |
|---|---|
| `npm test` (`tsx --test src/lib/calc.test.ts`) | **PASS**: 56/56 tests, 17 suites (21.5 s) |
| `tsc --noEmit` (via `node node_modules/typescript/bin/tsc`) | **PASS**: exit 0 |
| `eslint src` | **SKIPPED**: still running after 550 s on the SMB mount (exit 124) |
| `next build` | **SKIPPED**: too slow on the SMB mount. No record in HANDOFF or SHARED_NOTES shows a passing build for the current tree, so PLAN acceptance criterion #3 is unverified |
| Codex probe script (`npx tsx docs/audit/audit-probes-Codex-2026-10-13.ts`) | Ran. Its output is the evidence for several findings below |
| JEV routing | Not run for this audit |

---

## 2. Executive summary

The engine is clean, pure TypeScript with source metadata, and the tests and types pass. The previous audit round fixed the worst confounder (income × age). The headline number is still wrong or misleading in several common cases:

1. **"Looking for: Any" is miscalculated.** It undercounts by about 63% in a realistic bisexual scenario.
2. **The "90% confidence interval" is not statistical.** It is a heuristic formula, yet the UI labels it a 90% CI.
3. **The correlation boost** changes the headline number but not the funnel, and the boost factors are not validated.
4. **No input validation in the engine.** It can return negative match counts or probabilities above 1.
5. **The project is in a fragile repo state.** The whole Next.js app is **untracked** in git, the committed `vercel.json` still deploys the deleted `v3/` prototype, and HANDOFF's only next step ("commit") has not been done.

Severity scale: **P0** means wrong or misleading output, or a risk of losing work. **P1** means a material accuracy or provenance gap. **P2** means a minor bug or polish item.

---

## 3. Findings: calculation engine (`src/lib/calc.ts`)

### P0-1. "Any" target gender is aggregated incorrectly
- **Where:** `calculateDatingPool` (`calc.ts:622-661`) and `orientationProbability` (`calc.ts:351-353`).
- **What:** For `lookingFor: "Any"`, each per-gender factor (height, income, body, single, baldness) is blended by the gender split on its own, and the blended factors are then multiplied together. That equals Σ_g w_g·∏ f_g only when the factors are identical across genders. Height in particular differs hugely by gender. On top of that, the bisexual "Any" orientation factor is `straight·0.5 + gay·0.5 + bi` (≈0.51). The correct value is roughly "men who date women + women who date women".
- **Evidence (probe):** Female bisexual user, age 25–35, £75k+, height 180–190 cm. The **"Any" result is 33,198**, while **"Male" + "Female" is 90,586**.
- **Fix:** Compute the full pipeline once per target gender and sum the two pools. Don't blend factors.

### P0-2. The "90% CI" is a heuristic but is presented as a statistical interval
- **Where:** `calculateConfidenceInterval` (`calc.ts:553-604`). The UI labels it a "90% CI" and the methodology text says it is "derived from demographic survey error propagation".
- **What:** The formula is σ = √(0.0018·activeFilters + 0.0009 or 0.0036). It takes no input from any dataset's sampling error. `activeFilterCount` always includes Gender and Orientation, and also includes "Any height", because a 140–210 cm range gives about 0.9999, which counts as below 1.
- **Evidence (probe):** With every filter at its broadest, the output is `≈ 25,754,000 [22,210,000 – 29,863,000]`. That is ±15% on what is essentially a census headcount.
- **Fix:** Either relabel it as an "illustrative uncertainty band (model + data)", or derive it properly, for example with Monte Carlo over the per-dataset standard errors. Count only filters the user actually set.

### P0-3. The correlation adjustment changes the headline but not the funnel, and is unvalidated
- **Where:** `calc.ts:708-726`.
- **What:** `correlationDiscount` (1.15, 1.35 or 1.65) multiplies the final probability. The `steps` funnel uses the unadjusted cumulative value. The factors have no cited source. The only cap is `min(genderProb, …)`, not the Fréchet bound `min(p_income, p_edu)`.
- **Evidence (probe):** £100k+ income and degree, with correlation on. The headline is **596,204**, but the last funnel step is **361,335**.
- **Fix:** Either apply the adjustment as a visible funnel step with a stated source, or replace it with an income × education joint table and remove the flag.

### P1-4. No input sanitising: negative counts and probabilities above 1
- An inverted height range (`min 200, max 150`) gives **−25,742,929 matches**. `heightProbability` has no clamp.
- Duplicate selections are summed: `selectedEthnicities = ['White British' ×10]` gives a probability of **7.72** and 203M "remaining". The same applies to body type, children and marriage lists.
- The UI currently guards height order (`page.tsx:264`), but the engine is the public seam (ADR-001), so it must validate itself.
- **Fix:** In `calculateDatingPool`, sort min and max, de-duplicate the lists with `new Set`, and clamp every factor and the total to [0, 1]. Add tests.

### P1-5. Results jump at age 18–99: the age-weighted tables don't reconcile to the marginals
- `getIncomeDistributionForAge` and `getEducationDistributionForAge` return the national marginal for exactly `[18, 99]`, and the age-weighted mix for anything else.
- **Evidence (probe):** Postgraduate share is **9.97%** age-weighted vs **11.4%** marginal. Income ≥£75k is 8.099% vs 8.102%. So a user moving the slider from 18–99 to 18–98 sees education results jump by about 14%.
- The test "full adult age range (18-99) matches national…" is **tautological**: it exercises the shortcut, not the data.
- **Fix:** Drop the shortcut so every range uses the age-weighted path, and rescale the by-age education rows so that their age-weighted sum equals the marginal. Change the test to compare `[18, 98]` and `[18, 99]`.

### P1-6. Children and marriage history ignore age and sex
- `CHILDREN_DISTRIBUTION` (43% with no children) applies equally to an 18–24 and a 40–49 target. **Probe:** the "No children" ratio is a flat 0.43 for every age.
- `MARRIAGE_HISTORY` is a single all-age distribution. It interacts with the age-conditioned `SINGLE_AVAILABILITY_BY_AGE`, so a young "never married" pool is undercounted and an older one overcounted.
- After the income fix, these are now the largest remaining independence distortions.
- **Fix:** Source age × sex tables: ONS families/households for dependent children, and the Census 2021 TS002 legal partnership × age table.

### P1-7. The regional breakdown assumes the same match probability in every region
- `calculateRegionalPool` scales only by adult population. London's age, ethnicity and income mix differs sharply from Wales or the North East, so a region plus ethnicity or income filter can be badly wrong. This is disclosed nowhere in the UI.
- **Fix:** Disclose it now. Longer term, condition at least age and ethnicity by region (Census TS021 by region).

### P2-8. Small engine bugs
- `ageProbability` (`calc.ts:67-80`): the whole 90+ bucket is added whenever `hi ≥ 90`, even if `lo > hi`. **Probe:** `ageProbability(99,99)` and `ageProbability(100,100)` both return 1.14%, the full 90+ mass.
- `cmToFeetInches(152.3)` returns **4′12″**. Inch rounding needs a carry into the feet value.
- The trade-off income tiers (`INCOME_TIERS`, `calc.ts:796`) don't match the UI's `INCOME_OPTIONS` (`page.tsx:49`). Example: at £42,200 the engine predicts the pool at £37,430, but "Apply" sets £34,963. At £25,000 it predicts £11,440 but applies £24,785. Use one shared tier list.
- `orientationProbability`: when a straight or gay user picks "Any", it returns only `bi` (a heavy undercount for a contradictory input). Either block that combination in the UI or define it explicitly.
- The bottleneck comment says it excludes "single availability", but the code doesn't (`calc.ts:687-688`).
- ONS "Other" and "Prefer not to say" (2.9%) are silently redistributed by renormalising orientation.

---

## 4. Findings: data and provenance (`src/lib/data.ts`, `scratch/`)

### P1-9. The income-by-age data is modelled, not extracted, and can't be reproduced from the repo
- The HANDOFF and SHARED_NOTES say the data was "extracted and calibrated HMRC SPI Table 3.2". But `scratch/generate_age_income.py` builds each age band's distribution from a **log-normal fitted to Table 3.2 median and mean**, and `scratch/run_ras.py` then rakes it to the Table 3.3 marginals. That is a reasonable method, but the shape is modelled. `data.ts` notes and the UI copy should say so.
- The female top-bracket targets in `run_ras.py` (£500k–£1M = 0.000494, £1M+ = 0.000185) **differ from `INCOME_DISTRIBUTION_FEMALE` in `data.ts`** (0.000352 and 0.000141). The calibrated table and the marginal therefore don't share a source.
- `scratch/` and `archive/` are both **gitignored**. The generator scripts and the raw source spreadsheets (formerly `v3/sources/*.xlsx` and `*.ods`, now deleted from the tracked tree) are **not version-controlled**, so the numbers can't be regenerated from the repo.
- **Fix:** Move the generators to `scripts/data/` (tracked), add the source files or their download URLs and hashes, and regenerate from a single marginal.

### P1-10. Low-provenance or unverified datasets shown to users
Datasets with no per-figure citation, which I could not verify in this audit:
- `CHILDREN_DISTRIBUTION`: its own note says "Provenance weak".
- `BALDNESS_BY_AGE`: period "n/a", source "BAD; research". The prevalence definition (which Norwood grade) is unstated.
- `MARRIAGE_STATISTICS_DATA.marriageRateByEthnicity`, `interEthnicMarriage.*`, `commonPairings` and `legalPartnerships2023` (231,949): no table references, and the values look modelled.
- `FERTILITY_AND_BIRTH_DATA.parentalAgeTrends`: 2022 mean maternal age is **31.5**. As I recall, ONS *Births in England and Wales: 2022* reported a standardised mean of about **30.9**. Verify before release. IVF success is the same 32% for under-20, 20–29 and 30–34, which looks like a placeholder.
- `ETHNICITY_DISTRIBUTION`: a hand-adjusted UK approximation (disclosed).
- `UK_REGIONS`: adult populations are hand-rounded, the base years are mixed, and the source is described only as an "ONS regional population baseline".
- **Fix:** Add a `tableRef` and `url` to `Sourced<T>`, and make a test fail on any dataset that lacks them.

### P1-11. Geography mismatch (known, still open)
Education, marriage and single availability use England & Wales data, and body type and height use England-only data. All are applied to a UK adult base of 55.0M. This is disclosed in `DATA_QUALITY_NOTES`. Either scope the tool to England & Wales or source the Scotland and Northern Ireland equivalents. Census 2021 education covers people aged 16+, while the app's base is 18+.

### Verified OK (spot checks)
- Distributions sum to 1 (tested). The age single-year table, gender split and adult population are internally consistent.
- `MIN_WAGE_ANNUAL` = £12.71 × 37.5 × 52 = £24,784.50, which matches the code ✓.
- The income-by-age £1M+ male totals reconcile approximately with the national marginal (about 22k men).
- The `mustBeSingle` / `MARRIAGE_HISTORY` renormalisation (ADR-001) is implemented as specified.

---

## 5. Findings: UI (`src/app`, `src/components`)

- **P2-12 Permalinks drop filters.** The URL sync (`page.tsx:179-217`) leaves out ethnicity, body type, children and marital-status selections, so a shared link silently shows a different result.
- **P2-13 `edu` URL parameter isn't validated** (`page.tsx:132-134`). An unknown value makes the engine return 1.0 while the dropdown shows a value that isn't in its list. Validate against `EDUCATION_ORDER`.
- **P2-14 Over-claiming copy.** The caveats block says income and education conditioning is "eliminating independence distortions" and that the CI comes from "survey error propagation". Both overstate what is implemented (see P0-2 and P1-9).
- **P2-15 The map comment says 400×520 but the SVG viewBox is 400×500** (`RegionalMapTab.tsx:11,145`). Cosmetic.
- **BOOT §7 non-compliance (required by the bundle):**
  - No footer GitHub icon linking to `https://www.passportpowell.com/card` (`target="_blank" rel="noopener noreferrer"`). `grep` finds no footer and no such link.
  - No Tailscale remote-access link in the UI, and no `tailscale serve` command in HANDOFF.

---

## 6. Findings: repo, deploy and governance

### P0-16. Uncommitted work and a stale deploy
- `git status`: **`src/`, `package.json`, `package-lock.json`, `tsconfig.json`, `AGENTS.md` and `docs/` are untracked.** All the Streamlit and `v3/` files show as deleted (D). HEAD `954e2dd` is "configure Vercel routes for v3 calculator".
- The committed `vercel.json` routes `/` to `v3/calculator.html`. If Vercel builds from `main`, production is still the old v3 prototype.
- The remote is `passportpowell/uk-dating-pool-calculator-streamlit`, a misleading name for a Next.js app. There is also a stale branch `publish-next-react` (last commit 2026-07-07).
- The tree sits only on the NAS, uncommitted, so a single bad sync loses months of work.
- **Fix:** Commit on a branch (for example `next-migration`), confirm the Vercel project settings, then merge. Consider renaming the GitHub repo. Commit only when you ask, per `BOOT.md` §7.

### P1-17. Handoff files are stale or inconsistent
- `docs/ACTIVE.md` still shows T-01 as `[~] IN_PROGRESS` and T-02 to T-05 as `UNCLAIMED`, while HANDOFF says all items are done. That contradicts `/prime`.
- `docs/HANDOFF.md` has no `Routing` line and no Workspace ID (both required by `AGENTS.md` and `00-START-HERE.md`). Its Status reads "READY & VERIFIED" without a build.
- `README.md` says "21 rigorous unit tests"; the actual count is 56.
- `SHARED_NOTES.md` is 64 KB and about 480 lines, well past the 200-line rotation rule, and has not been rotated to `docs/archive/`. The latest entry breaks the 5-line limit, and the 2026-09-29 entry has mangled characters ("vailable", "pm test", "px tsx").
- `docs/DECISIONS.md` has no ADR for the bivariate conditioning, the CI method or the correlation flag, all of which are lasting modelling choices.
- `docs/ADVERSARIAL_AUDIT_3_ROUNDS.md` cites `scratch/round1_luna.md`, which does not exist in `scratch/`.

### P1-18. Hygiene and secrets
- The project `.env` holds keys for **Supabase (secret key), the Vercel AI Gateway and OpenRouter**. The app uses none of them. The file is gitignored (good), but `BOOT.md` §2 puts credentials in the bundle `.env`. Remove unused secrets from the project. Some key names contain spaces (`vercel ai gateway key`), so they won't parse in most dotenv loaders.
- `.gitignore` contains `*copy*`, `*Copy*` and `*COPY*`. These silently ignore any future file with "copy" in its name (for example `CopyButton.tsx` or `copyright.md`). Narrow them to `* - Copy.*` patterns.
- `.gitignore copy` is a stray file from another project; it contains tender-scraper rules. Delete or archive it.
- Leftover Streamlit artefacts in the root: `.venv/` (Python 3.10 site-packages), `.streamlit/config.toml` and `tsconfig.tsbuildinfo`. Move them to `archive/` or delete them.
- `tsconfig.json` uses `"include": ["**/*.ts"]`, so the audit probe in `docs/audit/` is type-checked with the app. Harmless now, but exclude `docs/`.

### P2-19. Toolchain on the SMB mount
`eslint src` doesn't finish within 9 minutes on the NAS. `npm test` takes about 21 s and `tsc` takes several minutes. As `AGENTS.md` notes, lint and build checks need a local mirror (`robocopy` to `%TEMP%`) or a CI job. Add a GitHub Actions workflow (`npm ci && npm test && tsc && lint && build`) so verification stops depending on the NAS.

---

## 7. Prioritised action list

| # | Priority | Action | Files |
|---|---|---|---|
| 1 | P0 | Commit the Next.js tree on a branch; fix the Vercel target | git, `vercel.json` |
| 2 | P0 | Compute the "Any" pool as the sum of two per-gender pools | `calc.ts` |
| 3 | P0 | Relabel or properly derive the "90% CI"; count only filters the user set | `calc.ts`, `page.tsx`, methodology |
| 4 | P0 | Show the correlation boost as a funnel step, or remove it | `calc.ts`, `page.tsx` |
| 5 | P1 | Validate inputs in the engine (order, de-duplicate, clamp) and add tests | `calc.ts`, `calc.test.ts` |
| 6 | P1 | Remove the `[18,99]` shortcut; reconcile the by-age tables; fix the tautological tests | `calc.ts`, `data.ts`, tests |
| 7 | P1 | Track the data-generation scripts and source files; reconcile the female marginal | `scratch/` → `scripts/data/` |
| 8 | P1 | Condition children and marriage history on age and sex | `data.ts`, `calc.ts` |
| 9 | P1 | Add `tableRef`/`url` to `Sourced<T>`; verify or flag the low-provenance datasets | `data.ts` |
| 10 | P1 | Disclose that regional probability is uniform (later: regional age and ethnicity) | `RegionalMapTab.tsx` |
| 11 | P1 | Refresh ACTIVE, HANDOFF (Routing, Workspace ID) and README; rotate SHARED_NOTES; add ADRs | docs |
| 12 | P1 | Remove unused secrets from the project `.env`; narrow `.gitignore`; clean up leftovers | root |
| 13 | P2 | Fix the 90+ age bug, feet/inches carry, trade-off tier mismatch, permalink multiselects, `edu` validation | `calc.ts`, `page.tsx` |
| 14 | P2 | Add the BOOT footer GitHub icon and Tailscale link | `page.tsx`, `layout.tsx` |
| 15 | P2 | Add a CI workflow for lint, typecheck, test and build | `.github/workflows/` |

---

## 8. What is good

- The engine is a clean, pure-function seam (`calculateDatingPool`) with no React coupling, and it is fast and testable.
- Every core dataset carries `Sourced<T>` metadata, and the known limits are listed in `DATA_QUALITY_NOTES` and surfaced in the UI.
- The age-conditioned income, education, height and single-availability data are real improvements over the flat Streamlit version.
- The `mustBeSingle` double-count fix (ADR-001) is correct and tested.
- Tests and the typecheck pass. The `<Suspense>` wrapper around `useSearchParams` and the sensitivity recursion guard are both in place.
