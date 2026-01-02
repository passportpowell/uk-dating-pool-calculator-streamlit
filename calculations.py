"""
UK Dating Pool Calculator - Calculations Module
Contains all probability calculation functions
"""

from scipy import stats
from data import (
    AGE_DISTRIBUTION, MALE_HEIGHT_MEAN, MALE_HEIGHT_STD,
    FEMALE_HEIGHT_MEAN, FEMALE_HEIGHT_STD, INCOME_DISTRIBUTION_MALE,
    INCOME_DISTRIBUTION_FEMALE, EDUCATION_DISTRIBUTION, ETHNICITY_DISTRIBUTION,
    BODY_TYPE_DISTRIBUTION_MALE, BODY_TYPE_DISTRIBUTION_FEMALE,
    CHILDREN_DISTRIBUTION, MARRIAGE_HISTORY, BALDNESS_BY_AGE,
    SEXUAL_ORIENTATION_DISTRIBUTION
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


def calculate_baldness_probability(baldness_preference, age_range):
    """Calculate probability of baldness preference match for males"""
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
            if user_gender and user_gender in ["Male", "Female"]:
                return straight_rate * 0.5 + gay_rate * 0.5 + bi_rate
            else:
                return straight_rate * 0.5 + gay_rate * 0.5 + bi_rate
        else:
            return bi_rate
    
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
