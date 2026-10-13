import SiteShell from "@/components/SiteShell";
import { sourceLibrary, childrenStatus } from "@/lib/calculator";
export default function Sources() {
  return (
    <SiteShell>
      <div className="intro">
        <span className="eyebrow">Traceable inputs</span>
        <h1>
          Sources behind
          <br />
          <em>the estimate.</em>
        </h1>
        <p>
          Every active input has an original publication or table. Check its
          date, coverage and the way it is used before interpreting a result.
        </p>
      </div>
      <div className="source-grid">
        {sourceLibrary.map((s) => (
          <article id={s.id} className="panel source-card" key={s.id}>
            <h2>{s.title}</h2>
            <p>{s.explanation}</p>
            <dl>
              <dt>Reference</dt>
              <dd>{String(s.reference)}</dd>
              <dt>Coverage</dt>
              <dd>{s.geography}</dd>
              <dt>Table / query</dt>
              <dd>{String(s.tables)}</dd>
              {s.sha256 && (
                <>
                  <dt>SHA-256</dt>
                  <dd>{s.sha256}</dd>
                </>
              )}
            </dl>
            <p>
              <a href={s.url} target="_blank" rel="noopener noreferrer">
                Original publisher ↗
              </a>
              {s.apiURL && (
                <>
                  {" "}
                  ·{" "}
                  <a href={s.apiURL} target="_blank" rel="noopener noreferrer">
                    Exact API query ↗
                  </a>
                </>
              )}
              {s.file && (
                <>
                  {" "}
                  ·{" "}
                  <a href={s.file} download>
                    Retained data
                  </a>
                </>
              )}
            </p>
          </article>
        ))}
      </div>
      <section className="panel" style={{ marginTop: 24 }}>
        <h2>Children and co-parents</h2>
        <p>{childrenStatus.explanation}</p>
        <p>
          Household measures do not establish whether an adult has grown-up
          children or children living elsewhere. The number of different
          co-parents is not included.
        </p>
      </section>
    </SiteShell>
  );
}
