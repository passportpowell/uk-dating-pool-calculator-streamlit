"""
UK Cost of Living Calculator - Family Lifestyle Calculator
Calculate the annual household income required to maintain a specific lifestyle
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.utils.styles import CUSTOM_CSS

# Page configuration
st.set_page_config(
    page_title="Cost of Living Calculator - UK Dating Statistics",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">💰 Cost of Living Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Calculate the annual household income needed to support your lifestyle goals</div>', unsafe_allow_html=True)

# UK Regional Cost Data (2024-2026 estimates)
# Sources: ONS House Price Index (2024), Rightmove (Q4 2024), Zoopla (2024)
REGIONAL_COSTS = {
    "London": {
        "avg_house_price": 535000,
        "avg_rent_monthly": 2200,
        "cost_multiplier": 1.4,
        "avg_property_deposit": 50000  # Helping children deposit
    },
    "South East": {
        "avg_house_price": 425000,
        "avg_rent_monthly": 1650,
        "cost_multiplier": 1.25,
        "avg_property_deposit": 50000
    },
    "South West": {
        "avg_house_price": 360000,
        "avg_rent_monthly": 1400,
        "cost_multiplier": 1.15,
        "avg_property_deposit": 50000
    },
    "East of England": {
        "avg_house_price": 395000,
        "avg_rent_monthly": 1550,
        "cost_multiplier": 1.2,
        "avg_property_deposit": 50000
    },
    "West Midlands": {
        "avg_house_price": 285000,
        "avg_rent_monthly": 1150,
        "cost_multiplier": 1.0,
        "avg_property_deposit": 50000
    },
    "East Midlands": {
        "avg_house_price": 265000,
        "avg_rent_monthly": 1050,
        "cost_multiplier": 0.95,
        "avg_property_deposit": 50000
    },
    "North West": {
        "avg_house_price": 245000,
        "avg_rent_monthly": 1100,
        "cost_multiplier": 0.95,
        "avg_property_deposit": 50000
    },
    "Yorkshire and Humber": {
        "avg_house_price": 235000,
        "avg_rent_monthly": 1000,
        "cost_multiplier": 0.9,
        "avg_property_deposit": 50000
    },
    "North East": {
        "avg_house_price": 185000,
        "avg_rent_monthly": 850,
        "cost_multiplier": 0.85,
        "avg_property_deposit": 50000
    },
    "Scotland": {
        "avg_house_price": 205000,
        "avg_rent_monthly": 1050,
        "cost_multiplier": 0.95,
        "avg_property_deposit": 50000
    },
    "Wales": {
        "avg_house_price": 225000,
        "avg_rent_monthly": 950,
        "cost_multiplier": 0.9,
        "avg_property_deposit": 50000
    },
    "Northern Ireland": {
        "avg_house_price": 195000,
        "avg_rent_monthly": 900,
        "cost_multiplier": 0.85,
        "avg_property_deposit": 50000
    }
}

# Education costs (annual, 2024-2026 estimates)
# Sources: ISC Census (2025), gov.uk, Coram Childcare Survey (2025)
EDUCATION_COSTS = {
    "nursery_public": 0,  # Free for 15-30 hours/week
    "nursery_private": 8000,  # Full-time private nursery (~£160/week)
    "public_primary": 0,  # Free state education
    "public_secondary": 0,  # Free state education
    "private_primary": 15000,  # Average per year
    "private_secondary": 18000,  # Average per year
    "private_boarding_primary": 32000,  # Boarding school
    "private_boarding_secondary": 40000,  # Boarding school
}

# University costs (per year, 2025-2026)
# Sources: gov.uk (2025), Student Finance England (2025/26)
UNIVERSITY_COSTS = {
    "tuition_fees": 9250,  # Maximum annual tuition 2025/26
    "maintenance_london": 13348,  # Living costs in London
    "maintenance_outside_london": 10227,  # Living costs outside London
    "total_3_year_degree": 58000  # Approximate total for 3 years
}

# Car costs (annual, 2025-2026 estimates) - EXCLUDING depreciation
# Sources: AA Motoring Costs (2025), RAC Report (2024), Nimblefins (2025)
# Based on 6,000 miles per year per car (UK median for non-driving jobs)
CAR_COSTS = {
    "small_car": {
        "insurance": 450,  # UK median comprehensive
        "fuel": 600,  # 6,000 miles @ 50mpg, £1.45/litre
        "tax": 190,  # VED Band B-C
        "mot_service": 250,  # MOT £55 + service £200
        "repairs": 300,  # Average annual repairs/tyres
    },
    "medium_car": {
        "insurance": 550,
        "fuel": 800,  # 6,000 miles @ 40mpg
        "tax": 190,
        "mot_service": 300,
        "repairs": 400,
    },
    "large_car": {
        "insurance": 700,
        "fuel": 1100,  # 6,000 miles @ 32mpg
        "tax": 190,
        "mot_service": 350,
        "repairs": 500,
    },
    "electric": {
        "insurance": 600,
        "fuel": 200,  # Electricity for 6,000 miles
        "tax": 0,  # Currently exempt
        "mot_service": 200,  # Lower service costs
        "repairs": 250,
    }
}

# Basic household costs (annual, per person)
# Sources: ONS Family Spending Survey (FYE 2024), Living Costs and Food Survey (2024)
BASE_LIVING_COSTS = {
    "food_per_person": 2600,  # £217/month per person
    "utilities_base": 2400,  # Gas, electric, water, council tax (£200/month)
    "clothing_per_person": 800,  # £67/month per person
    "healthcare_per_person": 350,  # NHS extras: prescriptions, dental, opticians
    "entertainment_per_person": 900,  # Excludes holidays (£75/month)
    "household_goods": 1200,  # Furniture, appliances, repairs (£100/month)
    "insurance_base": 800,  # Home/contents insurance (£67/month)
}

# Communications costs - varies by household size
# Sources: Ofcom Communications Market Report (2024)
COMMUNICATIONS_COSTS = {
    "broadband": 360,  # £30/month average UK broadband
    "adult_mobile": 120,  # £10/month per adult SIM-only
    "teen_mobile": 96,  # £8/month for 14+ teens
}

# Childcare baselines (hourly, 2025-2026)
# Sources: Coram Family & Childcare Survey (2025), Ofsted (2024)
CHILDCARE_BASE = {
    "under5_hourly": 7.50,  # Median UK hourly nursery/childminder cost
    "school_age_hourly": 5.50,  # Wraparound / after-school club median
    "weeks_per_year": 48  # Paid weeks per year after holidays
}

# Activities for children (per session)
# Sources: Sport England (2024), ISM Music Lessons Survey (2024)
ACTIVITY_COSTS = {
    "per_session": 10,  # Median: clubs £8-12, sports £10-15, music £15-20
    "weeks_per_year": 38  # School term weeks
}

# Holidays / trips baselines (per trip)
# Sources: ABTA Holiday Habits (2025), ONS Travel Trends (2024)
HOLIDAY_COSTS = {
    "per_adult_trip": 650,  # Median blend domestic/international
    "per_child_trip": 400  # Children cost ~60% of adult
}

# Retirement calculations
# Source: PLSA Retirement Living Standards (2025), Money Helper (2025)
RETIREMENT_NEEDS = {
    "minimum_single": 14400,  # Minimum Living Standard per year
    "moderate_single": 31300,  # Moderate Living Standard per year
    "comfortable_single": 43100,  # Comfortable Living Standard per year
    "minimum_couple": 22400,
    "moderate_couple": 43100,
    "comfortable_couple": 59000
}

def calculate_communications_cost(num_parents, child_ages):
    """Calculate communications costs including phones for teenagers"""
    cost = COMMUNICATIONS_COSTS["broadband"]
    cost += num_parents * COMMUNICATIONS_COSTS["adult_mobile"]
    # Add mobile for children 14+
    teens = sum(1 for age in child_ages if age >= 14)
    cost += teens * COMMUNICATIONS_COSTS["teen_mobile"]
    return cost, teens

def calculate_housing_costs(
    region,
    ownership_status,
    household_size,
    home_price=None,
    deposit_percent=20,
    mortgage_rate=0.05,
    custom_rent=None,
    planning_to_buy=False,
    years_until_purchase=5
):
    """Calculate annual housing costs with option to save for future purchase"""
    regional_data = REGIONAL_COSTS[region]
    
    chosen_price = home_price if home_price and home_price > 0 else regional_data["avg_house_price"]
    deposit_ratio = deposit_percent / 100
    
    annual_housing = 0
    deposit_savings = 0
    
    if ownership_status == "Own with mortgage":
        mortgage = chosen_price * (1 - deposit_ratio)
        monthly_rate = mortgage_rate / 12
        term_months = 25 * 12
        monthly_payment = (mortgage * monthly_rate) / (1 - (1 + monthly_rate) ** (-term_months))
        annual_housing = monthly_payment * 12
        annual_housing += 2000  # Maintenance, repairs, insurance
    elif ownership_status == "Renting":
        rent_monthly = custom_rent if custom_rent and custom_rent > 0 else regional_data["avg_rent_monthly"]
        annual_housing = rent_monthly * 12
        
        # If planning to buy, calculate deposit savings
        if planning_to_buy and years_until_purchase > 0:
            target_deposit = chosen_price * deposit_ratio
            # Calculate annual savings needed (3% growth assumption)
            if years_until_purchase > 1:
                deposit_savings = target_deposit / ((1.03**years_until_purchase - 1) / 0.03)
            else:
                deposit_savings = target_deposit
    else:  # Own outright
        annual_housing = 2000  # Maintenance and insurance only
    
    return annual_housing, deposit_savings

def calculate_car_costs(cars_per_household, car_type, child_ages=[], children_with_cars=0):
    """Calculate annual car costs WITHOUT depreciation, including children 18+ with cars"""
    # Count children 18+ who have cars
    total_cars = cars_per_household + children_with_cars
    
    if total_cars == 0:
        return 0, {}
    
    if car_type == "Small car":
        costs = CAR_COSTS["small_car"]
    elif car_type == "Medium car":
        costs = CAR_COSTS["medium_car"]
    elif car_type == "Large/SUV":
        costs = CAR_COSTS["large_car"]
    else:  # Electric
        costs = CAR_COSTS["electric"]
    
    cost_per_car = sum(costs.values())
    total_cost = cost_per_car * cars_per_household
    
    # Add costs for children's cars (assume small cars)
    if children_with_cars > 0:
        child_car_cost = sum(CAR_COSTS["small_car"].values())
        total_cost += child_car_cost * children_with_cars
    
    return total_cost, costs

def calculate_childcare_costs(child_ages, hours_under5, hours_school_age, region, rate_under5=None, rate_school=None):
    """Calculate annual childcare costs using regional multipliers"""
    multiplier = REGIONAL_COSTS[region]["cost_multiplier"]
    rate_u5 = (rate_under5 if rate_under5 and rate_under5 > 0 else CHILDCARE_BASE["under5_hourly"]) * multiplier
    rate_school = (rate_school if rate_school and rate_school > 0 else CHILDCARE_BASE["school_age_hourly"]) * multiplier

    under5_count = sum(1 for age in child_ages if age < 5)
    school_age_count = sum(1 for age in child_ages if 5 <= age <= 11)

    annual_under5 = under5_count * hours_under5 * rate_u5 * CHILDCARE_BASE["weeks_per_year"]
    annual_school = school_age_count * hours_school_age * rate_school * CHILDCARE_BASE["weeks_per_year"]

    return annual_under5 + annual_school, {
        "under5_hourly": rate_u5,
        "school_hourly": rate_school,
        "under5_children": under5_count,
        "school_children": school_age_count,
        "median_under5": CHILDCARE_BASE["under5_hourly"],
        "median_school": CHILDCARE_BASE["school_age_hourly"]
    }

def calculate_nursery_costs(child_ages, school_type):
    """Calculate nursery costs for under-5s (separate from childcare)"""
    under5_count = sum(1 for age in child_ages if age < 5)
    if under5_count == 0:
        return 0
    
    if school_type in ["Private (Day)", "Private (Boarding)"]:
        return under5_count * EDUCATION_COSTS["nursery_private"]
    else:
        return 0  # Free 15-30 hours for state nursery

def calculate_school_costs(child_ages, school_type):
    """Calculate school costs for children 5-18 (excludes nursery)"""
    total_cost = 0
    
    for age in child_ages:
        if age >= 5 and age <= 11:
            # Primary school
            if school_type == "Private (Day)":
                total_cost += EDUCATION_COSTS["private_primary"]
            elif school_type == "Private (Boarding)":
                total_cost += EDUCATION_COSTS["private_boarding_primary"]
            # Public is free
        elif age >= 12 and age <= 18:
            # Secondary school
            if school_type == "Private (Day)":
                total_cost += EDUCATION_COSTS["private_secondary"]
            elif school_type == "Private (Boarding)":
                total_cost += EDUCATION_COSTS["private_boarding_secondary"]
            # Public is free
    
    return total_cost

def calculate_child_activities_cost(child_ages, activities_per_week, cost_per_session, weeks_per_year):
    """Calculate annual activities cost per child"""
    if activities_per_week <= 0 or cost_per_session <= 0:
        return 0
    num_children = len(child_ages)
    return num_children * activities_per_week * cost_per_session * weeks_per_year

def calculate_holiday_cost(num_parents, num_children, holidays_per_year, cost_per_adult_trip, cost_per_child_trip):
    """Calculate holiday costs per year"""
    if holidays_per_year <= 0:
        return 0
    return holidays_per_year * (
        num_parents * cost_per_adult_trip + num_children * cost_per_child_trip
    )

def calculate_university_costs(num_children, pay_for_uni, region):
    """Calculate university support costs per child in university"""
    if not pay_for_uni:
        return 0
    
    if region == "London":
        annual_per_child = UNIVERSITY_COSTS["tuition_fees"] + UNIVERSITY_COSTS["maintenance_london"] * 0.5
    else:
        annual_per_child = UNIVERSITY_COSTS["tuition_fees"] + UNIVERSITY_COSTS["maintenance_outside_london"] * 0.5
    
    return annual_per_child

def calculate_home_deposit_savings(num_children, help_deposit, deposit_amount_per_child, years_until_needed):
    """Calculate annual savings needed for children's home deposits"""
    if not help_deposit or years_until_needed <= 0:
        return 0
    
    total_needed = deposit_amount_per_child * num_children
    
    # Annual savings required (assuming 3% investment growth)
    if years_until_needed > 1:
        annual_savings = total_needed / ((1.03**years_until_needed - 1) / 0.03)
    else:
        annual_savings = total_needed
    
    return annual_savings

def calculate_base_living_costs(household_size, region, child_ages, num_parents):
    """Calculate basic living costs for household"""
    multiplier = REGIONAL_COSTS[region]["cost_multiplier"]
    
    total = 0
    total += BASE_LIVING_COSTS["food_per_person"] * household_size * multiplier
    total += BASE_LIVING_COSTS["utilities_base"] * multiplier
    total += BASE_LIVING_COSTS["clothing_per_person"] * household_size * multiplier
    total += BASE_LIVING_COSTS["healthcare_per_person"] * household_size * multiplier
    total += BASE_LIVING_COSTS["entertainment_per_person"] * household_size * multiplier
    total += BASE_LIVING_COSTS["household_goods"] * multiplier
    total += BASE_LIVING_COSTS["insurance_base"] * multiplier
    
    # Communications varies by household
    comms_cost, teens = calculate_communications_cost(num_parents, child_ages)
    total += comms_cost
    
    return total, comms_cost, teens

def calculate_retirement_savings(parent_age_1, parent_age_2, retirement_lifestyle, current_pension_pot):
    """Calculate annual retirement savings needed and how long money will last"""
    retirement_age = 67  # UK state pension age
    
    # Years until retirement (average of both parents)
    avg_parent_age = (parent_age_1 + parent_age_2) / 2 if parent_age_2 > 0 else parent_age_1
    years_to_retirement = max(retirement_age - avg_parent_age, 0)
    
    if years_to_retirement <= 0:
        return 0, 0, 0  # Already retired
    
    # Target pension pot based on lifestyle
    if retirement_lifestyle == "Minimum":
        annual_need = RETIREMENT_NEEDS["minimum_couple"] if parent_age_2 > 0 else RETIREMENT_NEEDS["minimum_single"]
    elif retirement_lifestyle == "Moderate":
        annual_need = RETIREMENT_NEEDS["moderate_couple"] if parent_age_2 > 0 else RETIREMENT_NEEDS["moderate_single"]
    else:  # Comfortable
        annual_need = RETIREMENT_NEEDS["comfortable_couple"] if parent_age_2 > 0 else RETIREMENT_NEEDS["comfortable_single"]
    
    # Calculate required pension pot (using 4% withdrawal rate)
    required_pot = annual_need * 25
    
    # Subtract state pension
    state_pension_annual = 11502 * (2 if parent_age_2 > 0 else 1)  # 2025/26 rate
    state_pension_pot_equivalent = state_pension_annual * 25
    
    remaining_needed = max(required_pot - current_pension_pot - state_pension_pot_equivalent, 0)
    
    # Annual savings needed (assuming 5% investment growth)
    if years_to_retirement > 0:
        annual_savings = remaining_needed / ((1.05**years_to_retirement - 1) / 0.05)
    else:
        annual_savings = 0
    
    # Calculate how long current pot would last (4% withdrawal)
    years_money_lasts = (current_pension_pot + state_pension_pot_equivalent) / annual_need if annual_need > 0 else 0
    
    return annual_savings, years_money_lasts, state_pension_annual

def calculate_emergency_savings(monthly_expenses, emergency_months):
    """Calculate emergency fund target"""
    return (monthly_expenses * emergency_months) / 10  # Spread over 10 years

# Sidebar inputs
st.sidebar.header("Family Details")

# Parent ages
col1, col2 = st.sidebar.columns(2)
with col1:
    parent1_age = st.number_input("Parent 1 Age", min_value=18, max_value=80, value=35)
with col2:
    parent2_age = st.number_input("Parent 2 Age (0 if single)", min_value=0, max_value=80, value=33)

num_parents = 2 if parent2_age > 0 else 1

# Children
num_children = st.sidebar.number_input("Number of Children", min_value=0, max_value=10, value=2)

child_ages = []
# Defaults for childcare/activities
hours_under5 = 0
hours_school_age = 0
custom_under5_rate = 0.0
custom_school_rate = 0.0
activities_per_week = 0
cost_per_activity = ACTIVITY_COSTS["per_session"]
activity_weeks = ACTIVITY_COSTS["weeks_per_year"]

if num_children > 0:
    st.sidebar.subheader("Children's Ages")
    cols = st.sidebar.columns(min(num_children, 3))
    for i in range(num_children):
        col_idx = i % 3
        with cols[col_idx]:
            age = st.number_input(f"Child {i+1}", min_value=0, max_value=25, value=min(5 + i*2, 15), key=f"child_{i}")
            child_ages.append(age)

    # Childcare
    st.sidebar.header("Childcare (paid hours)")
    hours_under5 = st.sidebar.number_input(f"Hours/week for under 5s (0 = use free entitlement only, median paid: {CHILDCARE_BASE['under5_hourly']:.2f}/hr)", min_value=0, max_value=60, value=0, step=1)
    hours_school_age = st.sidebar.number_input(f"Hours/week for 5-11 wraparound (0 = none, median: £{CHILDCARE_BASE['school_age_hourly']:.2f}/hr)", min_value=0, max_value=30, value=0, step=1)
    if hours_under5 > 0:
        custom_under5_rate = st.sidebar.number_input(
            f"Under 5 hourly rate (£, 0 = use median £{CHILDCARE_BASE['under5_hourly']:.2f}/hr)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=0.5
        )
    if hours_school_age > 0:
        custom_school_rate = st.sidebar.number_input(
            f"School-age hourly rate (£, 0 = use median £{CHILDCARE_BASE['school_age_hourly']:.2f}/hr)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=0.5
        )

    # Activities
    st.sidebar.header("Child Activities")
    activities_per_week = st.sidebar.slider("Activities per child per week", min_value=0, max_value=7, value=1)
    cost_per_activity = st.sidebar.number_input(
        f"Cost per activity session (£, median: £{ACTIVITY_COSTS['per_session']})",
        min_value=0,
        max_value=200,
        value=ACTIVITY_COSTS["per_session"],
        step=1
    )
    activity_weeks = st.sidebar.slider("Weeks per year for activities", min_value=0, max_value=52, value=ACTIVITY_COSTS["weeks_per_year"])

# Location
st.sidebar.header("Location & Housing")
region = st.sidebar.selectbox(
    "Region",
    list(REGIONAL_COSTS.keys())
)

ownership_status = st.sidebar.selectbox(
    "Current Housing Status",
    ["Own with mortgage", "Renting", "Own outright"]
)

# Housing detail inputs
use_custom_home_price = False
home_price = 0
custom_rent = 0
planning_to_buy = False
years_until_purchase = 0

if ownership_status != "Renting":
    use_custom_home_price = st.sidebar.checkbox("Use custom home price", value=False)
    home_price = st.sidebar.number_input(
        f"Home purchase price (£) (0 = use regional avg £{REGIONAL_COSTS[region]['avg_house_price']:,})",
        min_value=0,
        max_value=3000000,
        value=0 if not use_custom_home_price else REGIONAL_COSTS[region]["avg_house_price"],
        step=5000
    )
    deposit_percent = st.sidebar.slider("Deposit (%)", min_value=5, max_value=50, value=20, step=1)
    mortgage_rate = st.sidebar.slider("Mortgage interest rate (%)", min_value=2.0, max_value=8.0, value=5.0, step=0.1) / 100
else:
    custom_rent = st.sidebar.number_input(
        f"Monthly rent (£) (0 = use regional avg £{REGIONAL_COSTS[region]['avg_rent_monthly']:,})",
        min_value=0,
        max_value=5000,
        value=0,
        step=50
    )
    planning_to_buy = st.sidebar.checkbox("Planning to buy a home in future?", value=False)
    if planning_to_buy:
        years_until_purchase = st.sidebar.slider("Years until purchase", min_value=1, max_value=15, value=5)
        use_custom_home_price = st.sidebar.checkbox("Use custom target home price", value=False)
        home_price = st.sidebar.number_input(
            f"Target home price (£) (0 = use regional avg £{REGIONAL_COSTS[region]['avg_house_price']:,})",
            min_value=0,
            max_value=3000000,
            value=0 if not use_custom_home_price else REGIONAL_COSTS[region]["avg_house_price"],
            step=5000
        )
        deposit_percent = st.sidebar.slider("Target deposit (%)", min_value=5, max_value=50, value=20, step=1)
        mortgage_rate = 0.05
    else:
        deposit_percent = 0
        mortgage_rate = 0.05

# Education
st.sidebar.header("Education Preferences")
school_type = st.sidebar.selectbox(
    "School Type (5-18 years)",
    ["Public (State)", "Private (Day)", "Private (Boarding)"]
)

pay_for_university = st.sidebar.checkbox(f"Pay for children's university degrees (median: £{UNIVERSITY_COSTS['tuition_fees']:,}/yr tuition)", value=True)

# Children's first home
help_with_deposit = st.sidebar.checkbox("Help children with first home deposit", value=True)
if help_with_deposit and num_children > 0:
    deposit_per_child = st.sidebar.number_input(
        "Deposit amount per child (£)",
        min_value=0,
        max_value=200000,
        value=50000,
        step=5000,
        help="How much you want to give each child towards their first home deposit (median UK first-time buyer deposit: £50,000)"
    )
    youngest_age = min(child_ages) if child_ages else 0
    years_until_deposit = max(25 - youngest_age, 5)  # Assume help when child is 25
    years_until_deposit = st.sidebar.slider(
        "Years until first child needs deposit",
        min_value=1,
        max_value=30,
        value=years_until_deposit
    )
else:
    deposit_per_child = 0
    years_until_deposit = 0

# Cars
st.sidebar.header("Transportation")
cars = st.sidebar.number_input("Parent cars in household", min_value=0, max_value=5, value=2)
if cars > 0:
    car_type = st.sidebar.selectbox(
        "Typical car type (parents)",
        ["Small car", "Medium car", "Large/SUV", "Electric"]
    )
else:
    car_type = "Small car"

# Check if any children are 18+
children_18_plus = sum(1 for age in child_ages if age >= 18) if num_children > 0 else 0
if children_18_plus > 0:
    children_with_cars = st.sidebar.number_input(
        f"Children (18+) with cars (max {children_18_plus})",
        min_value=0,
        max_value=children_18_plus,
        value=0,
        help="Children's cars assumed to be small cars"
    )
else:
    children_with_cars = 0

# Holidays
st.sidebar.header("Holidays & Trips")
holidays_per_year = st.sidebar.slider("Holidays per year", min_value=0, max_value=6, value=1)
holiday_cost_per_adult = st.sidebar.number_input(
    f"Cost per adult per trip (£) (median: £{HOLIDAY_COSTS['per_adult_trip']})",
    min_value=0,
    max_value=5000,
    value=HOLIDAY_COSTS["per_adult_trip"],
    step=50
)
holiday_cost_per_child = st.sidebar.number_input(
    f"Cost per child per trip (£) (median: £{HOLIDAY_COSTS['per_child_trip']})",
    min_value=0,
    max_value=5000,
    value=HOLIDAY_COSTS["per_child_trip"],
    step=50
)

# Retirement
st.sidebar.header("Retirement Planning")
retirement_lifestyle = st.sidebar.selectbox(
    "Target retirement lifestyle",
    ["Minimum", "Moderate", "Comfortable"]
)

current_pension_pot = st.sidebar.number_input(
    "Current pension pot (£)",
    min_value=0,
    max_value=5000000,
    value=50000,
    step=10000
)

# Savings
st.sidebar.header("Savings Goals")
target_savings = st.sidebar.number_input(
    "Target annual savings (£)",
    min_value=0,
    max_value=500000,
    value=5000,
    step=1000
)

emergency_fund_months = st.sidebar.slider(
    "Emergency fund (months of expenses)",
    min_value=0,
    max_value=12,
    value=6
)

calculate_button = st.sidebar.button("Calculate Required Income", type="primary")

# Main content
if calculate_button:
    household_size = num_parents + num_children
    
    # Calculate all costs
    housing_cost, future_deposit_savings = calculate_housing_costs(
        region,
        ownership_status,
        household_size,
        home_price=home_price if home_price > 0 else None,
        deposit_percent=deposit_percent,
        mortgage_rate=mortgage_rate,
        custom_rent=custom_rent if custom_rent > 0 else None,
        planning_to_buy=planning_to_buy,
        years_until_purchase=years_until_purchase
    )
    
    nursery_cost = calculate_nursery_costs(child_ages, school_type)
    school_cost = calculate_school_costs(child_ages, school_type)
    
    # University costs
    children_in_uni = sum(1 for age in child_ages if 18 <= age <= 21)
    university_cost = calculate_university_costs(children_in_uni, pay_for_university, region) * children_in_uni
    
    # Childcare and activities
    childcare_meta = {"under5_hourly": 0, "school_hourly": 0, "under5_children": 0, "school_children": 0}
    if num_children > 0:
        childcare_cost, childcare_meta = calculate_childcare_costs(
            child_ages,
            hours_under5,
            hours_school_age,
            region,
            custom_under5_rate,
            custom_school_rate
        )
    else:
        childcare_cost = 0
    activities_cost = calculate_child_activities_cost(child_ages, activities_per_week, cost_per_activity, activity_weeks)
    
    # Holidays
    holiday_cost = calculate_holiday_cost(num_parents, num_children, holidays_per_year, holiday_cost_per_adult, holiday_cost_per_child)
    
    # Children's home deposits
    home_deposit_savings = calculate_home_deposit_savings(num_children, help_with_deposit, deposit_per_child, years_until_deposit)
    
    # Cars
    car_cost, car_breakdown = calculate_car_costs(cars, car_type, child_ages, children_with_cars)
    
    # Living costs
    living_costs, comms_cost, teens_with_phones = calculate_base_living_costs(household_size, region, child_ages, num_parents)
    
    # Retirement
    retirement_savings, years_money_lasts, state_pension_annual = calculate_retirement_savings(parent1_age, parent2_age, retirement_lifestyle, current_pension_pot)
    
    # Calculate total monthly expenses for emergency fund
    monthly_expenses = (housing_cost + nursery_cost + school_cost + university_cost + car_cost + living_costs + childcare_cost + activities_cost + holiday_cost) / 12
    emergency_savings = calculate_emergency_savings(monthly_expenses, emergency_fund_months)
    
    # Total annual costs
    total_annual_cost = (
        housing_cost +
        future_deposit_savings +
        nursery_cost +
        school_cost +
        university_cost +
        childcare_cost +
        activities_cost +
        holiday_cost +
        home_deposit_savings +
        car_cost +
        living_costs +
        retirement_savings +
        target_savings +
        emergency_savings
    )
    
    # Display summary table
    st.markdown("---")
    st.header("📊 Cost Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Annual Cost", f"£{total_annual_cost:,.0f}")
    with col2:
        st.metric("Monthly Cost", f"£{total_annual_cost/12:,.0f}")
    with col3:
        gross_income_needed = total_annual_cost / 0.7
        st.metric("Required Gross Income", f"£{gross_income_needed:,.0f}")
    with col4:
        st.metric("After-tax Rate Needed", f"{(total_annual_cost/gross_income_needed)*100:.0f}%")
    
    # Detailed summary table
    st.subheader("Detailed Cost Breakdown Table")
    summary_data = {
        "Category": [],
        "Annual Cost": [],
        "Monthly Cost": [],
        "% of Total": []
    }
    
    categories = [
        ("Housing", housing_cost),
        ("Future Home Deposit Savings", future_deposit_savings),
        ("Nursery (Under 5s)", nursery_cost),
        ("School (5-18)", school_cost),
        ("University Support", university_cost),
        ("Paid Childcare (Non-School)", childcare_cost),
        ("Children's Activities", activities_cost),
        ("Holidays & Travel", holiday_cost),
        ("Transportation (Cars)", car_cost),
        ("Food & Groceries", BASE_LIVING_COSTS["food_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]),
        ("Utilities & Council Tax", BASE_LIVING_COSTS["utilities_base"] * REGIONAL_COSTS[region]["cost_multiplier"]),
        ("Communications", comms_cost),
        ("Clothing", BASE_LIVING_COSTS["clothing_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]),
        ("Healthcare", BASE_LIVING_COSTS["healthcare_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]),
        ("Entertainment", BASE_LIVING_COSTS["entertainment_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]),
        ("Household Goods", BASE_LIVING_COSTS["household_goods"] * REGIONAL_COSTS[region]["cost_multiplier"]),
        ("Insurance", BASE_LIVING_COSTS["insurance_base"] * REGIONAL_COSTS[region]["cost_multiplier"]),
        ("Children's Home Deposits", home_deposit_savings),
        ("Retirement Savings", retirement_savings),
        ("Emergency Fund Build", emergency_savings),
        ("Additional Savings", target_savings),
    ]
    
    for name, cost in categories:
        if cost > 0:
            summary_data["Category"].append(name)
            summary_data["Annual Cost"].append(f"£{cost:,.0f}")
            summary_data["Monthly Cost"].append(f"£{cost/12:,.0f}")
            summary_data["% of Total"].append(f"{(cost/total_annual_cost)*100:.1f}%")
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed breakdowns by category
    st.subheader("📊 Detailed Cost Breakdown")
    
    # Housing
    if housing_cost > 0:
        with st.expander("🏠 Housing", expanded=True):
            st.markdown(f"**Annual Cost: £{housing_cost:,.0f} | Monthly: £{housing_cost/12:,.0f}**")
            
            if ownership_status in ["Own with mortgage", "Own outright"]:
                if ownership_status == "Own with mortgage":
                    chosen_price = home_price if home_price and home_price > 0 else REGIONAL_COSTS[region]["avg_house_price"]
                    deposit_amt = chosen_price * (deposit_percent / 100)
                    loan_amt = chosen_price - deposit_amt
                    st.write(f"- Mortgage payment: £{housing_cost - 2000:,.0f}/year (£{(housing_cost - 2000)/12:,.0f}/month)")
                    st.write(f"  - Property price: £{chosen_price:,}")
                    st.write(f"  - Deposit: £{deposit_amt:,} ({deposit_percent}%)")
                    st.write(f"  - Mortgage amount: £{loan_amt:,}")
                    st.write(f"  - Interest rate: {mortgage_rate*100:.2f}%")
                    st.write(f"  - Term: 25 years")
                    st.write(f"- Maintenance & insurance: £2,000/year")
                else:
                    st.write(f"- Own outright (no mortgage)")
                    st.write(f"- Maintenance & insurance: £{housing_cost:,.0f}/year")
            else:
                rent_monthly = custom_rent if custom_rent and custom_rent > 0 else REGIONAL_COSTS[region]["avg_rent_monthly"]
                st.write(f"- Rent: £{housing_cost:,.0f}/year (£{rent_monthly:,.0f}/month)")
                st.write(f"  - Based on {region} {'custom' if custom_rent else 'median'} rental prices")
                if planning_to_buy:
                    st.write(f"- Currently renting while saving for future home purchase")
            
            st.markdown("**📊 Data Sources:** [ONS House Price Index (2024)](https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/housepriceindex/latest), [UK Finance Mortgage Stats (2024)](https://www.ukfinance.org.uk/data-and-research/data/mortgages)")
            st.markdown("**📐 Methodology:** Mortgage calculated using standard annuity formula over 25 years. Maintenance assumes £2k/year for repairs and insurance.")
    
    # Future home deposit savings
    if future_deposit_savings > 0:
        with st.expander("🏡 Future Home Deposit Savings"):
            st.markdown(f"**Annual Savings: £{future_deposit_savings:,.0f} | Monthly: £{future_deposit_savings/12:,.0f}**")
            target_price = home_price if home_price and home_price > 0 else REGIONAL_COSTS[region]["avg_house_price"]
            target_deposit = target_price * (deposit_percent / 100)
            st.write(f"- Target property price: £{target_price:,}")
            st.write(f"- Target deposit ({deposit_percent}%): £{target_deposit:,}")
            st.write(f"- Years until purchase: {years_until_purchase}")
            st.write(f"- Assuming 3% annual investment returns")
            
            st.markdown("**📊 Data Sources:** Regional house prices from [ONS](https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/housepriceindex/latest)")
            st.markdown("**📐 Methodology:** Savings calculated using compound interest formula with 3% annual growth (conservative estimate for stocks & shares ISA).")
    
    # Nursery
    if nursery_cost > 0:
        with st.expander("👶 Nursery (Children Under 5)"):
            st.markdown(f"**Annual Cost: £{nursery_cost:,.0f} | Monthly: £{nursery_cost/12:,.0f}**")
            under5_count = sum(1 for age in child_ages if age < 5)
            st.write(f"- {under5_count} child(ren) under 5 years old")
            if nursery_type == "Public (15-30 free hours)":
                st.write(f"- Using government-funded childcare (15-30 hours/week)")
                st.write(f"- Additional hours at £{CHILDCARE_BASE['under5_hourly']:.2f}/hour (median)")
            else:
                st.write(f"- Private nursery at £{CHILDCARE_BASE['under5_hourly']:.2f}/hour (median)")
                st.write(f"- Full-time: ~£8,000-10,000 per child per year")
            
            st.markdown("**📊 Data Sources:** [Coram Family & Childcare Survey (2025)](https://www.coram.org.uk/childcare-survey), [gov.uk Free Childcare](https://www.gov.uk/help-with-childcare-costs)")
            st.markdown("**📐 Methodology:** Hourly rates adjusted by regional cost multiplier. Government schemes provide 15-30 free hours/week for eligible families.")
    
    # School costs
    if school_cost > 0:
        with st.expander("🎓 School Education (Ages 5-18)"):
            st.markdown(f"**Annual Cost: £{school_cost:,.0f} | Monthly: £{school_cost/12:,.0f}**")
            school_age_children = [age for age in child_ages if 5 <= age <= 18]
            st.write(f"- {len(school_age_children)} child(ren) in school (ages 5-18)")
            st.write(f"- School type: {school_type}")
            
            if school_type == "Public (State)":
                st.write(f"- State education is free at point of use")
                st.write(f"- Cost shown includes uniforms, trips, supplies (~£500/child/year)")
            elif school_type == "Private (Day)":
                st.write(f"- Day school fees: £{EDUCATION_COSTS['private_day']:,}/year per child (median)")
                st.write(f"- Includes tuition, lunch, basic activities")
            else:
                st.write(f"- Boarding school fees: £{EDUCATION_COSTS['private_boarding']:,}/year per child (median)")
                st.write(f"- Includes tuition, accommodation, meals")
            
            st.markdown("**📊 Data Sources:** [Independent Schools Council (ISC) Census (2025)](https://www.isc.co.uk/research/), [gov.uk State Education](https://www.gov.uk/types-of-school)")
            st.markdown("**📐 Methodology:** Private school fees are annual averages from ISC. State schools are free but additional costs (uniforms, trips) estimated at £500/year.")
    
    # University
    if university_cost > 0:
        with st.expander("🎓 University Support"):
            st.markdown(f"**Annual Cost: £{university_cost:,.0f} | Monthly: £{university_cost/12:,.0f}**")
            uni_age_children = sum(1 for age in child_ages if 18 <= age <= 21)
            if uni_age_children > 0:
                st.write(f"- {uni_age_children} child(ren) currently at university")
                st.write(f"- Tuition fees: £{UNIVERSITY_COSTS['tuition_fees']:,}/year (England median)")
                st.write(f"- Accommodation: £{UNIVERSITY_COSTS['accommodation']:,}/year (median)")
                st.write(f"- Living costs: £{UNIVERSITY_COSTS['living_costs']:,}/year")
                st.write(f"- Total per student: £{sum(UNIVERSITY_COSTS.values()):,}/year")
            else:
                years_ahead = min(18 - age for age in child_ages if age < 18)
                st.write(f"- Saving for future university costs")
                st.write(f"- First child reaches university age in {years_ahead} years")
                st.write(f"- Projected cost per child: £{sum(UNIVERSITY_COSTS.values()):,}/year")
    
    # Childcare (paid, non-school hours)
    if childcare_cost > 0:
        with st.expander("👨‍👩‍👧 Paid Childcare (Wraparound & After-School)"):
            st.markdown(f"**Annual Cost: £{childcare_cost:,.0f} | Monthly: £{childcare_cost/12:,.0f}**")
            if childcare_hours > 0:
                st.write(f"- Hours per week: {childcare_hours}")
                st.write(f"- Under-5 rate: £{CHILDCARE_BASE['under5_hourly']:.2f}/hour (median)")
                st.write(f"- School-age rate: £{CHILDCARE_BASE['school_age_hourly']:.2f}/hour (median)")
                st.write(f"- Covers breakfast clubs, after-school care, holiday clubs")
                st.write(f"- Regional multiplier: {REGIONAL_COSTS[region]['cost_multiplier']}x")
            else:
                st.write("- No additional childcare hours selected")
    
    # Activities
    if activities_cost > 0:
        with st.expander("⚽ Children's Activities"):
            st.markdown(f"**Annual Cost: £{activities_cost:,.0f} | Monthly: £{activities_cost/12:,.0f}**")
            st.write(f"- Sessions per child per week: {activities_per_week}")
            st.write(f"- Cost per session: £{cost_per_activity} (median: £{ACTIVITY_COSTS['per_session']})")
            st.write(f"- {activity_weeks} weeks per year")
            st.write(f"- Total per child: £{activities_per_week * cost_per_activity * activity_weeks:,.0f}/year")
            st.write("- Examples: football, swimming, music lessons, dance, martial arts, scouts")
            
            st.markdown("**📊 Data Sources:** [Sport England (2024)](https://www.sportengland.org/), [ISM Music Lesson Costs (2024)](https://www.ism.org/)")
            st.markdown("**📐 Methodology:** Based on median costs for one activity session (sport, music, or other structured activity). Varies by activity type and location.")
    
    # Holidays
    if holiday_cost > 0:
        with st.expander("✈️ Holidays & Travel"):
            st.markdown(f"**Annual Cost: £{holiday_cost:,.0f} | Monthly: £{holiday_cost/12:,.0f}**")
            st.write(f"- Holidays per year: {holidays_per_year}")
            st.write(f"- Adults: {num_parents} × £{holiday_cost_per_adult:,}/trip (median: £{HOLIDAY_COSTS['per_adult_trip']:,})")
            st.write(f"- Children: {num_children} × £{holiday_cost_per_child:,}/trip (median: £{HOLIDAY_COSTS['per_child_trip']:,})")
            st.write(f"- Cost per trip: £{(num_parents * holiday_cost_per_adult + num_children * holiday_cost_per_child):,.0f}")
            st.write("- Based on median UK family holiday costs (mix of UK/Europe)")
            
            st.markdown("**📊 Data Sources:** [ABTA Holiday Habits Report (2025)](https://www.abta.com/industry-zone/reports-and-publications/abta-holiday-habits-report), [ONS Travel Trends (2024)](https://www.ons.gov.uk/peoplepopulationandcommunity/leisureandtourism/datasets/overseastravelandtourism)")
            st.markdown("**📐 Methodology:** Median costs per person for mix of UK and European holidays. Does not include long-haul or luxury travel.")
    
    # Transportation
    if car_cost > 0:
        with st.expander("🚗 Transportation (Cars)"):
            st.markdown(f"**Annual Cost: £{car_cost:,.0f} | Monthly: £{car_cost/12:,.0f}**")
            st.write(f"- Number of cars: {cars}")
            st.write(f"- Car type: {car_type}")
            
            car_breakdown = CAR_COSTS.get(car_type.lower().replace("/", "_").replace(" ", "_"), CAR_COSTS["medium_car"])
            cost_per_car = sum(car_breakdown.values())
            
            st.write(f"\n**Parent car costs (6,000 miles/year per car - UK median):**")
            st.write(f"- Insurance: £{car_breakdown['insurance']:,}/year")
            st.write(f"- Fuel: £{car_breakdown['fuel']:,}/year")
            st.write(f"- Road tax: £{car_breakdown['tax']:,}/year")
            st.write(f"- Service/MOT: £{car_breakdown['mot_service']:,}/year")
            st.write(f"- Repairs: £{car_breakdown['repairs']:,}/year")
            st.write(f"- **Subtotal: £{cost_per_car:,}/year per parent car**")
            
            if children_with_cars > 0:
                child_car_cost = sum(CAR_COSTS['small_car'].values())
                st.write(f"\n**Children's cars ({children_with_cars} small car(s)):**")
                st.write(f"- Cost per car: £{child_car_cost:,}/year")
                st.write(f"- Total for children: £{child_car_cost * children_with_cars:,}/year")
            
            st.write(f"\n**Note:** Depreciation (~£1,500-2,500/year) not included in running costs calculation")
            
            st.markdown("**📊 Data Sources:** [AA Motoring Costs (2025)](https://www.theaa.com/driving-advice/driving-costs), [RAC Report on Motoring (2024)](https://www.rac.co.uk/drive/news/motoring-news/rac-report-on-motoring/), [Nimblefins Study (2025)](https://www.nimblefins.co.uk/average-cost-run-car-uk)")
            st.markdown("**📐 Methodology:** Costs based on 6,000 miles/year (UK median for non-driving jobs). Fuel at £1.45/litre petrol, electric at £0.08/kWh home charging.")
    
    # Basic living costs breakdown
    st.markdown("### 🏠 Basic Living Costs")
    
    with st.expander("🛒 Food & Groceries"):
        food_cost = BASE_LIVING_COSTS["food_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]
        st.markdown(f"**Annual Cost: £{food_cost:,.0f} | Monthly: £{food_cost/12:,.0f}**")
        st.write(f"- Household size: {household_size} people")
        st.write(f"- Base cost: £{BASE_LIVING_COSTS['food_per_person']/12:,.0f}/person/month")
        st.write(f"- Regional multiplier: {REGIONAL_COSTS[region]['cost_multiplier']}x")
        st.write("- Based on ONS Family Spending Survey (2024)")
    
    with st.expander("💡 Utilities & Council Tax"):
        utilities_cost = BASE_LIVING_COSTS["utilities_base"] * REGIONAL_COSTS[region]["cost_multiplier"]
        st.markdown(f"**Annual Cost: £{utilities_cost:,.0f} | Monthly: £{utilities_cost/12:,.0f}**")
        st.write(f"- Electricity & gas: ~£1,200/year (Ofgem Price Cap 2025)")
        st.write(f"- Water: ~£450/year")
        st.write(f"- Council tax (Band D): ~£2,100/year")
        st.write(f"- Regional multiplier: {REGIONAL_COSTS[region]['cost_multiplier']}x")
    
    with st.expander("📱 Communications"):
        st.markdown(f"**Annual Cost: £{comms_cost:,.0f} | Monthly: £{comms_cost/12:,.0f}**")
        st.write(f"- Broadband: £{COMMUNICATIONS_COSTS['broadband']/12:.0f}/month")
        st.write(f"- Adult mobile plans: {num_parents} × £{COMMUNICATIONS_COSTS['adult_mobile']/12:.0f}/month")
        teens = sum(1 for age in child_ages if age >= 14)
        if teens > 0:
            st.write(f"- Teen mobile plans (14+): {teens} × £{COMMUNICATIONS_COSTS['teen_mobile']/12:.0f}/month")
        st.write("- Based on Ofcom pricing data (2024)")
    
    with st.expander("👕 Clothing"):
        clothing_cost = BASE_LIVING_COSTS["clothing_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]
        st.markdown(f"**Annual Cost: £{clothing_cost:,.0f} | Monthly: £{clothing_cost/12:,.0f}**")
        st.write(f"- Per person: £{BASE_LIVING_COSTS['clothing_per_person']/12:,.0f}/month")
        st.write(f"- Household: {household_size} people")
    
    with st.expander("🏥 Healthcare"):
        healthcare_cost = BASE_LIVING_COSTS["healthcare_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]
        st.markdown(f"**Annual Cost: £{healthcare_cost:,.0f} | Monthly: £{healthcare_cost/12:,.0f}**")
        st.write(f"- Prescriptions, dental, optical, over-the-counter")
        st.write(f"- Per person: £{BASE_LIVING_COSTS['healthcare_per_person']/12:,.0f}/month")
    
    with st.expander("🎬 Entertainment"):
        entertainment_cost = BASE_LIVING_COSTS["entertainment_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"]
        st.markdown(f"**Annual Cost: £{entertainment_cost:,.0f} | Monthly: £{entertainment_cost/12:,.0f}**")
        st.write(f"- Streaming services, cinema, days out, hobbies")
        st.write(f"- Per person: £{BASE_LIVING_COSTS['entertainment_per_person']/12:,.0f}/month")
    
    with st.expander("🛋️ Household Goods"):
        household_cost = BASE_LIVING_COSTS["household_goods"] * REGIONAL_COSTS[region]["cost_multiplier"]
        st.markdown(f"**Annual Cost: £{household_cost:,.0f} | Monthly: £{household_cost/12:,.0f}**")
        st.write(f"- Furniture, appliances, repairs, cleaning supplies")
    
    with st.expander("🛡️ Insurance"):
        insurance_cost = BASE_LIVING_COSTS["insurance_base"] * REGIONAL_COSTS[region]["cost_multiplier"]
        st.markdown(f"**Annual Cost: £{insurance_cost:,.0f} | Monthly: £{insurance_cost/12:,.0f}**")
        st.write(f"- Home/contents insurance, life insurance")
    
    # Long-term savings
    st.markdown("### 💰 Long-Term Savings & Goals")
    
    if home_deposit_savings > 0:
        with st.expander("🏠 Children's First Home Deposits"):
            st.markdown(f"**Annual Savings: £{home_deposit_savings:,.0f} | Monthly: £{home_deposit_savings/12:,.0f}**")
            total_needed = deposit_per_child * num_children
            st.write(f"- Amount per child: £{deposit_per_child:,}")
            st.write(f"- Total for {num_children} child(ren): £{total_needed:,}")
            st.write(f"- Years until needed: {years_until_deposit}")
            st.write(f"- Assuming 3% annual investment returns")
            st.write(f"- Helps children get on property ladder")
    
    if retirement_savings > 0:
        with st.expander("🏖️ Retirement Savings"):
            st.markdown(f"**Annual Savings: £{retirement_savings:,.0f} | Monthly: £{retirement_savings/12:,.0f}**")
            
            # Calculate years until retirement
            retirement_age = 67
            avg_parent_age = (parent1_age + parent2_age) / 2 if parent2_age > 0 else parent1_age
            years_to_retirement = max(retirement_age - avg_parent_age, 0)
            
            # Get target annual income based on lifestyle
            if retirement_lifestyle == "Minimum":
                target_annual = RETIREMENT_NEEDS["minimum_couple"] if parent2_age > 0 else RETIREMENT_NEEDS["minimum_single"]
            elif retirement_lifestyle == "Moderate":
                target_annual = RETIREMENT_NEEDS["moderate_couple"] if parent2_age > 0 else RETIREMENT_NEEDS["moderate_single"]
            else:
                target_annual = RETIREMENT_NEEDS["comfortable_couple"] if parent2_age > 0 else RETIREMENT_NEEDS["comfortable_single"]
            
            st.write(f"- Current retirement pot: £{current_pension_pot:,}")
            st.write(f"- Target annual income in retirement: £{target_annual:,}")
            st.write(f"- Years until retirement: {years_to_retirement:.0f}")
            st.write(f"- State pension per person: £{state_pension_annual/2 if parent2_age > 0 else state_pension_annual:,.0f}/year (2025/26)")
            
            if years_money_lasts > 0:
                years_display = int(years_money_lasts)
                months_display = int((years_money_lasts - years_display) * 12)
                st.write(f"\n**Retirement Duration:**")
                st.write(f"- Your pot will last: **{years_display} years and {months_display} months**")
                st.write(f"- Based on 4% safe withdrawal rate")
                st.write(f"- Includes State Pension income")
            
            st.markdown("**📊 Data Sources:** [PLSA Retirement Living Standards (2025)](https://www.plsa.co.uk/retirement-living-standards), [gov.uk State Pension (2025/26)](https://www.gov.uk/state-pension), [Money Helper](https://www.moneyhelper.org.uk/en/pensions-and-retirement)")
            st.markdown("**📐 Methodology:** Uses 4% safe withdrawal rate (Trinity Study). Assumes 5% investment returns. State Pension: £11,502/person (2025/26).")
    
    if emergency_savings > 0:
        with st.expander("🚨 Emergency Fund"):
            st.markdown(f"**Annual Savings: £{emergency_savings:,.0f} | Monthly: £{emergency_savings/12:,.0f}**")
            st.write(f"- Target: {emergency_fund_months} months of expenses")
            st.write(f"- Target amount: £{emergency_fund_months * total_annual_cost / 12:,.0f}")
            st.write(f"- Years to build: 10")
    
    if target_savings > 0:
        with st.expander("💎 Additional Savings"):
            st.markdown(f"**Annual Savings: £{target_savings:,.0f} | Monthly: £{target_savings/12:,.0f}**")
            st.write(f"- User-specified savings goal")
    
    # Regional comparison
    st.markdown("---")
    st.subheader("📍 Regional Cost Comparison")
    
    comparison_data = []
    for reg, data in REGIONAL_COSTS.items():
        comparison_data.append({
            "Region": reg,
            "Avg House Price": f"£{data['avg_house_price']:,}",
            "Avg Monthly Rent": f"£{data['avg_rent_monthly']:,}",
            "Cost Multiplier": f"{data['cost_multiplier']}x"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, hide_index=True, use_container_width=True)
    
    # Key insights
    st.markdown("---")
    st.subheader("💡 Key Insights & Analytics")
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Largest Single Expense", 
                 max(categories, key=lambda x: x[1])[0],
                 f"£{max(categories, key=lambda x: x[1])[1]:,.0f}/year")
    
    with col2:
        savings_total = home_deposit_savings + retirement_savings + emergency_savings + target_savings
        st.metric("Total Savings Rate",
                 f"£{savings_total:,.0f}/year",
                 f"{(savings_total/total_annual_cost)*100:.1f}% of total")
    
    with col3:
        essential_housing = housing_cost + future_deposit_savings
        st.metric("Housing Costs",
                 f"£{essential_housing:,.0f}/year",
                 f"{(essential_housing/total_annual_cost)*100:.1f}% of total")
    
    with col4:
        children_costs = nursery_cost + school_cost + university_cost + childcare_cost + activities_cost + home_deposit_savings
        st.metric("Total Child-Related Costs",
                 f"£{children_costs:,.0f}/year",
                 f"{(children_costs/total_annual_cost)*100:.1f}% of total")
    
    st.markdown("---")
    
    # Charts row
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**📊 Top 10 Expenses by Category**")
        # Get top 10 categories
        top_10_categories = sorted([(name, cost) for name, cost in categories if cost > 0], 
                                   key=lambda x: x[1], reverse=True)[:10]
        if top_10_categories:
            chart_data = pd.DataFrame(top_10_categories, columns=["Category", "Annual Cost"])
            st.bar_chart(chart_data.set_index("Category"), height=400)
    
    with chart_col2:
        st.markdown("**📈 Cost Breakdown by Type**")
        # Categorize costs
        essential_costs = housing_cost + living_costs + car_cost + comms_cost
        child_costs = nursery_cost + school_cost + university_cost + childcare_cost + activities_cost
        savings_costs = home_deposit_savings + retirement_savings + emergency_savings + target_savings + future_deposit_savings
        lifestyle_costs = holiday_cost + (BASE_LIVING_COSTS["entertainment_per_person"] * household_size * REGIONAL_COSTS[region]["cost_multiplier"])
        
        breakdown_data = pd.DataFrame({
            "Category": ["Essential Living", "Child-Related", "Savings & Future", "Lifestyle"],
            "Annual Cost": [essential_costs, child_costs, savings_costs, lifestyle_costs]
        })
        st.bar_chart(breakdown_data.set_index("Category"), height=400, color="#FF6B6B")
    
    st.markdown("---")
    
    # More detailed stats
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.markdown("**📉 Monthly Cost Distribution**")
        monthly_breakdown = {
            "Housing": housing_cost / 12,
            "Food & Living": living_costs / 12,
            "Transportation": car_cost / 12,
            "Children": (nursery_cost + school_cost + childcare_cost + activities_cost) / 12,
            "Savings": savings_total / 12,
            "Other": (holiday_cost + comms_cost) / 12
        }
        monthly_df = pd.DataFrame(list(monthly_breakdown.items()), columns=["Category", "Monthly Cost"])
        monthly_df = monthly_df[monthly_df["Monthly Cost"] > 0].sort_values("Monthly Cost", ascending=False)
        st.dataframe(monthly_df.style.format({"Monthly Cost": "£{:,.0f}"}), hide_index=True, use_container_width=True)
        
        # Percentage of income going to different areas
        st.markdown("**🎯 Budget Allocation**")
        st.progress(essential_costs / total_annual_cost, text=f"Essential: {(essential_costs/total_annual_cost)*100:.1f}%")
        st.progress(child_costs / total_annual_cost, text=f"Children: {(child_costs/total_annual_cost)*100:.1f}%")
        st.progress(savings_costs / total_annual_cost, text=f"Savings: {(savings_costs/total_annual_cost)*100:.1f}%")
    
    with stat_col2:
        st.markdown("**📊 Cost Comparison by Household Size**")
        # Show per-person annual costs
        per_person_cost = total_annual_cost / household_size if household_size > 0 else 0
        st.write(f"- Cost per person: **£{per_person_cost:,.0f}/year** (£{per_person_cost/12:,.0f}/month)")
        st.write(f"- Per parent: **£{total_annual_cost/num_parents:,.0f}/year** (£{total_annual_cost/num_parents/12:,.0f}/month)")
        if num_children > 0:
            child_only_costs = nursery_cost + school_cost + university_cost + childcare_cost + activities_cost + home_deposit_savings
            st.write(f"- Per child direct cost: **£{child_only_costs/num_children:,.0f}/year** (£{child_only_costs/num_children/12:,.0f}/month)")
        
        # Timeline visualization
        st.markdown("**📅 Financial Timeline**")
        if years_until_deposit > 0 and help_with_deposit:
            st.write(f"🏠 Children's deposits: **{years_until_deposit:.0f} years**")
        if planning_to_buy and years_until_purchase > 0:
            st.write(f"🏡 Home purchase: **{years_until_purchase} years**")
        
        retirement_age = 67
        avg_parent_age = (parent1_age + parent2_age) / 2 if parent2_age > 0 else parent1_age
        years_to_retirement = max(retirement_age - avg_parent_age, 0)
        if years_to_retirement > 0:
            st.write(f"🏖️ Retirement: **{years_to_retirement:.0f} years**")
            if years_money_lasts > 0:
                st.write(f"   └ Pot lasts: **{int(years_money_lasts)} years**")
        
        youngest_child = min(child_ages) if child_ages else 0
        if youngest_child < 18:
            st.write(f"🎓 Last child turns 18: **{18 - youngest_child} years**")

else:
    st.info("👈 Configure your family details and lifestyle preferences in the sidebar, then click 'Calculate Required Income'")
    
    st.markdown("---")
    st.subheader("Quick Reference - Median Costs Used")
    
    ref_data = {
        "Item": [
            "Childcare (under 5)",
            "Wraparound care (5-11)",
            "Child activity session",
            "Holiday per adult",
            "Holiday per child",
            "Small car running costs",
            "Medium car running costs",
            "Broadband monthly",
            "Adult mobile monthly",
            "Teen mobile monthly",
            "Food per person monthly",
            "Utilities monthly",
        ],
        "Median Cost": [
            f"£{CHILDCARE_BASE['under5_hourly']:.2f}/hour",
            f"£{CHILDCARE_BASE['school_age_hourly']:.2f}/hour",
            f"£{ACTIVITY_COSTS['per_session']}/session",
            f"£{HOLIDAY_COSTS['per_adult_trip']}/trip",
            f"£{HOLIDAY_COSTS['per_child_trip']}/trip",
            f"£{sum(CAR_COSTS['small_car'].values()):,}/year (6k miles)",
            f"£{sum(CAR_COSTS['medium_car'].values()):,}/year (6k miles)",
            f"£{COMMUNICATIONS_COSTS['broadband']/12:.0f}",
            f"£{COMMUNICATIONS_COSTS['adult_mobile']/12:.0f}",
            f"£{COMMUNICATIONS_COSTS['teen_mobile']/12:.0f}",
            f"£{BASE_LIVING_COSTS['food_per_person']/12:.0f}",
            f"£{BASE_LIVING_COSTS['utilities_base']/12:.0f}",
        ]
    }
    
    ref_df = pd.DataFrame(ref_data)
    st.dataframe(ref_df, hide_index=True, use_container_width=True)

# Data sources
st.markdown("---")
with st.expander("📚 Data Sources & Methodology"):
    st.markdown("""
    ### Data Sources (with years)
    
    **Housing Costs:**
    - [ONS House Price Index (2024)](https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/housepriceindex/latest)
    - [Rightmove Rental Index (Q4 2024)](https://www.rightmove.co.uk/news/rental-price-tracker/)
    - [Zoopla Average Rents (2024)](https://www.zoopla.co.uk/discover/property-news/rental-market-report/)
    - [UK Finance Mortgage Statistics (2024)](https://www.ukfinance.org.uk/data-and-research/data/mortgages)
    - [Bank of England Base Rate (January 2026)](https://www.bankofengland.co.uk/monetary-policy/the-interest-rate-bank-rate)
    
    **Education:**
    - [Independent Schools Council (ISC) Census (2025)](https://www.isc.co.uk/research/)
    - [gov.uk State Education (2025)](https://www.gov.uk/types-of-school)
    - [gov.uk Tuition Fee Regulations (2025/26 Academic Year)](https://www.gov.uk/student-finance/tuition-fees)
    - [Student Finance England Maintenance Loans (2025/26)](https://www.gov.uk/student-finance)
    - [Coram Family & Childcare Survey (2025)](https://www.coram.org.uk/childcare-survey)
    
    **Living Costs:**
    - [ONS Family Spending Survey (Financial Year Ending 2024)](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/expenditure/bulletins/familyspendingintheuk/latest)
    - [ONS Living Costs and Food Survey (2024)](https://www.ons.gov.uk/surveys/informationforhouseholdsandindividuals/householdandindividualsurveys/livingcostsandfoodsurvey)
    - [ONS Regional Price Indices (2024)](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/regionalhousepriceindicestablesataglance)
    
    **Transportation:**
    - [AA Motoring Costs Survey (2025)](https://www.theaa.com/driving-advice/driving-costs)
    - [RAC Report on Motoring (2024)](https://www.rac.co.uk/drive/news/motoring-news/rac-report-on-motoring/)
    - [Nimblefins Car Running Costs Study (2025)](https://www.nimblefins.co.uk/average-cost-run-car-uk)
    - [Department for Transport National Travel Survey (2023)](https://www.gov.uk/government/collections/national-travel-survey-statistics) - Average mileage data
    
    **Communications:**
    - [Ofcom Communications Market Report (2024)](https://www.ofcom.org.uk/research-and-data/multi-sector-research/cmr)
    - Average broadband and mobile pricing (Q4 2024)
    
    **Childcare & Activities:**
    - [Coram Family & Childcare Survey (2025)](https://www.coram.org.uk/childcare-survey)
    - [Ofsted Childcare Costs (2024)](https://www.gov.uk/find-ofsted-inspection-report)
    - [Sport England Participation Costs (2024)](https://www.sportengland.org/)
    - [ISM (Incorporated Society of Musicians) Lesson Costs (2024)](https://www.ism.org/)
    
    **Holidays:**
    - [ABTA Holiday Habits Report (2025)](https://www.abta.com/industry-zone/reports-and-publications/abta-holiday-habits-report)
    - [ONS Travel Trends (2024)](https://www.ons.gov.uk/peoplepopulationandcommunity/leisureandtourism/datasets/overseastravelandtourism)
    - [VisitBritain Domestic Tourism Spend (2024)](https://www.visitbritain.org/visitor-economy-facts)
    
    **Retirement:**
    - [Pension and Lifetime Savings Association (PLSA) Retirement Living Standards (2025)](https://www.plsa.co.uk/retirement-living-standards)
    - [Money Helper Retirement Planning Guidance (2025)](https://www.moneyhelper.org.uk/en/pensions-and-retirement)
    - [gov.uk State Pension Rates (2025/26 Tax Year)](https://www.gov.uk/state-pension)
    
    ### Methodology
    
    **Car Costs:**
    - Based on 6,000 miles per year per car (UK median for non-driving jobs)
    - Excludes depreciation (not a cash outflow for existing vehicles)
    - Fuel calculated at £1.45/litre petrol (January 2026)
    - Electric calculated at £0.08/kWh home charging rate
    
    **Gross Income Calculation:**
    - Assumes 30% average tax and National Insurance rate
    - Net income = Gross income × 0.7
    - This is simplified; actual tax depends on income level
    
    **Regional Adjustments:**
    - Cost multipliers based on ONS regional price indices (2024)
    - Housing uses actual regional averages
    
    **Retirement Calculations:**
    - Uses 4% safe withdrawal rate (Trinity Study methodology)
    - Includes State Pension at £11,502/person/year (2025/26)
    - Assumes 5% annual investment returns
    
    **Children's Deposits:**
    - Customizable amount per child (default £50,000 - typical UK first-time buyer deposit)
    - 3% annual investment growth assumed
    
    ### Assumptions & Limitations
    
    - All costs based on 2024-2026 median UK data
    - Individual circumstances vary significantly
    - Tax calculations are simplified
    - Investment returns not guaranteed
    - Inflation not explicitly modeled in projections
    
    This calculator provides estimates for planning purposes only and should not be considered financial advice.
    """)
