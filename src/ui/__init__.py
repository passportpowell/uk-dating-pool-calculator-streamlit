"""
UI Module - Streamlit User Interface Components

Contains all Streamlit-based UI rendering functions for different sections.
"""

from .sidebar import create_sidebar
from .results import display_results, display_probability_breakdown_tab, display_criteria_tab, display_map_tab
from .marriage_stats import display_marriage_statistics_tab
from .income_stats import display_income_demographics_tab
from .baby_stats import display_baby_statistics_tab

__all__ = [
    'create_sidebar',
    'display_results',
    'display_probability_breakdown_tab',
    'display_criteria_tab',
    'display_map_tab',
    'display_marriage_statistics_tab',
    'display_income_demographics_tab',
    'display_baby_statistics_tab'
]
