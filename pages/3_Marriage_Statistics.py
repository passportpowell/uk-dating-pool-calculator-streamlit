"""
UK Dating Pool Calculator - Marriage Statistics Page
Comprehensive marriage, divorce, and family statistics
"""

import streamlit as st
from src.utils.styles import CUSTOM_CSS
from src.ui.marriage_stats import display_marriage_statistics_tab
from src.ui.sidebar import create_sidebar
from src.data.provenance import show_data_provenance

# Page configuration
st.set_page_config(
    page_title="Marriage Statistics - UK Dating Pool Calculator",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">💍 Marriage Statistics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Comprehensive marriage, divorce, and family data for the UK</div>', unsafe_allow_html=True)

# Get minimal defaults from sidebar (full preferences live on the Dating Pool Calculator page)
inputs = create_sidebar(show_preferences=False)

# Display marriage statistics tab
display_marriage_statistics_tab(inputs['user_orientation'], inputs['looking_for'], inputs['user_gender'])

# Show provenance for transparency
with st.expander("Data Provenance", expanded=False):
    show_data_provenance()

# Files used for this page
with st.expander("Files Used (Marriage Statistics)", expanded=False):
    st.markdown(
        """
- data/raw/marital_status_and_living_arrangements_2002_2024.xlsx (marital status by age and sex)
- data/raw/Families and households in the UK 2024.pdf (family composition)
- data/raw/United Kingdom population mid-year estimate 2025.xls (population context)
- data/raw/censusbasedstatisticsuk2021.xlsx (Table_01, age/sex counts)
- data/processed/single_rate_by_age.csv (single / never married rates for calculations)
        """
    )
