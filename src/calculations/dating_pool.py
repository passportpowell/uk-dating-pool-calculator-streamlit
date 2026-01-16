"""
UK Dating Pool Calculator - Calculations Module
Contains all probability calculation functions
"""

from scipy import stats
from src.data.constants import (
    AGE_DISTRIBUTION, MALE_HEIGHT_MEAN, MALE_HEIGHT_STD,
    FEMALE_HEIGHT_MEAN, FEMALE_HEIGHT_STD, INCOME_DISTRIBUTION_MALE,
    INCOME_DISTRIBUTION_FEMALE, EDUCATION_DISTRIBUTION, ETHNICITY_DISTRIBUTION,
    BODY_TYPE_DISTRIBUTION_MALE, BODY_TYPE_DISTRIBUTION_FEMALE,
    CHILDREN_DISTRIBUTION, MARRIAGE_HISTORY, BALDNESS_BY_AGE,
    SEXUAL_ORIENTATION_DISTRIBUTION, SELF_EMPLOYMENT_RATE_BY_AGE_GENDER,
    SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE, SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE
)


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
        (1000000, 10000000, income_dist["£1M+"])
    ]
    
    probability = 0
    for bracket_low, bracket_high, pct in income_brackets:
        if min_income <= bracket_low:
            # Entire bracket is at or above minimum, include all of it
            probability += pct
        elif min_income < bracket_high:
            # min_income falls within this bracket, prorate
            bracket_width = bracket_high - bracket_low
            included_width = bracket_high - min_income
            probability += pct * (included_width / bracket_width)
    
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


def calculate_self_employed_income_probability(min_income, gender):
    """Calculate probability self-employed person earns at or above minimum income"""
    income_dist = SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE if gender == "Male" else SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE
    
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
        (1000000, 10000000, income_dist["£1M+"])
    ]
    
    probability = 0
    for bracket_low, bracket_high, pct in income_brackets:
        if min_income <= bracket_low:
            probability += pct
        elif min_income < bracket_high:
            bracket_width = bracket_high - bracket_low
            included_width = bracket_high - min_income
            probability += pct * (included_width / bracket_width)
    
    return probability


def get_self_employment_rate_by_age(age_min, age_max):
    """Calculate self-employment rate for age range (weighted average across gender)"""
    from src.data.constants import GENDER_SPLIT
    
    total_years = 0
    weighted_rate = 0.0
    
    for age_band, rates_by_gender in SELF_EMPLOYMENT_RATE_BY_AGE_GENDER.items():
        if age_band == "65+":
            band_min, band_max = 65, 99
        else:
            band_min, band_max = map(int, age_band.split('-'))
        
        overlap_min = max(age_min, band_min)
        overlap_max = min(age_max, band_max)
        
        if overlap_max >= overlap_min:
            years = overlap_max - overlap_min + 1
            total_years += years
            # Blend male and female rates
            blended_rate = (rates_by_gender["Male"] * GENDER_SPLIT["Male"] + 
                          rates_by_gender["Female"] * GENDER_SPLIT["Female"])
            weighted_rate += blended_rate * years
    
    if total_years == 0:
        return 0.0
    return weighted_rate / total_years


def get_self_employment_rate_by_age_gender(age_min, age_max, gender):
    """Calculate self-employment rate for specific age range and gender"""
    total_years = 0
    weighted_rate = 0.0
    
    for age_band, rates_by_gender in SELF_EMPLOYMENT_RATE_BY_AGE_GENDER.items():
        if age_band == "65+":
            band_min, band_max = 65, 99
        else:
            band_min, band_max = map(int, age_band.split('-'))
        
        overlap_min = max(age_min, band_min)
        overlap_max = min(age_max, band_max)
        
        if overlap_max >= overlap_min:
            years = overlap_max - overlap_min + 1
            total_years += years
            weighted_rate += rates_by_gender.get(gender, 0.1) * years
    
    if total_years == 0:
        return 0.0
    return weighted_rate / total_years


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


def calculate_marriage_probability(acceptable_marriage_history, user_gender, looking_for_gender, user_orientation):
    """Calculate probability someone has acceptable marriage history
    
    Args:
        acceptable_marriage_history: List of acceptable marriage statuses
        user_gender: Gender of the user ("Male" or "Female")
        looking_for_gender: Gender being sought ("Male", "Female", or "Any")
        user_orientation: Sexual orientation of user
    
    Returns:
        Probability (0-1) that someone matches the marriage criteria
    """
    # Determine which marriage statistics to use based on orientation
    orientation_key = "opposite-sex"
    
    if user_orientation == "Gay or Lesbian":
        if (user_gender == "Male" and looking_for_gender == "Male") or \
           (user_gender == "Female" and looking_for_gender == "Female"):
            orientation_key = "same-sex"
    elif user_orientation == "Bisexual":
        if (user_gender == "Male" and looking_for_gender == "Male") or \
           (user_gender == "Female" and looking_for_gender == "Female"):
            orientation_key = "same-sex"
        elif looking_for_gender == "Any":
            prob_opposite = sum(MARRIAGE_HISTORY["opposite-sex"][status] for status in acceptable_marriage_history)
            prob_same = sum(MARRIAGE_HISTORY["same-sex"][status] for status in acceptable_marriage_history)
            return (prob_opposite + prob_same) / 2
    
    probability = 0
    for status in acceptable_marriage_history:
        probability += MARRIAGE_HISTORY[orientation_key][status]
    return probability


def calculate_baldness_probability(baldness_preference, age_range, target_gender=None):
    """
    Calculate probability of baldness preference match.
    
    NOTE: Baldness is only relevant for male targets (applies to men).
    For female targets, return 1.0 (no filtering).
    """
    # Only apply baldness filter if target is male
    if target_gender == "Female":
        return 1.0
    
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
    
    # If looking for any gender - blend compatible orientations for all user orientations
    if looking_for_gender == "Any":
        if user_orientation == "Heterosexual/Straight":
            # Straight user can date any gender: match with straight + all bi
            return straight_rate + bi_rate
        elif user_orientation == "Gay or Lesbian":
            # Gay user can date any gender (of their orientation): match with gay + all bi
            return gay_rate + bi_rate
        elif user_orientation == "Bisexual":
            # Bisexual user can date any gender: match with all orientations
            return 1.0  # All orientations are compatible with bisexual
        else:
            return 1.0
    
    # For specific gender selection
    if user_orientation == "Heterosexual/Straight":
        if user_gender == "Male" and looking_for_gender == "Male":
            return bi_rate
        elif user_gender == "Female" and looking_for_gender == "Female":
            return bi_rate
        else:
            return straight_rate + bi_rate
    
    elif user_orientation == "Gay or Lesbian":
        if user_gender == "Male" and looking_for_gender == "Female":
            return bi_rate
        elif user_gender == "Female" and looking_for_gender == "Male":
            return bi_rate
        else:
            return gay_rate + bi_rate
    
    elif user_orientation == "Bisexual":
        if user_gender == "Male":
            if looking_for_gender == "Male":
                return gay_rate + bi_rate
            elif looking_for_gender == "Female":
                return straight_rate + bi_rate
        elif user_gender == "Female":
            if looking_for_gender == "Female":
                return gay_rate + bi_rate
            elif looking_for_gender == "Male":
                return straight_rate + bi_rate
        else:
            return straight_rate + gay_rate + bi_rate
    
    return 1.0


# ============================================================================
# NEW ACCURATE CALCULATION PIPELINE (v2)
# ============================================================================
# These functions implement the proper population pipeline:
# Adults -> Employed -> Single -> Income threshold
# This accounts for ASHE coverage (employees only) and realistic rates by age

def get_single_rate_by_age(age_min, age_max):
    """
    Get single rate for a specific age range, weighted by years in range.
    Source: ONS Families & Households 2022
    """
    from src.data.constants import SINGLE_RATE_BY_AGE
    
    total_years = 0
    weighted_sum = 0.0
    
    for age_range, single_rate in SINGLE_RATE_BY_AGE.items():
        range_min, range_max = map(int, age_range.split('-')) if '-' in age_range else (int(age_range.replace('+', '')), 99)
        
        overlap_min = max(age_min, range_min)
        overlap_max = min(age_max, range_max)
        
        if overlap_max >= overlap_min:
            years = overlap_max - overlap_min + 1
            total_years += years
            weighted_sum += years * single_rate
    
    if total_years == 0:
        return 0.35  # fallback to overall rate
    return weighted_sum / total_years


def get_employment_rate_by_age_gender(age_min, age_max, gender):
    """
    Get employment rate for a specific age range and gender.
    Source: ONS Labour Force Survey 2023
    """
    from src.data.constants import EMPLOYMENT_RATE_BY_AGE_GENDER
    
    total_years = 0
    weighted_sum = 0.0
    
    for age_range, rates in EMPLOYMENT_RATE_BY_AGE_GENDER.items():
        range_min, range_max = map(int, age_range.split('-')) if '-' in age_range else (int(age_range.replace('+', '')), 99)
        
        overlap_min = max(age_min, range_min)
        overlap_max = min(age_max, range_max)
        
        if overlap_max >= overlap_min:
            years = overlap_max - overlap_min + 1
            total_years += years
            weighted_sum += years * rates.get(gender, 0.70)  # fallback to ~70% if not found
    
    if total_years == 0:
        return 0.70  # fallback to ~70% employment
    return weighted_sum / total_years


def calculate_population_pipeline(age_min, age_max, gender, ethnicity_list, uk_adult_pop):
    """
    Calculate population through the proper pipeline:
    Adults -> Employed -> Single -> Ready for income filter
    
    Returns: {
        'total_adults': int,
        'employed': int,
        'employed_pct': float,
        'single_employed': int,
        'single_employed_pct': float,
    }
    
    This approach:
    - Only applies income data to employed population (matches ASHE denominator)
    - Uses age-band-specific single rates (not flat 35%)
    - Transparent about each filtering stage
    - Maintains float precision through stages, rounds at end
    """
    from src.data.constants import ETHNICITY_DISTRIBUTION, GENDER_SPLIT, AGE_DISTRIBUTION
    
    # Stage 1: Calculate age share
    age_share = calculate_age_probability(age_min, age_max)
    
    # Stage 2: Calculate ethnicity share
    if ethnicity_list:
        ethnicity_share = sum(ETHNICITY_DISTRIBUTION.get(e, 0) for e in ethnicity_list)
        if ethnicity_share <= 0:
            # Fail loudly if no matching ethnicities found
            raise ValueError(f"No matching ethnicities found. Selected: {ethnicity_list}")
    else:
        ethnicity_share = 1.0  # All ethnicities
    
    # Stage 3: Calculate gender share and employment rate
    if gender == "Any":
        # Blend male and female: use weighted average of employment rates
        male_employ_rate = get_employment_rate_by_age_gender(age_min, age_max, "Male")
        female_employ_rate = get_employment_rate_by_age_gender(age_min, age_max, "Female")
        # Weight by gender split: male 49.2%, female 50.8%
        employment_rate = (male_employ_rate * GENDER_SPLIT["Male"]) + (female_employ_rate * GENDER_SPLIT["Female"])
        gender_share = 1.0
    else:
        gender_share = GENDER_SPLIT.get(gender, 0.5)
        employment_rate = get_employment_rate_by_age_gender(age_min, age_max, gender)
    
    # Total adults in this demographic (keep as float for precision)
    total_adults_float = uk_adult_pop * age_share * ethnicity_share * gender_share
    
    # Stage 4: Apply employment rate (keep as float)
    employed_float = total_adults_float * employment_rate
    employed_pct = employment_rate * 100
    
    # Stage 5: Apply single rate (age-specific, keep as float)
    single_rate = get_single_rate_by_age(age_min, age_max)
    single_employed_float = employed_float * single_rate
    single_employed_pct = single_rate * 100
    
    # Round to integers only at final output
    return {
        'total_adults': int(round(total_adults_float)),
        'employed': int(round(employed_float)),
        'employed_pct': employed_pct,
        'single_employed': int(round(single_employed_float)),
        'single_employed_pct': single_employed_pct,
    }
