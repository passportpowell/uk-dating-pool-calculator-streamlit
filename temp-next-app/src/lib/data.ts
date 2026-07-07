/**
 * UK Dating Pool Calculator — framework-neutral data layer
 * Ported from the Streamlit app's data.py, with corrections and source metadata.
 *
 * Design goals (agreed by codex/gemini/claude in SHARED_NOTES):
 *  - Every dataset carries {geography, period, source} so correctness is auditable.
 *  - Distributions are normalised at load so they sum to exactly 1.0.
 *  - Known corrections vs the original Streamlit data are called out in `notes`.
 *
 * KNOWN GEOGRAPHY CAVEAT: ethnicity, education, marriage and body-type figures are
 * England & Wales (Census 2021 / HSE). They are currently applied to a UK-wide adult
 * population. Either scope the whole tool to England & Wales or re-source these UK-wide.
 * This mismatch is flagged per-record via `geography` and in DATA_QUALITY_NOTES.
 */

export type Distribution = Record<string, number>;

export interface Sourced<T> {
  value: T;
  geography: string;
  period: string;
  source: string;
  notes?: string;
}

/** Normalise a distribution so its values sum to exactly 1.0. */
export function normalize(dist: Distribution): Distribution {
  const s = Object.values(dist).reduce((a, b) => a + b, 0);
  const out: Distribution = {};
  for (const k of Object.keys(dist)) out[k] = dist[k] / s;
  return out;
}

// ── Population ────────────────────────────────────────────────────────────────
export const UK_TOTAL_POPULATION = 69_281_437; // ONS mid-2024 estimate.
export const UK_ADULT_POPULATION = 55_022_253; // ONS mid-2024, ages 18+ from single-year age table.

// UK adult gender split, ages 18+ (ONS mid-2024): 26,625,856 male / 28,396,397 female.
export const GENDER_SPLIT = { male: 0.483910679703, female: 0.516089320297 };

// ── Age (share of adults 18+) ────────────────────────────────────────────────
export const AGE_DISTRIBUTION: Sourced<Distribution> = {
  geography: "UK",
  period: "mid-2024",
  source: "ONS Mid-Year Population Estimates, MYE2 single-year age table",
  value: {
    "18-24": 0.105257794515,
    "25-34": 0.169851223649,
    "35-44": 0.16911143206,
    "45-54": 0.154727888006,
    "55-64": 0.161845426431,
    "65+": 0.239206235339,
  },
};

export const AGE_SINGLE_YEAR_DISTRIBUTION: Sourced<Distribution> = {
  geography: "UK",
  period: "mid-2024",
  source: "ONS Mid-Year Population Estimates, MYE2 single-year age table",
  notes: "Values are shares of UK adults aged 18+; 90+ is grouped by ONS.",
  value: {
    "18": 0.014665266433,
    "19": 0.014873073264,
    "20": 0.014924325254,
    "21": 0.014881233598,
    "22": 0.014958075235,
    "23": 0.015254119093,
    "24": 0.015701701637,
    "25": 0.016215675501,
    "26": 0.016456941521,
    "27": 0.016782682454,
    "28": 0.016520661195,
    "29": 0.016699134439,
    "30": 0.017091357564,
    "31": 0.017113512237,
    "32": 0.017538594794,
    "33": 0.017747019556,
    "34": 0.017685644388,
    "35": 0.017545301171,
    "36": 0.017714160124,
    "37": 0.017304580385,
    "38": 0.017173887809,
    "39": 0.017059134238,
    "40": 0.016508775095,
    "41": 0.01648974643,
    "42": 0.016352820013,
    "43": 0.016478460088,
    "44": 0.016484566708,
    "45": 0.015789157162,
    "46": 0.014649018462,
    "47": 0.014362225407,
    "48": 0.01466606611,
    "49": 0.014928596254,
    "50": 0.015104343328,
    "51": 0.015681328062,
    "52": 0.016258458191,
    "53": 0.016856307211,
    "54": 0.01643238782,
    "55": 0.016800675174,
    "56": 0.016751331502,
    "57": 0.016827209893,
    "58": 0.016732339186,
    "59": 0.016794913869,
    "60": 0.016545523863,
    "61": 0.016140378694,
    "62": 0.015701120054,
    "63": 0.015094801734,
    "64": 0.014457132462,
    "65": 0.014044372192,
    "66": 0.013607966944,
    "67": 0.012973696297,
    "68": 0.012430152578,
    "69": 0.011874940853,
    "70": 0.011781033394,
    "71": 0.011492041229,
    "72": 0.01102848333,
    "73": 0.0109845193,
    "74": 0.010995769294,
    "75": 0.011113521651,
    "76": 0.011532879252,
    "77": 0.012246517786,
    "78": 0.009182175801,
    "79": 0.008664494346,
    "80": 0.008396184722,
    "81": 0.007540839885,
    "82": 0.006495735462,
    "83": 0.005548173391,
    "84": 0.005467169801,
    "85": 0.005113149402,
    "86": 0.004654534957,
    "87": 0.004084565567,
    "88": 0.003550654314,
    "89": 0.003039333922,
    "90+": 0.01136332967,
  },
};

// ── Ethnicity (Census 2021, England & Wales) ─────────────────────────────────
export const ETHNICITY_DISTRIBUTION: Sourced<Distribution> = {
  geography: "UK (adjusted approximation)",
  period: "Census 2021",
  source: "ONS Census 2021 — Ethnic group, adjusted for Scotland and Northern Ireland mix",
  notes:
    "Approximate UK-wide adjustment from England & Wales census categories. Replace with harmonised UK census data before final release.",
  value: normalize({
    "White British": 0.785,
    "White Irish": 0.012,
    "White Other": 0.055,
    "Asian/Asian British - Indian": 0.027,
    "Asian/Asian British - Pakistani": 0.022,
    "Asian/Asian British - Bangladeshi": 0.009,
    "Asian/Asian British - Chinese": 0.008,
    "Asian/Asian British - Other": 0.018,
    "Black/Black British - African": 0.022,
    "Black/Black British - Caribbean": 0.009,
    "Black/Black British - Other": 0.004,
    "Mixed - White & Black Caribbean": 0.008,
    "Mixed - White & Black African": 0.004,
    "Mixed - White & Asian": 0.007,
    "Mixed - Other": 0.006,
    Arab: 0.005,
    "Other ethnic group": 0.016,
  }),
};

// ── Height (cm), normal distribution parameters ──────────────────────────────
export const HEIGHT = {
  geography: "England",
  period: "HSE 2024",
  source: "NHS Health Survey for England 2024, Adult and child overweight and obesity Table 1",
  notes: "Means are age-band specific. Standard deviations are retained from the previous anthropometric model because HSE Table 1 publishes means and standard errors, not full height distributions.",
  male: {
    std: 7.1,
    meansByAge: [
      { min: 18, max: 24, mean: 177.7045 },
      { min: 25, max: 34, mean: 177.6362 },
      { min: 35, max: 44, mean: 176.6255 },
      { min: 45, max: 54, mean: 176.3871 },
      { min: 55, max: 64, mean: 175.2743 },
      { min: 65, max: 74, mean: 174.0244 },
      { min: 75, max: 99, mean: 170.3811 },
    ],
  },
  female: {
    std: 6.5,
    meansByAge: [
      { min: 18, max: 24, mean: 164.1858 },
      { min: 25, max: 34, mean: 163.5577 },
      { min: 35, max: 44, mean: 163.4727 },
      { min: 45, max: 54, mean: 163.1705 },
      { min: 55, max: 64, mean: 161.8571 },
      { min: 65, max: 74, mean: 159.6522 },
      { min: 75, max: 99, mean: 157.4034 },
    ],
  },
};

// ── Income (share within gender) ─────────────────────────────────────────────
// Ordered brackets used by the income CDF in calc.ts.
export const INCOME_BRACKETS: Array<{ label: string; low: number; high: number }> = [
  { label: "Under £20k", low: 0, high: 20000 },
  { label: "£20k-£30k", low: 20000, high: 30000 },
  { label: "£30k-£40k", low: 30000, high: 40000 },
  { label: "£40k-£50k", low: 40000, high: 50000 },
  { label: "£50k-£75k", low: 50000, high: 75000 },
  { label: "£75k-£100k", low: 75000, high: 100000 },
  { label: "£100k-£150k", low: 100000, high: 150000 },
  { label: "£150k-£250k", low: 150000, high: 250000 },
  { label: "£250k-£500k", low: 250000, high: 500000 },
  { label: "£500k-£1M", low: 500000, high: 1000000 },
  { label: "£1M+", low: 1000000, high: 10000000 },
];

export const INCOME_DISTRIBUTION_MALE: Sourced<Distribution> = {
  geography: "UK",
  period: "HMRC SPI 2023/24 + ONS mid-2024 adult population",
  source: "HMRC Personal Income Statistics Table 3.3, total income before tax by sex",
  notes:
    "Converted from rounded taxpayer counts into an all-adult approximation by assigning non-taxpayers to the under-20k bracket. The 70k-100k and 200k-300k HMRC bands are split linearly to fit app thresholds.",
  value: normalize({
    "Under £20k": 0.392320007,
    "£20k-£30k": 0.191543138,
    "£30k-£40k": 0.143469566,
    "£40k-£50k": 0.093142545,
    "£50k-£75k": 0.100090679,
    "£75k-£100k": 0.038496415,
    "£100k-£150k": 0.023172964,
    "£150k-£250k": 0.011004341,
    "£250k-£500k": 0.006046754,
    "£500k-£1M": 0.001614972,
    "£1M+": 0.000826265,
  }),
};

export const INCOME_DISTRIBUTION_FEMALE: Sourced<Distribution> = {
  geography: "UK",
  period: "HMRC SPI 2023/24 + ONS mid-2024 adult population",
  source: "HMRC Personal Income Statistics Table 3.3, total income before tax by sex",
  notes:
    "Converted from rounded taxpayer counts into an all-adult approximation by assigning non-taxpayers to the under-20k bracket. The 70k-100k and 200k-300k HMRC bands are split linearly to fit app thresholds.",
  value: normalize({
    "Under £20k": 0.57565039,
    "£20k-£30k": 0.179248093,
    "£30k-£40k": 0.10106916,
    "£40k-£50k": 0.058105963,
    "£50k-£75k": 0.054155932,
    "£75k-£100k": 0.017226364,
    "£100k-£150k": 0.009191307,
    "£150k-£250k": 0.003662436,
    "£250k-£500k": 0.001725571,
    "£500k-£1M": 0.000352157,
    "£1M+": 0.000140863,
  }),
};

// ── Education (highest qualification) ────────────────────────────────────────
// CORRECTED vs original data.py, which put degree+ at 41% (undergrad 27% + postgrad 14%).
// Census 2021 (E&W) reports Level 4+ ≈ 33.8% of usual residents 16+. Mapped to the app's
// 5 buckets below (degree+ = 0.224 + 0.114 = 0.338 to match the Census total).
export const EDUCATION_ORDER = [
  "Below GCSE",
  "GCSE/O-Level",
  "A-Level or equivalent",
  "Undergraduate degree",
  "Postgraduate degree",
] as const;

export const EDUCATION_DISTRIBUTION: Sourced<Distribution> = {
  geography: "England & Wales",
  period: "Census 2021",
  source: "ONS Census 2021 — Highest level of qualification (16+)",
  notes:
    "Corrected: original app overstated degree+ at 41%. Census 2021 Level 4+ ≈ 33.8%. " +
    "Undergrad/postgrad split approximated from APS higher-degree share (~11%).",
  value: {
    "Below GCSE": 0.278, // No qualifications + Level 1
    "GCSE/O-Level": 0.187, // Level 2 + apprenticeship
    "A-Level or equivalent": 0.197, // Level 3 + other
    "Undergraduate degree": 0.224, // Level 4+ minus postgrad share
    "Postgraduate degree": 0.114, // higher-degree share (APS)
  },
};

// ── Body type (BMI categories) ───────────────────────────────────────────────
export const BODY_TYPE_ORDER = [
  "Underweight (BMI < 18.5)",
  "Healthy weight (BMI 18.5-24.9)",
  "Overweight (BMI 25-29.9)",
  "Obese (BMI 30+)",
] as const;

export const BODY_TYPE_DISTRIBUTION_MALE: Sourced<Distribution> = {
  geography: "England",
  period: "HSE 2024",
  source: "NHS Health Survey for England 2024, Adult and child overweight and obesity Table 3",
  value: {
    "Underweight (BMI < 18.5)": 0.017667149548,
    "Healthy weight (BMI 18.5-24.9)": 0.287021591515,
    "Overweight (BMI 25-29.9)": 0.40326883659,
    "Obese (BMI 30+)": 0.292042422348,
  },
};

export const BODY_TYPE_DISTRIBUTION_FEMALE: Sourced<Distribution> = {
  geography: "England",
  period: "HSE 2024",
  source: "NHS Health Survey for England 2024, Adult and child overweight and obesity Table 3",
  value: {
    "Underweight (BMI < 18.5)": 0.02756267701,
    "Healthy weight (BMI 18.5-24.9)": 0.354620925635,
    "Overweight (BMI 25-29.9)": 0.311848998824,
    "Obese (BMI 30+)": 0.305967398531,
  },
};

// ── Relationship availability ────────────────────────────────────────────────
export const SINGLE_RATE = 0.35; // Legacy fallback only; live calculation uses SINGLE_AVAILABILITY_BY_AGE.

export const SINGLE_AVAILABILITY_BY_AGE: Sourced<{ male: Distribution; female: Distribution }> = {
  geography: "England & Wales",
  period: "2024",
  source: "ONS Population estimates by marital status and living arrangements, Tables 5 and 6",
  notes:
    "Uses 'not living in a couple' by age and sex as the best available official proxy for dating availability. This is not the same as legal marital status or self-reported willingness to date.",
  value: {
    male: {
      "18-29": 0.79295308856,
      "30-34": 0.322917447711,
      "35-39": 0.231715562592,
      "40-44": 0.23926669259,
      "45-49": 0.214242116767,
      "50-54": 0.220779955069,
      "55-59": 0.243293229861,
      "60-64": 0.245385057997,
      "65-69": 0.286889161889,
      "70+": 0.31299631326,
    },
    female: {
      "18-29": 0.70401876962,
      "30-34": 0.247391998799,
      "35-39": 0.206127285724,
      "40-44": 0.242138336128,
      "45-49": 0.242289393749,
      "50-54": 0.290588802005,
      "55-59": 0.299269177148,
      "60-64": 0.310748195778,
      "65-69": 0.370596832496,
      "70+": 0.534421141468,
    },
  },
};

// ── Children (share of adults by number of children) ─────────────────────────
export const CHILDREN_ORDER = ["No children", "1 child", "2 children", "3+ children"] as const;
export const CHILDREN_DISTRIBUTION: Sourced<Distribution> = {
  geography: "UK",
  period: "2022",
  source: "ONS Families and Households 2022",
  notes: "Provenance weak — verify this is an adult child-count distribution, not a family/fertility stat.",
  value: {
    "No children": 0.43,
    "1 child": 0.18,
    "2 children": 0.24,
    "3+ children": 0.15,
  },
};

// ── Marriage history ─────────────────────────────────────────────────────────
export const MARRIAGE_ORDER = ["Never married", "Currently married", "Divorced", "Widowed"] as const;
export const MARRIAGE_HISTORY: Sourced<{ "opposite-sex": Distribution; "same-sex": Distribution }> = {
  geography: "England & Wales",
  period: "2022",
  source: "ONS Marriage statistics",
  notes: "Same-sex marriage legal since 2014, so currently-married rates are lower for same-sex couples.",
  value: {
    "opposite-sex": {
      "Never married": 0.42,
      "Currently married": 0.46,
      Divorced: 0.09,
      Widowed: 0.03,
    },
    "same-sex": {
      "Never married": 0.89,
      "Currently married": 0.08,
      Divorced: 0.02,
      Widowed: 0.01,
    },
  },
};

// ── Male pattern baldness by age ─────────────────────────────────────────────
export const BALDNESS_BY_AGE: Sourced<Distribution> = {
  geography: "UK/academic",
  period: "n/a",
  source: "British Association of Dermatologists; androgenetic alopecia research",
  value: {
    "18-29": 0.16,
    "30-39": 0.32,
    "40-49": 0.53,
    "50-59": 0.63,
    "60+": 0.8,
  },
};

// ── Sexual orientation ───────────────────────────────────────────────────────
export const SEXUAL_ORIENTATION_DISTRIBUTION: Sourced<Distribution> = {
  geography: "UK",
  period: "2024",
  source: "ONS Sexual orientation, UK 2024",
  notes:
    "ONS estimates 93.4% heterosexual or straight, 2.1% gay or lesbian, and 1.6% bisexual. Residual responses are mapped to the existing app buckets.",
  value: {
    "Heterosexual/Straight": 0.934,
    "Gay or Lesbian": 0.021,
    Bisexual: 0.016,
    Other: 0.011,
    "Prefer not to say": 0.018,
  },
};

// ── Salary benchmarks (dropdown labels) ──────────────────────────────────────
export const MIN_WAGE_ANNUAL = 24785; // NLW 21+ £12.71/hr (April 2026) × 37.5h × 52, rounded.
export const MEDIAN_SALARY = 34963; // ONS ASHE 2023 median full-time
export const AVERAGE_SALARY = 42200; // ONS ASHE 2023 mean full-time

// ── Regions (population + centroid for the map) ──────────────────────────────
export interface Region {
  population: number;
  adultPop: number;
  lat: number;
  lon: number;
}
export const UK_REGIONS: Record<string, Region> = {
  London: { population: 9_002_488, adultPop: 7_200_000, lat: 51.5074, lon: -0.1278 },
  "South East": { population: 9_278_144, adultPop: 7_400_000, lat: 51.3, lon: -0.8 },
  "North West": { population: 7_417_397, adultPop: 5_900_000, lat: 53.4808, lon: -2.2426 },
  "East of England": { population: 6_398_497, adultPop: 5_100_000, lat: 52.2405, lon: 0.5186 },
  "West Midlands": { population: 6_021_653, adultPop: 4_800_000, lat: 52.4862, lon: -1.8904 },
  "South West": { population: 5_764_881, adultPop: 4_700_000, lat: 50.7, lon: -3.5 },
  "Yorkshire and The Humber": { population: 5_541_262, adultPop: 4_400_000, lat: 53.9583, lon: -1.0803 },
  "East Midlands": { population: 4_934_939, adultPop: 3_900_000, lat: 52.8, lon: -1.2 },
  Scotland: { population: 5_479_900, adultPop: 4_400_000, lat: 55.9533, lon: -3.1883 },
  Wales: { population: 3_107_494, adultPop: 2_500_000, lat: 52.1307, lon: -3.7837 },
  "Northern Ireland": { population: 1_910_000, adultPop: 1_500_000, lat: 54.5973, lon: -5.9301 },
  "North East": { population: 2_647_000, adultPop: 2_100_000, lat: 54.9783, lon: -1.6178 },
};

// ── Outstanding data-quality notes (surface these in the UI) ──────────────────
export const DATA_QUALITY_NOTES = [
  "Geography mismatch remains for education/marriage/body-type: several inputs are England & Wales or England datasets applied to a UK adult pool.",
  "Adult population and age shares now use ONS mid-2024 single-year age estimates; update when the next ONS release lands.",
  "Income is an all-adult approximation from HMRC taxpayer counts plus ONS adult population; it is not a joint income-by-age dating-market model.",
  "Filters are multiplied as independent; real correlations (income×education×age) make niche 'high' criteria underestimates.",
  "Availability uses ONS 'not living in a couple' as a proxy. It is not the same as self-reported willingness to date.",
];
