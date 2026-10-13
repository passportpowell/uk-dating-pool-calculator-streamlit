import Link from "next/link";
import SiteShell from "@/components/SiteShell";
export default function Methodology() {
  return (
    <SiteShell>
      <div className="intro">
        <span className="eyebrow">How it works</span>
        <h1>
          Published facts.
          <br />
          <em>Estimated overlap.</em>
        </h1>
        <p>
          The calculator answers: what share of adults in the selected group
          meet these requirements?
        </p>
      </div>
      <section className="panel">
        <h2>Start with the right population</h2>
        <p>
          The starting pool is everyone aged 18 or above of the selected sex, in
          the selected location. The age requirement narrows that pool; it does
          not change the percentage denominator. The 90+ group is included once.
        </p>
        <h2>Calculate within each age and sex</h2>
        <p>
          We apply the available rates within each age and sex group, then add
          their estimated counts. Where a published table measures two
          requirements together, that table is used for their overlap.
        </p>
        <h2>What we have to assume</h2>
        <p>
          Published sources do not measure every requirement together. Combining
          the remaining rates assumes that their overlap follows those rates
          within each group. Income, relationship status, health and other
          characteristics may still be related, so the combined count is an
          estimate.
        </p>
        <p>
          Some tables cover England or England and Wales and are used as proxies
          elsewhere. Each result and the source library explain these limits.
          Height uses published averages and an assumed distribution; its
          sensitivity comparison has no claimed confidence level.
        </p>
        <h2>Read the breakdown</h2>
        <p>
          “Remaining” is the share of the original starting pool after that
          step. “Drop” is the share removed from the preceding step. The final
          step and headline use the same calculation.
        </p>
        <h2>Children and missing information</h2>
        <p>
          A household child measure only describes children living in that
          household. Someone with no dependent children at home may still have
          children living elsewhere or grown-up children. Biological, adopted
          and co-parent details are included only when supported by the source.
          Any requirement we cannot account for is stated in the result.
        </p>
        <h2>Share and compare</h2>
        <p>
          A scenario link includes every canonical requirement in a versioned
          format. Three scenarios can be compared in the current tab. Downloaded
          results retain requirements, the breakdown and source references.
        </p>
        <p>
          <Link href="/sources">Inspect every active source</Link>
        </p>
      </section>
    </SiteShell>
  );
}
