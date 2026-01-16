"""
UK Dating Pool Calculator - Baby & Child Health Page
Baby and child health statistics
"""

import streamlit as st
from src.utils.styles import CUSTOM_CSS
from src.ui.baby_stats import display_baby_statistics_tab
from src.ui.sidebar import create_sidebar
from src.data.provenance import show_data_provenance

# Page configuration
st.set_page_config(
    page_title="Baby & Child Health - UK Dating Pool Calculator",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">👶 Baby & Child Health Statistics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">UK health statistics for babies and children</div>', unsafe_allow_html=True)

# Get minimal defaults from sidebar (full preferences live on the Dating Pool Calculator page)
inputs = create_sidebar(show_preferences=False)

# Display baby statistics tab
display_baby_statistics_tab()

# Show provenance for transparency
with st.expander("Data Provenance", expanded=False):
    show_data_provenance()
