# UK Dating Statistic Calculator — Completion Plan

## Goal
Complete the Next.js / React / TypeScript migration of the UK Dating Statistic Calculator at the repository root so it achieves full functional, statistical, and visual parity with both the legacy Streamlit application (`archive/streamlit_legacy/`) and the V3 statistical audit (`archive/v3_legacy/`), while remaining 100% client-side and Vercel-ready.

## Scope & Out-of-Scope
- **In Scope**:
  1. **Handoff & Repo Governance**: Switch the project to the `- Base Prompts and Skill` handoff protocol (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `SHARED_NOTES.md`, `docs/HANDOFF.md`, `docs/PLAN.md`, `docs/ACTIVE.md`, `docs/DECISIONS.md`).
  2. **Toolchain & Fast Local Verification**: Ensure unit tests (`npm test`), TypeScript typechecking (`npx tsc --noEmit`), and production builds (`npm run build`) run cleanly and deterministically from the project root without hanging on SMB/UNC paths.
  3. **Model & Data Layer Enhancements (`src/lib/data.ts`, `src/lib/calc.ts`)**:
     - Export regional distribution helper (`calculateRegionalPool`) using `UK_REGIONS` and the `regional_scale` normalization so regional estimates sum to the national estimate.
     - Export source-backed UK Marriage, Living Arrangements, Divorce, and Ethnicity/Interracial Marriage datasets (`MARRIAGE_STATISTICS_DATA`), with the ONS-verified 2022 marriage counts (`246,897` total, `239,097` opposite-sex, `7,800` same-sex — fixing the legacy `249,793` error flagged in earlier audits).
     - Export source-backed UK Fertility, Parental Age, and Maternal/Child Health datasets (`FERTILITY_AND_BIRTH_DATA`) from ONS Birth Characteristics, HFEA, and MBRRACE-UK.
     - Compute `oneInN` odds, selectivity tier (`selectivityLabel`, `selectivityTone`), and empty-filter diagnostics in `calculateDatingPool()`.
  4. **Main Calculator UI Completion (`src/app/page.tsx`)**:
     - Add **1-in-N odds**, **Selectivity Reality Check badge**, **Active Criteria Summary chips**, and a **Reset to Defaults** action on the results dashboard.
     - Add empty multi-select warnings when a user deselects all options in Ethnicity, Body Type, Children, or Marital Status.
     - Sync the Marital Status filter UI when `mustBeSingle` is checked so "Currently married" is clearly shown as excluded by the single/available rule.
     - Add tabbed dashboard views under the headline result:
       1. **📊 Filter Cascade & Criteria**: Interactive funnel, step-by-step table, and active filter breakdown.
       2. **🗺️ UK Regional Map & Breakdown**: Interactive SVG UK regional bubble/choropleth map + ranked 12-region breakdown table with top-region metrics.
       3. **💍 Marriage & Union Statistics**: Orientation-aware UK marriage, cohabitation, divorce, and ethnic/interfaith marriage statistics with interactive visual bars.
       4. **👶 Fertility & Maternal Age Insights**: ONS parental age trends, maternal age pregnancy/genetic risk matrix, and HFEA IVF success rates by age bracket.
  5. **Methodology & Source Library Completion (`src/app/methodology/page.tsx`)**:
     - Include all 13 active datasets (`CHILDREN_DISTRIBUTION`, `MARRIAGE_HISTORY`, `BALDNESS_BY_AGE`, plus regional and marriage/fertility sources) in the dataset wiring cards and official links.
  6. **Comprehensive Test Coverage (`src/lib/calc.test.ts`)**:
     - Expand unit tests to verify regional math reconciliation, `oneInN` and selectivity tiers, empty-filter edge cases, and ONS-corrected marriage/fertility data integrity.
- **Out of Scope**:
  - Deleting or modifying archived files inside `archive/`.
  - Introducing server-side Python/FastAPI dependencies that break static/edge Vercel deployment.

## Deliverables
- Handoff protocol files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `SHARED_NOTES.md`, `docs/HANDOFF.md`, `docs/PLAN.md`, `docs/ACTIVE.md`, `docs/DECISIONS.md`)
- Enhanced `src/lib/data.ts`, `src/lib/calc.ts`, and expanded `src/lib/calc.test.ts`
- Feature-complete `src/app/page.tsx` and `src/app/methodology/page.tsx`
- Clean test, typecheck, and build verification

## Acceptance Criteria
1. All unit tests in `src/lib/calc.test.ts` pass (`npm test`).
2. TypeScript compiles cleanly with zero errors (`npx tsc --noEmit`).
3. Next.js production build succeeds (`npm run build`).
4. All 4 dashboard tabs (Cascade, Regional Map, Marriage Stats, Fertility & Maternal Age) and `/methodology` render cleanly on desktop and mobile viewports without horizontal overflow or layout shift.

## Numbered Steps
1. Initialize handoff protocol files and restore `SHARED_NOTES.md` history in project root.
2. Repair/verify root `node_modules` and `npm test` / `tsc` execution on the workspace.
3. Expand `src/lib/data.ts` and `src/lib/calc.ts` with regional breakdown math, `oneInN`/selectivity metadata, and source-corrected Marriage & Fertility datasets.
4. Expand `src/lib/calc.test.ts` to test all new calculations and data invariants.
5. Upgrade `src/app/page.tsx` with the 4-tab analytical dashboard (Filter Cascade + Active Criteria, Interactive UK Regional Map + Table, Marriage Statistics, Fertility & Maternal Age) and UX fixes.
6. Update `src/app/methodology/page.tsx` and `README.md` to document all datasets and features.
7. Run full verification (`npm test`, `npx tsc --noEmit`, `npm run build`), checkpoint `docs/HANDOFF.md`, `docs/ACTIVE.md`, and `SHARED_NOTES.md`.
