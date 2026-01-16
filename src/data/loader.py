"""
Data Loader: Overrides for distributions from local cache.
Loads CSV files from data/processed/ to override curated constants in src.data.constants.
"""

import os
import csv
from typing import Dict, Tuple, List, Any

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")


def _load_simple_kv_csv(path: str) -> Dict[str, float]:
    out: Dict[str, float] = {}
    if not os.path.exists(path):
        return out
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # expects columns: key,value
        for row in reader:
            k = row.get("key")
            v = row.get("value")
            if k is None or v is None:
                continue
            try:
                out[k] = float(v)
            except ValueError:
                continue
    # normalize to 1.0 if sums close
    s = sum(out.values())
    if s > 0:
        out = {k: (v / s) for k, v in out.items()}
    return out


def _load_employment_csv(path: str) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {}
    if not os.path.exists(path):
        return out
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # expects columns: age_band,gender,rate
        for row in reader:
            band = row.get("age_band")
            gender = row.get("gender")
            rate = row.get("rate")
            if not band or not gender or rate is None:
                continue
            try:
                r = float(rate)
            except ValueError:
                continue
            out.setdefault(band, {})[gender] = r
    return out


def load_override_data() -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Load available override datasets from cache.
    Returns (overrides, provenance)
    """
    overrides: Dict[str, Any] = {}
    provenance: List[Dict[str, Any]] = []

    # Ethnicity distribution
    eth_path = os.path.join(CACHE_DIR, "ethnicity_distribution.csv")
    eth = _load_simple_kv_csv(eth_path)
    if eth:
        overrides["ETHNICITY_DISTRIBUTION"] = eth
        provenance.append({
            "dataset": "Ethnicity Distribution",
            "file": os.path.basename(eth_path)
        })

    # Single rate by age
    single_path = os.path.join(CACHE_DIR, "single_rate_by_age.csv")
    single = _load_simple_kv_csv(single_path)
    if single:
        overrides["SINGLE_RATE_BY_AGE"] = single
        provenance.append({
            "dataset": "Single Rate by Age",
            "file": os.path.basename(single_path)
        })

    # Employment rate by age/gender
    emp_path = os.path.join(CACHE_DIR, "employment_rate_by_age_gender.csv")
    emp = _load_employment_csv(emp_path)
    if emp:
        overrides["EMPLOYMENT_RATE_BY_AGE_GENDER"] = emp
        provenance.append({
            "dataset": "Employment Rate by Age & Gender",
            "file": os.path.basename(emp_path)
        })

    # Employee income distributions
    inc_m_path = os.path.join(CACHE_DIR, "income_distribution_male.csv")
    inc_f_path = os.path.join(CACHE_DIR, "income_distribution_female.csv")
    inc_m = _load_simple_kv_csv(inc_m_path)
    inc_f = _load_simple_kv_csv(inc_f_path)
    if inc_m:
        overrides["INCOME_DISTRIBUTION_MALE"] = inc_m
        provenance.append({
            "dataset": "Income Distribution (Male)",
            "file": os.path.basename(inc_m_path)
        })
    if inc_f:
        overrides["INCOME_DISTRIBUTION_FEMALE"] = inc_f
        provenance.append({
            "dataset": "Income Distribution (Female)",
            "file": os.path.basename(inc_f_path)
        })

    # Self-employed income distributions
    se_m_path = os.path.join(CACHE_DIR, "self_employed_income_distribution_male.csv")
    se_f_path = os.path.join(CACHE_DIR, "self_employed_income_distribution_female.csv")
    se_m = _load_simple_kv_csv(se_m_path)
    se_f = _load_simple_kv_csv(se_f_path)
    if se_m:
        overrides["SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE"] = se_m
        provenance.append({
            "dataset": "Self-Employed Income (Male)",
            "file": os.path.basename(se_m_path)
        })
    if se_f:
        overrides["SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE"] = se_f
        provenance.append({
            "dataset": "Self-Employed Income (Female)",
            "file": os.path.basename(se_f_path)
        })

    # Attach metadata.json if present
    meta_path = os.path.join(CACHE_DIR, "metadata.json")
    if os.path.exists(meta_path):
        import json
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                if isinstance(meta, list):
                    provenance = meta
        except Exception:
            pass

    return overrides, provenance
