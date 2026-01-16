import streamlit as st
import pandas as pd
from typing import List, Dict

try:
    from src.data.constants import DATA_PROVENANCE
except Exception:
    DATA_PROVENANCE = []


def show_data_provenance():
    st.subheader("Data Provenance")
    if not DATA_PROVENANCE:
        st.info("Using curated static distributions bundled with the app. Configure data/processed/ and run fetch_sources.py to enable live data overrides.")
        return
    # Expect a list of dicts
    df = pd.DataFrame(DATA_PROVENANCE)
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.caption("Provenance shows dataset names, source URLs, last fetched timestamps, and any fetch notes/errors.")
