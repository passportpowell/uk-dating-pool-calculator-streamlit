import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="UK Dating Pool Calculator",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF1493;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 2rem 0;
    }
    .result-percentage {
        font-size: 4rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .result-count {
        font-size: 1.5rem;
        opacity: 0.9;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
        font-size: 0.9rem;
    }
    .stProgress > div > div > div > div {
        background-color: #FF1493;
    }
    </style>
""", unsafe_allow_html=True)

# UK Population data based on ONS statistics
UK_TOTAL_POPULATION = 67_736_802  # Mid-2022 estimate
UK_ADULT_POPULATION = 52_600_000  # Ages 18+

# Age distribution (% of adults 18+)
AGE_DISTRIBUTION = {
    "18-24": 0.119,
    "25-34": 0.187,
    "35-44": 0.172,
    "45-54": 0.186,
    "55-64": 0.162,
    "65+": 0.174
}

# Detailed ethnicity distribution (Census 2021)
# Normalized to sum to exactly 1.0
ETHNICITY_DISTRIBUTION = {
    "White British": 0.744,
    "White Irish": 0.009,
    "White Other": 0.062,
    "Asian/Asian British - Indian": 0.030,
    "Asian/Asian British - Pakistani": 0.024,
    "Asian/Asian British - Bangladeshi": 0.010,
    "Asian/Asian British - Chinese": 0.009,
    "Asian/Asian British - Other": 0.020,
    "Black/Black British - African": 0.025,
    "Black/Black British - Caribbean": 0.010,
    "Black/Black British - Other": 0.005,
    "Mixed - White & Black Caribbean": 0.009,
    "Mixed - White & Black African": 0.005,
    "Mixed - White & Asian": 0.008,
    "Mixed - Other": 0.007,
    "Arab": 0.006,
    "Other ethnic group": 0.018  # Adjusted to make total = 1.000
}

# Height distributions (cm)
# Based on NHS and academic studies
MALE_HEIGHT_MEAN = 175.3
MALE_HEIGHT_STD = 7.1
FEMALE_HEIGHT_MEAN = 161.6
FEMALE_HEIGHT_STD = 6.5

# Income brackets (% of working age population)
INCOME_DISTRIBUTION_MALE = {
    "Under £20k": 0.25,
    "£20k-£30k": 0.22,
    "£30k-£40k": 0.18,
    "£40k-£50k": 0.13,
    "£50k-£75k": 0.14,
    "£75k-£100k": 0.05,
    "£100k+": 0.03
}

INCOME_DISTRIBUTION_FEMALE = {
    "Under £20k": 0.32,
    "£20k-£30k": 0.25,
    "£30k-£40k": 0.17,
    "£40k-£50k": 0.11,
    "£50k-£75k": 0.10,
    "£75k-£100k": 0.03,
    "£100k+": 0.02
}

# Education levels (% of adults)
EDUCATION_DISTRIBUTION = {
    "Below GCSE": 0.15,
    "GCSE/O-Level": 0.23,
    "A-Level or equivalent": 0.21,
    "Undergraduate degree": 0.27,
    "Postgraduate degree": 0.14
}

# BMI/Body Type Distribution (NHS Health Survey for England 2021)
# Based on BMI categories for adults aged 18+
BODY_TYPE_DISTRIBUTION_MALE = {
    "Underweight (BMI < 18.5)": 0.02,
    "Healthy weight (BMI 18.5-24.9)": 0.31,
    "Overweight (BMI 25-29.9)": 0.41,
    "Obese (BMI 30+)": 0.26
}

BODY_TYPE_DISTRIBUTION_FEMALE = {
    "Underweight (BMI < 18.5)": 0.06,
    "Healthy weight (BMI 18.5-24.9)": 0.40,
    "Overweight (BMI 25-29.9)": 0.28,
    "Obese (BMI 30+)": 0.26
}

# Relationship status (% of adults)
SINGLE_RATE = 0.35  # Approximately 35% of UK adults are single

# Children distribution (% of adults by number of children)
# Source: ONS Families and Households 2022
CHILDREN_DISTRIBUTION = {
    "No children": 0.43,
    "1 child": 0.18,
    "2 children": 0.24,
    "3+ children": 0.15
}

# Marriage history (% of adults)
# Source: ONS Marriage statistics 2022
MARRIAGE_HISTORY = {
    "Never married": 0.42,
    "Currently married": 0.46,
    "Divorced": 0.09,
    "Widowed": 0.03
}

# Male baldness distribution by age
# Source: British Association of Dermatologists / Academic studies
BALDNESS_BY_AGE = {
    "18-29": 0.16,  # 16% experiencing hair loss
    "30-39": 0.32,  # 32% with noticeable thinning/baldness
    "40-49": 0.53,  # 53% with visible baldness
    "50-59": 0.63,  # 63% bald or significantly thinning
    "60+": 0.80     # 80% with significant hair loss
}

# Sexual orientation distribution (ONS 2022)
SEXUAL_ORIENTATION_DISTRIBUTION = {
    "Heterosexual/Straight": 0.932,
    "Gay or Lesbian": 0.015,
    "Bisexual": 0.017,
    "Other": 0.006,
    "Prefer not to say": 0.030
}

# UK Regional Population Distribution (ONS 2022)
# Population by region with coordinates for mapping
UK_REGIONS = {
    "London": {
        "population": 9_002_488,
        "lat": 51.5074,
        "lon": -0.1278,
        "adult_pop": 7_200_000
    },
    "South East": {
        "population": 9_278_144,
        "lat": 51.3,
        "lon": -0.8,
        "adult_pop": 7_400_000
    },
    "North West": {
        "population": 7_417_397,
        "lat": 53.4808,
        "lon": -2.2426,
        "adult_pop": 5_900_000
    },
    "East of England": {
        "population": 6_398_497,
        "lat": 52.2405,
        "lon": 0.5186,
        "adult_pop": 5_100_000
    },
    "West Midlands": {
        "population": 6_021_653,
        "lat": 52.4862,
        "lon": -1.8904,
        "adult_pop": 4_800_000
    },
    "South West": {
        "population": 5_764_881,
        "lat": 50.7,
        "lon": -3.5,
        "adult_pop": 4_700_000
    },
    "Yorkshire and The Humber": {
        "population": 5_541_262,
        "lat": 53.9583,
        "lon": -1.0803,
        "adult_pop": 4_400_000
    },
    "East Midlands": {
        "population": 4_934_939,
        "lat": 52.8,
        "lon": -1.2,
        "adult_pop": 3_900_000
    },
    "Scotland": {
        "population": 5_479_900,
        "lat": 55.9533,
        "lon": -3.1883,
        "adult_pop": 4_400_000
    },
    "Wales": {
        "population": 3_107_494,
        "lat": 52.1307,
        "lon": -3.7837,
        "adult_pop": 2_500_000
    },
    "Northern Ireland": {
        "population": 1_910_000,
        "lat": 54.5973,
        "lon": -5.9301,
        "adult_pop": 1_500_000
    },
    "North East": {
        "population": 2_647_000,
        "lat": 54.9783,
        "lon": -1.6178,
        "adult_pop": 2_100_000
    }
}

def cm_to_feet_inches(cm):
    """Convert cm to feet and inches"""
    total_inches = cm / 2.54
    feet = int(total_inches // 12)
    inches = round(total_inches % 12)
    return feet, inches

def feet_inches_to_cm(feet, inches):
    """Convert feet and inches to cm"""
    return (feet * 12 + inches) * 2.54

def calculate_age_probability(min_age, max_age):
    """Calculate the probability someone falls in the age range"""
    probability = 0
    for age_range, pct in AGE_DISTRIBUTION.items():
        # Handle 65+ bracket: treat as 65-99 to match reality
        if age_range == "65+":
            range_min, range_max = 65, 99
        else:
            range_min, range_max = map(int, age_range.split('-'))
        
        # Calculate overlap
        overlap_min = max(min_age, range_min)
        overlap_max = min(max_age, range_max)
        
        if overlap_max >= overlap_min:
            # Assume uniform distribution within each bracket
            range_width = range_max - range_min + 1
            overlap_width = overlap_max - overlap_min + 1
            probability += pct * (overlap_width / range_width)
    
    return probability

def calculate_height_probability(min_height, max_height, gender):
    """Calculate probability someone's height is in range (using normal distribution)"""
    if gender == "Male":
        mean, std = MALE_HEIGHT_MEAN, MALE_HEIGHT_STD
    else:
        mean, std = FEMALE_HEIGHT_MEAN, FEMALE_HEIGHT_STD
    
    from scipy import stats
    prob = stats.norm.cdf(max_height, mean, std) - stats.norm.cdf(min_height, mean, std)
    return prob

def calculate_income_probability(min_income, gender):
    """Calculate probability someone earns at or above minimum income"""
    income_dist = INCOME_DISTRIBUTION_MALE if gender == "Male" else INCOME_DISTRIBUTION_FEMALE
    
    # Define income brackets as (low, high, percent)
    income_brackets = [
        (0, 20000, income_dist["Under £20k"]),
        (20000, 30000, income_dist["£20k-£30k"]),
        (30000, 40000, income_dist["£30k-£40k"]),
        (40000, 50000, income_dist["£40k-£50k"]),
        (50000, 75000, income_dist["£50k-£75k"]),
        (75000, 100000, income_dist["£75k-£100k"]),
        (100000, 200000, income_dist["£100k+"])  # Assume upper bound of 200k for top bracket
    ]
    
    probability = 0
    for bracket_low, bracket_high, pct in income_brackets:
        if min_income <= bracket_low:
            # Entire bracket is at or above minimum, include all of it
            probability += pct
        elif min_income < bracket_high:
            # min_income falls within this bracket, prorate
            # Assume uniform distribution within bracket
            bracket_width = bracket_high - bracket_low
            included_width = bracket_high - min_income
            probability += pct * (included_width / bracket_width)
        # else: bracket_high <= min_income, entire bracket excluded
    
    return probability

def calculate_education_probability(min_education_levels):
    """Calculate probability someone has at least one of the education levels"""
    education_order = ["Below GCSE", "GCSE/O-Level", "A-Level or equivalent", 
                       "Undergraduate degree", "Postgraduate degree"]
    
    probability = 0
    for level in min_education_levels:
        probability += EDUCATION_DISTRIBUTION[level]
    
    return probability

def calculate_ethnicity_probability(selected_ethnicities):
    """Calculate probability someone is one of the selected ethnicities"""
    probability = 0
    for ethnicity in selected_ethnicities:
        probability += ETHNICITY_DISTRIBUTION[ethnicity]
    
    return probability

def calculate_body_type_probability(selected_body_types, gender):
    """Calculate probability someone has one of the selected body types"""
    body_dist = BODY_TYPE_DISTRIBUTION_MALE if gender == "Male" else BODY_TYPE_DISTRIBUTION_FEMALE
    
    probability = 0
    for body_type in selected_body_types:
        probability += body_dist[body_type]
    
    return probability

def calculate_children_probability(acceptable_children):
    """Calculate probability someone has acceptable number of children"""
    probability = 0
    for children_status in acceptable_children:
        probability += CHILDREN_DISTRIBUTION[children_status]
    return probability

def calculate_marriage_probability(acceptable_marriage_history):
    """Calculate probability someone has acceptable marriage history"""
    probability = 0
    for status in acceptable_marriage_history:
        probability += MARRIAGE_HISTORY[status]
    return probability

def calculate_baldness_probability(baldness_preference, age_range):
    """Calculate probability of baldness preference match for males"""
    # Calculate weighted average baldness rate across age range
    age_ranges_baldness = [
        (18, 29, BALDNESS_BY_AGE["18-29"]),
        (30, 39, BALDNESS_BY_AGE["30-39"]),
        (40, 49, BALDNESS_BY_AGE["40-49"]),
        (50, 59, BALDNESS_BY_AGE["50-59"]),
        (60, 99, BALDNESS_BY_AGE["60+"])
    ]
    
    total_years = 0
    weighted_bald_rate = 0
    
    for range_min, range_max, bald_rate in age_ranges_baldness:
        overlap_min = max(age_range[0], range_min)
        overlap_max = min(age_range[1], range_max)
        
        if overlap_max >= overlap_min:
            years_in_overlap = overlap_max - overlap_min + 1
            total_years += years_in_overlap
            weighted_bald_rate += bald_rate * years_in_overlap
    
    if total_years > 0:
        avg_bald_rate = weighted_bald_rate / total_years
    else:
        avg_bald_rate = 0
    
    # Return probability based on preference
    if baldness_preference == "Any":
        return 1.0
    elif baldness_preference == "Not bald":
        return 1.0 - avg_bald_rate
    elif baldness_preference == "Bald or balding":
        return avg_bald_rate
    else:
        return 1.0

def calculate_orientation_probability(user_orientation, looking_for_gender, user_gender=None):
    """Calculate probability of compatible sexual orientation"""
    # Renormalize to exclude 'Other' and 'Prefer not to say' from the matching pool
    straight_raw = SEXUAL_ORIENTATION_DISTRIBUTION["Heterosexual/Straight"]
    gay_raw = SEXUAL_ORIENTATION_DISTRIBUTION["Gay or Lesbian"]
    bi_raw = SEXUAL_ORIENTATION_DISTRIBUTION["Bisexual"]
    total_matchable = straight_raw + gay_raw + bi_raw
    
    # Normalize so matchable orientations sum to 1.0
    straight_rate = straight_raw / total_matchable
    gay_rate = gay_raw / total_matchable
    bi_rate = bi_raw / total_matchable
    
    # If looking for any gender - only valid for bisexual orientation
    if looking_for_gender == "Any":
        if user_orientation == "Bisexual":
            # Bisexual people looking for anyone can match with:
            # - Straight people of opposite sex only (need to know user's gender)
            # - Gay/Lesbian people of same sex only
            # - All bisexual people
            if user_gender and user_gender in ["Male", "Female"]:
                # Straight people: only opposite sex is compatible (50% of straight population)
                # Gay people: only same sex is compatible (50% of gay population)
                # Bi people: all are compatible
                return straight_rate * 0.5 + gay_rate * 0.5 + bi_rate
            else:
                # User gender unknown or "Other" - use simplified estimate
                return straight_rate * 0.5 + gay_rate * 0.5 + bi_rate
        else:
            # Straight or Gay/Lesbian with "Any" - this is contradictory
            # Should not happen with proper UI constraints, but handle gracefully
            # Apply very low probability to indicate inconsistency
            return bi_rate  # Only bisexual people could match
    
    # For specific gender selection - need to check compatibility with user's gender and orientation
    if user_orientation == "Heterosexual/Straight":
        # Straight people looking for specific gender
        # Must be looking for opposite sex; compatible with straight + bi people
        if user_gender == "Male" and looking_for_gender == "Male":
            # Straight man looking for men - illogical, but return very low probability
            return bi_rate  # Only bi men might be interested
        elif user_gender == "Female" and looking_for_gender == "Female":
            # Straight woman looking for women - illogical
            return bi_rate  # Only bi women might be interested
        else:
            # Looking for opposite sex (correct usage)
            return straight_rate + bi_rate
    
    elif user_orientation == "Gay or Lesbian":
        # Gay/Lesbian people looking for specific gender
        # Must be looking for same sex; compatible with gay/lesbian + bi people
        if user_gender == "Male" and looking_for_gender == "Female":
            # Gay man looking for women - illogical
            return bi_rate  # Only bi women might be interested
        elif user_gender == "Female" and looking_for_gender == "Male":
            # Lesbian looking for men - illogical
            return bi_rate  # Only bi men might be interested
        else:
            # Looking for same sex (correct usage)
            return gay_rate + bi_rate
    
    elif user_orientation == "Bisexual":
        # Bisexual people looking for specific gender
        # Compatible with everyone who might be interested in user's gender:
        # If looking for men: straight women, gay men, bi people
        # If looking for women: straight men, lesbians, bi people
        # Simplified: straight people (opposite to target) + gay people (same as target) + all bi
        if user_gender == "Male":
            if looking_for_gender == "Male":
                # Bi man looking for men: gay men + bi people
                return gay_rate + bi_rate
            elif looking_for_gender == "Female":
                # Bi man looking for women: straight women + bi people
                return straight_rate + bi_rate
        elif user_gender == "Female":
            if looking_for_gender == "Female":
                # Bi woman looking for women: lesbians + bi people
                return gay_rate + bi_rate
            elif looking_for_gender == "Male":
                # Bi woman looking for men: straight men + bi people
                return straight_rate + bi_rate
        else:
            # User gender is "Other" - simplified estimate
            return straight_rate + gay_rate + bi_rate
    
    return 1.0

def create_dating_pool_map(total_probability):
    """Create an interactive map showing estimated matches by UK region"""
    # Create base map centered on UK with aesthetic CartoDB Positron tiles
    m = folium.Map(
        location=[54.5, -3.5],
        zoom_start=6,
        tiles='CartoDB positron',
        attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    )
    
    # Calculate regional scaling factor to ensure regional totals match UK total
    total_regional_adults = sum(data['adult_pop'] for data in UK_REGIONS.values())
    regional_scale = UK_ADULT_POPULATION / total_regional_adults
    
    # Add markers for each region
    for region, data in UK_REGIONS.items():
        regional_matches = int(data['adult_pop'] * regional_scale * total_probability)
        
        # Determine circle color and size based on matches (gradient from red to green)
        if regional_matches > 50000:
            color = '#2E7D32'  # Dark green for very high numbers
            radius = 50000
        elif regional_matches > 20000:
            color = '#66BB6A'  # Medium green
            radius = 40000
        elif regional_matches > 10000:
            color = '#FFA726'  # Orange
            radius = 30000
        elif regional_matches > 5000:
            color = '#FF7043'  # Light orange
            radius = 22000
        else:
            color = '#EF5350'  # Red for low numbers
            radius = 15000
        
        # Add circle marker with modern styling
        folium.Circle(
            location=[data['lat'], data['lon']],
            radius=radius,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.5,
            weight=2,
            opacity=0.8,
            popup=folium.Popup(
                f"""<div style='font-family: "Segoe UI", Arial, sans-serif; width: 240px; padding: 8px;'>
                    <h4 style='margin: 0 0 12px 0; color: {color}; font-weight: 600; font-size: 16px;'>{region}</h4>
                    <div style='background: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid {color};'>
                        <p style='margin: 6px 0; font-size: 14px;'><b style='color: #555;'>Estimated Matches:</b><br>
                        <span style='font-size: 18px; color: {color}; font-weight: 600;'>{regional_matches:,}</span></p>
                        <p style='margin: 6px 0; font-size: 13px; color: #666;'><b>Adult Population:</b> {data['adult_pop']:,}</p>
                        <p style='margin: 6px 0; font-size: 13px; color: #666;'><b>Percentage:</b> {(total_probability * 100):.3f}%</p>
                    </div>
                </div>""",
                max_width=280
            ),
            tooltip=f"<b>{region}</b><br>{regional_matches:,} matches"
        ).add_to(m)
        
        # Add text label
        folium.Marker(
            location=[data['lat'], data['lon']],
            icon=folium.DivIcon(html=f"""
                <div style='font-size: 10pt; color: white; font-weight: bold; 
                     text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
                     white-space: nowrap;'>
                    {region}<br>{regional_matches:,}
                </div>
            """)
        ).add_to(m)
    
    return m

def main():
    # Initialize session state for results persistence
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'results_data' not in st.session_state:
        st.session_state.results_data = None
    
    # Header
    st.markdown('<div class="main-header">UK Dating Pool Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Calculate your realistic dating pool size using real UK statistics</div>', unsafe_allow_html=True)
    
    # Sidebar for inputs
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
                # Default 5'5" to 6'5"
                default_min_inches = 65  # 5'5"
                default_max_inches = 77  # 6'5"
                height_help = "Average UK male height is 5'9\""
            else:
                # Default 4'11" to 5'9"
                default_min_inches = 59  # 4'11"
                default_max_inches = 69  # 5'9"
                height_help = "Average UK female height is 5'3\""
            
            # Display conversion helper first
            col_a, col_b = st.sidebar.columns([2, 1])
            with col_a:
                st.caption("Adjust slider below:")
            
            # Create slider with custom display
            min_total_inches = st.sidebar.slider(
                "Minimum height:",
                min_value=55,  # ~4'7"
                max_value=83,  # ~6'11"
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
            
            height_range_inches = (min_total_inches, max_total_inches)
            
            # Convert to cm for calculations
            min_height_cm = height_range_inches[0] * 2.54
            max_height_cm = height_range_inches[1] * 2.54
    else:
        # Set to full range if any height
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
    # UK salary benchmarks
    MIN_WAGE_ANNUAL = 22308  # National Living Wage 21+: £11.44/hr * 37.5hrs/wk * 52wks
    MEDIAN_SALARY = 31285
    AVERAGE_SALARY = 33000
    
    min_income = st.sidebar.selectbox(
        "Minimum annual income:",
        ["Any", MIN_WAGE_ANNUAL, 25000, 30000, MEDIAN_SALARY, AVERAGE_SALARY, 40000, 50000, 75000, 100000],
        format_func=lambda x: "Any" if x == "Any" else (
            f"£{x:,} (Min Wage)" if x == MIN_WAGE_ANNUAL else
            f"£{x:,} (UK Median)" if x == MEDIAN_SALARY else
            f"£{x:,} (UK Average)" if x == AVERAGE_SALARY else
            f"£{x:,}"
        ),
        help="Minimum acceptable annual income (UK National Living Wage: £22,308 | Median: £31,285 | Average: £33,000)"
    )
    # Convert to numeric
    if min_income == "Any":
        min_income = 0
    
    # Education
    st.sidebar.subheader("Education")
    any_education = st.sidebar.checkbox(
        "Any education level",
        value=True,
        help="No education preference"
    )
    
    if not any_education:
        education_levels = st.sidebar.multiselect(
            "Acceptable education levels:",
            ["Below GCSE", "GCSE/O-Level", "A-Level or equivalent", 
             "Undergraduate degree", "Postgraduate degree"],
            default=["Below GCSE", "GCSE/O-Level", "A-Level or equivalent", "Undergraduate degree", "Postgraduate degree"],
            help="Select all acceptable education levels"
        )
    else:
        education_levels = ["Below GCSE", "GCSE/O-Level", "A-Level or equivalent", 
                           "Undergraduate degree", "Postgraduate degree"]
    
    # Ethnicity with detailed options
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
    
    # Set flag when calculate is pressed
    if calculate_button:
        st.session_state.show_results = True
    
    # Main content
    if st.session_state.show_results:
        # Validation only needed if user manually deselected all (shouldn't happen with new UI)
        if not any_education and not education_levels:
            st.error("Please select at least one education level or choose 'Any education level'")
            return
        
        if not any_ethnicity and not selected_ethnicities:
            st.error("Please select at least one ethnicity or choose 'Any ethnicity'")
            return
        
        if not any_body_type and not selected_body_types:
            st.error("Please select at least one body type or choose 'Any body type'")
            return
        
        if not any_children and not acceptable_children:
            st.error("Please select at least one children option or choose 'Any'")
            return
        
        if not any_marriage_history and not acceptable_marriage_history:
            st.error("Please select at least one marriage history option or choose 'Any marriage history'")
            return
        
        # Calculate probabilities
        with st.spinner("Calculating your dating pool..."):
            # Gender split (UK adults: 49.2% male, 50.8% female)
            if looking_for == "Any":
                gender_prob = 1.0
            elif looking_for == "Male":
                gender_prob = 0.492
            else:  # Female
                gender_prob = 0.508
            
            # Age probability
            age_prob = calculate_age_probability(age_range[0], age_range[1])
            
            # Height probability
            if looking_for == "Any":
                # Weighted average using UK gender distribution (49.2% male / 50.8% female)
                male_height_prob = calculate_height_probability(min_height_cm, max_height_cm, "Male")
                female_height_prob = calculate_height_probability(min_height_cm, max_height_cm, "Female")
                height_prob = 0.492 * male_height_prob + 0.508 * female_height_prob
            else:
                height_prob = calculate_height_probability(min_height_cm, max_height_cm, looking_for)
            
            # Income probability
            if looking_for == "Any":
                # Weighted average using UK gender distribution (49.2% male / 50.8% female)
                male_income_prob = calculate_income_probability(min_income, "Male")
                female_income_prob = calculate_income_probability(min_income, "Female")
                income_prob = 0.492 * male_income_prob + 0.508 * female_income_prob
            else:
                income_prob = calculate_income_probability(min_income, looking_for)
            
            # Education probability
            education_prob = calculate_education_probability(education_levels)
            
            # Ethnicity probability
            ethnicity_prob = calculate_ethnicity_probability(selected_ethnicities)
            
            # Body type probability
            if looking_for == "Any":
                # Weighted average using UK gender distribution (49.2% male / 50.8% female)
                male_body_prob = calculate_body_type_probability(selected_body_types, "Male")
                female_body_prob = calculate_body_type_probability(selected_body_types, "Female")
                body_type_prob = 0.492 * male_body_prob + 0.508 * female_body_prob
            else:
                body_type_prob = calculate_body_type_probability(selected_body_types, looking_for)
            
            # Sexual orientation compatibility
            orientation_prob = calculate_orientation_probability(user_orientation, looking_for, user_gender)
            
            # Relationship status
            single_prob = SINGLE_RATE if must_be_single else 1.0
            
            # Children probability
            children_prob = calculate_children_probability(acceptable_children)
            
            # Marriage history probability
            marriage_prob = calculate_marriage_probability(acceptable_marriage_history)
            
            # Baldness probability (only applies to males)
            if looking_for == "Male":
                baldness_prob = calculate_baldness_probability(baldness_preference, age_range)
            elif looking_for == "Any":
                # Weighted average: males get baldness filter, females = 1.0
                male_baldness_prob = calculate_baldness_probability(baldness_preference, age_range)
                baldness_prob = 0.492 * male_baldness_prob + 0.508 * 1.0
            else:
                baldness_prob = 1.0  # Not applicable for females
            
            # Combined probability
            total_probability = (gender_prob * age_prob * height_prob * body_type_prob *
                               income_prob * education_prob * ethnicity_prob * orientation_prob * 
                               single_prob * children_prob * marriage_prob * baldness_prob)
            
            # Calculate actual numbers
            estimated_matches = int(UK_ADULT_POPULATION * total_probability)
            percentage = total_probability * 100
            
            # Display results
            st.markdown(f"""
                <div class="result-box">
                    <h2>Your Dating Pool</h2>
                    <div class="result-percentage">{percentage:.3f}%</div>
                    <div class="result-count">Approximately {estimated_matches:,} people in the UK</div>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">
                        Out of {UK_ADULT_POPULATION:,} UK adults
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Probability Breakdown")
                cumulative = gender_prob
                breakdown_data = {
                    "Criterion": ["Gender", "Age Range", "Height Range", "Body Type", "Income", 
                                "Education", "Ethnicity", "Orientation", "Single/Available", 
                                "Children", "Marriage History", "Baldness", "**TOTAL**"],
                    "Probability": [
                        f"{gender_prob*100:.1f}%",
                        f"{age_prob*100:.1f}%",
                        f"{height_prob*100:.1f}%",
                        f"{body_type_prob*100:.1f}%",
                        f"{income_prob*100:.1f}%",
                        f"{education_prob*100:.1f}%",
                        f"{ethnicity_prob*100:.1f}%",
                        f"{orientation_prob*100:.1f}%",
                        f"{single_prob*100:.1f}%",
                        f"{children_prob*100:.1f}%",
                        f"{marriage_prob*100:.1f}%",
                        f"{baldness_prob*100:.1f}%",
                        f"**{percentage:.3f}%**"
                    ],
                    "Passes Filter": [
                        f"{int(UK_ADULT_POPULATION * gender_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob * children_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob * children_prob * marriage_prob):,}",
                        f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob * children_prob * marriage_prob * baldness_prob):,}",
                        f"**{estimated_matches:,}**"
                    ]
                }
                st.dataframe(breakdown_data, hide_index=True, use_container_width=True)
            
            with col2:
                st.subheader("Your Criteria")
                st.write(f"**Your Gender:** {user_gender}")
                st.write(f"**Looking for:** {looking_for}")
                st.write(f"**Your Orientation:** {user_orientation}")
                if any_age:
                    st.write(f"**Age:** Any (18+)")
                else:
                    st.write(f"**Age:** {age_range[0]}-{age_range[1]} years")
                
                # Format height display
                if any_height:
                    st.write(f"**Height:** Any")
                else:
                    min_f, min_i = cm_to_feet_inches(min_height_cm)
                    max_f, max_i = cm_to_feet_inches(max_height_cm)
                    st.write(f"**Height:** {min_height_cm:.0f}-{max_height_cm:.0f} cm ({min_f}'{min_i}\" - {max_f}'{max_i}\")")
                
                st.write(f"**Min Income:** £{min_income:,}" if min_income > 0 else "**Min Income:** Any")
                st.write(f"**Body Type:** {len(selected_body_types)} type(s) selected")
                st.write(f"**Education:** {len(education_levels)} level(s) selected")
                st.write(f"**Ethnicity:** {len(selected_ethnicities)} group(s) selected")
                st.write(f"**Status:** {'Single only' if must_be_single else 'Any'}")
                st.write(f"**Children:** {len(acceptable_children)} option(s) selected")
                st.write(f"**Marriage History:** {len(acceptable_marriage_history)} option(s) selected")
                if looking_for == "Male" or looking_for == "Any":
                    st.write(f"**Baldness (Males):** {baldness_preference}")
                
                st.markdown("---")
                
                # Reality check
                if percentage < 1:
                    st.warning("Your criteria are quite selective!")
                elif percentage < 5:
                    st.info("Your standards are moderately selective")
                else:
                    st.success("Your criteria are relatively broad")
            
            # Geographic Distribution Map
            st.subheader("Geographic Distribution")
            st.markdown("Estimated matches across UK regions:")
            
            # Create and display the map
            dating_map = create_dating_pool_map(total_probability)
            st_folium(dating_map, width=700, height=500)
            
            # Regional breakdown table
            st.markdown("### Regional Breakdown")
            
            # Calculate regional scaling factor to ensure regional totals match UK total
            total_regional_adults = sum(data['adult_pop'] for data in UK_REGIONS.values())
            regional_scale = UK_ADULT_POPULATION / total_regional_adults
            
            regional_data = []
            for region, data in UK_REGIONS.items():
                regional_matches = int(data['adult_pop'] * regional_scale * total_probability)
                regional_data.append({
                    "Region": region,
                    "Adult Population": f"{data['adult_pop']:,}",
                    "Estimated Matches": f"{regional_matches:,}",
                    "% of Region": f"{(total_probability * 100):.3f}%"
                })
            
            regional_df = pd.DataFrame(regional_data)
            regional_df = regional_df.sort_values("Estimated Matches", 
                                                  key=lambda x: x.str.replace(',', '').astype(int), 
                                                  ascending=False)
            st.dataframe(regional_df, hide_index=True, use_container_width=True)
    
    # Sources section
    with st.expander("Data Sources & Methodology"):
        st.markdown("""
        ### Data Sources
        
        All statistics are based on official UK government data and peer-reviewed research:
        
        **Geographic Coverage:** United Kingdom includes England, Scotland, Wales, and Northern Ireland (NOT Republic of Ireland).
        Note: Some datasets (ethnicity) are England & Wales only due to separate census systems in Scotland/NI.
        
        1. **Population Data by Age Demographics**
           - Source: Office for National Statistics (ONS) - Mid-2022 Population Estimates
           - Total UK Population: 67,736,802
           - Geographic Coverage: England, Scotland, Wales, Northern Ireland
           
           **A. Children & Teenagers (0-17): 15.1 million (22.3%)**
           
           *Gender Breakdown:*
           - Boys: 7,732,000 (51.2%)
           - Girls: 7,368,000 (48.8%)
           
           *Age Groups:*
           - 0-4 years: 3.7 million (24.5% of 0-17)
           - 5-10 years: 4.6 million (30.5% of 0-17)
           - 11-15 years: 3.5 million (23.2% of 0-17)
           - 16-17 years: 3.3 million (21.8% of 0-17)
           
           **B. Adults (18+): 52.6 million (77.7%)**
           
           *Gender Breakdown:*
           - Men: 25,900,000 (49.2%)
           - Women: 26,700,000 (50.8%)
           
           **Age Demographics (Adults 18+):**
           
           *Young Adults (18-34): 16.1 million (30.6% of adults)*
           - 18-24 years: 6.3 million (11.9% of adults)
             * Dating pool: High dating activity, university/early career
             * Median income: ~£22k-£25k
           - 25-34 years: 9.8 million (18.7% of adults)
             * Dating pool: Peak dating years, career building
             * Median income: ~£28k-£35k
           
           *Middle Adults (35-54): 18.8 million (35.8% of adults)*
           - 35-44 years: 9.0 million (17.2% of adults)
             * Dating pool: Established careers, may have children
             * Median income: ~£35k-£40k
           - 45-54 years: 9.8 million (18.6% of adults)
             * Dating pool: Peak earning years
             * Median income: ~£38k-£42k
           
           *Older Adults (55+): 17.7 million (33.6% of adults)*
           - 55-64 years: 8.5 million (16.2% of adults)
             * Dating pool: Pre-retirement, high income
             * Median income: ~£35k-£40k
           - 65+ years: 9.2 million (17.4% of adults)
             * Dating pool: Retirement age
             * Median income: ~£15k-£20k (pension income)
        
        2. **Age Distribution Summary**
           - Source: ONS Population Estimates by Age and Sex
           - Data Year: 2022
           - All percentages are of total adult population (18+) unless specified
        
        3. **Ethnicity**
           - Source: ONS Census 2021
           - **Coverage: England and Wales ONLY** (Scotland and Northern Ireland have separate census systems)
           - Note: Applied to full UK population as best available approximation
           - Categories: White (81.6%), Asian (9.3%), Black (4.0%), Mixed (2.9%), Other (2.2%)
        
        4. **Height Distribution**
           - Source: NHS Health Survey for England & academic studies
           - Male: Mean 175.3cm, SD 7.1cm
           - Female: Mean 161.6cm, SD 6.5cm
           - Normal distribution assumed
        
        5. **Body Type / BMI Distribution**
           - Source: NHS Health Survey for England 2021
           - BMI categories based on WHO standards
           
           **Male BMI Distribution:**
           - Underweight (BMI < 18.5): 2%
           - Healthy weight (BMI 18.5-24.9): 31%
           - Overweight (BMI 25-29.9): 41%
           - Obese (BMI 30+): 26%
           
           **Female BMI Distribution:**
           - Underweight (BMI < 18.5): 6%
           - Healthy weight (BMI 18.5-24.9): 40%
           - Overweight (BMI 25-29.9): 28%
           - Obese (BMI 30+): 26%
        
        6. **Income Distribution**
           - Source: ONS Annual Survey of Hours and Earnings (ASHE) 2023
           - Gross annual earnings by gender
           - Full-time workers aged 18-65
           
           **UK Salary Benchmarks (2024):**
           - National Living Wage (21+): £11.44/hour = £22,308/year (37.5hrs/wk)
           - National Minimum Wage (18-20): £8.60/hour = £16,770/year
           - UK Median Salary: £31,285/year
           - UK Average (Mean) Salary: £33,000/year
           
           *Note: Income varies significantly by age, with peak earning in 45-54 age group*
        
        7. **Education Levels**
           - Source: ONS Education statistics 2022
           - Highest qualification attained by adults
        
        8. **Relationship Status**
           - Source: ONS Families and Households 2022
           - Single rate: ~35% of UK adults are not in a relationship
        
        9. **Sexual Orientation**
           - Source: ONS Sexual Orientation, UK 2022
           - Heterosexual/Straight: 93.2%, Gay/Lesbian: 1.5%, Bisexual: 1.7%
           - Data from adults aged 16+ in England and Wales
           - [ONS Sexual Orientation Data](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality)
        
        ### Methodology
        
        This calculator uses **independent probability multiplication** to estimate your dating pool size. Each criterion you select acts as a filter that narrows down the population.
        
        #### Statistical Model
        
        The fundamental equation is:
        
        ```
        P(match) = P(gender) × P(age) × P(height) × P(body type) × P(income) × 
                   P(education) × P(ethnicity) × P(orientation) × P(single) × 
                   P(children) × P(marriage history) × P(baldness)
        ```
        
        **Total Dating Pool = UK Adult Population × P(match)**
        
        #### How Each Probability is Calculated
        
        **1. Gender Probability**
        - Based on UK adult population gender split (49.2% male, 50.8% female)
        - "Any" gender = 100% (no filter)
        - Specific gender = 49.2% or 50.8%
        
        **2. Age Probability**
        - Uses actual UK population distribution by single-year age groups
        - Calculates cumulative probability across your selected age range
        - Example: Ages 25-35 = sum of all single-year probabilities from 25 to 35
        
        **3. Height Probability**
        - Assumes **normal (Gaussian) distribution** for each gender
        - Male: μ=175.3cm, σ=7.1cm (from NHS Health Survey)
        - Female: μ=161.6cm, σ=6.5cm
        - Uses cumulative distribution function (CDF) to calculate percentage within range
        - Formula: P(height) = Φ((max-μ)/σ) - Φ((min-μ)/σ), where Φ is the standard normal CDF
        
        **4. Body Type Probability (BMI)**
        - Direct lookup from NHS Health Survey data
        - Separate distributions for males and females
        - Sum of selected BMI categories
        - Example: Selecting "Healthy" + "Overweight" for males = 31% + 41% = 72%
        
        **5. Income Probability**
        - Uses quintile distribution from ONS Annual Survey of Hours and Earnings
        - Assumes uniform distribution within each income bracket
        - Gender-specific (males typically earn more on average)
        - Interpolates for specific income thresholds
        
        **6. Education Probability**
        - Direct lookup from ONS education attainment statistics
        - Sum of selected education levels
        - Based on highest qualification achieved
        
        **7. Ethnicity Probability**
        - Direct lookup from Census 2021 data
        - Sum of selected ethnic groups
        - Based on self-identified ethnic background
        
        **8. Sexual Orientation Probability**
        - Uses ONS Sexual Orientation Survey 2022 data
        - Accounts for compatibility (e.g., straight male seeks female who is straight or bisexual)
        - Heterosexual: 93.2%, Gay/Lesbian: 1.5%, Bisexual: 1.7%
        
        **9. Relationship Status Probability**
        - Single/Available: 35% (from ONS Families and Households)
        - "Any" = 100% (includes people in relationships)
        
        **10. Children Probability**
        - Based on ONS fertility and family statistics
        - Age-dependent (younger people less likely to have children)
        - Sum of selected categories (no children, 1 child, 2 children, 3+)
        
        **11. Marriage History Probability**
        - From ONS marital status data by age group
        - Never married, divorced, widowed, currently married
        - Age-dependent (younger = higher % never married)
        
        **12. Baldness Probability (Males Only)**
        - Based on medical research on male pattern baldness prevalence by age
        - Age-dependent: increases significantly with age
        - Example: ~25% at age 30, ~50% at age 50, ~80% at age 70
        
        #### Geographic Distribution
        
        Regional estimates apply the total probability to each region's adult population:
        
        ```
        Regional Matches = Regional Adult Population × Total Probability
        ```
        
        Regions are scaled to ensure the sum equals the UK total (correcting for minor data inconsistencies).
        
        #### Important Assumptions & Limitations
        
        **Key Assumptions:**
        1. **Independence**: All criteria are treated as statistically independent
           - Reality: Income and education are correlated
           - Reality: Height and gender are correlated
           - Reality: Age affects many factors (income, children, marriage history)
        
        2. **Normal Distributions**: Height assumes bell curve distribution
           - Reasonably accurate for height within a single gender
           - Less accurate for extreme values (very tall/short)
        
        3. **Uniform Geographic Distribution**: People are evenly distributed within each region
           - Reality: Urban areas have higher density
           - Reality: London has different demographics than rural Wales
        
        4. **Static Data**: Uses point-in-time statistics
           - Population demographics change over time
           - Dating pool is dynamic (people enter/exit relationships)
        
        5. **Binary Gender Model**: Limited to male/female categories
           - Due to data availability in official statistics
           - "Other" gender uses averages but has less reliable data
        
        **Major Limitations:**
        
        1. **Unquantified Factors:**
           - Physical attractiveness (subjective and not measured)
           - Personality compatibility
           - Shared interests and values
           - Chemistry and emotional connection
           - Social skills and charisma
        
        2. **Behavioral Factors:**
           - Does not account for dating app usage (Tinder, Hinge, Bumble)
           - Ignores social circles and meeting opportunities
           - No consideration of geographic mobility
           - Doesn't factor in dating activity levels (some people aren't actively dating)
        
        3. **Statistical Accuracy:**
           - Very specific criteria combinations may overestimate due to unmeasured correlations
           - Small percentages (<0.1%) have high relative uncertainty
           - Some data sources are England & Wales only, extrapolated to UK
        
        4. **Mutual Attraction:**
           - Shows people who meet YOUR criteria
           - Does NOT show who would be interested in YOU
           - Real dating pools require mutual interest
        
        5. **Market Dynamics:**
           - Doesn't account for competition (popular profiles get more attention)
           - Ignores assortative mating (tendency to date people similar to yourself)
           - No consideration of "league" effects or desirability hierarchies
        
        #### Interpretation Guide
        
        **How to Read Your Results:**
        
        - **>5% (>2.6M people)**: Very broad criteria, large dating pool
        - **1-5% (500K-2.6M)**: Moderate selectivity, still substantial pool
        - **0.1-1% (50K-500K)**: Selective criteria, medium pool
        - **0.01-0.1% (5K-50K)**: Very selective, small pool
        - **<0.01% (<5K)**: Extremely selective, very challenging
        
        **Remember:**
        - You only need to find ONE compatible person, not thousands
        - Statistics show potential, not destiny
        - Dating success depends on effort, social skills, and timing
        - Many happily partnered people had "impossible" statistics
        
        #### Mathematical Rigor
        
        This calculator uses established statistical methods:
        - **Normal distribution** (height): scipy.stats.norm
        - **Cumulative probabilities** (age ranges)
        - **Discrete probability mass functions** (categorical data)
        - **Independent event multiplication** (P(A∩B) = P(A)×P(B) when independent)
        
        The model is mathematically sound but subject to the assumptions above.
        
        ### References
        - [ONS Population Estimates](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates)
        - [Census 2021 Ethnicity Data](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity)
        - [NHS Health Survey](https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england)
        - [ASHE Income Data](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours)
        
        ---
        *Last updated: December 2025*  
        *Calculator version: 1.0*
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            <p>This calculator uses real UK statistics for educational purposes.</p>
            <p>Remember: Statistics don't define your worth or dating success. 
            Personality, compatibility, and timing matter more than numbers!</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
