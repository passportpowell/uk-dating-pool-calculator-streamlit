"""
UK Dating Pool Calculator - Sidebar UI Module
Contains sidebar input components
"""

import streamlit as st
from src.data.constants import (
    ETHNICITY_DISTRIBUTION, MIN_WAGE_ANNUAL, 
    MEDIAN_SALARY, AVERAGE_SALARY
)
from src.calculations.dating_pool import cm_to_feet_inches

# Explicitly export public API for safer imports
__all__ = ["create_sidebar"]


def _default_inputs():
    """Provide safe defaults when the full preference sidebar is hidden."""
    return {
        "user_gender": "Male",
        "user_orientation": "Heterosexual/Straight",
        "looking_for": "Female",
        "age_range": (25, 35),
        "min_height_cm": 140,
        "max_height_cm": 210,
        "selected_body_types": [
            "Underweight (BMI < 18.5)",
            "Healthy weight (BMI 18.5-24.9)",
            "Overweight (BMI 25-29.9)",
            "Obese (BMI 30+)"
        ],
        "min_income": 0,
        "education_level": "Any",
        "selected_ethnicities": list(ETHNICITY_DISTRIBUTION.keys()),
        "must_be_single": True,
        "acceptable_children": ["No children", "1 child", "2 children", "3+ children"],
        "acceptable_marriage_history": ["Never married", "Divorced", "Widowed"],
        "baldness_preference": "Any",
        "calculate_button": False,
    }


def create_sidebar(show_preferences: bool = True):
    """Create the sidebar. When show_preferences is False, return defaults without rendering all controls."""
    if not show_preferences:
        st.sidebar.header("Navigation")
        st.sidebar.info("Full dating preferences live on the Dating Pool Calculator page.")
        st.sidebar.markdown("---")
        return _default_inputs()

    st.sidebar.header("Your Preferences")
    st.sidebar.markdown("---")
    
    # User's own gender
    st.sidebar.subheader("About You")
    user_gender = st.sidebar.selectbox(
        "Your gender:",
        ["Male", "Female", "Other"],
        help="Your own gender identity"
    )
    
    # Sexual orientation
    st.sidebar.subheader("Sexual Orientation")
    user_orientation = st.sidebar.selectbox(
        "Your orientation:",
        ["Heterosexual/Straight", "Gay or Lesbian", "Bisexual"],
        help="Filter by sexual orientation compatibility (based on ONS 2022 data)"
    )
    
    # Gender selection - dynamically filtered based on orientation and user gender
    if user_orientation == "Heterosexual/Straight":
        if user_gender == "Male":
            looking_for_options = ["Female"]
            default_looking_for = "Female"
        elif user_gender == "Female":
            looking_for_options = ["Male"]
            default_looking_for = "Male"
        else:  # Other
            looking_for_options = ["Any", "Male", "Female"]
            default_looking_for = "Any"
    elif user_orientation == "Gay or Lesbian":
        if user_gender == "Male":
            looking_for_options = ["Male"]
            default_looking_for = "Male"
        elif user_gender == "Female":
            looking_for_options = ["Female"]
            default_looking_for = "Female"
        else:  # Other
            looking_for_options = ["Any", "Male", "Female"]
            default_looking_for = "Any"
    else:  # Bisexual
        looking_for_options = ["Any", "Male", "Female"]
        default_looking_for = "Any"
    
    looking_for = st.sidebar.selectbox(
        "Looking for:",
        looking_for_options,
        index=0,
        help="Gender you're interested in"
    )
    
    # Age range
    st.sidebar.subheader("Age")
    any_age = st.sidebar.checkbox(
        "Any age (adults only)",
        value=False,
        help="No age preference (18+)"
    )
    
    if not any_age:
        age_range = st.sidebar.slider(
            "Age range:",
            min_value=18,
            max_value=99,
            value=(25, 35),
            help="Preferred age range"
        )
    else:
        age_range = (18, 99)
    
    # Height range
    st.sidebar.subheader("Height")
    any_height = st.sidebar.checkbox(
        "Any height",
        value=True,
        help="No height preference"
    )
    
    if not any_height:
        height_unit = st.sidebar.radio(
            "Unit:",
            ["Metric (cm)", "Imperial (ft'in\")"],
            horizontal=True,
            index=0
        )
        
        if height_unit == "Metric (cm)":
            if looking_for == "Male":
                default_height = (165, 195)
                height_help = "Average UK male height is 175.3cm (5'9\")"
            else:
                default_height = (150, 175)
                height_help = "Average UK female height is 161.6cm (5'3\")"
            
            height_range = st.sidebar.slider(
                "Height range (cm):",
                min_value=140,
                max_value=210,
                value=default_height,
                help=height_help
            )
            min_height_cm, max_height_cm = height_range
        else:
            # Imperial (feet and inches)
            if looking_for == "Male":
                default_min_inches = 65  # 5'5"
                default_max_inches = 77  # 6'5"
                height_help = "Average UK male height is 5'9\""
            else:
                default_min_inches = 59  # 4'11"
                default_max_inches = 69  # 5'9"
                height_help = "Average UK female height is 5'3\""
            
            col_a, col_b = st.sidebar.columns([2, 1])
            with col_a:
                st.caption("Adjust slider below:")
            
            min_total_inches = st.sidebar.slider(
                "Minimum height:",
                min_value=55,
                max_value=83,
                value=default_min_inches,
                format="%d",
                help=height_help,
                label_visibility="visible"
            )
            min_ft = min_total_inches // 12
            min_in = min_total_inches % 12
            st.sidebar.markdown(f"**Min: {min_ft}'{min_in}\"** ({min_total_inches:.0f} inches)")
            
            max_total_inches = st.sidebar.slider(
                "Maximum height:",
                min_value=55,
                max_value=83,
                value=default_max_inches,
                format="%d",
                help=height_help,
                label_visibility="visible"
            )
            max_ft = max_total_inches // 12
            max_in = max_total_inches % 12
            st.sidebar.markdown(f"**Max: {max_ft}'{max_in}\"** ({max_total_inches:.0f} inches)")
            
            min_height_cm = min_total_inches * 2.54
            max_height_cm = max_total_inches * 2.54
            
            if min_height_cm > max_height_cm:
                min_height_cm, max_height_cm = max_height_cm, min_height_cm
    else:
        min_height_cm, max_height_cm = 140, 210
    
    # Body Type / BMI
    st.sidebar.subheader("Body Type")
    any_body_type = st.sidebar.checkbox(
        "Any body type",
        value=True,
        help="No body type preference"
    )
    
    if not any_body_type:
        selected_body_types = st.sidebar.multiselect(
            "Acceptable body types:",
            ["Underweight (BMI < 18.5)", "Healthy weight (BMI 18.5-24.9)", 
             "Overweight (BMI 25-29.9)", "Obese (BMI 30+)"],
            default=["Underweight (BMI < 18.5)", "Healthy weight (BMI 18.5-24.9)", 
                     "Overweight (BMI 25-29.9)", "Obese (BMI 30+)"],
            help="Select all acceptable body types based on BMI categories"
        )
    else:
        selected_body_types = ["Underweight (BMI < 18.5)", "Healthy weight (BMI 18.5-24.9)", 
                              "Overweight (BMI 25-29.9)", "Obese (BMI 30+)"]
    
    # Income
    st.sidebar.subheader("Income")
    min_income = st.sidebar.selectbox(
        "Minimum annual income (includes this amount and all higher):",
        ["Any", MIN_WAGE_ANNUAL, 25000, 30000, MEDIAN_SALARY, AVERAGE_SALARY, 
         40000, 50000, 75000, 100000, 150000, 250000, 500000, 1000000],
        format_func=lambda x: "Any" if x == "Any" else (
            f"£{x:,} (Min Wage)" if x == MIN_WAGE_ANNUAL else
            f"£{x:,} (UK Median)" if x == MEDIAN_SALARY else
            f"£{x:,} (UK Average)" if x == AVERAGE_SALARY else
            f"£{x:,} (Millionaire+)" if x == 1000000 else
            f"£{x:,}"
        ),
        help="Minimum acceptable annual income. Includes EVERYONE earning this amount or MORE."
    )
    if min_income == "Any":
        min_income = 0
    
    # Education
    st.sidebar.subheader("Education")
    education_level = st.sidebar.selectbox(
        "Minimum education level (includes this level and all higher levels):",
        ["Any", "Below GCSE", "GCSE/O-Level", "A-Level or equivalent", 
         "Undergraduate degree", "Postgraduate degree"],
        index=0,
        help="Select minimum acceptable education level."
    )
    
    # Ethnicity
    st.sidebar.subheader("Ethnicity")
    any_ethnicity = st.sidebar.checkbox(
        "Any ethnicity",
        value=True,
        help="No ethnicity preference"
    )
    
    if not any_ethnicity:
        selected_ethnicities = st.sidebar.multiselect(
            "Select specific ethnicities:",
            list(ETHNICITY_DISTRIBUTION.keys()),
            default=list(ETHNICITY_DISTRIBUTION.keys()),
            help="Select all acceptable ethnic backgrounds"
        )
    else:
        selected_ethnicities = list(ETHNICITY_DISTRIBUTION.keys())
    
    # Relationship status filter
    st.sidebar.subheader("Availability")
    must_be_single = st.sidebar.checkbox(
        "Must be single/available",
        value=True,
        help="Filter for people not currently in relationships"
    )
    
    # Children preference
    st.sidebar.subheader("Children")
    any_children = st.sidebar.checkbox(
        "Any (with or without children)",
        value=True,
        help="No preference about children"
    )
    
    if not any_children:
        acceptable_children = st.sidebar.multiselect(
            "Acceptable:",
            ["No children", "1 child", "2 children", "3+ children"],
            default=["No children"],
            help="Select all acceptable options"
        )
    else:
        acceptable_children = ["No children", "1 child", "2 children", "3+ children"]
    
    # Marriage history
    st.sidebar.subheader("Marriage History")
    any_marriage_history = st.sidebar.checkbox(
        "Any marriage history",
        value=True,
        help="No preference about marriage history"
    )
    
    if not any_marriage_history:
        acceptable_marriage_history = st.sidebar.multiselect(
            "Acceptable:",
            ["Never married", "Currently married", "Divorced", "Widowed"],
            default=["Never married", "Divorced", "Widowed"],
            help="Select all acceptable marriage histories"
        )
    else:
        acceptable_marriage_history = ["Never married", "Currently married", "Divorced", "Widowed"]
    
    # Handle conflict: if "must be single" is checked, remove "Currently married"
    if must_be_single and "Currently married" in acceptable_marriage_history:
        acceptable_marriage_history = [h for h in acceptable_marriage_history if h != "Currently married"]
        if not any_marriage_history:
            st.sidebar.info("💡 'Currently married' was automatically excluded because 'Must be single' is checked.")
    
    # Baldness (only for males)
    if looking_for == "Male" or looking_for == "Any":
        st.sidebar.subheader("Hair (Males)")
        baldness_preference = st.sidebar.selectbox(
            "Baldness preference:",
            ["Any", "Not bald", "Bald or balding"],
            help="Preference for male pattern baldness (varies by age)"
        )
    else:
        baldness_preference = "Any"
    
    st.sidebar.markdown("---")
    calculate_button = st.sidebar.button("Calculate", type="primary", use_container_width=True)
    
    # Return all inputs as a dictionary
    return {
        "user_gender": user_gender,
        "user_orientation": user_orientation,
        "looking_for": looking_for,
        "age_range": age_range,
        "min_height_cm": min_height_cm,
        "max_height_cm": max_height_cm,
        "selected_body_types": selected_body_types,
        "min_income": min_income,
        "education_level": education_level,
        "selected_ethnicities": selected_ethnicities,
        "must_be_single": must_be_single,
        "acceptable_children": acceptable_children,
        "acceptable_marriage_history": acceptable_marriage_history,
        "baldness_preference": baldness_preference,
        "calculate_button": calculate_button
    }
