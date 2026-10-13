import rawPopulation from "../../public/evidence/evidence.json";
import rawFilters from "../../public/evidence/filters.json";
import childrenEvidence from "../../public/evidence/children-ipsos-2025.json";
import manifest from "../../public/evidence/manifest.json";

export type Sex = "Males" | "Females" | "Persons";
export interface Criteria {
  geo: string;
  sex: Sex;
  min: number;
  max: number;
  relationship: string;
  income: number;
  orientation: string;
  bmi: string;
  education: string;
  ethnicity: string;
  heightMin: number | null;
  heightMax: number | null;
  spread: number;
  children: string;
}
export interface Source {
  id: string;
  title: string;
  url: string;
  file?: string;
  tables: string;
  reference: string;
  geography: string;
  sha256?: string;
  apiURL?: string;
  explanation: string;
}
type SourceRecord = Omit<Source, "explanation">;
interface Population {
  name: string;
  Males: number[];
  Females: number[];
  Persons: number[];
  sourceRows: Record<Sex, string>;
}
interface Relationship {
  mode: string;
  sex: Sex;
  age: string;
  category: string;
  count: number | string | null;
  cv: string;
  cell: string;
}
interface Evidence {
  population: Record<string, Population>;
  relationships: Relationship[];
  sources: SourceRecord[];
}
interface JointRow {
  country: string;
  sex: Sex;
  min: number;
  max: number;
  education: string;
  ethnicity: string;
  count: number;
  ref: string;
}
interface Health {
  min: number;
  max: number;
  mean: number;
  heightCell: string;
  bmi: (number | null)[];
  bmiCells: string[];
}
interface OrientationBand {
  min: number;
  max: number;
  categories: Record<string, { rate: number | null; cell: string; cv: string }>;
}
interface Filters {
  income: Record<
    string,
    { low: number; high: number | null; taxpayers: number; cell: string }[]
  >;
  health: Record<string, Health[]>;
  jointCensus: JointRow[];
  orientationByAgeSex: Record<string, OrientationBand[]>;
  sources: SourceRecord[];
  jointSource: SourceRecord;
  orientationSource: SourceRecord;
}
const evidence = rawPopulation as unknown as Evidence;
const filters = rawFilters as unknown as Filters;
export const SEX_LABELS = {
  Males: "Men",
  Females: "Women",
  Persons: "Men and women",
};
export const RELATIONSHIP_LABELS = {
  any: "No preference",
  partnered: "Married or living with partner",
  single: "Single",
  divorced: "Divorced",
  widowed: "Widowed",
};
export const ORIENTATION_LABELS = {
  any: "No preference",
  straight: "Straight",
  gay: "Gay or lesbian",
  bi: "Bisexual",
  straightBi: "Straight or bisexual",
  gayBi: "Gay, lesbian or bisexual",
};
export const BMI_LABELS = {
  any: "No preference",
  "0": "Underweight (BMI below 18.5)",
  "1": "Healthy weight (BMI 18.5–24.9)",
  "2": "Overweight (BMI 25–29.9)",
  "3": "Obese (BMI 30+)",
};
export const EDUCATION_LABELS = {
  any: "No preference",
  none: "No formal qualifications",
  level1plus: "GCSEs / Level 1 or higher",
  level2plus: "5+ GCSE passes / Level 2 or higher",
  level3plus: "A-levels / Level 3 or higher",
  level4: "HNC/HND, degree or postgraduate",
  apprenticeship: "Apprenticeship as highest qualification",
  other: "Other / unknown qualification level",
};
export const ETHNICITY_LABELS = {
  any: "No preference",
  White: "White",
  Asian: "Asian",
  Black: "Black",
  Mixed: "Mixed",
  Other: "Other ethnic group",
};
export const CHILDREN_LABELS = {
  any: "No preference",
  none: "No under-18 children living with them",
  one: "Up to 1 under-18 child living with them",
  two: "Up to 2 under-18 children living with them",
  threePlus: "3 or more under-18 children living with them",
};
export const childrenStatus = {
  available: true,
  label: "Children under 18 living with them",
  explanation:
    "Ipsos counts children aged 17 or under living permanently or temporarily with an adult who has parental responsibility. Published age rates are used for both sexes because joint age-and-sex rates are unavailable; ages 18–24 use the 16–24 band. Children living elsewhere, grown-up children and different co-parents are not counted. The question does not distinguish biological and adopted children.",
};
export const INCOME_OPTIONS = [
  0, 20000, 30000, 40000, 50000, 70000, 75000, 100000, 150000, 200000, 300000,
  500000, 1000000,
];
export const DEFAULT_CRITERIA: Criteria = {
  geo: "K02000001",
  sex: "Males",
  min: 25,
  max: 39,
  relationship: "single",
  income: 0,
  orientation: "any",
  bmi: "any",
  education: "any",
  ethnicity: "any",
  heightMin: null,
  heightMax: null,
  spread: 7,
  children: "any",
};
export const geographies = Object.entries(evidence.population)
  .filter(([code]) => code !== "K03000001")
  .map(([code, p]) => ({ code, name: p.name }));
const regions = geographies.filter(
  (g) =>
    g.code.startsWith("E12") ||
    ["W92000004", "S92000003", "N92000002"].includes(g.code),
);
const descriptions: Record<string, string> = {
  population:
    "We start with all adults of your selected sex in your chosen location, then keep your chosen ages. The final age option includes everyone aged 90 and over.",
  relationships:
    "We use the published age-and-sex groups. Single means not living with a partner; some people may be dating someone who lives elsewhere. Partnered means a married/civil-partnered or cohabiting couple sharing a home. Divorced and widowed describe legal marriage status and may include people with new partners. England-and-Wales rates are used as a proxy elsewhere.",
  income:
    "We divide published taxpayer counts by all UK adults of the same sex. This is total taxable income before tax, including pensions and investments. Rates are not specific to age or region. A threshold within a source band uses linear interpolation; this remains an approximation.",
  health:
    "Height uses measured average heights for each age and sex, plus a normal curve and your assumed spread. The spread is not an NHS statistic. BMI uses measured age-and-sex category shares. England survey rates are a proxy elsewhere; BMI does not describe appearance.",
  orientation:
    "We use reported sexual identity by age and sex. Other identities and unanswered questions are not assigned to any group. Identity does not establish attraction to a particular person. The 16–24 band is used for ages 18–24.",
  education:
    "Census counts combine age, sex, qualification and ethnicity. HNC/HND, degrees and postgraduate qualifications share one category. Apprenticeships and unknown-level qualifications stay separate. English regions use England rates; Scotland and Northern Ireland use an England-and-Wales proxy.",
  ethnicity:
    "This step uses ethnicity within the selected qualification, age and sex group, preserving the measured overlap between those preferences. These are 2021 Census counts. English regions use England rates; Scotland and Northern Ireland use an England-and-Wales proxy.",
  children: childrenStatus.explanation,
};
export const sourceLibrary: Source[] = [
  ...evidence.sources,
  ...filters.sources,
  filters.orientationSource,
  filters.jointSource,
  {
    ...filters.jointSource,
    id: "education",
    title: "Qualifications within the joint Census table",
  },
  manifest.sources.find((s) => s.id === "children")!,
].map((s) => ({
  ...s,
  file: s.file ? `/evidence/${s.file}` : undefined,
  explanation: descriptions[s.id],
}));
export interface Stage {
  label: string;
  sourceId: string;
  count: number;
  remainingPct: number;
  dropPct: number;
}
export interface Calculation {
  state: Criteria;
  count: number;
  base: number;
  p: number;
  oneIn: number | null;
  stages: Stage[];
  notes: string[];
  rows: {
    geo: string;
    sex: string;
    age: number | string;
    population: number;
    estimated: number;
    rates: number[];
    refs: string[];
  }[];
  heightSensitivity: { low: number; high: number } | null;
  relaxations: {
    label: string;
    patch: Partial<Criteria>;
    count: number;
    p: number;
  }[];
}
const sum = (a: number[]) => a.reduce((x, y) => x + y, 0);
const enumCheck = (
  key: string,
  value: unknown,
  labels: Record<string, string>,
) => {
  if (typeof value !== "string" || !Object.hasOwn(labels, value))
    throw Error(`Choose a supported ${key}.`);
};
export function validateCriteria(input: unknown): Criteria {
  if (input === null || typeof input !== "object" || Array.isArray(input))
    throw Error("Invalid saved criteria.");
  const incoming = input as Record<string, unknown>;
  if (Object.keys(incoming).some((k) => !Object.hasOwn(DEFAULT_CRITERIA, k)))
    throw Error("Saved criteria contain unsupported fields.");
  const c = { ...DEFAULT_CRITERIA, ...incoming } as Criteria;
  if (typeof c.geo !== "string" || !Object.hasOwn(evidence.population, c.geo))
    throw Error("Choose a supported location.");
  enumCheck("target group", c.sex, SEX_LABELS);
  enumCheck("relationship status", c.relationship, RELATIONSHIP_LABELS);
  enumCheck("orientation", c.orientation, ORIENTATION_LABELS);
  enumCheck("BMI category", c.bmi, BMI_LABELS);
  enumCheck("qualification", c.education, EDUCATION_LABELS);
  enumCheck("ethnic group", c.ethnicity, ETHNICITY_LABELS);
  enumCheck("children preference", c.children, CHILDREN_LABELS);
  if (!childrenStatus.available && c.children !== "any")
    throw Error(
      "The children preference cannot be calculated from verified data yet.",
    );
  if (
    !Number.isInteger(c.min) ||
    !Number.isInteger(c.max) ||
    c.min < 18 ||
    c.max > 90 ||
    c.min > c.max
  )
    throw Error(
      "Use whole ages 18–90 in ascending order. 90 includes everyone aged 90+.",
    );
  if (!INCOME_OPTIONS.includes(c.income))
    throw Error("Choose a supported income threshold.");
  for (const [name, v] of [
    ["Minimum height", c.heightMin],
    ["Maximum height", c.heightMax],
  ] as const) {
    if (v !== null && (!Number.isFinite(v) || v < 100 || v > 230))
      throw Error(`${name} must be 100–230 cm, or blank.`);
  }
  if (
    c.heightMin !== null &&
    c.heightMax !== null &&
    c.heightMin >= c.heightMax
  )
    throw Error("Minimum height must be below maximum height.");
  if (!Number.isFinite(c.spread) || c.spread < 3 || c.spread > 15)
    throw Error("Assumed height spread must be 3–15 cm.");
  return c;
}
export function cmToFeetInches(cm: number) {
  if (!Number.isFinite(cm) || cm < 0) throw Error("Invalid height.");
  const inches = Math.round(cm / 2.54);
  return { feet: Math.floor(inches / 12), inches: inches % 12 };
}
export function feetInchesToCm(feet: number, inches: number) {
  if (
    !Number.isInteger(feet) ||
    feet < 0 ||
    !Number.isFinite(inches) ||
    inches < 0 ||
    inches >= 12
  )
    throw Error(
      "Use whole feet and inches from 0 up to, but not including, 12.",
    );
  return (feet * 12 + inches) * 2.54;
}
export function normalCDF(x: number) {
  const z = Math.abs(x) / Math.SQRT2,
    t = 1 / (1 + 0.3275911 * z);
  const erf =
    1 -
    ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) *
      t +
      0.254829592) *
      t *
      Math.exp(-z * z);
  return (1 + (x < 0 ? -erf : erf)) / 2;
}
function bandIncludes(band: string, age: number) {
  const ns = band.match(/\d+/g)?.map(Number);
  return Boolean(ns && age >= ns[0] && (ns.length === 1 || age <= ns[1]));
}
function measuredSum(rows: Relationship[]) {
  if (
    !rows.length ||
    rows.some((r) => typeof r.count !== "number" || !Number.isFinite(r.count))
  )
    throw Error(
      "Selected ONS relationship cells are unavailable or suppressed. Choose another relationship preference.",
    );
  return sum(rows.map((r) => r.count as number));
}
function relationshipRate(c: Criteria, sex: Sex, age: number) {
  if (c.relationship === "any") return { rate: 1, refs: [], unreliable: false };
  const living = ["single", "partnered"].includes(c.relationship);
  const all = evidence.relationships.filter(
    (r) =>
      r.sex === sex &&
      r.mode === (living ? "living" : "marital") &&
      bandIncludes(r.age, age),
  );
  const selected = all.filter((r) =>
    living
      ? r.category.startsWith(
          c.relationship === "single"
            ? "Not living in a couple:"
            : "Living in a couple:",
        )
      : r.category === (c.relationship === "divorced" ? "Divorced" : "Widowed"),
  );
  const total = measuredSum(all);
  if (total <= 0) throw Error("No relationship denominator available.");
  return {
    rate: measuredSum(selected) / total,
    refs: all.map((r) => r.cell),
    unreliable: selected.some((r) => r.cv === "d"),
  };
}
function incomeRate(c: Criteria, sex: Sex) {
  if (c.income === 0) return { rate: 1, refs: [] };
  let count = 0;
  const refs: string[] = [];
  for (const b of filters.income[sex]) {
    if (c.income <= b.low) {
      count += b.taxpayers;
      refs.push(b.cell);
    } else if (b.high !== null && c.income < b.high) {
      count += (b.taxpayers * (b.high - c.income)) / (b.high - b.low);
      refs.push(b.cell);
    }
  }
  return {
    rate: count / sum(evidence.population.K02000001[sex].slice(18)),
    refs,
  };
}
const educationGroups: Record<string, string[]> = {
  any: [
    "none",
    "level1",
    "level2",
    "apprenticeship",
    "level3",
    "level4",
    "other",
  ],
  none: ["none"],
  level1plus: ["level1", "level2", "level3", "level4"],
  level2plus: ["level2", "level3", "level4"],
  level3plus: ["level3", "level4"],
  level4: ["level4"],
  apprenticeship: ["apprenticeship"],
  other: ["other"],
};
function jointRates(c: Criteria, geo: string, sex: Sex, age: number) {
  const countries =
    geo === "W92000004"
      ? ["W92000004"]
      : geo === "E92000001" || geo.startsWith("E12")
        ? ["E92000001"]
        : ["E92000001", "W92000004"];
  const all = filters.jointCensus.filter(
    (r) =>
      r.sex === sex &&
      age >= r.min &&
      age <= r.max &&
      countries.includes(r.country),
  );
  const qualified = all.filter((r) =>
    educationGroups[c.education].includes(r.education),
  );
  const matching = qualified.filter(
    (r) => c.ethnicity === "any" || r.ethnicity === c.ethnicity,
  );
  const total = sum(all.map((r) => r.count)),
    q = sum(qualified.map((r) => r.count));
  if (!total) throw Error("Joint Census denominator unavailable.");
  return {
    qualification: q / total,
    ethnicity: q ? sum(matching.map((r) => r.count)) / q : 0,
    refs: matching.map((r) => r.ref),
  };
}
function orientationRate(c: Criteria, sex: Sex, age: number) {
  if (c.orientation === "any") return { rate: 1, refs: [], unreliable: false };
  const band = filters.orientationByAgeSex[sex].find(
    (b) => age >= b.min && age <= b.max,
  );
  const keys =
    c.orientation === "straightBi"
      ? ["straight", "bi"]
      : c.orientation === "gayBi"
        ? ["gay", "bi"]
        : [c.orientation];
  const values = keys.map((k) => band?.categories[k]);
  if (values.some((v) => !v || v.rate === null))
    throw Error("ONS orientation cells unavailable.");
  return {
    rate: sum(values.map((v) => v!.rate!)),
    refs: values.map((v) => v!.cell),
    unreliable: values.some((v) => v!.cv === "d"),
  };
}
function populationLocations(geo: string) {
  if (geo === "K02000001") return regions.map((r) => r.code);
  if (geo === "K04000001")
    return regions
      .filter((r) => r.code.startsWith("E12") || r.code === "W92000004")
      .map((r) => r.code);
  return [geo];
}
function childrenRate(c: Criteria, age: number) {
  if (c.children === "any") return 1;
  const q = childrenEvidence.tables.QD6;
  const band =
    age <= 24
      ? "16-24"
      : age <= 34
        ? "25-34"
        : age <= 44
          ? "35-44"
          : age <= 54
            ? "45-54"
            : age <= 64
              ? "55-64"
              : age <= 74
                ? "65-74"
                : "75+";
  const column = q.columns.indexOf(band),
    counts = q.weightedCounts;
  const count =
    c.children === "none"
      ? counts.none[column]
      : c.children === "one"
        ? counts.none[column] + counts.one[column]
        : c.children === "two"
          ? counts.none[column] + counts.one[column] + counts.two[column]
          : counts.three[column] + counts.fourPlus[column];
  return count / q.weightedBase[column];
}
function compute(c: Criteria): Calculation {
  const sexes: Sex[] = c.sex === "Persons" ? ["Males", "Females"] : [c.sex];
  const locations = populationLocations(c.geo);
  const base = sum(
    locations.flatMap((geo) =>
      sexes.map((sex) => sum(evidence.population[geo][sex].slice(18))),
    ),
  );
  const stages: Stage[] = [
    ["Starting adult population", "population"],
    ["Age range", "population"],
    ["Relationship status", "relationships"],
    ["Income", "income"],
    ["Orientation", "orientation"],
    ["Height", "health"],
    ["Weight category (BMI)", "health"],
    ["Qualifications", "education"],
    ["Ethnic group", "ethnicity"],
    ["Children under 18 living with them", "children"],
  ].map(([label, sourceId]) => ({
    label,
    sourceId,
    count: 0,
    remainingPct: 0,
    dropPct: 0,
  }));
  stages[0].count = base;
  const rows: Calculation["rows"] = [];
  let unreliable = false;
  for (const geo of locations)
    for (const sex of sexes) {
      const income = incomeRate(c, sex);
      for (let age = c.min; age <= c.max; age++) {
        const original = evidence.population[geo][sex][age];
        if (!Number.isFinite(original))
          throw Error("Population source cell unavailable.");
        let n = original;
        stages[1].count += n;
        const relationship = relationshipRate(c, sex, age),
          orientation = orientationRate(c, sex, age),
          joint = jointRates(c, geo, sex, age);
        unreliable ||= relationship.unreliable || orientation.unreliable;
        const health = filters.health[sex].find(
          (r) => age >= r.min && age <= r.max,
        );
        if (!health) throw Error("Health source band unavailable.");
        const activeHeight = c.heightMin !== null || c.heightMax !== null;
        const lower =
          c.heightMin === null
            ? 0
            : normalCDF((c.heightMin - health.mean) / c.spread);
        const upper =
          c.heightMax === null
            ? 1
            : normalCDF((c.heightMax - health.mean) / c.spread);
        const height = activeHeight ? Math.max(0, upper - lower) : 1;
        const bmi = c.bmi === "any" ? 1 : health.bmi[Number(c.bmi)];
        if (bmi === null)
          throw Error(
            `NHS BMI cell unavailable for ${SEX_LABELS[sex].toLowerCase()} aged ${age}. Choose another BMI preference.`,
          );
        const rates = [
          relationship.rate,
          income.rate,
          orientation.rate,
          height,
          bmi,
          joint.qualification,
          joint.ethnicity,
          childrenRate(c, age),
        ];
        rates.forEach((rate, i) => {
          if (!Number.isFinite(rate) || rate < 0 || rate > 1.000001)
            throw Error("Invalid source rate.");
          n *= Math.min(1, rate);
          stages[i + 2].count += n;
        });
        rows.push({
          geo,
          sex,
          age: age === 90 ? "90+" : age,
          population: original,
          estimated: n,
          rates,
          refs: [
            String(evidence.population[geo].sourceRows[sex]),
            ...relationship.refs,
            ...income.refs,
            ...orientation.refs,
            ...joint.refs,
            ...(activeHeight ? [health.heightCell] : []),
            ...(c.bmi !== "any" ? [health.bmiCells[Number(c.bmi)]] : []),
            ...(c.children !== "any" ? ["Ipsos QD6/Table636/page172"] : []),
          ],
        });
      }
    }
  stages.forEach((s, i) => {
    s.remainingPct = base ? (s.count / base) * 100 : 0;
    s.dropPct =
      i && stages[i - 1].count
        ? Math.max(0, 1 - s.count / stages[i - 1].count) * 100
        : 0;
  });
  const count = stages.at(-1)!.count,
    p = base ? count / base : 0;
  const notes = [
    "The percentage is out of all selected-sex adults aged 18+ in your chosen location. Population counts are pinned to mid-2024; 90 means the full 90+ group.",
    "Rates are multiplied within each sex and age group, then added. Remaining overlaps between preferences are unknown, so the combined result is an estimate. No statistical confidence interval is claimed.",
    childrenStatus.explanation,
  ];
  if (c.relationship !== "any") notes.push(descriptions.relationships);
  if (c.income > 0) notes.push(descriptions.income);
  if (c.heightMin !== null || c.heightMax !== null)
    notes.push(
      `Height spread is your modelling assumption: ${c.spread} cm. Sensitivity shows the result with spread ${Math.max(3, c.spread - 2)} and ${Math.min(15, c.spread + 2)} cm; it is not a confidence interval.`,
    );
  if (c.bmi !== "any" || c.heightMin !== null || c.heightMax !== null)
    notes.push(descriptions.health);
  if (c.education !== "any" || c.ethnicity !== "any")
    notes.push(
      "Qualification and ethnicity use observed joint 2021 counts. Income, orientation and relationship status are not jointly measured with these characteristics.",
    );
  if (c.orientation !== "any") notes.push(descriptions.orientation);
  if (unreliable)
    notes.push(
      "Some selected survey cells are marked unreliable by ONS. Source-cell references are retained in the downloadable result.",
    );
  return {
    state: c,
    count,
    base,
    p,
    oneIn: p > 0 ? 1 / p : null,
    stages,
    notes,
    rows,
    heightSensitivity: null,
    relaxations: [],
  };
}
export function calculatePool(input: Criteria): Calculation {
  const c = validateCriteria(input),
    result = compute(c);
  if (c.heightMin !== null || c.heightMax !== null) {
    const a = compute({ ...c, spread: Math.max(3, c.spread - 2) }).count,
      b = compute({ ...c, spread: Math.min(15, c.spread + 2) }).count;
    result.heightSensitivity = { low: Math.min(a, b), high: Math.max(a, b) };
  }
  const alternatives: {
    label: string;
    patch: Partial<Criteria>;
    active: boolean;
  }[] = [
    {
      label: "Remove income minimum",
      patch: { income: 0 },
      active: c.income > 0,
    },
    {
      label: "Accept any height",
      patch: { heightMin: null, heightMax: null },
      active: c.heightMin !== null || c.heightMax !== null,
    },
    {
      label: "Any relationship status",
      patch: { relationship: "any" },
      active: c.relationship !== "any",
    },
    {
      label: "Any BMI category",
      patch: { bmi: "any" },
      active: c.bmi !== "any",
    },
    {
      label: "Any qualification",
      patch: { education: "any" },
      active: c.education !== "any",
    },
    {
      label: "Any ethnic group",
      patch: { ethnicity: "any" },
      active: c.ethnicity !== "any",
    },
    {
      label: "Any orientation",
      patch: { orientation: "any" },
      active: c.orientation !== "any",
    },
    {
      label: "Any number of children at home",
      patch: { children: "any" },
      active: c.children !== "any",
    },
  ];
  result.relaxations = alternatives
    .filter((a) => a.active)
    .map(({ label, patch }) => {
      const r = compute({ ...c, ...patch });
      return { label, patch, count: r.count, p: r.p };
    });
  return result;
}
export function calculateRegions(input: Criteria) {
  const c = validateCriteria(input);
  return regions
    .map((r) => {
      const result = compute({ ...c, geo: r.code });
      return {
        geo: r.code,
        name: r.name,
        base: result.base,
        count: result.count,
        p: result.p,
      };
    })
    .sort((a, b) => b.count - a.count);
}
