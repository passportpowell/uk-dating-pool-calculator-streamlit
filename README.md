# UK Dating Pool Calculator

Estimate the number and share of selected-sex adults meeting requirements. Next.js/TypeScript app with separate calculator, explorer, sources and methodology pages.

## Run and verify

```sh
npm ci
npm test
npm run typecheck
npm run lint
npm run verify:evidence
npm run build
npm start -- --hostname 127.0.0.1 --port 3000
```

On the NAS, use a disposable local verification mirror containing source/config/public evidence/tests, excluding `.env`, credentials and `.git`. The NAS remains canonical. GitHub Actions repeats checks on Linux.

## Evidence and limits

The denominator is all selected-sex adults aged 18+ in the chosen location. Population is pinned to ONS mid-2024; age 90 includes the full 90+ group once. Calculate within local sex-and-age strata, then sum. Both-sex results add male and female counts; national results reconcile to twelve regions.

Qualification and ethnicity use observed joint Census 2021 counts. Other overlaps remain assumptions. England/England-and-Wales rates are disclosed proxies elsewhere. Income is HMRC taxable total income, including pensions/investments, not salary alone; sex-specific national rates are not age-conditioned. Unverified calibrated tails, degree/postgraduate splits, correlation boosts and confidence claims are removed. Height uses measured age/sex averages with an assumed spread and sensitivity comparison.

Children use Ipsos QD6/Table636/PDFpage172: under-18 children living permanently or temporarily with an adult who has parental responsibility. Published age rates are a proxy for both sexes; ages18–24 use16–24. Children living elsewhere, grown-up children, adoption-specific rates and different co-parent counts are not established by this filter. The old fixed43% childlessness multiplier is removed.

Single means not living in a couple. Partnered means a married/civil-partnered or cohabiting couple sharing a home; married people living apart are not identified by that category. Divorced/widowed describe legal status and can include new partners. Missing/suppressed source cells produce a visible error. Unsupported medical-risk and marriage-by-ethnicity claims are removed.

## Reproducibility

- `src/lib/calculator.ts`: validated pure engine; `calculator.test.ts`: regression tests.
- `public/evidence/`: active extracts, original official files, publisher/table metadata and fingerprints.
- `scripts/data/verify-evidence.mjs`: fingerprint and invariant checks.
- `scripts/data/prepare-evidence.mjs`: recovery from the existing local archive; not required on a fresh checkout because active evidence is committed.
- `scripts/data/children_inspect.py`: verifies the original Ipsos PDF's questions/counts and fingerprint. The full third-party PDF stays local/linked; the limited factual extraction is committed.
- `docs/audit/`: audit reports and dispositions; `docs/archive/`: pre-remediation engine and historical notes. Original local `archive/` remains intact.

Scenario links include every canonical requirement in `{v:1,criteria:...}`. Exports retain requirements, breakdown, source-cell rows and limitations. Comparisons stay in the current tab. The calculator uses no account, database, tracking service or project credential.

## Hosting and local remote access

Vercel Root Directory must be repository root, framework Next.js, build `npm run build`. Clear the historical `temp-next-app` dashboard setting. Git push does not confirm production deployment.

For a local preview on port3000, the configured footer MagicDNS link requires a local service:

```sh
tailscale serve https / http://127.0.0.1:3000
```

The link does not establish that service is running. No cloud or tailnet settings are changed by this project.

## Rights

Existing MIT `LICENSE` applies to project code. Original ONS/HMRC/NHS publisher attribution and applicable upstream terms, including Open Government Licence where supplied, remain attached to data. Third-party data are not relicensed under MIT. Ipsos retains publication rights; the original PDF is linked rather than redistributed, and the limited factual extraction retains attribution and coverage notes.
