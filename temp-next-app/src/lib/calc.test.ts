import { describe, it, expect } from "vitest";
import {
  AGE_DISTRIBUTION,
  BODY_TYPE_DISTRIBUTION_FEMALE,
  BODY_TYPE_DISTRIBUTION_MALE,
  CHILDREN_DISTRIBUTION,
  EDUCATION_DISTRIBUTION,
  ETHNICITY_DISTRIBUTION,
  INCOME_DISTRIBUTION_FEMALE,
  INCOME_DISTRIBUTION_MALE,
  MARRIAGE_HISTORY,
  SEXUAL_ORIENTATION_DISTRIBUTION,
  GENDER_SPLIT,
  UK_ADULT_POPULATION,
  type Distribution,
} from "./data";
import {
  ageProbability,
  calculateDatingPool,
  educationProbability,
  incomeProbability,
  marriageProbability,
  normalCdf,
  type CalculatorInput,
} from "./calc";

const sum = (d: Distribution) => Object.values(d).reduce((a, b) => a + b, 0);

describe("distributions sum to 1.0", () => {
  const cases: Array<[string, Distribution]> = [
    ["age", AGE_DISTRIBUTION.value],
    ["ethnicity", ETHNICITY_DISTRIBUTION.value],
    ["income male", INCOME_DISTRIBUTION_MALE.value],
    ["income female", INCOME_DISTRIBUTION_FEMALE.value],
    ["education", EDUCATION_DISTRIBUTION.value],
    ["body male", BODY_TYPE_DISTRIBUTION_MALE.value],
    ["body female", BODY_TYPE_DISTRIBUTION_FEMALE.value],
    ["children", CHILDREN_DISTRIBUTION.value],
    ["marriage opposite-sex", MARRIAGE_HISTORY.value["opposite-sex"]],
    ["marriage same-sex", MARRIAGE_HISTORY.value["same-sex"]],
  ];
  it.each(cases)("%s", (_name, dist) => {
    expect(sum(dist)).toBeCloseTo(1.0, 6);
  });

  it("orientation distribution sums to 1.0", () => {
    expect(sum(SEXUAL_ORIENTATION_DISTRIBUTION.value)).toBeCloseTo(1.0, 6);
  });
});

describe("normal CDF", () => {
  it("is 0.5 at the mean", () => {
    expect(normalCdf(175.3, 175.3, 7.1)).toBeCloseTo(0.5, 4);
  });
  it("covers ~full mass over a wide range", () => {
    expect(normalCdf(210, 175.3, 7.1) - normalCdf(140, 175.3, 7.1)).toBeCloseTo(1.0, 3);
  });
});

describe("filter probabilities are valid", () => {
  it("age over full adult range ≈ 1.0", () => {
    expect(ageProbability(18, 99)).toBeCloseTo(1.0, 6);
  });
  it("age 35-41 uses exact ONS single-year shares", () => {
    expect(ageProbability(35, 41)).toBeCloseTo(0.11979559, 6);
  });
  it("income at £0 minimum = everyone", () => {
    expect(incomeProbability(0, "Male")).toBeCloseTo(1.0, 6);
    expect(incomeProbability(0, "Female")).toBeCloseTo(1.0, 6);
  });
  it("education 'Any' = 1.0 and degree+ ≈ 0.338 (Census-corrected)", () => {
    expect(educationProbability("Any")).toBe(1.0);
    expect(educationProbability("Undergraduate degree")).toBeCloseTo(0.338, 3);
  });
});

describe("availability double-count is fixed", () => {
  it("mustBeSingle renormalises marriage history over unmarried people", () => {
    // Default acceptable when single = never/divorced/widowed => the whole unmarried pool => 1.0
    const p = marriageProbability(
      ["Never married", "Divorced", "Widowed"],
      "Male",
      "Female",
      "Heterosexual/Straight",
      true,
    );
    expect(p).toBeCloseTo(1.0, 6);
  });
});

describe("README worked example reproduces", () => {
  it("female / 25-35 / any-height / 30k+ / degree+ / single ≈ prior ~0.37%", () => {
    const input: CalculatorInput = {
      userGender: "Male",
      orientation: "Heterosexual/Straight",
      lookingFor: "Female",
      ageRange: [25, 35],
      minHeightCm: 140,
      maxHeightCm: 210,
      minIncome: 30000,
      educationLevel: "Undergraduate degree",
      selectedEthnicities: Object.keys(ETHNICITY_DISTRIBUTION.value),
      selectedBodyTypes: Object.keys(BODY_TYPE_DISTRIBUTION_FEMALE.value),
      mustBeSingle: true,
      acceptableChildren: Object.keys(CHILDREN_DISTRIBUTION.value),
      acceptableMarriage: ["Never married", "Divorced", "Widowed"],
      baldnessPreference: "Any",
    };
    const r = calculateDatingPool(input);
    expect(r.percentage).toBeGreaterThan(0.2);
    expect(r.percentage).toBeLessThan(0.6);
    expect(r.estimatedMatches).toBeGreaterThan(0);
  });
});

describe("every step probability is a valid probability", () => {
  it("all steps in [0,1]", () => {
    const input: CalculatorInput = {
      userGender: "Female",
      orientation: "Heterosexual/Straight",
      lookingFor: "Male",
      ageRange: [25, 40],
      minHeightCm: 170,
      maxHeightCm: 195,
      minIncome: 34963,
      educationLevel: "A-Level or equivalent",
      selectedEthnicities: Object.keys(ETHNICITY_DISTRIBUTION.value),
      selectedBodyTypes: Object.keys(BODY_TYPE_DISTRIBUTION_MALE.value),
      mustBeSingle: true,
      acceptableChildren: Object.keys(CHILDREN_DISTRIBUTION.value),
      acceptableMarriage: ["Never married", "Divorced", "Widowed"],
      baldnessPreference: "Not bald",
    };
    const r = calculateDatingPool(input);
    for (const step of r.steps) {
      expect(step.probability).toBeGreaterThanOrEqual(0);
      expect(step.probability).toBeLessThanOrEqual(1.0000001);
    }
    expect(r.totalProbability).toBeGreaterThanOrEqual(0);
    expect(r.totalProbability).toBeLessThanOrEqual(1);
  });
});

describe("target denominator metadata", () => {
  it("reports percentages against the selected target gender pool", () => {
    const input: CalculatorInput = {
      userGender: "Female",
      orientation: "Heterosexual/Straight",
      lookingFor: "Male",
      ageRange: [35, 41],
      minHeightCm: 181,
      maxHeightCm: 210,
      minIncome: 75000,
      educationLevel: "Any",
      selectedEthnicities: Object.keys(ETHNICITY_DISTRIBUTION.value),
      selectedBodyTypes: Object.keys(BODY_TYPE_DISTRIBUTION_MALE.value),
      mustBeSingle: true,
      acceptableChildren: Object.keys(CHILDREN_DISTRIBUTION.value),
      acceptableMarriage: ["Never married", "Divorced", "Widowed", "Currently married"],
      baldnessPreference: "Any",
    };
    const r = calculateDatingPool(input);
    expect(r.basePopulation).toBe(Math.round(UK_ADULT_POPULATION * GENDER_SPLIT.male));
    expect(r.baseLabel).toBe("UK adult men aged 18+");
    expect(r.targetPercentage).toBeCloseTo(r.percentage / GENDER_SPLIT.male, 6);
  });
});
