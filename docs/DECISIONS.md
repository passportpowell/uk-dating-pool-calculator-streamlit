# Architecture Decision Records (ADRs)

## ADR-002: Observed strata and explicit proxy limits (2026-10-13)

Accepted. Supersedes ADR-001's old calculation interface, gender blending, generic distribution normalization and unmarried renormalization. The authoritative seam is `calculatePool` in `src/lib/calculator.ts`.

Use retained ONS location/sex/single-age counts; calculate the complete filter pipeline within each stratum before summing. Age90 represents90+ once. Use observed joint Census qualification/ethnicity counts, preserving apprenticeships and unknown levels. One relationship selector uses the published living/legal taxonomy, without an additional availability factor. Unknown/suppressed cells reject rather than become zero.

Exclude unverified age-income log-normal tails, invented degree/postgraduate splits, scalar correlation boosts, arbitrary confidence intervals and unverified clinical/reference claims. HMRC sex-specific national taxable-income shares are explicitly unconditioned on age. Height spread remains an explicit modelling assumption with a sensitivity comparison.

Ipsos QD6 supplies an acceptable narrower fallback: parental responsibility for children17 or under living permanently or temporarily with the adult. Use the published age marginal as a labelled proxy for both sexes, with16–24 used for18–24. Do not infer all-parenthood, adopted-child-specific, grown-up-child, nonresident-child or co-parent rates from separate marginals. Original PDF remains local/linked; commit limited factual extraction and fingerprints.

Source scripts, metadata, retained official files, tests and the active engine are committed. Existing archives and unused credentials are preserved. Code license does not relicense upstream data. Browser links/exports include all criteria and source rows; exact relaxation patches use the same location. Any future confidence claim requires a justified estimator and variance calculation.

Keep lasting architectural and design choices here. Use this format (from `codebase-design` and `domain-modeling`).

---

## ADR-001: Client-Side Next.js + TypeScript Engine with Sourced Data Records

- **Date**: 2026-09-29
- **Status**: Accepted
- **Authors / Models**: Claude, Codex, Gemini / Antigravity

### Context
The original UK Dating Pool Calculator was a Python/Streamlit application (`app.py`, `calculations.py`, `data.py`) with Folium maps and large narrative tabs (`ui_marriage_stats.py`, `ui_baby_stats_content.py`). Streamlit is incompatible with zero-config serverless deployment on Vercel and suffered from data bugs (availability double-counting between `SINGLE_RATE` and `MARRIAGE_HISTORY`, overstated degree+ share at 41% vs Census 33.8%, and misstated 2022 ONS marriage totals).

### Decision
1. Use Next.js 16 + React 19 + Tailwind CSS v4 + TypeScript at the repository root as the canonical production application, archiving legacy prototypes under `archive/`.
2. Implement all probability and regional calculations as pure, zero-dependency functions in `src/lib/calc.ts` using an Abramowitz & Stegun `erf`-based normal CDF in place of SciPy.
3. Wrap every statistical dataset in `src/lib/data.ts` in a `Sourced<T>` contract (`{ value, geography, period, source, notes? }`) with normalized distributions (`sum = 1.0`).
4. Renormalize `MARRIAGE_HISTORY` over unmarried categories when `mustBeSingle` is enabled so availability is never double-counted.

### Interface & Seam Placement
- **Interface**: `calculateDatingPool(input: CalculatorInput): CalculatorResult` and `calculateRegionalPool(totalProbability: number): RegionalResult[]` in `src/lib/calc.ts`.
- **Seam**: `src/lib/calc.ts` is the pure domain boundary; `src/lib/calc.test.ts` tests the engine directly without React/DOM coupling.
- **Internal Details Hidden**: Normal CDF (`erf`) approximation, age-band overlap weighting, gender blending for `"Any"`, and unmarried renormalization.

### Consequences
- **Positive**: Instant client-side recalculations, zero backend infrastructure cost on Vercel, auditable source metadata per dataset, and fast unit tests.
- **Negative / Trade-offs**: Independent filter multiplication remains an approximation where joint cross-tabulations are unavailable; explicitly disclosed in UI caveats and `/methodology`.

### Alternatives Considered
- **Keep Streamlit + Python**: Rejected because Streamlit requires persistent WebSockets and cannot deploy natively on Vercel static/serverless hosting.
- **Separate Python FastAPI microservice for SciPy**: Rejected because `scipy.stats.norm.cdf` is trivially replaced by a 12-line `erf` implementation with `< 1.5e-7` error.
