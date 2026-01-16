"""
Calculations Module - Core Mathematical Functions

Contains all probability calculations and demographic analysis functions.
"""

from .dating_pool import (
    cm_to_feet_inches,
    feet_inches_to_cm,
    calculate_age_probability,
    calculate_height_probability,
    calculate_income_probability,
    calculate_education_probability,
    calculate_ethnicity_probability,
    calculate_body_type_probability,
    calculate_children_probability,
    calculate_marriage_probability,
    calculate_orientation_probability,
    calculate_baldness_probability,
    calculate_self_employed_income_probability
)

__all__ = [
    'cm_to_feet_inches',
    'feet_inches_to_cm',
    'calculate_age_probability',
    'calculate_height_probability',
    'calculate_income_probability',
    'calculate_education_probability',
    'calculate_ethnicity_probability',
    'calculate_body_type_probability',
    'calculate_children_probability',
    'calculate_marriage_probability',
    'calculate_orientation_probability',
    'calculate_baldness_probability',
    'calculate_self_employed_income_probability'
]
