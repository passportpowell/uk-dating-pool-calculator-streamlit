"""
UK Dating Pool Calculator - Dating Pool Calculator Page
Calculate your dating pool size based on your preferences
"""

import streamlit as st
import pandas as pd
import numpy as np

# Import from modular files
from src.data.constants import UK_ADULT_POPULATION
from src.utils.styles import CUSTOM_CSS
from src.ui.sidebar import create_sidebar
from src.ui.results import display_results, display_probability_breakdown_tab, display_criteria_tab, display_map_tab
from src.calculations.dating_pool import (
    calculate_age_probability,
    calculate_height_probability,
    calculate_income_probability,
    calculate_education_probability,
    calculate_ethnicity_probability,
    calculate_body_type_probability,
    calculate_orientation_probability,
    calculate_children_probability,
    calculate_marriage_probability,
    calculate_baldness_probability
)

# Page configuration
st.set_page_config(
    page_title="Dating Pool Calculator - UK Dating Statistics",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎯 Dating Pool Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enter your preferences below and calculate your realistic dating pool size</div>', unsafe_allow_html=True)

# Create sidebar and get all inputs
inputs = create_sidebar()

# Main content
if inputs['calculate_button']:
    # Validation
    if inputs['education_level'] not in ["Any", "Below GCSE", "GCSE/O-Level", "A-Level or equivalent", "Undergraduate degree", "Postgraduate degree"]:
        st.error("Please select a valid education level")
        st.stop()
    
    if not inputs['selected_ethnicities']:
        st.error("Please select at least one ethnicity or choose 'Any ethnicity'")
        st.stop()
    
    if not inputs['selected_body_types']:
        st.error("Please select at least one body type or choose 'Any body type'")
        st.stop()
    
    if not inputs['acceptable_children']:
        st.error("Please select at least one children option or choose 'Any'")
        st.stop()
    
    if not inputs['acceptable_marriage_history']:
        st.error("Please select at least one marriage history option or choose 'Any marriage history'")
        st.stop()
    
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
        
        # Create tabs for detailed breakdown
        st.markdown("---")
        st.markdown("### Detailed Analysis")
        
        tab1, tab2, tab3 = st.tabs(["📊 Probability Breakdown", "⚙️ Your Criteria", "🗺️ Map Breakdown"])
        
        with tab1:
            display_probability_breakdown_tab(inputs, probabilities, estimated_matches, percentage)
        
        with tab2:
            display_criteria_tab(inputs)
        
        with tab3:
            display_map_tab(total_probability, estimated_matches)

else:
    st.info("👈 Use the sidebar to enter your preferences and click **Calculate** to see your dating pool size.")
    
    st.markdown("""
    ### How It Works
    
    This calculator uses official UK statistics to estimate how many people match your dating criteria:
    
    1. **Enter your preferences** in the sidebar (age, height, income, etc.)
    2. Click **Calculate** to see your results
    3. View detailed breakdowns showing how each filter affects your dating pool
    4. See geographic distribution across UK regions
    
    All calculations use real data from:
    - ONS Census 2021
    - NHS Health Survey for England 2021
    - ONS Labour Force Survey 2023
    - And other official sources
    """)
