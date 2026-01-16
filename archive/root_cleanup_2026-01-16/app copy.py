"""
UK Dating Pool Calculator - Main Application
Modular version of the dating pool calculator with clean separation of concerns

Modules:
- data.py: All statistical data and constants
- calculations.py: Probability calculation functions
- map_visualization.py: Map creation for geographic distribution
- styles.py: CSS styling
- ui_sidebar.py: Sidebar input components
- ui_results.py: Results display (breakdown, criteria, map tabs)

Note: Marriage statistics tab (tab4) content is extensive (~2000 lines) and remains
imported from the original app_original_full.py for now. To fully modularize it, 
extract lines 1290-3200 from app_original_full.py into a new ui_marriage_stats.py module.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import from modular files
from data import UK_ADULT_POPULATION
from styles import CUSTOM_CSS
from ui_sidebar import create_sidebar
from ui_results import display_results, display_probability_breakdown_tab, display_criteria_tab, display_map_tab
from ui_marriage_stats_content import display_marriage_statistics_tab
from ui_baby_stats_content import display_baby_statistics_tab
from ui_income_stats_content import display_income_demographics_tab
from calculations import (
    calculate_age_probability,
    calculate_height_probability,
    calculate_income_probability,
    calculate_education_probability,
    calculate_ethnicity_probability,
    calculate_body_type_probability,
    calculate_orientation_probability,
    calculate_children_probability,
    calculate_marriage_probability,
    calculate_baldness_probability,
    calculate_population_pipeline,
    get_employment_rate_by_age_gender
)

# Import the marriage statistics tab from original file
# (To fully modularize, move this to a separate ui_marriage_stats.py file)
import sys
sys.path.insert(0, 'e:\\OneDrive\\Github\\UK dating statistic calculator')


# Page configuration
st.set_page_config(
    page_title="UK Dating Pool Calculator",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def main():
    # Initialize session state for results persistence
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'results_data' not in st.session_state:
        st.session_state.results_data = None
    
    # Header
    st.markdown('<div class="main-header">UK Dating Pool Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Calculate your realistic dating pool size using real UK statistics \n for United Kingdom includes England, Scotland, Wales, and Northern Ireland (NOT Republic of Ireland)</div>', unsafe_allow_html=True)
    
    # Create sidebar and get all inputs
    inputs = create_sidebar()
    
    # Set flag when calculate is pressed
    if inputs['calculate_button']:
        st.session_state.show_results = True
    
    # Main content
    if st.session_state.show_results:
        # Validation
        if inputs['education_level'] not in ["Any", "Below GCSE", "GCSE/O-Level", "A-Level or equivalent", "Undergraduate degree", "Postgraduate degree"]:
            st.error("Please select a valid education level")
            return
        
        if not inputs['selected_ethnicities']:
            st.error("Please select at least one ethnicity or choose 'Any ethnicity'")
            return
        
        if not inputs['selected_body_types']:
            st.error("Please select at least one body type or choose 'Any body type'")
            return
        
        if not inputs['acceptable_children']:
            st.error("Please select at least one children option or choose 'Any'")
            return
        
        if not inputs['acceptable_marriage_history']:
            st.error("Please select at least one marriage history option or choose 'Any marriage history'")
            return
        
        # Calculate probabilities
        with st.spinner("Calculating your dating pool..."):
            # Gender split (UK adults: 49.2% male, 50.8% female)
            if inputs['looking_for'] == "Any":
                gender_prob = 1.0
            elif inputs['looking_for'] == "Male":
                gender_prob = 0.492
            else:  # Female
                gender_prob = 0.508
            
            # Age probability
            age_prob = calculate_age_probability(inputs['age_range'][0], inputs['age_range'][1])
            
            # Height probability
            if inputs['looking_for'] == "Any":
                male_height_prob = calculate_height_probability(inputs['min_height_cm'], inputs['max_height_cm'], "Male")
                female_height_prob = calculate_height_probability(inputs['min_height_cm'], inputs['max_height_cm'], "Female")
                height_prob = 0.492 * male_height_prob + 0.508 * female_height_prob
            else:
                height_prob = calculate_height_probability(inputs['min_height_cm'], inputs['max_height_cm'], inputs['looking_for'])
            
            # Income probability
            if inputs['looking_for'] == "Any":
                male_income_prob = calculate_income_probability(inputs['min_income'], "Male")
                female_income_prob = calculate_income_probability(inputs['min_income'], "Female")
                income_prob = 0.492 * male_income_prob + 0.508 * female_income_prob
            else:
                income_prob = calculate_income_probability(inputs['min_income'], inputs['looking_for'])
            
            # Education probability
            education_prob = calculate_education_probability(inputs['education_level'])
            
            # Ethnicity probability
            ethnicity_prob = calculate_ethnicity_probability(inputs['selected_ethnicities'])
            
            # Body type probability
            if inputs['looking_for'] == "Any":
                male_body_prob = calculate_body_type_probability(inputs['selected_body_types'], "Male")
                female_body_prob = calculate_body_type_probability(inputs['selected_body_types'], "Female")
                body_type_prob = 0.492 * male_body_prob + 0.508 * female_body_prob
            else:
                body_type_prob = calculate_body_type_probability(inputs['selected_body_types'], inputs['looking_for'])
            
            # Sexual orientation compatibility
            orientation_prob = calculate_orientation_probability(inputs['user_orientation'], inputs['looking_for'], inputs['user_gender'])
            
            # Relationship status
            if inputs['must_be_single']:
                # Use age-specific single rate for accuracy
                from calculations import get_single_rate_by_age
                single_prob = get_single_rate_by_age(inputs['age_range'][0], inputs['age_range'][1])
            else:
                single_prob = 1.0
            
            # Children probability
            children_prob = calculate_children_probability(inputs['acceptable_children'])
            
            # Marriage history probability
            marriage_prob = calculate_marriage_probability(
                inputs['acceptable_marriage_history'],
                inputs['user_gender'],
                inputs['looking_for'],
                inputs['user_orientation']
            )
            
            # Baldness probability (only applies to males)
            if inputs['looking_for'] == "Male":
                baldness_prob = calculate_baldness_probability(inputs['baldness_preference'], inputs['age_range'], "Male")
            elif inputs['looking_for'] == "Any":
                male_baldness_prob = calculate_baldness_probability(inputs['baldness_preference'], inputs['age_range'], "Male")
                female_baldness_prob = calculate_baldness_probability(inputs['baldness_preference'], inputs['age_range'], "Female")
                # Average: 49.2% male, 50.8% female
                baldness_prob = 0.492 * male_baldness_prob + 0.508 * female_baldness_prob
            else:
                baldness_prob = 1.0  # Female or other gender - no baldness filter
            
            # Combined probability
            total_probability = (gender_prob * age_prob * height_prob * body_type_prob *
                               income_prob * education_prob * ethnicity_prob * 
                               orientation_prob * single_prob * children_prob * marriage_prob * baldness_prob)
            
            # Calculate actual numbers
            estimated_matches = int(UK_ADULT_POPULATION * total_probability)
            percentage = total_probability * 100
            
            # Store probabilities tuple
            probabilities = (gender_prob, age_prob, height_prob, body_type_prob, income_prob,
                           education_prob, ethnicity_prob, orientation_prob, single_prob,
                           children_prob, marriage_prob, baldness_prob)
            
            # Display results
            display_results(inputs, probabilities, estimated_matches, percentage)
            
            st.markdown("---")
            
            # Create tabs for detailed breakdown
            st.markdown("""
                <style>
                .stTabs [data-baseweb="tab-list"] {
                    justify-content: center;
                }
                .stTabs [data-baseweb="tab-list"] button {
                    font-size: 1.8rem !important;
                    padding: 30px 60px !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Create session state for tab selection if not exists
            if 'selected_tab' not in st.session_state:
                st.session_state.selected_tab = 0
            
            # Tab grid layout (2 rows x 3 columns)
            st.markdown("### Navigation")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Probability Breakdown", use_container_width=True, key="tab_0"):
                    st.session_state.selected_tab = 0
            with col2:
                if st.button("⚙️ Your Criteria", use_container_width=True, key="tab_1"):
                    st.session_state.selected_tab = 1
            with col3:
                if st.button("🗺️ Map Breakdown", use_container_width=True, key="tab_2"):
                    st.session_state.selected_tab = 2
            
            col4, col5, col6 = st.columns(3)
            with col4:
                if st.button("💷 Income Demographics", use_container_width=True, key="tab_3"):
                    st.session_state.selected_tab = 3
            with col5:
                if st.button("💍 Marriage Statistics", use_container_width=True, key="tab_4"):
                    st.session_state.selected_tab = 4
            with col6:
                if st.button("👶 Baby & Child Health", use_container_width=True, key="tab_5"):
                    st.session_state.selected_tab = 5
            
            st.divider()
            
            # Display selected tab content
            if st.session_state.selected_tab == 0:
                display_probability_breakdown_tab(inputs, probabilities, estimated_matches, percentage)
            
            elif st.session_state.selected_tab == 1:
                display_criteria_tab(inputs)
            
            elif st.session_state.selected_tab == 2:
                display_map_tab(total_probability, estimated_matches)
            
            elif st.session_state.selected_tab == 3:
                display_income_demographics_tab(inputs)

            elif st.session_state.selected_tab == 4:
                # Marriage Statistics Tab - now properly modularized
                display_marriage_statistics_tab(inputs['user_orientation'], inputs['looking_for'], inputs['user_gender'])
            
            elif st.session_state.selected_tab == 5:
                # Baby & Child Health Statistics Tab
                display_baby_statistics_tab()
    
    # Sources section
    with st.expander("Data Sources & Methodology"):
        st.markdown("""
        ### Data Sources
        
        All statistics are based on official UK government data and peer-reviewed research.
        For full data sources and methodology, please refer to the original app_original_full.py file
        or the comprehensive documentation section (lines 3270-3390).
        
        **Key Sources:**
        - ONS Population Estimates (Mid-2022)
        - ONS Census 2021 - Ethnic Group, England and Wales
        - NHS Health Survey for England 2021
        - ONS Annual Survey of Hours and Earnings (ASHE) 2023
        - HMRC Income Tax Liabilities Statistics
        - ONS Sexual Orientation, UK 2022
        - ONS Families and Households 2022
        - ONS Marriage & Divorce Statistics 2022
        - British Association of Dermatologists (baldness data)
        
        ### Methodology
        
        This calculator uses **independent probability multiplication** to estimate your dating pool size.
        Each criterion acts as a filter that narrows down the population.
        
        For detailed methodology, assumptions, and limitations, please refer to the
        comprehensive documentation in app_original_full.py (lines 3270-3390).
        """)


if __name__ == "__main__":
    main()
