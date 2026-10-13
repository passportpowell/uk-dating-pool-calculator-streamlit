"use client";
import { useState } from "react";
import Link from "next/link";
import SiteShell from "@/components/SiteShell";
import {
  DEFAULT_CRITERIA,
  calculateRegions,
  SEX_LABELS,
  type Criteria,
} from "@/lib/calculator";
export default function Explorer() {
  const [sex, setSex] = useState<Criteria["sex"]>("Persons");
  const rows = calculateRegions({ ...DEFAULT_CRITERIA, sex, min: 18, max: 90, relationship: "any" });
  return (
    <SiteShell>
      <div className="intro">
        <span className="eyebrow">Data explorer</span>
        <h1>
          The population
          <br />
          <em>behind the pool.</em>
        </h1>
        <p>
          Explore adult population baselines by country and English region.
          These are starting populations, before dating requirements are
          applied.
        </p>
      </div>
      <section className="panel">
        <label>
          Population group{" "}
          <select
            value={sex}
            onChange={(e) => setSex(e.target.value as Criteria["sex"])}
          >
            {Object.entries(SEX_LABELS).map(([key, label]) => (
              <option value={key} key={key}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <div className="table-wrap">
          <table>
            <caption
              className="small"
              style={{ textAlign: "left", padding: "20px 0" }}
            >
              Adults aged 18+, using the retained ONS population reference. Open
              a location in the calculator to apply your requirements.
            </caption>
            <thead>
              <tr>
                <th scope="col">Location</th>
                <th scope="col">Adults aged 18+</th>
                <th scope="col">Calculator</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.geo}>
                  <th scope="row">{r.name}</th>
                  <td>{Math.round(r.base).toLocaleString("en-GB")}</td>
                  <td>
                    <Link
                      href={
                        "/?c=" +
                        encodeURIComponent(
                          JSON.stringify({
                            v: 1,
                            criteria: { ...DEFAULT_CRITERIA, geo: r.geo, sex },
                          }),
                        )
                      }
                    >
                      Choose {r.name}
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="small">
          Regional population differences are observed. Any filter applied using
          a wider geographic proxy is disclosed in the calculator.
        </p>
        <Link href="/sources">View population source and retained tables</Link>
      </section>
    </SiteShell>
  );
}
