import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="UK Dating Pool Calculator",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark Mode Optimized
st.markdown("""
    <style>
    /* Main header - bright gradient for visibility in dark mode */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #8b9eff 0%, #9d7bc4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    /* Sub-header - lighter color for dark mode */
    .sub-header {
        text-align: center;
        color: #b0b0b0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Result box - vibrant gradient that works in dark mode */
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(139, 158, 255, 0.3);
    }
    
    .result-percentage {
        font-size: 5rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
    }
    
    .result-count {
        font-size: 1.8rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Info cards - theme aware with semi-transparent background */
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        border-left: 4px solid #8b9eff;
        border: 1px solid rgba(139, 158, 255, 0.2);
    }
    
    .info-card h3 {
        color: #8b9eff;
        margin-top: 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    /* Metric highlights - brighter for dark mode */
    .metric-highlight {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
        box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling for dark mode */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.2);
    }
    
    /* Make sidebar widgets more visible */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] .stNumberInput label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    /* Improve dataframe styling for dark mode */
    .dataframe {
        font-size: 0.95rem;
    }
    
    /* Make dataframes more readable in dark mode */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid rgba(139, 158, 255, 0.2);
    }
    
    /* Improve tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        border: 1px solid rgba(139, 158, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: 1px solid rgba(139, 158, 255, 0.5);
    }
    
    /* Improve expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border: 1px solid rgba(139, 158, 255, 0.2);
        font-weight: 500;
    }
    
    /* Better text contrast */
    p, li, span, div {
        color: inherit;
    }
    
    /* Markdown headers */
    h1, h2, h3, h4 {
        color: #e0e0e0;
    }
    
    /* Caption text should be lighter but readable */
    .caption {
        color: #b0b0b0 !important;
    }
    
    /* Links should be visible */
    a {
        color: #8b9eff !important;
    }
    
    a:hover {
        color: #a8b8ff !important;
    }
    
    /* Make metric values stand out */
    [data-testid="stMetricValue"] {
        color: #8b9eff;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to normalize distributions
def _normalize(dist):
    """Normalize a distribution dictionary to sum to exactly 1.0"""
    s = sum(dist.values())
    return {k: v/s for k, v in dist.items()}

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
ETHNICITY_DISTRIBUTION = _normalize({
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
    "Other ethnic group": 0.018
})

# Height distributions (cm)
# Based on NHS and academic studies
MALE_HEIGHT_MEAN = 175.3
MALE_HEIGHT_STD = 7.1
FEMALE_HEIGHT_MEAN = 161.6
FEMALE_HEIGHT_STD = 6.5

# Income brackets (% of working age population)
# Income brackets (% of working age population)
# Source: ONS ASHE 2023 + HMRC Self Assessment data for high earners
INCOME_DISTRIBUTION_MALE = {
    "Under £20k": 0.25,
    "£20k-£30k": 0.22,
    "£30k-£40k": 0.18,
    "£40k-£50k": 0.13,
    "£50k-£75k": 0.14,
    "£75k-£100k": 0.05,
    "£100k-£150k": 0.02,  # HMRC Self Assessment data
    "£150k-£250k": 0.007, # HMRC: ~400k taxpayers
    "£250k-£500k": 0.003, # HMRC: ~180k taxpayers
    "£500k-£1M": 0.0006,  # HMRC: ~35k taxpayers
    "£1M+": 0.0004        # HMRC: ~23k taxpayers (millionaires+)
}

INCOME_DISTRIBUTION_FEMALE = {
    "Under £20k": 0.32,
    "£20k-£30k": 0.25,
    "£30k-£40k": 0.17,
    "£40k-£50k": 0.11,
    "£50k-£75k": 0.10,
    "£75k-£100k": 0.03,
    "£100k-£150k": 0.015, # HMRC Self Assessment data
    "£150k-£250k": 0.003, # HMRC: ~180k taxpayers
    "£250k-£500k": 0.0012,# HMRC: ~70k taxpayers
    "£500k-£1M": 0.0002,  # HMRC: ~12k taxpayers
    "£1M+": 0.0001        # HMRC: ~6k taxpayers (millionaires+)
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
# Source: British Association of Dermatologists & Academic research on androgenetic alopecia
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
        (100000, 150000, income_dist["£100k-£150k"]),
        (150000, 250000, income_dist["£150k-£250k"]),
        (250000, 500000, income_dist["£250k-£500k"]),
        (500000, 1000000, income_dist["£500k-£1M"]),
        (1000000, 10000000, income_dist["£1M+"])  # Assume upper bound of £10M for top bracket
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

def calculate_education_probability(min_education_level):
    """Calculate probability someone has the minimum education level or higher"""
    education_order = ["Below GCSE", "GCSE/O-Level", "A-Level or equivalent", 
                       "Undergraduate degree", "Postgraduate degree"]
    
    # If "Any" is selected, return 1.0
    if min_education_level == "Any":
        return 1.0
    
    # Find the index of the minimum level
    if min_education_level not in education_order:
        return 1.0
    
    min_index = education_order.index(min_education_level)
    
    # Sum probabilities from min_level and all levels above
    probability = 0
    for i in range(min_index, len(education_order)):
        probability += EDUCATION_DISTRIBUTION[education_order[i]]
    
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
    
    # Calculate all regional matches first to determine color scaling
    regional_matches_dict = {}
    for region, data in UK_REGIONS.items():
        regional_matches_dict[region] = int(data['adult_pop'] * regional_scale * total_probability)
    
    # Get min and max for color scaling
    max_matches = max(regional_matches_dict.values())
    min_matches = min(regional_matches_dict.values())
    
    # Add markers for each region
    for region, data in UK_REGIONS.items():
        regional_matches = regional_matches_dict[region]
        
        # Calculate color based on relative position (gradient from red to purple to blue)
        if max_matches > min_matches:
            ratio = (regional_matches - min_matches) / (max_matches - min_matches)
        else:
            ratio = 0.5
        
        # Color gradient: Red (low) -> Orange -> Yellow -> Green -> Blue -> Purple (high)
        if ratio < 0.2:
            color = '#EF5350'  # Red - very low
            radius = 18000
        elif ratio < 0.4:
            color = '#FF7043'  # Orange - low
            radius = 25000
        elif ratio < 0.6:
            color = '#FFA726'  # Amber - medium-low
            radius = 32000
        elif ratio < 0.8:
            color = '#66BB6A'  # Green - medium-high
            radius = 40000
        else:
            color = '#667eea'  # Purple - very high
            radius = 50000
        
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
    st.markdown('<div class="sub-header">Calculate your realistic dating pool size using real UK statistics \n for United Kingdom includes England, Scotland, Wales, and Northern Ireland (NOT Republic of Ireland)</div>', unsafe_allow_html=True)
    
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
            
            # Guard against min > max (in case sliders were set incorrectly)
            if min_height_cm > max_height_cm:
                min_height_cm, max_height_cm = max_height_cm, min_height_cm
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
        help="Minimum acceptable annual income. Includes EVERYONE earning this amount or MORE. (UK National Living Wage: £22,308 | Median: £31,285 | Average: £33,000)\n\nNote: High-income figures include self-employed, business owners, and company directors (HMRC Self Assessment data)."
    )
    # Convert to numeric
    if min_income == "Any":
        min_income = 0
    
    # Education
    st.sidebar.subheader("Education")
    
    education_level = st.sidebar.selectbox(
        "Minimum education level (includes this level and all higher levels):",
        ["Any", "Below GCSE", "GCSE/O-Level", "A-Level or equivalent", 
         "Undergraduate degree", "Postgraduate degree"],
        index=0,
        help="Select minimum acceptable education level. This will include everyone with this qualification OR HIGHER. E.g., selecting 'GCSE' includes GCSE, A-Level, Undergraduate, and Postgraduate degree holders."
    )
    
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
    
    # Handle conflict: if "must be single" is checked, remove "Currently married" from selection
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
    
    # Set flag when calculate is pressed
    if calculate_button:
        st.session_state.show_results = True
    
    # Main content
    if st.session_state.show_results:
        # Validation only needed if user manually deselected all (shouldn't happen with new UI)
        if education_level not in ["Any", "Below GCSE", "GCSE/O-Level", "A-Level or equivalent", "Undergraduate degree", "Postgraduate degree"]:
            st.error("Please select a valid education level")
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
            education_prob = calculate_education_probability(education_level)
            
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
            
            # Display results with improved layout
            st.markdown(f"""
                <div class="result-box">
                    <h2 style="margin: 0 0 1rem 0; font-size: 1.8rem; opacity: 0.95;">🎯 Your Dating Pool</h2>
                    <div class="result-percentage">{percentage:.3f}%</div>
                    <div class="result-count">≈ {estimated_matches:,} people in the UK</div>
                    <p style="margin-top: 1.5rem; font-size: 1rem; opacity: 0.9;">
                        Out of {UK_ADULT_POPULATION:,} UK adults
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Reality check banner
            col_center = st.columns([1, 2, 1])[1]
            with col_center:
                if percentage < 0.1:
                    st.error("🔥 Extremely selective criteria! Your dating pool is very small for the population.")
                elif percentage < 1:
                    st.warning("🔥 Extremely selective criteria! Your dating pool is very small for the population.")
                elif percentage < 5:
                    st.info("🔥 Extremely selective criteria! Your dating pool is very small for the population.")
                else:
                    st.success("✨ Relatively broad criteria. You have plenty of options!")
            
            st.markdown("---")
            
            # Breakdown with tabs for better organization
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
            
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Probability Breakdown", "⚙️ Your Criteria", "🗺️ Map Breakdown", "💍 Marriage Statistics"])
            
            with tab1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("### Filter Cascade", unsafe_allow_html=True)
                st.caption("Each filter progressively narrows down the pool")
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
                    "Remaining Pool": [
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
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("### Selected Filters", unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**👤 Your Gender:** {user_gender}")
                    st.markdown(f"**🔍 Looking for:** {looking_for}")
                    st.markdown(f"**🏳️‍🌈 Orientation:** {user_orientation}")
                    if any_age:
                        st.markdown(f"**🎂 Age:** <span class='metric-highlight'>Any (18+)</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**🎂 Age:** <span class='metric-highlight'>{age_range[0]}-{age_range[1]} years</span>", unsafe_allow_html=True)
                    
                    # Format height display
                    if any_height:
                        st.markdown(f"**📏 Height:** <span class='metric-highlight'>Any</span>", unsafe_allow_html=True)
                    else:
                        min_f, min_i = cm_to_feet_inches(min_height_cm)
                        max_f, max_i = cm_to_feet_inches(max_height_cm)
                        st.markdown(f"**📏 Height:** <span class='metric-highlight'>{min_height_cm:.0f}-{max_height_cm:.0f} cm ({min_f}'{min_i}\" - {max_f}'{max_i}\")</span>", unsafe_allow_html=True)
                    
                    if min_income > 0:
                        st.markdown(f"**💰 Min Income:** <span class='metric-highlight'>£{min_income:,}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**💰 Min Income:** <span class='metric-highlight'>Any</span>", unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"**🏋️ Body Type:** <span class='metric-highlight'>{len(selected_body_types)} type(s)</span>", unsafe_allow_html=True)
                    st.markdown(f"**🎓 Education:** <span class='metric-highlight'>{education_level} and above</span>", unsafe_allow_html=True)
                    st.markdown(f"**🌍 Ethnicity:** <span class='metric-highlight'>{len(selected_ethnicities)} group(s)</span>", unsafe_allow_html=True)
                    st.markdown(f"**💑 Status:** <span class='metric-highlight'>{'Single only' if must_be_single else 'Any'}</span>", unsafe_allow_html=True)
                    st.markdown(f"**👶 Children:** <span class='metric-highlight'>{len(acceptable_children)} option(s)</span>", unsafe_allow_html=True)
                    st.markdown(f"**💍 Marriage History:** <span class='metric-highlight'>{len(acceptable_marriage_history)} option(s)</span>", unsafe_allow_html=True)
                    if looking_for == "Male" or looking_for == "Any":
                        st.markdown(f"**👨 Baldness:** <span class='metric-highlight'>{baldness_preference}</span>", unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("### Geographic Distribution", unsafe_allow_html=True)
                st.caption("Circle size and color represent match density (red = low, purple = high)")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Create and display the map with larger size
                dating_map = create_dating_pool_map(total_probability)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st_folium(dating_map, width=1000, height=900)
                
                # Regional breakdown table
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("### Regional Breakdown Table", unsafe_allow_html=True)
                
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
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab4:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("### 💍 UK Marriage Statistics", unsafe_allow_html=True)
                st.caption("Based on Office for National Statistics (ONS) data - England & Wales 2022/2023")
                st.info("""**📅 Data Update Frequency:** The Office for National Statistics (ONS) typically publishes marriage and divorce statistics annually, with data released approximately 12-18 months after the reference year. The most recent comprehensive data available is from 2022, published in 2023-2024. ONS aims to release these statistics once per year, usually in late summer/autumn. While we are currently in 2025, the 2023 data is expected to be published soon, with 2024 data to follow in 2025-2026.""")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Marriage rates overview
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">', unsafe_allow_html=True)
                    st.markdown("#### Total Marriages (2022)")
                    st.markdown("### 249,793")
                    st.caption("England & Wales")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">', unsafe_allow_html=True)
                    st.markdown("#### Opposite-Sex")
                    st.markdown("### 242,842 (97.2%)")
                    st.caption("Heterosexual marriages")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">', unsafe_allow_html=True)
                    st.markdown("#### Same-Sex")
                    st.markdown("### 6,951 (2.8%)")
                    st.caption("3,474 male, 3,477 female")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Historical trend
                with st.expander("📈 Marriage Trends (2013-2022)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown("""**What this shows:** This tracks how marriage rates have changed over the past decade in England & Wales.
                Same-sex marriage became legal in March 2014, so 2013 shows zero same-sex marriages.""")
                    st.markdown("")
                    
                    marriage_trend_data = {
                        "Year": ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020*", "2021", "2022"],
                        "Total Marriages": ["262,240", "289,841", "239,020", "242,274", "244,710", "244,579", "247,964", "150,732", "234,795", "249,793"],
                        "Opposite-Sex": ["262,240", "287,469", "234,795", "237,775", "240,203", "239,945", "243,442", "147,880", "230,092", "242,842"],
                        "Same-Sex": ["0", "2,372", "4,225", "4,499", "4,507", "4,634", "4,522", "2,852", "4,703", "6,951"],
                        "Marriage Rate¹": ["22.5", "24.6", "20.1", "20.1", "20.1", "19.9", "20.0", "12.2", "18.9", "19.9"]
                    }
                    st.dataframe(marriage_trend_data, hide_index=True, use_container_width=True)
                    st.caption("¹ Marriage rate per 1,000 unmarried population aged 16+. *2020 affected by COVID-19 pandemic")
                    
                    # Chart for marriage trends
                    import plotly.graph_objects as go
                    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
                    opposite_sex = [262240, 287469, 234795, 237775, 240203, 239945, 243442, 147880, 230092, 242842]
                    same_sex = [0, 2372, 4225, 4499, 4507, 4634, 4522, 2852, 4703, 6951]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=years, y=opposite_sex, name='Opposite-Sex', 
                                            line=dict(color='#f5576c', width=3)))
                    fig.add_trace(go.Scatter(x=years, y=same_sex, name='Same-Sex',
                                            line=dict(color='#4facfe', width=3)))
                    fig.update_layout(
                        title='Marriage Trends Over Time',
                        xaxis_title='Year',
                        yaxis_title='Number of Marriages',
                        template='plotly_dark',
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""**Key Insights:**
                - **2014 spike:** First full year of same-sex marriage legalization created pent-up demand
                - **2020 crash:** COVID-19 pandemic caused 39% drop in marriages (lockdowns prevented ceremonies)
                - **Stable trend:** Opposite-sex marriages hover around 240,000 annually (excluding pandemic)
                - **Same-sex growth:** Increased from 2,372 (2014) to 6,951 (2022) - nearly 3x growth
                - **Overall trend:** Marriage rates remain relatively stable but lower than historical peaks""")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Age statistics
                with st.expander("🎂 Marriage by Age (2022)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown("""**What this shows:** The age when people in England & Wales get married, showing both first marriages and all marriages (including remarriages).
                    
                    **Understanding the statistics:**
                    - **Mean (Average):** Add all ages and divide by number of people. Affected by extreme values.
                    - **Median (Middle):** The exact middle value when all ages are sorted. 50% marry younger, 50% marry older.
                    - First marriage ages are younger because they exclude remarriages (which happen at older ages).""")
                    st.markdown("")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        age_summary = {
                            "Statistic": ["Mean (average) first marriage", "Median (middle) all marriages", "Age gap (mean)"],
                            "Men": ["34.0 years", "37.9 years", "2.0 years older"],
                            "Women": ["32.0 years", "35.5 years", "than women"]
                        }
                        st.dataframe(age_summary, hide_index=True, use_container_width=True)
                        st.caption("Mean = average of all ages. Median = middle value.")
                    
                    with col2:
                        age_distribution_marriages = {
                            "Age Group": ["16-24", "25-29", "30-34", "35-39", "40-44", "45-54", "55-64", "65+"],
                            "Men %": ["3.2%", "18.5%", "25.8%", "19.7%", "12.3%", "12.8%", "5.3%", "2.4%"],
                            "Women %": ["5.8%", "24.7%", "26.2%", "17.8%", "10.2%", "9.7%", "4.0%", "1.6%"]
                        }
                        st.dataframe(age_distribution_marriages, hide_index=True, use_container_width=True)
                        st.caption("% of all marriages happening in each age group")
                    
                    # Chart for age distribution
                    age_groups = ["16-24", "25-29", "30-34", "35-39", "40-44", "45-54", "55-64", "65+"]
                    men_pct = [3.2, 18.5, 25.8, 19.7, 12.3, 12.8, 5.3, 2.4]
                    women_pct = [5.8, 24.7, 26.2, 17.8, 10.2, 9.7, 4.0, 1.6]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=age_groups, y=men_pct, name='Men', marker_color='#667eea'))
                    fig.add_trace(go.Bar(x=age_groups, y=women_pct, name='Women', marker_color='#f5576c'))
                    fig.update_layout(
                        title='Marriage Age Distribution by Gender',
                        xaxis_title='Age Group',
                        yaxis_title='Percentage of Marriages',
                        template='plotly_dark',
                        barmode='group',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""**Key Insights:**
                    - **Peak ages:** Most marriages occur at ages 30-34 for both men (25.8%) and women (26.2%)
                    - **Women marry younger:** 5.8% of women marry ages 16-24 vs only 3.2% of men
                    - **Men marry later:** 12.8% of men marry ages 45-54 vs 9.7% of women (remarriages)
                    - **Traditional gap:** Men are on average 2 years older than women at first marriage
                    - **Median higher than mean:** This means remarriages (at older ages) pull the median up
                    - **Modern shift:** Compare to 1973 when mean first marriage was 26.3 (men) and 24.0 (women) - now 8 years later!""")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Divorce statistics
                with st.expander("💔 Divorce & Dissolution Statistics (2022)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown("""**What this shows:** How many marriages end in divorce and how long they typically last.
                    
                    **Understanding the statistics:**
                    - **Mean duration:** Average length of all marriages before divorce (add all durations ÷ number of divorces)
                    - **Median age:** The middle age - half divorce younger, half divorce older
                    - **Divorce rate:** Number of divorces per 1,000 married people per year""")
                    st.markdown("")
                    
                    st.markdown("### 📈 Historical Divorce & Dissolution Trends (1963-2022)")
                    st.markdown("""**What this shows:** This tracks how divorce rates have changed over nearly 60 years in England & Wales, showing major social and legal shifts.
                    
                    **Key Historical Events:**
                    - **1969:** Divorce Reform Act made divorce easier (effective 1971)
                    - **2004:** Civil Partnerships introduced for same-sex couples
                    - **2014:** Same-sex marriage legalized; civil partnerships decline
                    - **2022:** No-fault divorce introduced (April 2022)""")
                    st.markdown("")
                    
                    # Historical divorce data
                    divorce_trend_data = {
                        "Year": ["1963", "1971", "1980", "1985", "1990", "1995", "2000", "2005", "2010", "2015", "2019", "2020", "2021", "2022"],
                        "Divorces": ["32,000", "74,437", "148,301", "160,300", "165,658", "155,499", "141,135", "141,322", "119,589", "101,055", "107,599", "103,592", "113,505", "80,057"],
                        "Dissolutions": ["-", "-", "-", "-", "-", "-", "-", "167", "6,385", "5,734", "5,006", "3,956", "7,525", "2,112"],
                        "Total Breakups": ["32,000", "74,437", "148,301", "160,300", "165,658", "155,499", "141,135", "141,489", "125,974", "106,789", "112,605", "107,548", "121,030", "82,169"],
                        "Divorce Rate¹": ["2.5", "5.9", "12.0", "13.4", "13.6", "13.0", "12.7", "12.2", "10.8", "8.9", "8.9", "8.5", "9.6", "6.9"]
                    }
                    st.dataframe(divorce_trend_data, hide_index=True, use_container_width=True)
                    st.caption("¹ Divorce rate per 1,000 married population. Dissolutions = civil partnership breakups. 2022 data affected by timing of no-fault reform (April 2022)")
                    
                    # Chart for historical divorce trends
                    years_divorce = [1963, 1971, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2019, 2020, 2021, 2022]
                    divorces = [32000, 74437, 148301, 160300, 165658, 155499, 141135, 141322, 119589, 101055, 107599, 103592, 113505, 80057]
                    dissolutions = [0, 0, 0, 0, 0, 0, 0, 167, 6385, 5734, 5006, 3956, 7525, 2112]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=years_divorce, y=divorces, name='Divorces (Opposite-Sex)', 
                                            line=dict(color='#f5576c', width=3), fill='tonexty'))
                    fig.add_trace(go.Scatter(x=years_divorce, y=dissolutions, name='Civil Partnership Dissolutions',
                                            line=dict(color='#4facfe', width=3)))
                    
                    # Add annotations for key events
                    fig.add_annotation(x=1971, y=74437, text="1969 Reform Act<br>takes effect",
                                      showarrow=True, arrowhead=2, ax=-40, ay=-40)
                    fig.add_annotation(x=1993, y=165658, text="Peak: 165,658<br>divorces (1993)",
                                      showarrow=True, arrowhead=2, ax=0, ay=-50)
                    fig.add_annotation(x=2022, y=80057, text="2022: No-fault<br>reform",
                                      showarrow=True, arrowhead=2, ax=40, ay=-40)
                    
                    fig.update_layout(
                        title='Divorce and Dissolution Trends Over Time (1963-2022)',
                        xaxis_title='Year',
                        yaxis_title='Number of Divorces/Dissolutions',
                        template='plotly_dark',
                        height=500,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""**Key Insights:**
                    - **Dramatic increase 1963-1993:** Divorces rose from 32,000 to peak of 165,658 (actual peak was 1993)
                    - **1969 Reform Act impact:** Divorces more than doubled from 32,000 (1963) to 74,437 (1971) when reform took effect
                    - **Peak divorce era:** 1980s-1990s saw highest divorce rates (160,000+ annually)
                    - **Steady decline since 1993:** Divorces fell to 80,057 in 2022 - a 52% drop from peak
                    - **2022 anomaly:** Sharp drop due to no-fault reform timing - people delayed divorces until April 2022 for easier process
                    - **Civil partnerships declining:** Dissolutions peaked at 7,525 (2021) but dropped to 2,112 (2022) as fewer CPs formed
                    - **Marriage rate correlation:** Fewer marriages = fewer divorces (244,579 marriages in 2018 vs 397,000 in 1972)
                    
                    **Why divorce rates have fallen:**
                    - **Fewer marriages:** Marriage rate down from 8.9 per 1,000 (1972) to 4.4 per 1,000 (2019)
                    - **Cohabitation increase:** Couples live together longer before marrying - weaker relationships end before marriage
                    - **Older marriage age:** People marry at 34/32 (men/women) vs 26/24 in 1973 - more mature, stable relationships
                    - **Better relationship education:** More awareness of relationship skills, therapy access
                    - **Selection effect:** Those who marry today are more committed to marriage as institution
                    - **Economic factors:** Cost of divorce (legal fees, housing) deters some
                    
                    **Divorce rate context:**
                    - Peak rate: 13.6 per 1,000 married people (1990)
                    - 2022 rate: 6.9 per 1,000 married people - lowest since 1970s
                    - UK rate similar to France (7.5), lower than US (14.5), higher than Italy (3.2)
                    
                    **The "42% divorce rate" myth:**
                    - Often cited statistic is misleading projection
                    - Based on dividing annual divorces by annual marriages (which compares different cohorts)
                    - Actual survival analysis shows ~52% of marriages survive 30+ years
                    - Rate varies by age at marriage, education, income, cohabitation history""")
                    st.markdown("")
                    
                    divorce_overview = {
                        "Category": ["Opposite-Sex Divorces", "Same-Sex Divorces", "Civil Partnership (Male)", "Civil Partnership (Female)"],
                        "Total Cases": ["80,057", "1,170", "422", "494"],
                        "Mean Duration": ["12.7 years", "5.4 years", "7.8 years", "6.2 years"],
                        "Median Age at Divorce": ["M: 46.4, F: 43.9", "M: 42.1, F: 40.8", "45.3", "43.6"],
                        "Rate per 1,000": ["8.2", "16.8", "N/A", "N/A"]
                    }
                    st.dataframe(divorce_overview, hide_index=True, use_container_width=True)
                    
                    # Comparison accounting for different population sizes
                    st.markdown("")
                    st.markdown("#### 📊 Comparative Analysis (Rate-Adjusted)")
                    st.markdown("""**How this is calculated:** These rates are 'rate-adjusted' to allow fair comparison:
                    - **Divorce rate per 1,000 marriages** = (Number of divorces ÷ Number of married couples) × 1,000
                      - Opposite-sex: 80,057 divorces ÷ ~9.8 million married couples = 8.2 per 1,000 annually
                      - Same-sex: 1,170 divorces ÷ ~69,700 married couples = 16.8 per 1,000 annually
                    - **Duration vs baseline** = (Same-sex duration ÷ Opposite-sex duration) × 100 = (5.4 ÷ 12.7) × 100 = 42.5%
                    - **Rate comparison** = (Same-sex rate ÷ Opposite-sex rate - 1) × 100 = (16.8 ÷ 8.2 - 1) × 100 = 105% higher
                    
                    This controls for population size differences so we can compare like-with-like.""")
                    st.markdown("")
                    comparison_data = {
                        "Metric": [
                            "Divorce rate per 1,000 marriages",
                            "Mean marriage duration",
                            "Duration vs opposite-sex baseline",
                            "Median divorce age gap (M-F)"
                        ],
                        "Opposite-Sex": [
                            "8.2",
                            "12.7 years",
                            "Baseline (100%)",
                            "2.5 years"
                        ],
                        "Same-Sex": [
                            "16.8 (↑105% higher)",
                            "5.4 years",
                            "42.5% of baseline",
                            "1.3 years"
                        ]
                    }
                    st.dataframe(comparison_data, hide_index=True, use_container_width=True)
                    st.caption("Rate-adjusted: Accounts for different population sizes. Same-sex marriages are newer (legal since 2014), so shorter durations expected.")
                    
                    # Chart comparing divorce rates and duration
                    fig = go.Figure()
                    categories = ['Opposite-Sex', 'Same-Sex', 'Civil Partner (M)', 'Civil Partner (F)']
                    durations = [12.7, 5.4, 7.8, 6.2]
                    colors = ['#667eea', '#4facfe', '#f093fb', '#f5576c']
                    
                    fig.add_trace(go.Bar(
                        x=categories,
                        y=durations,
                        marker_color=colors,
                        text=[f"{d} yrs" for d in durations],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title='Mean Marriage Duration Before Divorce',
                        xaxis_title='Marriage Type',
                        yaxis_title='Years',
                        template='plotly_dark',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""**Key Insights:**
                    - **Opposite-sex divorce rate:** 8.2 per 1,000 married people = ~0.82% divorce annually
                    - **Same-sex higher rate:** 16.8 per 1,000 = double the opposite-sex rate (but sample is newer)
                    - **Shorter same-sex duration:** 5.4 years vs 12.7 years - BUT same-sex marriage only legal since 2014, so maximum possible duration is 8-9 years in 2022 data
                    - **Civil partnerships:** Middle ground at 6-8 years (these have existed since 2005, longer track record)
                    - **Age at divorce:** People divorce in their 40s on average - men slightly older
                    - **Why shorter same-sex duration?** New marriages haven't had time to reach 10+ years yet. Early adopters may have had relationship problems. More data needed after 2030.""")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Who initiates divorce
                with st.expander("⚖️ Who Initiates Divorce? (2022)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown("""**What this shows:** Which party files the legal paperwork to start divorce proceedings.
                    This is called being the 'petitioner' (pre-2022) or 'applicant' (post-2022 no-fault reform).
                    
                    **Why it matters:** Shows who takes action to end the marriage, which may indicate who is more dissatisfied or who has more resources/support to initiate.""")
                    st.markdown("")
                    
                    st.markdown("#### Opposite-Sex Divorces - Petitioner")
                    divorce_initiator = {
                        "Petitioner": ["Wife", "Husband", "Joint Application"],
                        "Number": ["50,436", "24,121", "5,500"],
                        "Percentage": ["63.0%", "30.1%", "6.9%"],
                        "Ratio": ["2.1 : 1", "(wife to husband)", "Both agree"]
                    }
                    st.dataframe(divorce_initiator, hide_index=True, use_container_width=True)
                    st.caption("**Women initiate ~63% of opposite-sex divorces - more than double the rate of men**")
                    
                    # Pie chart for divorce initiators
                    fig = go.Figure(data=[go.Pie(
                        labels=['Wife Initiated', 'Husband Initiated', 'Joint Application'],
                        values=[50436, 24121, 5500],
                        marker_colors=['#f5576c', '#667eea', '#4facfe'],
                        hole=0.4
                    )])
                    fig.update_layout(
                        title='Who Initiates Opposite-Sex Divorce?',
                        template='plotly_dark',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""**Key Insights:**
                    - **Women dominate initiation:** 63% of divorces filed by wives vs 30% by husbands
                    - **2:1 ratio:** For every divorce initiated by a husband, 2.1 are initiated by wives
                    - **Joint applications rare:** Only 6.9% are filed jointly (increased after no-fault reform in April 2022)
                    - **Why women initiate more:** Research suggests women have higher expectations for emotional connection, identify problems earlier, do more 'emotional labor', and are more likely to have social/family support for divorce
                    - **Men's reluctance:** Men report being 'blindsided' more often, suggesting they may not recognize relationship problems as early
                    - **Financial independence:** Women's increased workforce participation (since 1970s) makes divorce more financially viable""")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Reasons for divorce
                with st.expander("📋 Grounds for Divorce (2022)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown("""**What this shows:** The legal reasons (grounds) people use to file for divorce changed dramatically in April 2022.
                    
                    **Major reform:** England & Wales introduced 'no-fault' divorce in April 2022, ending the requirement to prove fault or blame your spouse. Before this, you had to cite specific grounds like adultery or behavior.""")
                    st.markdown("")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Traditional Grounds (Pre-April 2022)")
                        divorce_reasons_old = {
                            "Ground": ["Unreasonable behavior", "Adultery", "2-year separation (with consent)", "5-year separation", "Desertion"],
                            "% of Cases": ["35%", "15%", "30%", "18%", "2%"],
                            "Petitioner Trend": ["60% women", "70% women", "50/50 split", "60% women", "65% women"]
                        }
                        st.dataframe(divorce_reasons_old, hide_index=True, use_container_width=True)
                        st.caption("Historical data 2019-2021")
                    
                    with col2:
                        st.markdown("#### Post-Reform (April 2022 onwards)")
                        divorce_reasons_new = {
                            "Ground": ["Irretrievable breakdown (no-fault)", "  ↳ Filed by woman", "  ↳ Filed by man", "Joint application", "20-week cooling-off applied"],
                            "% of Cases": ["93.1%", "~58.7%", "~28.0%", "6.9%", "100%"],
                            "Impact": ["No blame required", "Part of 93.1%", "Part of 93.1%", "Both parties agree", "Mandatory waiting period"]
                        }
                        st.dataframe(divorce_reasons_new, hide_index=True, use_container_width=True)
                        st.caption("New system removes adversarial blame. Gender split within no-fault reflects who files the application.")
                        st.markdown("")
                        st.info("""ℹ️ **Note:** The 93.1% 'no-fault' category includes both male and female applicants (see 'Who Initiates Divorce?' section above for the 63% women / 30% men / 6.9% joint breakdown). Under no-fault reform, you don't need to prove grounds, but someone still has to file the application - the gender split for who files remains similar to before the reform.""")
                    
                    # Chart comparing old vs new system
                    fig = go.Figure()
                    old_grounds = ['Unreasonable\nbehavior', 'Adultery', '2-year\nseparation', '5-year\nseparation', 'Desertion']
                    old_percentages = [35, 15, 30, 18, 2]
                    fig.add_trace(go.Bar(
                        x=old_grounds,
                        y=old_percentages,
                        name='Pre-2022 System',
                        marker_color='#f5576c',
                        text=[f"{p}%" for p in old_percentages],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title='Legal Grounds for Divorce (Pre-April 2022)',
                        xaxis_title='Ground',
                        yaxis_title='Percentage of Cases',
                        template='plotly_dark',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""**Key Insights:**
                    - **No-fault revolution:** 93.1% now use simple "irretrievable breakdown" without proving fault
                    - **Joint applications increased:** From <2% to 6.9% - couples can now apply together
                    - **Old system problems:** Required blaming spouse, creating hostility; often forced people to wait 2-5 years
                    - **Unreasonable behavior** was the most common ground (35%) - a catch-all category that included anything from lack of affection to financial irresponsibility
                    - **Adultery bias:** Women cited adultery more (70%) because men's affairs were more likely to be discovered
                    - **Separation grounds:** Required living apart 2 years (with consent) or 5 years (without) - expensive and impractical
                    - **Reform benefits:** Reduces conflict, faster process, less expensive, protects children from parental conflict""")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Underlying reasons for divorce
                with st.expander("💡 Underlying Reasons for Divorce (Survey Data)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown("""**What this shows:** The **real reasons** marriages fail vs the **legal grounds** cited in court.
                    Legal grounds (above) are formalities; these survey results reveal what actually goes wrong in relationships.
                    
                    **Important:** Multiple reasons usually apply to each divorce - percentages don't sum to 100%.""")
                    st.markdown("")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Top Reasons Cited by Divorcing Couples")
                        underlying_reasons = {
                            "Reason": [
                                "Growing apart / Incompatibility",
                                "Lack of communication",
                                "Infidelity / Adultery",
                                "Financial problems / Money stress",
                                "Lack of intimacy",
                                "Unrealistic expectations",
                                "Substance abuse",
                                "Domestic abuse",
                                "Work-life imbalance",
                                "In-law interference"
                            ],
                            "% Citing": ["55%", "53%", "37%", "36%", "31%", "26%", "25%", "23%", "18%", "14%"],
                            "Gender Difference": [
                                "Similar",
                                "Women cite more",
                                "Equal",
                                "Men cite more",
                                "Women cite more",
                                "Women cite more",
                                "Women cite more",
                                "Women cite more",
                                "Women cite more",
                                "Women cite more"
                            ]
                        }
                        st.dataframe(underlying_reasons, hide_index=True, use_container_width=True)
                        st.caption("Survey data from divorcing couples - percentages show how many cited each reason")
                    
                    with col2:
                        # Chart for top divorce reasons
                        reasons_short = ['Growing\napart', 'Poor\ncommunication', 'Infidelity', 'Financial\nstress', 'No intimacy',
                                       'Unrealistic\nexpectations', 'Substance\nabuse', 'Domestic\nabuse', 'Work-life\nimbalance', 'In-law\nissues']
                        percentages = [55, 53, 37, 36, 31, 26, 25, 23, 18, 14]
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            y=reasons_short[::-1],  # Reverse for horizontal bar
                            x=percentages[::-1],
                            orientation='h',
                            marker_color='#667eea',
                            text=[f"{p}%" for p in percentages[::-1]],
                            textposition='auto'
                        ))
                        fig.update_layout(
                            title='Real Reasons for Divorce',
                            xaxis_title='% of Divorcing Couples Citing Reason',
                            template='plotly_dark',
                            height=500,
                            margin=dict(l=150)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""**Key Insights:**
                    - **Top 2 reasons:** "Growing apart" (55%) and "lack of communication" (53%) - these are gradual, not sudden events
                    - **Infidelity less common than thought:** Only 37% cite it (vs popular belief it causes most divorces)
                    - **Financial stress major factor:** 36% cite money problems - rent/mortgage, debt, different spending values
                    - **Women report more issues:** Women cite 8 out of 10 top reasons more than men - suggests women are more attuned to relationship problems or men are less aware
                    - **Men cite financial problems more:** Only reason men cite more - may feel pressure as traditional "provider"
                    - **Intimate relationship breakdown:** 31% cite lack of intimacy - not just sex, but emotional closeness too
                    - **Abuse underreported:** 23% cite domestic abuse, but actual rates likely higher due to shame/fear
                    
                    **Why women initiate more divorces:**
                    - Women report higher expectations for emotional connection
                    - More likely to identify relationship problems earlier
                    - Less likely to tolerate poor treatment or abuse
                    - Take on more emotional labor in relationships
                    - Financial independence increasing since 1970s
                    
                    **Timing patterns:**
                    - Peak divorce years: 5-7 years and 20+ years
                    - "Seven-year itch" is statistically real
                    - Long marriages end when children leave home
                    
                    **Warning signs:**
                    - Contempt, criticism, defensiveness, stonewalling ("Four Horsemen")
                    - Emotional disengagement before physical separation
                    - Average couple waits 6 years after problems start before seeking help""")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Marriage survival rates
                with st.expander("📊 Marriage Survival Rates (Opposite-Sex)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.caption("Estimated % of marriages still intact after N years (2022 cohort analysis)")
                    
                    survival_data = {
                        "Years Since Marriage": ["5 years", "10 years", "15 years", "20 years", "25 years", "30 years"],
                        "Survival Rate": ["89.8%", "78.9%", "69.7%", "62.1%", "56.3%", "52.0%"],
                        "Implication": [
                            "~10% end within 5 years",
                            "~21% end within 10 years",
                            "~30% end within 15 years",
                            "~38% end within 20 years",
                            "~44% end within 25 years",
                            "~48% end within 30 years"
                        ]
                    }
                    st.dataframe(survival_data, hide_index=True, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Economic factors
                with st.expander("💰 Marriage & Income Statistics", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Household Income by Marital Status (2023)")
                        income_marital = {
                            "Status": ["Married couple", "Cohabiting couple", "Single (never married)", "Divorced/Separated", "Widowed"],
                            "Median Income": ["£44,500", "£38,200", "£23,800", "£26,400", "£18,900"]
                        }
                        st.dataframe(income_marital, hide_index=True, use_container_width=True)
                        st.caption("Before housing costs (BHC)")
                    
                    with col2:
                        st.markdown("#### Marriage Rate by Education (Ages 25-44)")
                        education_marriage = {
                            "Education Level": ["Postgraduate degree", "Undergraduate degree", "A-Level/equivalent", "GCSE/O-Level", "Below GCSE"],
                            "Ever Married %": ["62%", "58%", "52%", "47%", "39%"]
                        }
                        st.dataframe(education_marriage, hide_index=True, use_container_width=True)
                        st.caption("% who have ever been married")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Children and marriage
                with st.expander("👶 Children & Marriage", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Births by Marital Status (2022)")
                        births_data = {
                            "Parent Status": ["Married or civil partnership", "Cohabiting", "Sole registration", "Other"],
                            "% of Births": ["58.7%", "33.4%", "7.6%", "0.3%"]
                        }
                        st.dataframe(births_data, hide_index=True, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### Families with Children (2023)")
                        families_data = {
                            "Family Type": ["Married couple", "Cohabiting couple", "Lone parent"],
                            "% of Families": ["62.8%", "17.9%", "19.3%"],
                            "Avg Children": ["1.89", "1.72", "1.73"]
                        }
                        st.dataframe(families_data, hide_index=True, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Death and widowhood
                with st.expander("🕊️ Widowhood Statistics", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    
                    widowhood_overview = {
                        "Statistic": [
                            "Total widowed population",
                            "Widowed women",
                            "Widowed men",
                            "Gender ratio",
                            "% of adults 16+"
                        ],
                        "Value": [
                            "3.4 million",
                            "2.5 million (73.5%)",
                            "0.9 million (26.5%)",
                            "2.8 women per 1 man",
                            "6.7%"
                        ]
                    }
                    st.dataframe(widowhood_overview, hide_index=True, use_container_width=True)
                    st.caption("Based on 2021 Census - England & Wales")
                    
                    st.markdown("")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Why More Widowed Women?")
                        widowhood_reasons = {
                            "Factor": [
                                "Life expectancy gap",
                                "Age difference at marriage",
                                "Remarriage rate (men)",
                                "Remarriage rate (women)",
                                "Health factors"
                            ],
                            "Detail": [
                                "Women live ~4 years longer",
                                "Women typically marry 2-3 years older men",
                                "Men remarry 2x more often",
                                "Women less likely to remarry after 60",
                                "Heart disease kills men earlier"
                            ]
                        }
                        st.dataframe(widowhood_reasons, hide_index=True, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### Widowhood by Age Group")
                        widowhood_age = {
                            "Age Group": ["45-54", "55-64", "65-74", "75-84", "85+"],
                            "% Widowed (Men)": ["0.8%", "2.5%", "7.8%", "20.3%", "43.2%"],
                            "% Widowed (Women)": ["1.6%", "5.3%", "15.8%", "38.7%", "69.8%"]
                        }
                        st.dataframe(widowhood_age, hide_index=True, use_container_width=True)
                        st.caption("Percentage widowed increases dramatically with age")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Remarriage statistics
                with st.expander("🔄 Remarriage Statistics (2022)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Marriages by Previous Marital Status")
                        remarriage_data = {
                            "Marital History": ["Both first marriage", "One remarriage", "Both remarriages"],
                            "Number": ["133,842", "73,288", "35,712"],
                            "% of Total": ["53.6%", "29.3%", "14.3%"]
                        }
                        st.dataframe(remarriage_data, hide_index=True, use_container_width=True)
                        st.caption("Opposite-sex marriages only")
                    
                    with col2:
                        st.markdown("#### Remarriage Rates & Timeline")
                        remarriage_timeline = {
                            "Metric": [
                                "Mean age at remarriage (men)",
                                "Mean age at remarriage (women)",
                                "Divorced men remarry within 10 yrs",
                                "Divorced women remarry within 10 yrs",
                                "Widowed men remarry",
                                "Widowed women remarry"
                            ],
                            "Value": [
                                "47.3 years",
                                "44.5 years",
                                "60%",
                                "54%",
                                "24% (higher rate)",
                                "11% (lower rate)"
                            ]
                        }
                        st.dataframe(remarriage_timeline, hide_index=True, use_container_width=True)
                    
                    st.markdown("")
                    st.markdown("#### Remarriage Success Rates")
                    remarriage_success = {
                        "Marriage Type": ["First marriage", "Second marriage", "Third+ marriage"],
                        "10-year survival rate": ["78.9%", "67.3%", "58.1%"],
                        "20-year survival rate": ["62.1%", "47.8%", "38.2%"],
                        "Key factors": [
                            "Learning curve, less experience",
                            "Blended families, financial complexity",
                            "Pattern repetition, unresolved issues"
                        ]
                    }
                    st.dataframe(remarriage_success, hide_index=True, use_container_width=True)
                    st.caption("Second and subsequent marriages have higher divorce risk")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Regional variations
                with st.expander("🗺️ Regional Marriage Rates (2022)", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.caption("Marriage rate per 1,000 unmarried population aged 16+")
                    
                    regional_marriage_data = {
                        "Region": ["London", "South East", "East of England", "South West", "West Midlands", 
                                  "East Midlands", "North West", "Yorkshire & Humber", "North East", "Wales"],
                        "Marriage Rate": ["23.4", "19.8", "18.9", "17.6", "20.1", "18.7", "19.5", "19.2", "17.8", "16.9"],
                        "Ranking": ["Highest", "2nd", "5th", "8th", "3rd", "6th", "4th", "5th", "7th", "Lowest"]
                    }
                    st.dataframe(regional_marriage_data, hide_index=True, use_container_width=True)
                    st.caption("London has highest marriage rate, Wales has lowest")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Modern trends
                with st.expander("🔄 Modern Marriage Trends", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### Declining Marriage Rates Over Time")
                        decline_data = {
                            "Year": ["1972 (Peak)", "1990", "2000", "2010", "2022"],
                            "Rate per 1,000": ["35.1", "28.4", "25.1", "21.3", "19.9"],
                            "% Change from Peak": ["0%", "-19.1%", "-28.5%", "-39.3%", "-43.3%"]
                        }
                        st.dataframe(decline_data, hide_index=True, use_container_width=True)
                        st.markdown("")
                        st.markdown("**Key factors in decline:**")
                        decline_reasons = {
                            "Factor": [
                                "Cohabitation acceptance",
                                "Economic pressure",
                                "House prices",
                                "Student debt",
                                "Career prioritization",
                                "Changing social norms"
                            ],
                            "Impact": [
                                "3.6M cohabiting couples",
                                "Cost of living crisis",
                                "Average: £290,000",
                                "Average: £45,000",
                                "Women's careers valued",
                                "Marriage less necessary"
                            ]
                        }
                        st.dataframe(decline_reasons, hide_index=True, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### Rising Marriage Age")
                        age_increase = {
                            "Year": ["1973", "1990", "2000", "2010", "2022"],
                            "Men (mean age)": ["26.3", "28.8", "30.8", "32.3", "34.0"],
                            "Women (mean age)": ["24.0", "26.7", "28.9", "30.1", "32.0"]
                        }
                        st.dataframe(age_increase, hide_index=True, use_container_width=True)
                        st.caption("Mean age at first marriage has increased ~8 years since 1970s")
                        st.markdown("")
                        st.markdown("**Cohabitation before marriage:**")
                        cohabitation_stats = {
                            "Metric": [
                                "Couples cohabit before marriage",
                                "Average cohabitation duration",
                                "Never-married 30-year-olds",
                                "Cohabiting couples in UK",
                                "% of families cohabiting"
                            ],
                            "Value": [
                                "84%",
                                "3.5 years",
                                "48%",
                                "3.6 million",
                                "17.9%"
                            ]
                        }
                        st.dataframe(cohabitation_stats, hide_index=True, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # International comparisons
                with st.expander("🌍 UK vs International Comparison", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    
                    international_data = {
                        "Country": ["Turkey", "United States", "Portugal", "France", "Germany", "UK", "Sweden", "Italy", "Spain"],
                        "Marriage Rate*": ["6.1", "5.1", "4.6", "3.5", "3.3", "3.2", "3.1", "2.9", "2.8"],
                        "Mean Age Women": ["27.8", "28.6", "33.1", "33.0", "32.5", "32.0", "34.5", "34.2", "34.7"],
                        "Mean Age Men": ["29.2", "30.4", "35.3", "35.6", "35.1", "34.0", "36.9", "36.5", "37.1"]
                    }
                    st.dataframe(international_data, hide_index=True, use_container_width=True)
                    st.caption("*Crude marriage rate per 1,000 population (2021-2022). UK has moderate marriage rate compared to Europe.")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Data sources
                with st.expander("📚 Data Sources", expanded=False):
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown("""
                    - **[ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022)**
                    - **[ONS Divorces in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/divorce/bulletins/divorcesinenglandandwales/2022)**
                    - **[ONS Census 2021 - Marital and Civil Partnership Status](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriageandcivilpartnershipstatusinenglandandwales/census2021)**
                    - **[ONS Families and Households: 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2023)**
                    - **[ONS Birth Statistics by Parents' Characteristics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/birthsbyparentscharacteristics)**
                    - **[ONS Annual Survey of Hours and Earnings](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2023)** - Income by marital status
                    - **[DWP Family Resources Survey 2023](https://www.gov.uk/government/statistics/family-resources-survey-financial-year-2022-to-2023)**
                    - **[Eurostat Marriage Statistics](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Marriage_and_divorce_statistics)** - International comparison data
                    
                    All statistics are for **England and Wales** unless specified UK-wide. Scotland and Northern Ireland 
                    publish separate statistics but follow similar trends.
                    
                    **Note:** Same-sex marriage became legal in England & Wales (March 2014), Scotland (December 2014), 
                    and Northern Ireland (January 2020). Civil partnerships available since 2005.
                    """)
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sources section
    with st.expander("Data Sources & Methodology"):
        st.markdown("""
        ### Data Sources
        
        All statistics are based on official UK government data and peer-reviewed research:
        
        **Geographic Coverage:** United Kingdom includes England, Scotland, Wales, and Northern Ireland (NOT Republic of Ireland).
        Note: Some datasets (ethnicity) are England & Wales only due to separate census systems in Scotland/NI.
        
        1. **Population Data by Age Demographics**
           - Source: [ONS Mid-2022 Population Estimates](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2022)
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
           - Source: [ONS Population Estimates by Age and Sex](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland)
           - Data Year: 2022
           - All percentages are of total adult population (18+) unless specified
        
        3. **Ethnicity**
           - Source: [ONS Census 2021 - Ethnic Group, England and Wales](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity/bulletins/ethnicgroupenglandandwales/census2021)
           - **Coverage: England and Wales ONLY** (Scotland and Northern Ireland have separate census systems)
           - Note: Applied to full UK population as best available approximation
           - Categories: White (81.6%), Asian (9.3%), Black (4.0%), Mixed (2.9%), Other (2.2%)
        
        4. **Height Distribution**
           - Source: [NHS Health Survey for England 2021](https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england/2021) & [Academic Studies on UK Height](https://www.bmj.com/content/bmj/early/2016/07/26/bmj.i3989.full.pdf)
           - **Male:** 
             * Mean (Average): 175.3cm (5'9") / Median: 175cm (5'9")
             * Standard Deviation: 7.1cm
           - **Female:** 
             * Mean (Average): 161.6cm (5'3.5") / Median: 162cm (5'4")
             * Standard Deviation: 6.5cm
           - Normal distribution assumed
        
        5. **Body Type / BMI Distribution**
           - Source: [NHS Health Survey for England 2021 - Adult Obesity](https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england/2021/part-1-overweight-and-obesity-in-adults-and-children)
           - BMI categories based on [WHO Standards](https://www.who.int/europe/news-room/fact-sheets/item/a-healthy-lifestyle---who-recommendations)
           
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
           - Source: [ONS Annual Survey of Hours and Earnings (ASHE) 2023](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2023) + [HMRC Income Tax Liabilities Statistics 2022-23](https://www.gov.uk/government/statistics/income-tax-liabilities-statistics-2020-to-2021)
           - Gross annual earnings by gender
           - Full-time workers aged 18-65
           - **High earners (£100k+):** Includes self-employed, business owners, and company directors from HMRC Self Assessment data
           
           **UK Salary Benchmarks (2024):**
           - National Living Wage (21+): £11.44/hour = £22,308/year (37.5hrs/wk) - [Gov.uk NLW Rates](https://www.gov.uk/national-minimum-wage-rates)
           - National Minimum Wage (18-20): £8.60/hour = £16,770/year
           - UK Median Salary: £31,285/year
           - UK Average (Mean) Salary: £33,000/year
           
           **High Income Distribution (HMRC Self Assessment 2022-23):**
           - £100k-£150k: ~1.5-2% (male), ~1.5% (female)
           - £150k-£250k: ~0.5-0.7% (male), ~0.3% (female)
           - £250k-£500k: ~0.3% (male), ~0.12% (female)
           - £500k-£1M: ~0.06% (male), ~0.02% (female)
           - £1M+: ~0.04% (male), ~0.01% (female)
           
           *Note: ASHE only captures PAYE employees. High earners often receive income through dividends, 
           capital gains, or business profits reported via Self Assessment. The combined ASHE + HMRC approach 
           provides a more complete picture of the income distribution, especially for entrepreneurs and 
           company directors who may underreport on traditional salary surveys.*
           
           *Income varies significantly by age, with peak earning in 45-54 age group*
        
        7. **Education Levels**
           - Source: [ONS Education and Training Statistics 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare)
           - Highest qualification attained by adults
        
        8. **Relationship Status**
           - Source: [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022)
           - Single rate: ~35% of UK adults are not in a relationship
        
        9. **Sexual Orientation**
           - Source: [ONS Sexual Orientation, UK 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality/bulletins/sexualidentityuk/2022)
           - Heterosexual/Straight: 93.2%, Gay/Lesbian: 1.5%, Bisexual: 1.7%
           - Data from adults aged 16+ in England and Wales
        
        10. **Children Distribution**
           - Source: [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022)
           - Percentage of adults by number of children
           - No children (43%), 1 child (18%), 2 children (24%), 3+ children (15%)
        
        11. **Marriage History**
           - Source: [ONS Marriage Statistics 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022)
           - Distribution by marital status: Never married (42%), Currently married (46%), Divorced (9%), Widowed (3%)
        
        12. **Male Pattern Baldness**
           - Source: [British Association of Dermatologists](https://www.bad.org.uk/) & [Academic Research on Androgenetic Alopecia](https://pubmed.ncbi.nlm.nih.gov/28396101/)
           - Age-dependent prevalence based on clinical studies
           - 18-29: 16%, 30-39: 32%, 40-49: 53%, 50-59: 63%, 60+: 80%
        
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
        - Uses combined data from ONS Annual Survey of Hours and Earnings (ASHE) + HMRC Self Assessment
        - ASHE captures PAYE employees (majority of workforce)
        - HMRC Self Assessment captures self-employed, business owners, and high earners receiving dividends/capital gains
        - Assumes uniform distribution within each income bracket
        - Gender-specific (males typically earn more on average)
        - Interpolates for specific income thresholds
        - **Minimum income filter:** Includes everyone earning AT OR ABOVE the selected threshold
        
        **6. Education Probability**
        - Direct lookup from ONS education attainment statistics
        - **Minimum education filter:** Selecting a level includes that level AND ALL HIGHER qualifications
        - Example: Selecting "GCSE" includes GCSE (23%) + A-Level (21%) + Undergraduate (27%) + Postgraduate (14%) = 85%
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
        - [ONS Population Estimates](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2022)
        - [ONS Census 2021 Ethnicity Data](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity/bulletins/ethnicgroupenglandandwales/census2021)
        - [NHS Health Survey for England 2021](https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england/2021)
        - [ONS Annual Survey of Hours and Earnings (ASHE)](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2023)
        - [HMRC Self Assessment Statistics](https://www.gov.uk/government/statistics/income-tax-liabilities-statistics-2020-to-2021) - High earner data
        - [ONS Sexual Orientation UK](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality/bulletins/sexualidentityuk/2022)
        - [ONS Families and Households](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022)
        
        ---
        *Last updated: December 2025*  
        *Calculator version: 1.0*
        """)
    
    # Marriage Statistics Section - Always Visible
    st.markdown("---")
    st.markdown("## 💍 UK Marriage & Relationship Statistics")
    st.caption("Comprehensive marriage, divorce, and relationship data for the UK (2022-2023)")
    
    st.info("**💡 Tip:** Use the calculator above first, then explore these statistics. When you calculate your dating pool, you'll see customized insights based on your criteria.")
    
    # Simple collapsible section for marriage stats
    with st.expander("📊 Explore Marriage Statistics", expanded=False):
        st.markdown("### Quick Facts")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Marriages (2022)", "249,793", help="England & Wales")
        with col2:
            st.metric("Opposite-Sex", "242,842", "97.2%")
        with col3:
            st.metric("Same-Sex", "6,951", "2.8%")
        
        st.markdown("---")
        st.markdown("""
        **For detailed marriage statistics including:**
        - Marriage trends over time
        - Age at marriage statistics
        - Divorce rates and reasons
        - Who initiates divorce
        - Remarriage statistics
        - Regional variations
        
        **👉 Use the calculator above and click the "💍 Marriage Statistics" tab in your results!**
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 1.2rem;'>
            <p>This calculator uses real UK statistics for educational purposes.</p>
            <p>Remember: Statistics don't define your worth or dating success. Taking Accountability and Responsibility in your Personality, and dating life is key!</p>
            <p>Find out what the type of person you want is looking for in return and be honest with yourself on whether you meet THEIR criteria.</p>

        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
