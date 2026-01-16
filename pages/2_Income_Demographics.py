"""
UK Dating Pool Calculator - Income Demographics Page
Income statistics and demographics explorer
"""

import streamlit as st
from src.utils.styles import CUSTOM_CSS
from src.ui.income_stats import display_income_demographics_tab
from src.ui.sidebar import create_sidebar
from src.data.provenance import show_data_provenance

# Page configuration
st.set_page_config(
    page_title="Income Demographics - UK Dating Pool Calculator",
    page_icon="💷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">💷 Income Demographics Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Explore UK income statistics by age, gender, and ethnicity</div>', unsafe_allow_html=True)

# Get minimal defaults from sidebar (full preferences live on the Dating Pool Calculator page)
inputs = create_sidebar(show_preferences=False)

# Display income demographics tab
display_income_demographics_tab(inputs)

# Show provenance for transparency
with st.expander("Data Provenance", expanded=False):
    show_data_provenance()

# Explicit files used for this page (raw + processed)
with st.expander("Files Used (Income Demographics)", expanded=False):
    st.markdown(
        """
- data/raw/censusbasedstatisticsuk2021.xlsx (Table_01, UK population by single year of age and sex)
- data/raw/Home Geography Table 8.7a   Annual pay - Gross 2024.xlsx (Male sheet, ONS ASHE 2024 percentiles)
- data/processed/income_distribution_male.csv (override for male income distribution)
- data/processed/income_distribution_female.csv (override for female income distribution)
- data/processed/employment_rate_by_age_gender.csv (employment rates)
- data/processed/single_rate_by_age.csv (single / never married rates)
        """
    )
