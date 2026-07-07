"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import {
  MIN_WAGE_ANNUAL,
  MEDIAN_SALARY,
  AVERAGE_SALARY,
  EDUCATION_ORDER,
  UK_ADULT_POPULATION,
  ETHNICITY_DISTRIBUTION,
  BODY_TYPE_DISTRIBUTION_MALE,
  BODY_TYPE_DISTRIBUTION_FEMALE,
  CHILDREN_DISTRIBUTION,
  DATA_QUALITY_NOTES,
} from "@/lib/data";
import {
  calculateDatingPool,
  cmToFeetInches,
  type CalculatorInput,
  type Gender,
  type LookingFor,
  type Orientation,
} from "@/lib/calc";

const INCOME_OPTIONS: Array<{ label: string; value: number }> = [
  { label: "Any income", value: 0 },
  { label: `£${MIN_WAGE_ANNUAL.toLocaleString("en-GB")} (Min Wage)`, value: MIN_WAGE_ANNUAL },
  { label: "£25,000+", value: 25000 },
  { label: `£${MEDIAN_SALARY.toLocaleString("en-GB")} (UK Median)`, value: MEDIAN_SALARY },
  { label: `£${AVERAGE_SALARY.toLocaleString("en-GB")} (UK Average)`, value: AVERAGE_SALARY },
  { label: "£50,000+", value: 50000 },
  { label: "£75,000+", value: 75000 },
  { label: "£100,000+", value: 100000 },
  { label: "£150,000+", value: 150000 },
  { label: "£250,000+", value: 250000 },
  { label: "£1,000,000+ (Millionaire)", value: 1000000 },
];

function fmt(n: number) {
  return n.toLocaleString("en-GB");
}

function clampInt(value: number, min: number, max: number) {
  if (!Number.isFinite(value)) return min;
  return Math.min(max, Math.max(min, Math.round(value)));
}

export default function Home() {
  // Core filters
  const [userGender, setUserGender] = useState<Gender>("Male");
  const [orientation, setOrientation] = useState<Orientation>("Heterosexual/Straight");
  const [lookingFor, setLookingFor] = useState<LookingFor>("Female");
  const [minAge, setMinAge] = useState(25);
  const [maxAge, setMaxAge] = useState(35);
  
  // Height filters
  const [anyHeight, setAnyHeight] = useState(true);
  const [minHeight, setMinHeight] = useState(150);
  const [maxHeight, setMaxHeight] = useState(180);
  
  // Lifestyle filters
  const [minIncome, setMinIncome] = useState(0);
  const [education, setEducation] = useState("Any");
  const [mustBeSingle, setMustBeSingle] = useState(true);
  const [baldness, setBaldness] = useState<"Any" | "Not bald" | "Bald or balding">("Any");

  // Multi-select lists (interactive filters)
  const [selectedEthnicities, setSelectedEthnicities] = useState<string[]>(() =>
    Object.keys(ETHNICITY_DISTRIBUTION.value)
  );
  const [selectedBodyTypes, setSelectedBodyTypes] = useState<string[]>(() =>
    Object.keys(BODY_TYPE_DISTRIBUTION_MALE.value)
  );
  const [acceptableChildren, setAcceptableChildren] = useState<string[]>(() =>
    Object.keys(CHILDREN_DISTRIBUTION.value)
  );
  const [acceptableMarriage, setAcceptableMarriage] = useState<string[]>(() => [
    "Never married",
    "Divorced",
    "Widowed",
    "Currently married",
  ]);

  // Section collapsible states
  const [showEthnicityFilter, setShowEthnicityFilter] = useState(false);
  const [showBodyTypeFilter, setShowBodyTypeFilter] = useState(false);
  const [showChildrenFilter, setShowChildrenFilter] = useState(false);
  const [showMarriageFilter, setShowMarriageFilter] = useState(false);

  // Re-sync body type options list when target gender changes
  const targetBodyTypeKeys = useMemo(() => {
    return lookingFor === "Male"
      ? Object.keys(BODY_TYPE_DISTRIBUTION_MALE.value)
      : lookingFor === "Female"
      ? Object.keys(BODY_TYPE_DISTRIBUTION_FEMALE.value)
      : [
          ...new Set([
            ...Object.keys(BODY_TYPE_DISTRIBUTION_MALE.value),
            ...Object.keys(BODY_TYPE_DISTRIBUTION_FEMALE.value),
          ]),
        ];
  }, [lookingFor]);

  const input: CalculatorInput = useMemo(
    () => ({
      userGender,
      orientation,
      lookingFor,
      ageRange: [Math.min(minAge, maxAge), Math.max(minAge, maxAge)],
      minHeightCm: anyHeight ? 140 : Math.min(minHeight, maxHeight),
      maxHeightCm: anyHeight ? 210 : Math.max(minHeight, maxHeight),
      minIncome,
      educationLevel: education,
      selectedEthnicities,
      selectedBodyTypes: selectedBodyTypes.filter((b) => targetBodyTypeKeys.includes(b)),
      mustBeSingle,
      acceptableChildren,
      acceptableMarriage,
      baldnessPreference: baldness,
    }),
    [
      userGender,
      orientation,
      lookingFor,
      minAge,
      maxAge,
      anyHeight,
      minHeight,
      maxHeight,
      minIncome,
      education,
      selectedEthnicities,
      selectedBodyTypes,
      targetBodyTypeKeys,
      mustBeSingle,
      acceptableChildren,
      acceptableMarriage,
      baldness,
    ]
  );

  const result = useMemo(() => calculateDatingPool(input), [input]);

  const hasOrientationConflict = useMemo(() => {
    const isSameSex = (userGender === "Male" && lookingFor === "Male") || (userGender === "Female" && lookingFor === "Female");
    const isOppositeSex = (userGender === "Male" && lookingFor === "Female") || (userGender === "Female" && lookingFor === "Male");
    
    if (orientation === "Heterosexual/Straight" && isSameSex) return true;
    if (orientation === "Gay or Lesbian" && isOppositeSex) return true;
    return false;
  }, [userGender, lookingFor, orientation]);

  const showBaldness = lookingFor === "Male" || lookingFor === "Any";

  const setMinAgeValue = (value: number) => {
    const next = clampInt(value, 18, 99);
    setMinAge(next);
    if (next > maxAge) setMaxAge(next);
  };

  const setMaxAgeValue = (value: number) => {
    const next = clampInt(value, 18, 99);
    setMaxAge(next);
    if (next < minAge) setMinAge(next);
  };

  const setMinHeightValue = (value: number) => {
    const next = clampInt(value, 140, 210);
    setMinHeight(next);
    if (next > maxHeight) setMaxHeight(next);
  };

  const setMaxHeightValue = (value: number) => {
    const next = clampInt(value, 140, 210);
    setMaxHeight(next);
    if (next < minHeight) setMinHeight(next);
  };

  // Multi-select toggle helpers
  const toggleEthnicity = (eth: string) => {
    setSelectedEthnicities((prev) =>
      prev.includes(eth) ? prev.filter((x) => x !== eth) : [...prev, eth]
    );
  };

  const toggleBodyType = (bt: string) => {
    setSelectedBodyTypes((prev) =>
      prev.includes(bt) ? prev.filter((x) => x !== bt) : [...prev, bt]
    );
  };

  const toggleChildren = (childOpt: string) => {
    setAcceptableChildren((prev) =>
      prev.includes(childOpt) ? prev.filter((x) => x !== childOpt) : [...prev, childOpt]
    );
  };

  const toggleMarriage = (marr: string) => {
    setAcceptableMarriage((prev) =>
      prev.includes(marr) ? prev.filter((x) => x !== marr) : [...prev, marr]
    );
  };

  return (
    <main className="mx-auto max-w-7xl px-3 py-5 sm:px-4 sm:py-8 md:px-8">
      {/* Premium Header */}
      <header className="mb-10 text-center md:text-left md:flex md:items-center md:justify-between border-b border-zinc-800 pb-6">
        <div>
          <h1 className="bg-gradient-to-r from-rose-400 via-pink-500 to-violet-400 bg-clip-text text-3xl font-extrabold tracking-tight text-transparent select-none sm:text-4xl md:text-5xl">
            UK Dating Pool Calculator
          </h1>
          <p className="mt-2 text-sm text-zinc-400 max-w-xl">
            Sourced from official ONS, NHS, and HMRC statistical sets. Adjust parameters to analyze your realistic matchmaking pool.
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex flex-wrap justify-center items-center gap-2 md:justify-end">
          <Link
            href="/methodology"
            className="inline-flex items-center rounded-full bg-zinc-900/80 px-3 py-1.5 text-xs font-semibold text-zinc-200 ring-1 ring-inset ring-zinc-700/80 transition-colors hover:bg-zinc-800 hover:text-white"
          >
            Methodology
          </Link>
          <span className="inline-flex items-center gap-1.5 rounded-full bg-rose-500/10 px-3 py-1.5 text-xs font-medium text-rose-400 ring-1 ring-inset ring-rose-500/20">
            <span className="h-1.5 w-1.5 rounded-full bg-rose-400 animate-pulse" />
            Live Client-Side Math
          </span>
        </div>
      </header>

      {/* Two-column layout grid */}
      <div className="grid gap-8 lg:grid-cols-[400px_minmax(0,1fr)] items-start">
        
        {/* Sticky Filters Panel (Left column) */}
        <section 
          className="glass-panel rounded-2xl p-5 space-y-6 overflow-visible pr-3 sm:p-6 lg:sticky lg:top-6 lg:w-[400px] lg:self-start lg:max-h-[85vh] lg:overflow-y-auto lg:pr-4"
          style={{ scrollbarGutter: "stable" }}
        >
          <h2 className="text-base font-semibold text-zinc-100 flex items-center gap-2 border-b border-zinc-800/80 pb-3">
            <svg className="w-5 h-5 text-rose-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Calculator Filters
          </h2>

          {/* Group 1: Identity & Preferences */}
          <div className="space-y-4">
            <Field label="Your Gender">
              <Segmented
                options={["Male", "Female"]}
                value={userGender}
                onChange={(v) => setUserGender(v as Gender)}
              />
            </Field>

            <Field label="Your Orientation">
              <Select
                value={orientation}
                onChange={(v) => {
                  const newOrient = v as Orientation;
                  setOrientation(newOrient);
                  // Dynamic lookingFor suggestion based on user gender + orientation
                  if (newOrient === "Heterosexual/Straight") {
                    setLookingFor(userGender === "Male" ? "Female" : "Male");
                  } else if (newOrient === "Gay or Lesbian") {
                    setLookingFor(userGender === "Male" ? "Male" : "Female");
                  } else {
                    setLookingFor("Any");
                  }
                }}
                options={["Heterosexual/Straight", "Gay or Lesbian", "Bisexual"]}
              />
            </Field>

            <Field label="Looking For">
              <Segmented
                options={["Male", "Female", "Any"]}
                value={lookingFor}
                onChange={(v) => setLookingFor(v as LookingFor)}
              />
            </Field>
          </div>

          {/* Group 2: Demographics */}
          <div className="space-y-4 border-t border-zinc-800/80 pt-4">
            <Field label={`Age Range: ${minAge} to ${maxAge}`}>
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <NumberInput
                    label="Min age"
                    value={minAge}
                    min={18}
                    max={99}
                    onChange={setMinAgeValue}
                  />
                  <NumberInput
                    label="Max age"
                    value={maxAge}
                    min={18}
                    max={99}
                    onChange={setMaxAgeValue}
                  />
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex-1">
                    <span className="text-[10px] text-zinc-500 uppercase block mb-1">Min</span>
                    <input
                      type="range"
                      min="18"
                      max="99"
                      value={minAge}
                      onChange={(e) => setMinAgeValue(Number(e.target.value))}
                      aria-label="Minimum age slider"
                      className="w-full accent-rose-500 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>
                  <div className="flex-1">
                    <span className="text-[10px] text-zinc-500 uppercase block mb-1">Max</span>
                    <input
                      type="range"
                      min="18"
                      max="99"
                      value={maxAge}
                      onChange={(e) => setMaxAgeValue(Number(e.target.value))}
                      aria-label="Maximum age slider"
                      className="w-full accent-rose-500 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>
                </div>
              </div>
            </Field>

            <Field label="Height Specifications">
              <label className="flex items-center gap-2.5 text-sm cursor-pointer select-none text-zinc-300">
                <input
                  type="checkbox"
                  checked={anyHeight}
                  onChange={(e) => setAnyHeight(e.target.checked)}
                  className="rounded border-zinc-700 bg-transparent text-rose-500 focus:ring-rose-500 focus:ring-offset-zinc-900"
                />
                Any height
              </label>
              {!anyHeight && (
                <div className="mt-3 space-y-3 animate-fade-in">
                  <div className="grid grid-cols-2 gap-3">
                    <NumberInput
                      label="Min height"
                      value={minHeight}
                      min={140}
                      max={210}
                      suffix="cm"
                      helper={`${cmToFeetInches(minHeight).feet}'${cmToFeetInches(minHeight).inches}"`}
                      onChange={setMinHeightValue}
                    />
                    <NumberInput
                      label="Max height"
                      value={maxHeight}
                      min={140}
                      max={210}
                      suffix="cm"
                      helper={`${cmToFeetInches(maxHeight).feet}'${cmToFeetInches(maxHeight).inches}"`}
                      onChange={setMaxHeightValue}
                    />
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex-1">
                      <input
                        type="range"
                        min="140"
                        max="210"
                        value={minHeight}
                        onChange={(e) => setMinHeightValue(Number(e.target.value))}
                        aria-label="Minimum height slider"
                        className="w-full accent-rose-500 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                    <div className="flex-1">
                      <input
                        type="range"
                        min="140"
                        max="210"
                        value={maxHeight}
                        onChange={(e) => setMaxHeightValue(Number(e.target.value))}
                        aria-label="Maximum height slider"
                        className="w-full accent-rose-500 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                  </div>
                </div>
              )}
            </Field>

            <Field label="Minimum Annual Income">
              <Select
                value={String(minIncome)}
                onChange={(v) => setMinIncome(Number(v))}
                options={INCOME_OPTIONS.map((o) => o.label)}
                values={INCOME_OPTIONS.map((o) => String(o.value))}
              />
            </Field>

            <Field label="Minimum Education Level">
              <Select
                value={education}
                onChange={setEducation}
                options={["Any education", ...EDUCATION_ORDER]}
                values={["Any", ...EDUCATION_ORDER]}
              />
            </Field>

            {showBaldness && (
              <Field label="Baldness Preference">
                <Select
                  value={baldness}
                  onChange={(v) => setBaldness(v as typeof baldness)}
                  options={["Any", "Not bald", "Bald or balding"]}
                />
              </Field>
            )}
          </div>

          {/* Group 3: Fine-grained multi-selects */}
          <div className="space-y-3 border-t border-zinc-800/80 pt-4">
            
            {/* Ethnicity Accordion */}
            <Accordion
              label="Preferred Ethnicity"
              count={selectedEthnicities.length}
              total={Object.keys(ETHNICITY_DISTRIBUTION.value).length}
              isOpen={showEthnicityFilter}
              onToggle={() => setShowEthnicityFilter(!showEthnicityFilter)}
            >
              <div className="flex gap-2 mb-2">
                <button
                  onClick={() => setSelectedEthnicities(Object.keys(ETHNICITY_DISTRIBUTION.value))}
                  className="text-[10px] text-rose-400 bg-rose-500/10 px-2 py-1 rounded hover:bg-rose-500/20 transition-colors cursor-pointer"
                >
                  All
                </button>
                <button
                  onClick={() => setSelectedEthnicities([])}
                  className="text-[10px] text-zinc-400 bg-zinc-800 px-2 py-1 rounded hover:bg-zinc-700 transition-colors cursor-pointer"
                >
                  None
                </button>
              </div>
              <div className="max-h-40 overflow-y-auto space-y-1.5 pr-2">
                {Object.keys(ETHNICITY_DISTRIBUTION.value).map((eth) => (
                  <label key={eth} className="flex items-center gap-2 text-xs text-zinc-300 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={selectedEthnicities.includes(eth)}
                      onChange={() => toggleEthnicity(eth)}
                      className="rounded border-zinc-700 bg-transparent text-rose-500 focus:ring-rose-500"
                    />
                    {eth}
                  </label>
                ))}
              </div>
            </Accordion>

            {/* Body Type Accordion */}
            <Accordion
              label="Preferred Body Type"
              count={selectedBodyTypes.filter((x) => targetBodyTypeKeys.includes(x)).length}
              total={targetBodyTypeKeys.length}
              isOpen={showBodyTypeFilter}
              onToggle={() => setShowBodyTypeFilter(!showBodyTypeFilter)}
            >
              <div className="space-y-1.5">
                {targetBodyTypeKeys.map((bt) => (
                  <label key={bt} className="flex items-center gap-2 text-xs text-zinc-300 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={selectedBodyTypes.includes(bt)}
                      onChange={() => toggleBodyType(bt)}
                      className="rounded border-zinc-700 bg-transparent text-rose-500 focus:ring-rose-500"
                    />
                    {bt}
                  </label>
                ))}
              </div>
            </Accordion>

            {/* Children Accordion */}
            <Accordion
              label="Family Status (Children)"
              count={acceptableChildren.length}
              total={Object.keys(CHILDREN_DISTRIBUTION.value).length}
              isOpen={showChildrenFilter}
              onToggle={() => setShowChildrenFilter(!showChildrenFilter)}
            >
              <div className="space-y-1.5">
                {Object.keys(CHILDREN_DISTRIBUTION.value).map((childOpt) => (
                  <label key={childOpt} className="flex items-center gap-2 text-xs text-zinc-300 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={acceptableChildren.includes(childOpt)}
                      onChange={() => toggleChildren(childOpt)}
                      className="rounded border-zinc-700 bg-transparent text-rose-500 focus:ring-rose-500"
                    />
                    {childOpt}
                  </label>
                ))}
              </div>
            </Accordion>

            {/* Marriage History Accordion */}
            <Accordion
              label="Acceptable Marital Status"
              count={acceptableMarriage.length}
              total={4}
              isOpen={showMarriageFilter}
              onToggle={() => setShowMarriageFilter(!showMarriageFilter)}
            >
              <div className="space-y-1.5">
                {["Never married", "Divorced", "Widowed", "Currently married"].map((marr) => (
                  <label key={marr} className="flex items-center gap-2 text-xs text-zinc-300 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={acceptableMarriage.includes(marr)}
                      onChange={() => toggleMarriage(marr)}
                      className="rounded border-zinc-700 bg-transparent text-rose-500 focus:ring-rose-500"
                    />
                    {marr}
                  </label>
                ))}
              </div>
            </Accordion>

            {/* Availability Option */}
            <div className="pt-2">
              <label className="flex items-center gap-2.5 text-sm cursor-pointer select-none text-zinc-300">
                <input
                  type="checkbox"
                  checked={mustBeSingle}
                  onChange={(e) => setMustBeSingle(e.target.checked)}
                  className="rounded border-zinc-700 bg-transparent text-rose-500 focus:ring-rose-500 focus:ring-offset-zinc-900"
                />
                Must be single / not living with partner
              </label>
            </div>
          </div>
        </section>

        {/* Results Pane (Right column) */}
        <section className="min-w-0 space-y-6">
          
          {/* Orientation Conflict Alert */}
          {hasOrientationConflict && (
            <div className="bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs md:text-sm rounded-2xl p-4 md:p-5 flex gap-3 items-start relative overflow-hidden backdrop-blur-md shadow-md animate-pulse">
              <span className="text-lg leading-none">⚠️</span>
              <div className="space-y-1">
                <p className="font-semibold text-amber-300">Orientation Mismatch Detected</p>
                <p className="text-zinc-300 leading-relaxed">
                  You have configured your orientation as <strong>{orientation}</strong> but are looking for <strong>{lookingFor}</strong>. The calculation will limit the matching pool to bisexual matches. For a more representative estimate, update your <strong>Orientation</strong> or <strong>Looking For</strong> filters.
                </p>
              </div>
            </div>
          )}
          
          {/* Main Glowing Result Banner */}
          <div className="glass-panel neon-border-glow min-h-[230px] rounded-3xl p-6 text-center relative overflow-hidden sm:p-8 md:p-10">
            {/* Background Glow */}
            <div className="absolute inset-0 bg-gradient-to-tr from-rose-500/10 via-violet-500/5 to-transparent pointer-events-none" />
            
            <div className="relative z-10 space-y-3">
              <h3 className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">
                Matching UK Dating Pool
              </h3>
              
              <div className="bg-gradient-to-r from-rose-400 via-pink-500 to-violet-400 bg-clip-text text-4xl font-extrabold leading-none tracking-tight text-transparent select-all neon-text-glow tabular-nums sm:text-5xl md:text-6xl xl:text-7xl">
                {result.targetPercentage.toFixed(4)}%
              </div>

              <div className="text-xl md:text-2xl font-bold text-zinc-100 mt-1">
                ≈ {fmt(result.estimatedMatches)} people
              </div>
              
              <div className="space-y-1 text-xs text-zinc-400">
                <p>out of {fmt(result.basePopulation)} {result.baseLabel}</p>
                {result.basePopulation !== UK_ADULT_POPULATION && (
                  <p>{result.percentage.toFixed(4)}% of all UK adults aged 18+</p>
                )}
              </div>
            </div>
          </div>

          {/* Funnel Graph representation */}
          <div className="glass-panel rounded-2xl p-6 space-y-5">
            <h3 className="text-sm font-semibold text-zinc-100 border-b border-zinc-800/80 pb-3 flex items-center gap-2">
              <svg className="w-4 h-4 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Filter Cascade Funnel
            </h3>

            <div className="space-y-4">
              {result.steps.map((s) => {
                const stepPercent = s.probability * 100;
                
                return (
                  <div key={s.criterion} className="space-y-1">
                    <div className="flex flex-col gap-1 text-xs sm:flex-row sm:items-center sm:justify-between">
                      <span className="font-medium text-zinc-300">{s.criterion}</span>
                      <span className="text-zinc-400 tabular-nums sm:text-right">
                        {stepPercent.toFixed(1)}% step pass · <span className="font-semibold text-zinc-200">{fmt(s.remaining)} left</span>
                      </span>
                    </div>
                    {/* Visual bar */}
                    <div className="h-2 w-full bg-zinc-900 rounded-full overflow-hidden border border-zinc-800/50">
                      <div
                        style={{ width: `${(s.remaining / UK_ADULT_POPULATION) * 100}%` }}
                        className="h-full bg-gradient-to-r from-rose-500 to-violet-600 rounded-full transition-all duration-500 ease-out"
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Caveats & methodology block */}
          <details className="group glass-panel rounded-2xl p-5 [&_summary::-webkit-details-marker]:hidden border border-amber-500/10 bg-amber-500/[0.01]">
            <summary className="flex items-center justify-between cursor-pointer select-none">
              <h3 className="text-sm font-semibold text-amber-400/90 flex items-center gap-2">
                <svg className="w-4.5 h-4.5 text-amber-500/90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Methodology & Statistical Caveats
              </h3>
              <span className="text-zinc-500 group-open:rotate-180 transition-transform">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </span>
            </summary>
            
            <div className="mt-4 text-xs leading-relaxed text-zinc-400 space-y-3 border-t border-zinc-800/50 pt-3">
              <p>
                <strong className="text-zinc-200">The Independence Assumption:</strong> This calculator models filters as mathematically independent variables. In reality, demographic traits are correlated (e.g., peak salary earners are concentrated in ages 35–54, rather than 18–24). Multiplying many niche parameters consecutively may underestimate or overestimate matches in real life.
              </p>
              <ul className="list-disc pl-4 space-y-2">
                {DATA_QUALITY_NOTES.map((note, idx) => (
                  <li key={idx}>{note}</li>
                ))}
              </ul>
              <Link
                href="/methodology"
                className="inline-flex text-xs font-semibold text-amber-300 underline decoration-amber-500/40 underline-offset-4 hover:text-amber-200"
              >
                Open full methodology, caveats, and sources
              </Link>
            </div>
          </details>
        </section>

      </div>
    </main>
  );
}

// ── Shared UI Sub-Components ──────────────────────────────────────────────────
function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5">
      <div className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 select-none">
        {label}
      </div>
      {children}
    </div>
  );
}

function Segmented({
  options,
  value,
  onChange,
}: {
  options: string[];
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div className="flex rounded-lg bg-zinc-950/60 p-0.5 border border-zinc-800/80">
      {options.map((o) => (
        <button
          key={o}
          type="button"
          onClick={() => onChange(o)}
          className={`flex-1 rounded-md py-1.5 text-xs font-semibold tracking-wide transition-all cursor-pointer ${
            value === o
              ? "bg-gradient-to-r from-rose-500 to-pink-600 text-white shadow-md"
              : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/40"
          }`}
        >
          {o}
        </button>
      ))}
    </div>
  );
}

function Select({
  value,
  onChange,
  options,
  values,
}: {
  value: string;
  onChange: (v: string) => void;
  options: readonly string[];
  values?: string[];
}) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded-lg bg-zinc-950/60 border border-zinc-800/80 px-3 py-2 text-xs font-semibold text-zinc-300 focus:border-rose-500 focus:ring-1 focus:ring-rose-500 outline-none cursor-pointer"
    >
      {options.map((o, i) => (
        <option key={o} value={values ? values[i] : o} className="bg-zinc-950 text-zinc-300">
          {o}
        </option>
      ))}
    </select>
  );
}

function NumberInput({
  label,
  value,
  min,
  max,
  onChange,
  suffix,
  helper,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  onChange: (v: number) => void;
  suffix?: string;
  helper?: string;
}) {
  return (
    <label className="block">
      <span className="mb-1 block text-[10px] font-semibold uppercase tracking-wider text-zinc-500">
        {label}
      </span>
      <span className="flex items-center rounded-lg border border-zinc-800/80 bg-zinc-950/60 px-3 py-2 focus-within:border-rose-500 focus-within:ring-1 focus-within:ring-rose-500">
        <input
          type="number"
          inputMode="numeric"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.currentTarget.value))}
          className="min-w-0 flex-1 bg-transparent text-xs font-semibold text-zinc-200 outline-none tabular-nums"
        />
        {suffix && <span className="ml-2 text-[10px] font-semibold uppercase text-zinc-500">{suffix}</span>}
      </span>
      {helper && <span className="mt-1 block text-[10px] text-zinc-500">{helper}</span>}
    </label>
  );
}

function Accordion({
  label,
  count,
  total,
  isOpen,
  onToggle,
  children,
}: {
  label: string;
  count: number;
  total: number;
  isOpen: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}) {
  return (
    <div className="border border-zinc-800 rounded-lg overflow-hidden bg-zinc-950/20">
      <button
        type="button"
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 text-left hover:bg-zinc-900/20 transition-colors cursor-pointer"
      >
        <span className="text-xs font-semibold text-zinc-300">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-semibold text-zinc-500 bg-zinc-900 px-2 py-0.5 rounded-full border border-zinc-800">
            {count === total ? "Any" : `${count}/${total}`}
          </span>
          <svg
            className={`w-3.5 h-3.5 text-zinc-500 transition-transform ${isOpen ? "rotate-180" : ""}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>
      {isOpen && <div className="p-3 border-t border-zinc-800/80 bg-zinc-950/40">{children}</div>}
    </div>
  );
}
