# UK Dating Pool Calculator: V3

V3 estimates how many UK adults meet a selected set of demographic filters. It includes a requirements calculator and a separate explorer for selected source tables.

The calculator's output is a modelled population estimate. It is not a measured joint count, a personal chance of finding a partner, or a compatibility score. Filter rates come from different sources and years; remaining correlations are unknown. Combined results do not have a statistical confidence interval.

## Run locally

Requires Node.js 20 or later. No third party JavaScript packages are needed at runtime.

```powershell
npm start
```

Open the localhost URL printed by the server. It binds to `127.0.0.1` on a random available port. Run the model tests with:

```powershell
npm test
```

## Data and method

- ONS mid-2024 population estimates provide the single-age starting population, including the published 90+ group.
- ONS 2025 relationship estimates retain their published age bands and cover England and Wales. The calculator applies these rates to single ages and, for other UK locations, uses them as an explicit geographic proxy.
- HMRC 2023/24 taxpayer counts approximate income shares. They are not age or region specific, do not cover every adult in the same way, and are not salary-only.
- ONS 2024 orientation estimates are age-banded and sex-specific; reliability markers are preserved.
- Optional height and BMI filters use NHS Health Survey for England data. The height standard deviation is a user-selected assumption, not a source estimate.
- Education and ethnicity filters use supported joint Census 2021 age, sex, country and qualification groups. Remaining filters are applied separately, so the final combination is still modelled.

The app displays denominators, source cells, reference periods, quality flags and relevant caveats. Data snapshots and source fingerprints live in `data/` and `sources/`; extraction scripts are in `scripts/`. The full review and known limitations are recorded in [`AUDIT.md`](AUDIT.md).

`calculator.html` is the requirements calculator served at `/`. `index.html` is the selected source-table explorer. The lightweight server uses Node.js built-ins; the browser app uses native ES modules.
