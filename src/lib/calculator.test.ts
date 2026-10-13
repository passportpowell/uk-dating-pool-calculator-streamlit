import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  calculatePool,
  calculateRegions,
  validateCriteria,
  DEFAULT_CRITERIA,
  cmToFeetInches,
  feetInchesToCm,
  sourceLibrary,
  RELATIONSHIP_LABELS,
  EDUCATION_LABELS,
  type Criteria,
} from "./calculator";
const base: Criteria = {
  ...DEFAULT_CRITERIA,
  min: 18,
  max: 90,
  relationship: "any",
};
const calc = (patch: Partial<Criteria> = {}) =>
  calculatePool({ ...base, ...patch });
const close = (a: number, b: number) =>
  assert.ok(
    Math.abs(a - b) <= Math.max(1e-6, Math.abs(b) * 1e-10),
    `${a} != ${b}`,
  );
describe("population and aggregation", () => {
  it("exact adult sex counts and Any sum", () => {
    close(calc().count, 26625856);
    close(calc({ sex: "Females" }).count, 28396397);
    close(calc({ sex: "Persons" }).count, 55022253);
  });
  it("Any equals male plus female with several strict filters", () => {
    const p: Partial<Criteria> = {
      min: 25,
      max: 34,
      income: 75000,
      heightMin: 180,
      heightMax: 190,
      education: "level4",
      ethnicity: "Black",
      orientation: "straightBi",
      children: "none",
    };
    close(
      calc({ ...p, sex: "Persons" }).count,
      calc({ ...p, sex: "Males" }).count + calc({ ...p, sex: "Females" }).count,
    );
  });
  it("age partitions add exactly with income and qualification", () => {
    const p: Partial<Criteria> = {
      education: "level4",
      income: 100000,
      min: 25,
      max: 44,
    };
    close(
      calc(p).count,
      calc({ ...p, max: 34 }).count + calc({ ...p, min: 35 }).count,
    );
  });
  it("national counts reconcile to all twelve regional calculations", () => {
    const c = {
      ...base,
      min: 25,
      max: 44,
      education: "level4",
      ethnicity: "Black",
      children: "one",
    };
    const r = calculatePool(c),
      regions = calculateRegions(c);
    assert.equal(regions.length, 12);
    close(
      r.count,
      regions.reduce((s, r) => s + r.count, 0),
    );
    close(
      r.base,
      regions.reduce((s, r) => s + r.base, 0),
    );
  });
  it("90+ is counted once and older single-year claims rejected", () => {
    const old = calc({ min: 90, max: 90 });
    assert.equal(old.rows.length, 12);
    assert.ok(old.count > 0);
    assert.throws(() => calc({ min: 99, max: 99 }), /ages/);
    assert.throws(() => calc({ min: 100, max: 100 }), /ages/);
  });
  it("selected region changes actual local population denominator", () => {
    const uk = calc(),
      london = calc({ geo: "E12000007" });
    assert.ok(london.base < uk.base);
    close(london.count, london.base);
  });
});
describe("measurement and result consistency", () => {
  it("headline equals last funnel stage without boost", () => {
    const r = calc({ income: 100000, education: "level4" });
    close(r.count, r.stages.at(-1)!.count);
    assert.equal(r.stages[0].remainingPct, 100);
    assert.ok(!("confidenceInterval" in r));
  });
  it("all funnel stages monotone and bounded", () => {
    const r = calc({
      income: 75000,
      orientation: "straightBi",
      children: "none",
    });
    for (let i = 1; i < r.stages.length; i++) {
      assert.ok(r.stages[i].count <= r.stages[i - 1].count + 1e-6);
      assert.ok(r.stages[i].dropPct >= 0 && r.stages[i].dropPct <= 100);
      assert.ok(
        r.stages[i].remainingPct >= 0 && r.stages[i].remainingPct <= 100,
      );
    }
  });
  it("blank height has pass rate exactly one", () => {
    const r = calc();
    const height = r.stages.find((s) => s.label === "Height")!;
    assert.equal(height.dropPct, 0);
    assert.equal(r.heightSensitivity, null);
  });
  it("reported orientation does not redistribute other/nonresponse", () => {
    const r = calc({ min: 25, max: 34, orientation: "straightBi" });
    for (const row of r.rows) assert.ok(row.rates[2] < 1);
  });
  it("joint qualifications/ethnicity are observed and unsupported degree splits reject", () => {
    const r = calc({
      min: 25,
      max: 34,
      education: "level4",
      ethnicity: "Black",
    });
    assert.ok(r.count > 0);
    assert.ok(
      r.rows.every((row) =>
        row.refs.some((ref) => ref.startsWith("observations[")),
      ),
    );
    assert.throws(
      () => calc({ education: "Postgraduate degree" }),
      /qualification/,
    );
    assert.ok(Object.hasOwn(EDUCATION_LABELS, "apprenticeship"));
  });
  it("five relationship choices and no extra availability multiplier", () => {
    assert.equal(Object.keys(RELATIONSHIP_LABELS).length, 5);
    assert.equal(
      calc({ min: 25, max: 29, relationship: "single" }).stages.filter(
        (s) => s.sourceId === "relationships",
      ).length,
      1,
    );
  });
  it("suppressed relationship data are not treated as zero", () => {
    assert.throws(
      () => calc({ min: 90, max: 90, relationship: "divorced" }),
      /unavailable|suppressed|denominator/,
    );
  });
  it("every relaxation matches exact patch in same location", () => {
    const c = {
      ...base,
      geo: "E12000007",
      min: 25,
      max: 34,
      income: 100000,
      heightMin: 180,
      heightMax: 195,
      education: "level4",
      ethnicity: "Black",
      children: "none",
    };
    const r = calculatePool(c);
    for (const t of r.relaxations) {
      const changed = calculatePool({ ...c, ...t.patch });
      close(t.count, changed.count);
      close(t.p, changed.p);
      assert.ok(t.count >= r.count - 1e-6);
    }
  });
  it("height sensitivity is named model comparison, not confidence", () => {
    const r = calc({ heightMin: 182, heightMax: 195 });
    assert.ok(r.heightSensitivity);
    assert.ok(r.heightSensitivity.low <= r.heightSensitivity.high);
    assert.ok(r.notes.some((n) => n.includes("not a confidence interval")));
  });
});
describe("children measured household fallback", () => {
  it("no-child rates change by age using published counts", () => {
    const a = calc({ min: 25, max: 34, children: "none" }),
      b = calc({ min: 55, max: 64, children: "none" });
    close(a.p / calc({ min: 25, max: 34 }).p, 341 / 766);
    close(b.p / calc({ min: 55, max: 64 }).p, 667 / 736);
    assert.ok(a.notes.some((n) => n.includes("Children living elsewhere")));
  });
  it("children none/up-to-one/up-to-two are monotonic", () => {
    const counts = ["none", "one", "two", "any"].map(
      (children) => calc({ min: 25, max: 34, children }).count,
    );
    for (let i = 1; i < counts.length; i++)
      assert.ok(counts[i] >= counts[i - 1]);
  });
  it("source links directly to exact PDF page", () => {
    assert.match(
      sourceLibrary.find((s) => s.id === "children")!.url,
      /#page=172$/,
    );
  });
});
describe("runtime validation and units", () => {
  for (const patch of [
    { min: 24.5 },
    { max: Infinity },
    { income: NaN },
    { income: -1 },
    { income: 12345 },
    { heightMin: 200, heightMax: 150 },
    { heightMin: NaN },
    { spread: 0 },
    { geo: "unknown" },
    { sex: "Alien" },
    { orientation: "unknown" },
    { children: "unknown" },
    { ethnicity: ["White", "White"] },
    { correlationAdjustment: true },
  ])
    it(`rejects ${JSON.stringify(patch)}`, () =>
      assert.throws(() => validateCriteria({ ...base, ...patch })));
  it("rejects non-object input", () => {
    for (const x of [null, [], 42, "bad"])
      assert.throws(() => validateCriteria(x));
  });
  it("six feet equals 182.88cm and rounded inches carry", () => {
    close(feetInchesToCm(6, 0), 182.88);
    assert.deepEqual(cmToFeetInches(152.3), { feet: 5, inches: 0 });
    assert.throws(() => feetInchesToCm(5, 12));
    assert.throws(() => feetInchesToCm(5.5, 0));
  });
  it("complete versioned canonical criteria round-trip", () => {
    const c = {
      ...base,
      geo: "W92000004",
      min: 25,
      max: 34,
      income: 50000,
      education: "level3plus",
      ethnicity: "Mixed",
      bmi: "1",
      children: "two",
    };
    const payload = JSON.parse(
      new URLSearchParams(
        "c=" + encodeURIComponent(JSON.stringify({ v: 1, criteria: c })),
      ).get("c")!,
    );
    assert.deepEqual(validateCriteria(payload.criteria), c);
  });
  it("all active sources have traceable metadata and retained fingerprints", () => {
    for (const s of sourceLibrary) {
      assert.ok(
        s.id &&
          s.title &&
          s.tables &&
          s.reference &&
          s.geography &&
          s.explanation,
      );
      assert.match(s.url, /^https:\/\//);
      assert.match(s.sha256!, /^[a-f0-9]{64}$/);
      assert.ok(s.file?.startsWith("/evidence/"));
    }
  });
});
