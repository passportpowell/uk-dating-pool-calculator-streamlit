# Audit remediation specification

Date: 2026-10-13. Owner: Codex. Scope: both audits in docs/audit and the earlier adversarial audit, preserving archived work and remote history.

## Decision
Use observed ONS population-by-sex-and-single-age counts and retained Census joint qualification/ethnicity tables. Apply remaining rates inside each stratum and sum. Keep unsupported data explicitly unavailable rather than inventing it. Remove false confidence intervals, unsourced correlation boosts, degree/postgraduate splits, and unverified medical/marriage reference figures. Source-backed household children data is an acceptable fallback only under its correct label.

## Tickets
1. Evidence recovery and engine regression tests — blocks 2, 3. Recover pinned files with fingerprints, retain prior engine code, validate numeric inputs and supported keys.
2. Stratum engine — blocked by 1; blocks 4. Correct Any/90+/sex-age integration, relationship taxonomy, joint education/ethnicity, nonresponse, local population denominators, same-scope relaxations.
3. Interface — blocked by contract from 1; blocks 4. Visible preferences, direct height units, exact versioned sharing, comparisons/export, plain per-stage source links, separate explorer/sources, accessible responsive layouts.
4. Verification and release — blocked by 2, 3. Tests/types/lint/build/browser, independent review, preserve remote commits and license, stage explicit scope, push fast-forward.

## Ownership and routing
JEV recommends inline (0.94 execution, low-confidence worker recommendation). Override: independent UI implementation and public children evidence review delegated; lead owns engine/config/docs/integration. One owner per path. Review required after integration.

## Acceptance
- Any equals male plus female; national totals reconcile to regional calculations; 90+ included once.
- Missing/suppressed source values never become zero; invalid inputs reject; output remains finite, bounded, and nonnegative.
- Result and funnel agree; relaxations apply the exact displayed patch in the same location.
- Full criteria survive URL/export round trips; all inputs are visible and labelled.
- Every active source has URL/table/reference/geography and retained evidence hash; unknown children/co-parent/medical rates do not silently change counts.
- Verification is recorded honestly. GitHub includes src/lib, provenance, tests and source files, excludes credentials, and preserves existing remote history.

## Audit disposition
All Codex A01–A22 and Claude P0-1–P2-19 are covered by the tickets. Unsupported recommendations are not blindly applied: do not rescale invented education splits into official data, do not relabel arbitrary ranges as statistical confidence, do not assume family tables count adult parents, and do not delete/rotate unused credentials without necessity. Private .env stays ignored and untouched. Historical code is retained in docs/archive and existing archive stays intact.
