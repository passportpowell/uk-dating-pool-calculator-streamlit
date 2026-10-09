# UK Dating Pool Calculator

A browser based demographic estimator for exploring how selected characteristics change an estimated UK adult population. It also includes an evidence explorer for selected source tables.

**The result is a modelled population estimate, not a measured joint count, a probability of finding a partner, or a personal compatibility score.** The filters rely on sources with different years, age bands and geographic coverage. Remaining relationships between filters are not known, so the combined estimate has no statistical confidence interval.

## Current calculator

The recommended version is the JavaScript application in [`v3/`](v3/README.md). It runs locally with Node.js 20 or later and uses no third party JavaScript packages at runtime.

```powershell
cd v3
npm start
```

Open the localhost address printed by the server. Run the model tests with:

```powershell
npm test
```

The local server binds to loopback on an operating system assigned port. This repository does not currently advertise a verified public demo.

## How the estimate is built

- The starting population uses ONS mid-2024 single-age estimates, including the published 90+ group.
- Relationship filters use ONS 2025 living-arrangement and marital-status estimates for England and Wales. Published age bands are retained; applying them to single ages and other UK geographies is an approximation.
- Income filters use HMRC 2023/24 taxpayer counts. They are not age or region specific and do not represent salary alone.
- Orientation filters use ONS 2024 age-band and sex estimates. Reliability flags are retained in the exported rows.
- Optional height and BMI filters use NHS Health Survey for England data. The height spread is a user-set model assumption.
- Education and ethnicity filters use supported joint Census 2021 age, sex, country, qualification and ethnicity counts. Other filters are combined with these rates; the full set of characteristics is not jointly observed.

Each result shows its sources, denominators, assumptions and limitations. Read the in-app notes before interpreting a filtered estimate. Source records and their pinned snapshot details are in [`v3/data/`](v3/data/), with the methodology documented in [`v3/AUDIT.md`](v3/AUDIT.md).

## Other material

The repository retains an earlier Python/Streamlit analysis in `app.py`. It is a separate legacy implementation and should not be assumed to use the same calculations or evidence as V3.

No repository license file is present. Do not infer a reuse license from a README badge or from the public availability of the source data.

## Author

[Otis Powell](https://github.com/passportpowell) · [LinkedIn](https://www.linkedin.com/in/otispowell/)
