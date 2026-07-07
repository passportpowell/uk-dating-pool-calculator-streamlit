/**
 * UK Dating Pool Calculator — calculation engine (TS port of calculations.py).
 * Pure functions, no dependencies. The only SciPy usage (norm.cdf) is replaced by
 * an erf-based normal CDF below, so this runs entirely client-side on Vercel.
 */

import {
  AGE_SINGLE_YEAR_DISTRIBUTION,
  BALDNESS_BY_AGE,
  BODY_TYPE_DISTRIBUTION_FEMALE,
  BODY_TYPE_DISTRIBUTION_MALE,
  CHILDREN_DISTRIBUTION,
  EDUCATION_DISTRIBUTION,
  EDUCATION_ORDER,
  ETHNICITY_DISTRIBUTION,
  GENDER_SPLIT,
  HEIGHT,
  INCOME_BRACKETS,
  INCOME_DISTRIBUTION_FEMALE,
  INCOME_DISTRIBUTION_MALE,
  MARRIAGE_HISTORY,
  SINGLE_AVAILABILITY_BY_AGE,
  SEXUAL_ORIENTATION_DISTRIBUTION,
  UK_ADULT_POPULATION,
  type Distribution,
} from "./data";

export type Gender = "Male" | "Female";
export type LookingFor = "Male" | "Female" | "Any";
export type Orientation = "Heterosexual/Straight" | "Gay or Lesbian" | "Bisexual";

// ── Unit helpers ─────────────────────────────────────────────────────────────
export function cmToFeetInches(cm: number): { feet: number; inches: number } {
  const totalInches = cm / 2.54;
  const feet = Math.floor(totalInches / 12);
  const inches = Math.round(totalInches % 12);
  return { feet, inches };
}

export function feetInchesToCm(feet: number, inches: number): number {
  return (feet * 12 + inches) * 2.54;
}

// ── Normal CDF (replaces scipy.stats.norm.cdf) ───────────────────────────────
// erf via Abramowitz & Stegun 7.1.26 (max abs error ~1.5e-7).
function erf(x: number): number {
  const sign = x < 0 ? -1 : 1;
  const ax = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * ax);
  const y =
    1 -
    ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) *
      t *
      Math.exp(-ax * ax);
  return sign * y;
}

export function normalCdf(x: number, mean: number, std: number): number {
  return 0.5 * (1 + erf((x - mean) / (std * Math.SQRT2)));
}

// ── Individual filter probabilities ──────────────────────────────────────────
export function ageProbability(minAge: number, maxAge: number): number {
  const lo = Math.max(18, Math.min(minAge, maxAge));
  const hi = Math.min(99, Math.max(minAge, maxAge));
  let probability = 0;
  for (const [ageKey, pct] of Object.entries(AGE_SINGLE_YEAR_DISTRIBUTION.value)) {
    if (ageKey === "90+") {
      if (hi >= 90) probability += pct;
      continue;
    }
    const age = Number(ageKey);
    if (age >= lo && age <= hi) probability += pct;
  }
  return probability;
}

function weightedAgeBandValue(
  ageRange: [number, number],
  bands: Array<{ min: number; max: number; mean?: number }>,
  valueForBand: (band: { min: number; max: number; mean?: number }) => number,
): number {
  let years = 0;
  let weighted = 0;
  for (const band of bands) {
    const overlapMin = Math.max(ageRange[0], band.min);
    const overlapMax = Math.min(ageRange[1], band.max);
    if (overlapMax >= overlapMin) {
      const overlapYears = overlapMax - overlapMin + 1;
      years += overlapYears;
      weighted += valueForBand(band) * overlapYears;
    }
  }
  return years > 0 ? weighted / years : valueForBand(bands[0]);
}

function heightParams(gender: Gender, ageRange?: [number, number]): { mean: number; std: number } {
  const params = gender === "Male" ? HEIGHT.male : HEIGHT.female;
  const defaultRange: [number, number] = [18, 99];
  const mean = weightedAgeBandValue(ageRange ?? defaultRange, params.meansByAge, (band) => band.mean ?? 0);
  return { mean, std: params.std };
}

export function heightProbability(minH: number, maxH: number, gender: Gender, ageRange?: [number, number]): number {
  const { mean, std } = heightParams(gender, ageRange);
  return normalCdf(maxH, mean, std) - normalCdf(minH, mean, std);
}

export function incomeProbability(minIncome: number, gender: Gender): number {
  const dist = gender === "Male" ? INCOME_DISTRIBUTION_MALE.value : INCOME_DISTRIBUTION_FEMALE.value;
  let probability = 0;
  for (const b of INCOME_BRACKETS) {
    const pct = dist[b.label];
    if (minIncome <= b.low) {
      probability += pct;
    } else if (minIncome < b.high) {
      const width = b.high - b.low;
      const included = b.high - minIncome;
      probability += pct * (included / width);
    }
  }
  return probability;
}

export function educationProbability(minLevel: string): number {
  if (minLevel === "Any") return 1.0;
  const idx = EDUCATION_ORDER.indexOf(minLevel as (typeof EDUCATION_ORDER)[number]);
  if (idx === -1) return 1.0;
  let probability = 0;
  for (let i = idx; i < EDUCATION_ORDER.length; i++) {
    probability += EDUCATION_DISTRIBUTION.value[EDUCATION_ORDER[i]];
  }
  return probability;
}

export function ethnicityProbability(selected: string[]): number {
  return selected.reduce((sum, e) => sum + (ETHNICITY_DISTRIBUTION.value[e] ?? 0), 0);
}

export function bodyTypeProbability(selected: string[], gender: Gender): number {
  const dist = gender === "Male" ? BODY_TYPE_DISTRIBUTION_MALE.value : BODY_TYPE_DISTRIBUTION_FEMALE.value;
  return selected.reduce((sum, b) => sum + (dist[b] ?? 0), 0);
}

export function childrenProbability(acceptable: string[]): number {
  return acceptable.reduce((sum, c) => sum + (CHILDREN_DISTRIBUTION.value[c] ?? 0), 0);
}

function ageBandProbability(ageRange: [number, number], dist: Distribution): number {
  let totalYears = 0;
  let weighted = 0;
  for (const [band, value] of Object.entries(dist)) {
    let lo: number;
    let hi: number;
    if (band.endsWith("+")) {
      lo = Number(band.replace("+", ""));
      hi = 99;
    } else {
      [lo, hi] = band.split("-").map(Number);
    }
    const overlapMin = Math.max(ageRange[0], lo);
    const overlapMax = Math.min(ageRange[1], hi);
    if (overlapMax >= overlapMin) {
      const years = overlapMax - overlapMin + 1;
      totalYears += years;
      weighted += value * years;
    }
  }
  return totalYears > 0 ? weighted / totalYears : 0;
}

export function singleAvailabilityProbability(ageRange: [number, number], gender: Gender): number {
  const dist = gender === "Male" ? SINGLE_AVAILABILITY_BY_AGE.value.male : SINGLE_AVAILABILITY_BY_AGE.value.female;
  return ageBandProbability(ageRange, dist);
}

/**
 * Marriage-history probability. When `mustBeSingle` is true the distribution is
 * renormalised over unmarried people, so it does NOT double-count with the single filter.
 */
export function marriageProbability(
  acceptable: string[],
  userGender: Gender,
  lookingFor: LookingFor,
  orientation: Orientation,
  mustBeSingle = false,
): number {
  const unmarried = ["Never married", "Divorced", "Widowed"];
  const sumOver = (dist: Distribution, keys: string[]) => keys.reduce((s, k) => s + (dist[k] ?? 0), 0);

  const sameSexAttracted =
    (userGender === "Male" && lookingFor === "Male") || (userGender === "Female" && lookingFor === "Female");

  let key: "opposite-sex" | "same-sex" = "opposite-sex";
  if (orientation === "Gay or Lesbian" && sameSexAttracted) key = "same-sex";
  else if (orientation === "Bisexual" && sameSexAttracted) key = "same-sex";
  else if (orientation === "Bisexual" && lookingFor === "Any") {
    // Blend opposite- and same-sex pools.
    const blend = (dist: Distribution) => {
      if (mustBeSingle) {
        const denom = sumOver(dist, unmarried);
        return denom > 0 ? sumOver(dist, acceptable.filter((s) => s !== "Currently married")) / denom : 0;
      }
      return sumOver(dist, acceptable);
    };
    return (blend(MARRIAGE_HISTORY.value["opposite-sex"]) + blend(MARRIAGE_HISTORY.value["same-sex"])) / 2;
  }

  const dist = MARRIAGE_HISTORY.value[key];
  if (mustBeSingle) {
    const denom = sumOver(dist, unmarried);
    return denom > 0 ? sumOver(dist, acceptable.filter((s) => s !== "Currently married")) / denom : 0;
  }
  return sumOver(dist, acceptable);
}

export function baldnessProbability(pref: "Any" | "Not bald" | "Bald or balding", ageRange: [number, number]): number {
  const bands: Array<[number, number, string]> = [
    [18, 29, "18-29"],
    [30, 39, "30-39"],
    [40, 49, "40-49"],
    [50, 59, "50-59"],
    [60, 99, "60+"],
  ];
  let totalYears = 0;
  let weighted = 0;
  for (const [lo, hi, key] of bands) {
    const overlapMin = Math.max(ageRange[0], lo);
    const overlapMax = Math.min(ageRange[1], hi);
    if (overlapMax >= overlapMin) {
      const years = overlapMax - overlapMin + 1;
      totalYears += years;
      weighted += BALDNESS_BY_AGE.value[key] * years;
    }
  }
  const avg = totalYears > 0 ? weighted / totalYears : 0;
  if (pref === "Not bald") return 1 - avg;
  if (pref === "Bald or balding") return avg;
  return 1.0;
}

export function orientationProbability(orientation: Orientation, lookingFor: LookingFor, userGender?: Gender): number {
  const raw = SEXUAL_ORIENTATION_DISTRIBUTION.value;
  const total = raw["Heterosexual/Straight"] + raw["Gay or Lesbian"] + raw["Bisexual"];
  const straight = raw["Heterosexual/Straight"] / total;
  const gay = raw["Gay or Lesbian"] / total;
  const bi = raw["Bisexual"] / total;

  if (lookingFor === "Any") {
    if (orientation === "Bisexual") return straight * 0.5 + gay * 0.5 + bi;
    return bi;
  }
  if (orientation === "Heterosexual/Straight") {
    if (userGender === "Male" && lookingFor === "Male") return bi;
    if (userGender === "Female" && lookingFor === "Female") return bi;
    return straight + bi;
  }
  if (orientation === "Gay or Lesbian") {
    if (userGender === "Male" && lookingFor === "Female") return bi;
    if (userGender === "Female" && lookingFor === "Male") return bi;
    return gay + bi;
  }
  if (orientation === "Bisexual") {
    if (userGender === "Male") return lookingFor === "Male" ? gay + bi : straight + bi;
    if (userGender === "Female") return lookingFor === "Female" ? gay + bi : straight + bi;
    return straight + gay + bi;
  }
  return 1.0;
}

// ── Orchestrator ─────────────────────────────────────────────────────────────
export interface CalculatorInput {
  userGender: Gender;
  orientation: Orientation;
  lookingFor: LookingFor;
  ageRange: [number, number];
  minHeightCm: number;
  maxHeightCm: number;
  minIncome: number;
  educationLevel: string; // "Any" | one of EDUCATION_ORDER
  selectedEthnicities: string[]; // all keys => "Any"
  selectedBodyTypes: string[];
  mustBeSingle: boolean;
  acceptableChildren: string[];
  acceptableMarriage: string[];
  baldnessPreference: "Any" | "Not bald" | "Bald or balding";
}

export interface FilterStep {
  criterion: string;
  probability: number;
  remaining: number;
}

export interface CalculatorResult {
  totalProbability: number;
  percentage: number;
  targetPercentage: number;
  basePopulation: number;
  baseLabel: string;
  estimatedMatches: number;
  steps: FilterStep[];
}

/** Blend a per-gender probability by the population gender split (used when lookingFor === "Any"). */
function blendByGender(fn: (g: Gender) => number): number {
  return GENDER_SPLIT.male * fn("Male") + GENDER_SPLIT.female * fn("Female");
}

export function calculateDatingPool(input: CalculatorInput): CalculatorResult {
  const genderProb =
    input.lookingFor === "Any" ? 1.0 : input.lookingFor === "Male" ? GENDER_SPLIT.male : GENDER_SPLIT.female;
  const basePopulation = Math.round(UK_ADULT_POPULATION * genderProb);
  const baseLabel =
    input.lookingFor === "Any"
      ? "UK adults aged 18+"
      : input.lookingFor === "Male"
      ? "UK adult men aged 18+"
      : "UK adult women aged 18+";

  const ageProb = ageProbability(input.ageRange[0], input.ageRange[1]);

  const heightProb =
    input.lookingFor === "Any"
      ? blendByGender((g) => heightProbability(input.minHeightCm, input.maxHeightCm, g, input.ageRange))
      : heightProbability(input.minHeightCm, input.maxHeightCm, input.lookingFor, input.ageRange);

  const incomeProb =
    input.lookingFor === "Any"
      ? blendByGender((g) => incomeProbability(input.minIncome, g))
      : incomeProbability(input.minIncome, input.lookingFor);

  const bodyProb =
    input.lookingFor === "Any"
      ? blendByGender((g) => bodyTypeProbability(input.selectedBodyTypes, g))
      : bodyTypeProbability(input.selectedBodyTypes, input.lookingFor);

  const educationProb = educationProbability(input.educationLevel);
  const ethnicityProb = ethnicityProbability(input.selectedEthnicities);
  const orientationProb = orientationProbability(input.orientation, input.lookingFor, input.userGender);
  const singleProb = input.mustBeSingle
    ? input.lookingFor === "Any"
      ? blendByGender((g) => singleAvailabilityProbability(input.ageRange, g))
      : singleAvailabilityProbability(input.ageRange, input.lookingFor)
    : 1.0;
  const childrenProb = childrenProbability(input.acceptableChildren);
  const marriageProb = marriageProbability(
    input.acceptableMarriage,
    input.userGender,
    input.lookingFor,
    input.orientation,
    input.mustBeSingle,
  );

  let baldnessProb = 1.0;
  if (input.lookingFor === "Male") {
    baldnessProb = baldnessProbability(input.baldnessPreference, input.ageRange);
  } else if (input.lookingFor === "Any") {
    baldnessProb = GENDER_SPLIT.male * baldnessProbability(input.baldnessPreference, input.ageRange) + GENDER_SPLIT.female * 1.0;
  }

  const factors: Array<[string, number]> = [
    ["Gender", genderProb],
    ["Age Range", ageProb],
    ["Height Range", heightProb],
    ["Body Type", bodyProb],
    ["Income", incomeProb],
    ["Education", educationProb],
    ["Ethnicity", ethnicityProb],
    ["Orientation", orientationProb],
    ["Single/Available", singleProb],
    ["Children", childrenProb],
    ["Marriage History", marriageProb],
    ["Baldness", baldnessProb],
  ];

  let cumulative = 1.0;
  const steps: FilterStep[] = factors.map(([criterion, probability]) => {
    cumulative *= probability;
    return { criterion, probability, remaining: Math.round(UK_ADULT_POPULATION * cumulative) };
  });

  const totalProbability = cumulative;
  const targetProbability = genderProb > 0 ? cumulative / genderProb : cumulative;
  return {
    totalProbability,
    percentage: totalProbability * 100,
    targetPercentage: targetProbability * 100,
    basePopulation,
    baseLabel,
    estimatedMatches: Math.round(UK_ADULT_POPULATION * totalProbability),
    steps,
  };
}
