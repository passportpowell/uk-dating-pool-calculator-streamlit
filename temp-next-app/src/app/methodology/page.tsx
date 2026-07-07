import Link from "next/link";
import {
  AGE_SINGLE_YEAR_DISTRIBUTION,
  BODY_TYPE_DISTRIBUTION_FEMALE,
  BODY_TYPE_DISTRIBUTION_MALE,
  DATA_QUALITY_NOTES,
  EDUCATION_DISTRIBUTION,
  ETHNICITY_DISTRIBUTION,
  GENDER_SPLIT,
  HEIGHT,
  INCOME_DISTRIBUTION_FEMALE,
  INCOME_DISTRIBUTION_MALE,
  SEXUAL_ORIENTATION_DISTRIBUTION,
  SINGLE_AVAILABILITY_BY_AGE,
  UK_ADULT_POPULATION,
  UK_TOTAL_POPULATION,
} from "@/lib/data";

function fmt(n: number) {
  return n.toLocaleString("en-GB");
}

function pct(n: number, digits = 1) {
  return `${(n * 100).toFixed(digits)}%`;
}

const datasets: Array<{
  name: string;
  covers: string;
  meta: {
    geography: string;
    period: string;
    source: string;
    notes?: string;
  };
}> = [
  {
    name: "Age and population base",
    covers: "UK adult population, target-gender denominator, and exact single-year age shares.",
    meta: AGE_SINGLE_YEAR_DISTRIBUTION,
  },
  {
    name: "Ethnicity",
    covers: "Preferred ethnic-group filter.",
    meta: ETHNICITY_DISTRIBUTION,
  },
  {
    name: "Height",
    covers: "Target height range using sex and age-band mean heights with a normal-distribution model.",
    meta: HEIGHT,
  },
  {
    name: "Income, male",
    covers: "Minimum annual income filter for male targets.",
    meta: INCOME_DISTRIBUTION_MALE,
  },
  {
    name: "Income, female",
    covers: "Minimum annual income filter for female targets.",
    meta: INCOME_DISTRIBUTION_FEMALE,
  },
  {
    name: "Education",
    covers: "Minimum education filter.",
    meta: EDUCATION_DISTRIBUTION,
  },
  {
    name: "Body type, male",
    covers: "Preferred BMI category filter for male targets.",
    meta: BODY_TYPE_DISTRIBUTION_MALE,
  },
  {
    name: "Body type, female",
    covers: "Preferred BMI category filter for female targets.",
    meta: BODY_TYPE_DISTRIBUTION_FEMALE,
  },
  {
    name: "Single or available",
    covers: "Must be single / not living with partner filter.",
    meta: SINGLE_AVAILABILITY_BY_AGE,
  },
  {
    name: "Sexual orientation",
    covers: "Compatibility adjustment for heterosexual, gay/lesbian, and bisexual selections.",
    meta: SEXUAL_ORIENTATION_DISTRIBUTION,
  },
];

const sourceLinks = [
  {
    label: "ONS mid-year population estimates, mid-2024",
    href: "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2024",
    usedFor: "Adult base, sex split, and single-year age shares.",
  },
  {
    label: "NHS Health Survey for England 2024 data tables",
    href: "https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england/2024",
    usedFor: "Height means and adult BMI/body-type distribution.",
  },
  {
    label: "HMRC Personal Income Statistics, Table 3.3",
    href: "https://www.gov.uk/government/statistics/personal-incomes-statistics-for-the-tax-year-2023-to-2024",
    usedFor: "Total income before tax by sex, converted into all-adult income approximations.",
  },
  {
    label: "ONS marital status and living arrangements estimates",
    href: "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesbymaritalstatusandlivingarrangements",
    usedFor: "Not living in a couple by age and sex as an availability proxy.",
  },
  {
    label: "ONS Sexual orientation, UK: 2024",
    href: "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality/bulletins/sexualidentityuk/2024",
    usedFor: "Sexual-orientation distribution used in orientation compatibility.",
  },
  {
    label: "ONS Census 2021 ethnicity topic summary",
    href: "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity/bulletins/ethnicgroupenglandandwales/census2021",
    usedFor: "Ethnic-group distribution baseline before UK-wide adjustment.",
  },
  {
    label: "ONS Census 2021 qualification topic summary",
    href: "https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare/bulletins/educationenglandandwales/census2021",
    usedFor: "Highest qualification distribution for the education filter.",
  },
];

export default function MethodologyPage() {
  return (
    <main className="mx-auto max-w-5xl px-3 py-5 sm:px-4 sm:py-8 md:px-8">
      <header className="border-b border-zinc-800 pb-6">
        <Link
          href="/"
          className="inline-flex items-center rounded-full bg-zinc-900/80 px-3 py-1.5 text-xs font-semibold text-zinc-200 ring-1 ring-inset ring-zinc-700/80 transition-colors hover:bg-zinc-800 hover:text-white"
        >
          Back to calculator
        </Link>
        <h1 className="mt-5 bg-gradient-to-r from-rose-400 via-pink-500 to-violet-400 bg-clip-text text-3xl font-extrabold tracking-tight text-transparent sm:text-4xl md:text-5xl">
          Methodology, Caveats, Sources
        </h1>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-400 sm:text-base">
          This calculator is a statistical estimate, not a census count of available partners.
          It combines official demographic datasets with a transparent independence model so
          each filter can be inspected and challenged.
        </p>
      </header>

      <section className="grid gap-3 py-6 sm:grid-cols-3">
        <Metric label="UK population" value={fmt(UK_TOTAL_POPULATION)} />
        <Metric label="Adults aged 18+" value={fmt(UK_ADULT_POPULATION)} />
        <Metric
          label="Adult sex split"
          value={`${pct(GENDER_SPLIT.male, 1)} men / ${pct(GENDER_SPLIT.female, 1)} women`}
        />
      </section>

      <section className="border-t border-zinc-800 py-7">
        <h2 className="text-lg font-semibold text-zinc-100">How The Result Is Calculated</h2>
        <div className="mt-4 space-y-4 text-sm leading-6 text-zinc-400">
          <p>
            The headline uses the selected target pool as the denominator. If the user is
            looking for men, the percentage is out of UK adult men aged 18+. If they are
            looking for women, it is out of UK adult women aged 18+. If they choose any
            gender, it is out of all UK adults aged 18+.
          </p>
          <p>
            The cascade multiplies the target-gender base by age, height, body type, income,
            education, ethnicity, orientation, availability, children, marriage history, and
            baldness filters. The app also shows the all-adult percentage underneath the
            headline when the target denominator is only men or only women.
          </p>
          <code className="block overflow-x-auto rounded-lg border border-zinc-800 bg-zinc-950/70 p-3 text-xs text-zinc-300">
            estimated matches = UK adults aged 18+ x target gender share x each selected filter probability
          </code>
        </div>
      </section>

      <section className="border-t border-zinc-800 py-7">
        <h2 className="text-lg font-semibold text-zinc-100">Current Dataset Wiring</h2>
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {datasets.map((dataset) => (
            <article key={dataset.name} className="glass-panel rounded-xl p-4">
              <h3 className="text-sm font-semibold text-zinc-100">{dataset.name}</h3>
              <p className="mt-2 text-xs leading-5 text-zinc-400">{dataset.covers}</p>
              <dl className="mt-3 space-y-2 text-xs">
                <DataRow label="Geography" value={dataset.meta.geography} />
                <DataRow label="Period" value={dataset.meta.period} />
                <DataRow label="Source" value={dataset.meta.source} />
                {dataset.meta.notes && <DataRow label="Note" value={dataset.meta.notes} />}
              </dl>
            </article>
          ))}
        </div>
      </section>

      <section className="border-t border-zinc-800 py-7">
        <h2 className="text-lg font-semibold text-zinc-100">Known Caveats</h2>
        <div className="mt-4 space-y-3 text-sm leading-6 text-zinc-400">
          <p>
            The largest limitation is correlation. Income, age, education, region, ethnicity,
            and relationship status are not independent in real life. The calculator currently
            multiplies each filter independently because official public tables rarely provide
            the full joint distribution needed for a dating-market model.
          </p>
          <ul className="list-disc space-y-2 pl-5">
            {DATA_QUALITY_NOTES.map((note) => (
              <li key={note}>{note}</li>
            ))}
            <li>
              Height uses official age-band means, but still models the spread with retained
              standard deviations because the public HSE table does not publish full
              height-percentile distributions.
            </li>
            <li>
              The availability filter means not living in a couple. It does not prove someone
              is dating, compatible, reachable, or interested.
            </li>
          </ul>
        </div>
      </section>

      <section className="border-t border-zinc-800 py-7">
        <h2 className="text-lg font-semibold text-zinc-100">Official Source Links</h2>
        <div className="mt-4 grid gap-3">
          {sourceLinks.map((source) => (
            <a
              key={source.href}
              href={source.href}
              target="_blank"
              rel="noreferrer"
              className="glass-panel rounded-xl p-4 transition-colors hover:border-rose-500/40"
            >
              <span className="block text-sm font-semibold text-zinc-100">{source.label}</span>
              <span className="mt-1 block text-xs leading-5 text-zinc-400">{source.usedFor}</span>
            </a>
          ))}
        </div>
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="glass-panel rounded-xl p-4">
      <div className="text-[10px] font-bold uppercase tracking-wider text-zinc-500">{label}</div>
      <div className="mt-1 text-lg font-bold text-zinc-100">{value}</div>
    </div>
  );
}

function DataRow({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="font-semibold uppercase tracking-wider text-zinc-500">{label}</dt>
      <dd className="mt-0.5 leading-5 text-zinc-300">{value}</dd>
    </div>
  );
}
