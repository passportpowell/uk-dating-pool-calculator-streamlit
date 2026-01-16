"""
Fetch official datasets and write normalized CSVs to data_cache/.
Supports API JSON endpoints and direct file downloads (CSV/XLSX).
Configure sources in data_sources.json.
"""

import os
import io
import json
from datetime import datetime
from typing import List, Dict

import pandas as pd
import requests

CACHE_DIR = os.path.join(os.path.dirname(__file__), "data_cache")
RAW_DIR = os.path.join(CACHE_DIR, "raw")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data_sources.json")

def _load_config() -> List[Dict[str, str]]:
    if not os.path.exists(CONFIG_PATH):
        return []
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_metadata(provenance: List[Dict[str, str]]):
    meta_path = os.path.join(CACHE_DIR, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)


def _normalize_simple_kv(df: pd.DataFrame) -> pd.DataFrame:
    # Expect columns: key,value (or try to infer first two columns)
    cols = list(df.columns)
    if "key" not in df.columns or "value" not in df.columns:
        if len(cols) >= 2:
            df = df.rename(columns={cols[0]: "key", cols[1]: "value"})
    df = df[["key", "value"]].copy()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna()
    s = df["value"].sum()
    if s > 0:
        df["value"] = df["value"] / s
    return df

def _parse_employment(df: pd.DataFrame) -> pd.DataFrame:
    # Expect columns: age_band,gender,rate
    cols = list(df.columns)
    mapping = {}
    # Try to align columns by names or position
    col_age = "age_band" if "age_band" in cols else cols[0]
    col_gender = "gender" if "gender" in cols else cols[1]
    col_rate = "rate" if "rate" in cols else cols[2]
    df = df.rename(columns={col_age: "age_band", col_gender: "gender", col_rate: "rate"})
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df = df.dropna()
    return df[["age_band", "gender", "rate"]]

def _save_df(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

def fetch_all():
    datasets = _load_config()
    provenance: List[Dict[str, str]] = []

    for ds in datasets:
        name = ds.get("name", "")
        source = ds.get("source", "")
        dtype = ds.get("type", "simple_kv")
        fmt = ds.get("format", "csv")
        outfile = ds.get("outfile", "out.csv")
        notes = ds.get("notes", "")

        if not source:
            provenance.append({
                "dataset": name,
                "source_url": source,
                "outfile": outfile,
                "last_fetched": datetime.utcnow().isoformat() + "Z",
                "error": "No source configured"
            })
            continue

        try:
            resp = requests.get(source, timeout=60)
            resp.raise_for_status()

            # Save raw
            raw_name = f"raw_{outfile}"
            raw_path = os.path.join(RAW_DIR, raw_name)
            with open(raw_path, "wb") as f:
                f.write(resp.content)

            # Parse by format
            if fmt.lower() == "csv":
                df = pd.read_csv(io.BytesIO(resp.content))
            elif fmt.lower() in ("xlsx", "excel"):
                df = pd.read_excel(io.BytesIO(resp.content))
            elif fmt.lower() == "json":
                data = resp.json()
                df = pd.json_normalize(data)
            else:
                df = pd.DataFrame()

            # Transform by type
            if dtype == "simple_kv":
                df = _normalize_simple_kv(df)
            elif dtype == "employment":
                df = _parse_employment(df)
            else:
                # Unknown type; write raw-parsed
                pass

            # Save normalized CSV
            out_path = os.path.join(CACHE_DIR, outfile)
            _save_df(df, out_path)

            provenance.append({
                "dataset": name,
                "source_url": source,
                "outfile": outfile,
                "last_fetched": datetime.utcnow().isoformat() + "Z",
                "notes": notes
            })
        except Exception as e:
            provenance.append({
                "dataset": name,
                "source_url": source,
                "outfile": outfile,
                "last_fetched": datetime.utcnow().isoformat() + "Z",
                "error": str(e)
            })

    _write_metadata(provenance)


if __name__ == "__main__":
    fetch_all()
