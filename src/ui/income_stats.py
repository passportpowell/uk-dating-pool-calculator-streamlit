"""
Income demographics tab showing UK income distribution by age, gender, and ethnicity.
Uses Census 2021 population data, 2022 single rates (ONS), and 2023 ASHE income distribution.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.constants import (
    UK_ADULT_POPULATION,
    ETHNICITY_DISTRIBUTION,
    INCOME_AGE_MULTIPLIERS,
    INCOME_ETHNICITY_MULTIPLIERS,
    GENDER_SPLIT,
    SINGLE_RATE,
    SINGLE_RATE_BY_AGE,
    EMPLOYMENT_RATE_BY_AGE_GENDER,
    SELF_EMPLOYMENT_RATE_BY_AGE_GENDER,
    SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE,
    SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE,
)
from src.calculations.dating_pool import (
    calculate_income_probability,
    calculate_self_employed_income_probability,
    calculate_age_probability,
    get_single_rate_by_age,
    get_employment_rate_by_age_gender,
    get_self_employment_rate_by_age_gender,
    calculate_population_pipeline,
)


def _age_income_multiplier(age_range):
    """Weighted multiplier for the selected age span."""
    total_years = 0
    weighted_sum = 0.0
    for band in INCOME_AGE_MULTIPLIERS:
        band_min, band_max = band["range"]
        overlap_min = max(age_range[0], band_min)
        overlap_max = min(age_range[1], band_max)
        if overlap_max >= overlap_min:
            years = overlap_max - overlap_min + 1
            total_years += years
            weighted_sum += years * band["multiplier"]
    if total_years == 0:
        return 1.0
    return weighted_sum / total_years


def _ethnicity_multiplier(selected_ethnicities):
    """Weighted multiplier based on selected ethnicities."""
    if not selected_ethnicities:
        return 1.0
    total_weight = 0.0
    weighted_sum = 0.0
    for ethnicity in selected_ethnicities:
        weight = ETHNICITY_DISTRIBUTION.get(ethnicity, 0)
        total_weight += weight
        weighted_sum += weight * INCOME_ETHNICITY_MULTIPLIERS.get(ethnicity, 1.0)
    if total_weight == 0:
        return 1.0
    return weighted_sum / total_weight


def _income_prob_with_adjusters(min_income, gender, age_range, selected_ethnicities):
    base = calculate_income_probability(min_income, gender)
    adjusted = base * _age_income_multiplier(age_range) * _ethnicity_multiplier(selected_ethnicities)
    return max(0.0, min(1.0, adjusted))


def _combined_probability(min_income, gender_filter, age_range, selected_ethnicities):
    if gender_filter == "Any":
        male_prob = _income_prob_with_adjusters(min_income, "Male", age_range, selected_ethnicities)
        female_prob = _income_prob_with_adjusters(min_income, "Female", age_range, selected_ethnicities)
        return {
            "Male": male_prob,
            "Female": female_prob,
            "Combined": (male_prob * GENDER_SPLIT["Male"]) + (female_prob * GENDER_SPLIT["Female"]),
        }
    prob = _income_prob_with_adjusters(min_income, gender_filter, age_range, selected_ethnicities)
    return {gender_filter: prob, "Combined": prob}


def _population_slice(age_range, selected_ethnicities, gender_filter):
    """Calculate population slice with validation."""
    age_share = calculate_age_probability(age_range[0], age_range[1])
    
    # Validate all ethnicities exist
    invalid_ethnicities = [e for e in selected_ethnicities if e not in ETHNICITY_DISTRIBUTION]
    if invalid_ethnicities:
        raise ValueError(f"Invalid ethnicities: {invalid_ethnicities}. Must be from: {list(ETHNICITY_DISTRIBUTION.keys())}")
    
    ethnicity_share = sum(ETHNICITY_DISTRIBUTION.get(e, 0) for e in selected_ethnicities)
    if ethnicity_share <= 0:
        raise ValueError("Selected ethnicities resulted in zero population share. Check ethnicity selection.")
    
    base_pop = UK_ADULT_POPULATION * age_share * ethnicity_share
    if gender_filter == "Any":
        return {
            "Male": base_pop * GENDER_SPLIT["Male"],
            "Female": base_pop * GENDER_SPLIT["Female"],
            "Combined": base_pop,
        }
    return {gender_filter: base_pop, "Combined": base_pop}


def display_income_demographics_tab(inputs=None):
    """Render the income demographics explorer with in-tab filters."""
    default_gender = "Any"
    if inputs and inputs.get("looking_for") in ["Male", "Female"]:
        default_gender = inputs["looking_for"]
    default_ethnicities = inputs.get("selected_ethnicities") if inputs else list(ETHNICITY_DISTRIBUTION.keys())
    default_age_range = inputs.get("age_range") if inputs else (25, 40)

    # Header with data sources in expander
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 💷 UK Income Demographics Explorer", unsafe_allow_html=True)
    
    with st.expander("📊 Data Sources & Methodology", expanded=False):
        st.markdown("""
**Data sources:**
- [ONS Census 2021](https://www.ons.gov.uk/census) - Ethnicity and gender distribution
- [ONS Families & Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages) - Single rates
- [ONS ASHE 2023](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/ashe1997to2015selectedestimates) - Employee income
- [HMRC Self Assessment](https://www.gov.uk/government/statistics/income-tax-liabilities-statistics) - Self-employed income

**Data years:** Census 2021, Single rates 2022, Employment & Income 2023. No 2025 data available. Using actual survey data only—no estimates or projections.
        """)
    
    st.info("💡 **How to use:** Select your criteria below to explore income demographics across the UK population.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Organize controls in a clean layout
    st.markdown("### Filters")
    
    # Row 1: Age, Gender, Employment Type
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age_range = st.slider(
            "Age range",
            min_value=18,
            max_value=75,
            value=(default_age_range[0], min(default_age_range[1], 75))
        )
    
    with col2:
        gender_filter = st.radio(
            "Gender",
            ["Any", "Male", "Female"],
            index=["Any", "Male", "Female"].index(default_gender),
            horizontal=True,
        )
    
    with col3:
        employment_type = st.radio(
            "Employment",
            ["Any", "Employees", "Self-employed", "Business owners"],
            horizontal=True
        )
    
    st.divider()
    
    # Row 2: Income input
    col_inc1, col_inc2 = st.columns([1, 2])
    
    with col_inc1:
        st.write("**Minimum income (£)**")
    
    with col_inc2:
        income_text = st.text_input(
            "Income",
            value="100000",
            placeholder="e.g., 100000",
            label_visibility="collapsed"
        )
        try:
            income_threshold = int(income_text.replace(",", ""))
            income_threshold = max(0, min(income_threshold, 1000000))
        except ValueError:
            st.error("Please enter a valid number")
            return
    
    st.divider()
    
    # Row 3: Ethnicity
    st.write("**Ethnic groups**")
    ethnicity_selection = st.multiselect(
        "Select groups",
        options=list(ETHNICITY_DISTRIBUTION.keys()),
        default=default_ethnicities,
        label_visibility="collapsed"
    )

    if not ethnicity_selection:
        st.warning("Select at least one ethnicity to calculate population count.")
        return

    st.divider()

    # Use new accurate population pipeline
    # This properly accounts for: Adults -> Employed -> Single -> Income threshold
    pipeline_result = calculate_population_pipeline(
        age_range[0], age_range[1], gender_filter, ethnicity_selection, UK_ADULT_POPULATION
    )
    
    total_adults = pipeline_result['total_adults']
    total_employed = pipeline_result['employed']
    employed_pct = pipeline_result['employed_pct']
    total_population_single = pipeline_result['single_employed']
    single_pct = pipeline_result['single_employed_pct']

    # Core rates used for the transparency table
    age_share = calculate_age_probability(age_range[0], age_range[1])
    ethnicity_share = sum(ETHNICITY_DISTRIBUTION.get(e, 0) for e in ethnicity_selection)
    single_rate = get_single_rate_by_age(age_range[0], age_range[1])
    if gender_filter == "Any":
        gender_share = 1.0
        male_employ_rate = get_employment_rate_by_age_gender(age_range[0], age_range[1], "Male")
        female_employ_rate = get_employment_rate_by_age_gender(age_range[0], age_range[1], "Female")
        employment_rate_used = male_employ_rate * GENDER_SPLIT["Male"] + female_employ_rate * GENDER_SPLIT["Female"]
    else:
        gender_share = GENDER_SPLIT[gender_filter]
        employment_rate_used = get_employment_rate_by_age_gender(age_range[0], age_range[1], gender_filter)

    male_self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Male")
    female_self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Female")
    if gender_filter == "Any":
        self_emp_rate_used = male_self_emp_rate * GENDER_SPLIT["Male"] + female_self_emp_rate * GENDER_SPLIT["Female"]
    else:
        self_emp_rate_used = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], gender_filter)

    # Defaults that will be overwritten in branches
    single_employees = 0
    single_self_employed = 0
    employee_income_prob = 0.0
    self_employed_income_prob = 0.0
    
    # Calculate self-employed breakdown
    if employment_type == "Any":
        # Include both employees and self-employed
        self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], gender_filter) if gender_filter in ["Male", "Female"] else 0.13
        if gender_filter == "Any":
            # Blend male and female self-employment rates
            male_self_emp = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Male")
            female_self_emp = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Female")
            self_emp_rate = male_self_emp * GENDER_SPLIT["Male"] + female_self_emp * GENDER_SPLIT["Female"]
        
        total_self_employed_single = int(total_population_single * self_emp_rate)
        total_employees_single = total_population_single - total_self_employed_single
        single_employees = total_employees_single
        single_self_employed = total_self_employed_single
        
        # Calculate income for both types
        employee_probs = _combined_probability(income_threshold, gender_filter, age_range, ethnicity_selection)
        employee_matches = int(total_employees_single * employee_probs.get("Combined", 0))
        employee_income_prob = employee_probs.get("Combined", 0)
        
        # Self-employed use different income distribution
        if gender_filter == "Male":
            self_emp_income_prob = calculate_self_employed_income_probability(income_threshold, "Male")
        elif gender_filter == "Female":
            self_emp_income_prob = calculate_self_employed_income_probability(income_threshold, "Female")
        else:
            male_prob = calculate_self_employed_income_probability(income_threshold, "Male")
            female_prob = calculate_self_employed_income_probability(income_threshold, "Female")
            self_emp_income_prob = male_prob * GENDER_SPLIT["Male"] + female_prob * GENDER_SPLIT["Female"]
        self_employed_income_prob = self_emp_income_prob
        
        self_emp_matches = int(total_self_employed_single * self_emp_income_prob)
        total_matches = employee_matches + self_emp_matches
        share_pct = 0 if total_population_single == 0 else (total_matches / total_population_single) * 100
        
    elif employment_type == "Self-employed":
        self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], gender_filter) if gender_filter in ["Male", "Female"] else 0.13
        if gender_filter == "Any":
            male_self_emp = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Male")
            female_self_emp = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Female")
            self_emp_rate = male_self_emp * GENDER_SPLIT["Male"] + female_self_emp * GENDER_SPLIT["Female"]
        
        total_self_employed_single = int(total_population_single * self_emp_rate)
        single_self_employed = total_self_employed_single
        single_employees = total_population_single - total_self_employed_single
        
        if gender_filter == "Male":
            income_prob = calculate_self_employed_income_probability(income_threshold, "Male")
        elif gender_filter == "Female":
            income_prob = calculate_self_employed_income_probability(income_threshold, "Female")
        else:
            male_prob = calculate_self_employed_income_probability(income_threshold, "Male")
            female_prob = calculate_self_employed_income_probability(income_threshold, "Female")
            income_prob = male_prob * GENDER_SPLIT["Male"] + female_prob * GENDER_SPLIT["Female"]
        self_employed_income_prob = income_prob
        
        total_matches = int(total_self_employed_single * income_prob)
        share_pct = 0 if total_population_single == 0 else (total_matches / total_population_single) * 100
        
    else:  # Employees only
        # Filter out self-employed
        self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], gender_filter) if gender_filter in ["Male", "Female"] else 0.13
        if gender_filter == "Any":
            male_self_emp = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Male")
            female_self_emp = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], "Female")
            self_emp_rate = male_self_emp * GENDER_SPLIT["Male"] + female_self_emp * GENDER_SPLIT["Female"]
        
        total_employees_single = int(total_population_single * (1 - self_emp_rate))
        single_employees = total_employees_single
        single_self_employed = int(total_population_single * self_emp_rate)
        
        probs = _combined_probability(income_threshold, gender_filter, age_range, ethnicity_selection)
        total_matches = int(total_employees_single * probs.get("Combined", 0))
        share_pct = 0 if total_employees_single == 0 else probs.get("Combined", 0) * 100
        employee_income_prob = probs.get("Combined", 0)

    # For "not single" metric: employed but not single
    total_employed_not_single = int(total_employed * (1 - get_single_rate_by_age(age_range[0], age_range[1])))
    
    # Calculate opposite sex population for comparison
    if gender_filter == "Male":
        opposite_gender = "Female"
    elif gender_filter == "Female":
        opposite_gender = "Male"
    else:
        opposite_gender = None
    
    opposite_sex_pop_same_race = 0
    opposite_sex_pop_all_races = 0
    if opposite_gender:
        # Use new pipeline for opposite sex too
        opp_pipeline = calculate_population_pipeline(
            age_range[0], age_range[1], opposite_gender, ethnicity_selection, UK_ADULT_POPULATION
        )
        opposite_sex_pop_same_race = opp_pipeline['single_employed']
        
        # All races version
        opp_all_races_pipeline = calculate_population_pipeline(
            age_range[0], age_range[1], opposite_gender, list(ETHNICITY_DISTRIBUTION.keys()), UK_ADULT_POPULATION
        )
        opposite_sex_pop_all_races = opp_all_races_pipeline['single_employed']

    # Calculate total in UK for selected race/gender (all ages, using employment rate too)
    ethnicity_share = sum(ETHNICITY_DISTRIBUTION.get(e, 0) for e in ethnicity_selection)
    if gender_filter == "Any":
        total_race_gender_all_ages = int(UK_ADULT_POPULATION * ethnicity_share)
    else:
        total_race_gender_all_ages = int(UK_ADULT_POPULATION * ethnicity_share * GENDER_SPLIT[gender_filter])

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        employment_label = employment_type if employment_type != "Any" else "All employment"
        st.metric("Earning £" + f"{income_threshold:,}"+"+", f"{total_matches:,}", help=f"{employment_label}")
    with col_b:
        st.metric("Share of single employed", f"{share_pct:.2f}%")
    with col_c:
        st.metric("Your employed singles", f"{int(total_population_single):,}")
    with col_d:
        st.metric("Your employed (not single)", f"{int(total_employed_not_single):,}")
    
    if employment_type != "Any":
        st.caption(f"Age {age_range[0]}-{age_range[1]}, {gender_filter}, {employment_type.lower()}, selected ethnicities. Population pipeline: {total_adults:,} adults → {total_employed:,} employed ({employed_pct:.0f}%) → {total_population_single:,} single ({single_pct:.0f}%). Single rates from [ONS Families & Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages), employment from [ONS Labour Force Survey 2023](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes), self-employment from [ONS Self-Employment Trends](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork).")
    else:
        st.caption(f"Age {age_range[0]}-{age_range[1]}, {gender_filter}, any employment type, selected ethnicities. Population pipeline: {total_adults:,} adults → {total_employed:,} employed ({employed_pct:.0f}%) → {total_population_single:,} single ({single_pct:.0f}%). Includes both employees (ASHE) and self-employed (HMRC). Single rates from [ONS Families & Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages).")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show comparison
    if opposite_gender and opposite_sex_pop_same_race > 0:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        # Use SINGLE population for ratio (dating context)
        ratio_same_race = opposite_sex_pop_same_race / total_population_single if total_population_single > 0 else 0
        ratio_all_races = opposite_sex_pop_all_races / total_population_single if total_population_single > 0 else 0
        st.markdown(f"### 💑 Dating Pool Context (Single only)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Your demographic (single):** {int(total_population_single):,} {gender_filter}s")
            st.markdown(f"**Earning £{income_threshold:,}+:** {total_matches:,} ({share_pct:.2f}%)")
        with col2:
            st.markdown(f"**Opposite sex (same ethnicity):** {int(opposite_sex_pop_same_race):,} {opposite_gender}s")
            st.markdown(f"**Ratio:** {ratio_same_race:.1f} {opposite_gender}s per 1 {gender_filter.lower()}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Gender breakdown table (showing employment pipeline)
    st.subheader("Population Pipeline (Single Employed)")
    st.caption("Shows the filtering applied: Total adults → Employed (LFS 2023) → Single (ONS F&H 2022). Income threshold then applied to single employed column.")
    
    breakdown_rows = []
    for test_gender in ["Male", "Female"]:
        if gender_filter != "Any" and gender_filter != test_gender:
            continue  # Skip if not matching filter
        
        # Calculate pipeline for each gender
        gender_pipeline = calculate_population_pipeline(
            age_range[0], age_range[1], test_gender, ethnicity_selection, UK_ADULT_POPULATION
        )
        
        single_employed = gender_pipeline['single_employed']
        
        if employment_type == "Any":
            # Include both employee and self-employed income distributions
            self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], test_gender)
            single_self_employed = int(single_employed * self_emp_rate)
            single_employees = single_employed - single_self_employed
            
            employee_probs = _combined_probability(income_threshold, test_gender, age_range, ethnicity_selection)
            employee_earning = int(single_employees * employee_probs.get("Combined", 0))
            
            self_emp_prob = calculate_self_employed_income_probability(income_threshold, test_gender)
            self_emp_earning = int(single_self_employed * self_emp_prob)
            
            earning_count = employee_earning + self_emp_earning
            breakdown_rows.append({
                "Gender": test_gender,
                "Adults": f"{gender_pipeline['total_adults']:,}",
                "Employed": f"{gender_pipeline['employed']:,}",
                "Employees": f"{single_employees:,}",
                "Self-employed": f"{single_self_employed:,}",
                f"Earning £{income_threshold:,}+": f"{earning_count:,}",
            })
        
        elif employment_type == "Self-employed":
            self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], test_gender)
            single_self_employed = int(single_employed * self_emp_rate)
            
            self_emp_prob = calculate_self_employed_income_probability(income_threshold, test_gender)
            earning_count = int(single_self_employed * self_emp_prob)
            
            breakdown_rows.append({
                "Gender": test_gender,
                "Adults": f"{gender_pipeline['total_adults']:,}",
                "Employed": f"{gender_pipeline['employed']:,}",
                "Self-employed Single": f"{single_self_employed:,}",
                f"Earning £{income_threshold:,}+": f"{earning_count:,}",
            })
        
        else:  # Employees only
            self_emp_rate = get_self_employment_rate_by_age_gender(age_range[0], age_range[1], test_gender)
            single_employees = int(single_employed * (1 - self_emp_rate))
            
            employee_probs = _combined_probability(income_threshold, test_gender, age_range, ethnicity_selection)
            earning_count = int(single_employees * employee_probs.get("Combined", 0))
            
            breakdown_rows.append({
                "Gender": test_gender,
                "Adults": f"{gender_pipeline['total_adults']:,}",
                "Employed": f"{gender_pipeline['employed']:,}",
                "Employee Single": f"{single_employees:,}",
                f"Earning £{income_threshold:,}+": f"{earning_count:,}",
            })
    
    breakdown_df = pd.DataFrame(breakdown_rows)
    st.dataframe(breakdown_df, hide_index=True, use_container_width=True)

    # Threshold comparison chart
    thresholds = [50000, 75000, 100000, 150000]
    chart_data = []
    for threshold in thresholds:
        if employment_type == "Self-employed":
            if gender_filter == "Any":
                male_prob = calculate_self_employed_income_probability(threshold, "Male")
                female_prob = calculate_self_employed_income_probability(threshold, "Female")
                combined_probs = {"Combined": male_prob * GENDER_SPLIT["Male"] + female_prob * GENDER_SPLIT["Female"]}
            else:
                combined_probs = {"Combined": calculate_self_employed_income_probability(threshold, gender_filter)}
        else:
            combined_probs = _combined_probability(threshold, gender_filter, age_range, ethnicity_selection)
        
        chart_data.append({
            "Threshold": threshold,
            "Share %": combined_probs["Combined"] * 100,
        })
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"£{row['Threshold']:,}" for row in chart_data],
        y=[row["Share %"] for row in chart_data],
        text=[f"{row['Share %']:.2f}%" for row in chart_data],
        textposition="auto",
        marker_color="#667eea",
    ))
    fig.update_layout(
        title="Probability of earning at or above each threshold",
        xaxis_title="Income threshold",
        yaxis_title="Share of selected group (%)",
        template="plotly_dark",
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True, key="income_threshold_chart")

    st.info(
        """**Self-Employment & Income Analysis:**

**Data Sources & Years:**
- [Census 2021](https://www.ons.gov.uk/census): Population, ethnicity, gender distribution
- [ONS Labour Force Survey 2023](https://www.ons.gov.uk/employmentandlabourmarket): Employment & self-employment rates by age & gender
- [ONS Families & Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages): Single rates by age band
- [ASHE 2023](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/ashe1997to2015selectedestimates): Employee income distribution
- [HMRC Self Assessment](https://www.gov.uk/government/statistics/income-tax-liabilities-statistics): Self-employed income distribution

**Employment Type Breakdown:**
- **Employees:** PAYE/salary workers. Income from ASHE 2023 survey. ~87% of UK workforce.
- **Self-employed:** Sole traders, partnerships, unincorporated. Income from HMRC Self Assessment data. ~13% of UK workforce.
- **Business owners:** Incorporated companies. Data from HMRC Corporation Tax Liabilities (separate analysis).
- **Any:** Blends employee + self-employed income distributions by employment type prevalence.

**Self-Employment Rates by Age:**
- 18–24: 5–6% self-employed
- 25–34: 9–12% self-employed
- 35–44: 12–16% self-employed
- 45–54: 14–18% self-employed
- 55–64: 17–21% self-employed
- 65+: 28–35% self-employed (many continue past pension age)

**Calculation Pipeline:**
1. Start with adults in age band + ethnicity + gender (Census 2021)
2. Apply employment rate (ONS LFS 2023) — only employed people earn income
3. Apply age-specific single rate (ONS F&H 2022) — varies by age
4. Split by employment type (ONS self-employment rates)
5. Apply income probability by type:
   - Employees: ASHE 2023 distribution
   - Self-employed: HMRC Self Assessment distribution

**Example:** Black Caribbean single females, ages 33–35, Self-employed
- Adults: 52.6M × 1.0% ethnicity × 50.8% female × age share = ~X
- Employed: X × ~78% employment rate (females 35–44) = ~Y
- Single: Y × 32% single rate (age 35–44) = ~Z
- Self-employed: Z × ~12% self-employment rate = ~W
- Earning £75k+: W × ~8% (self-employed distribution) = final count

**Key Differences (Employees vs Self-employed):**
- Self-employed have higher proportion earning below £20k (35-42% vs 25-32%)
- Self-employed have higher proportion earning above £150k (higher max earnings potential)
- More volatile earnings; HMRC data captures tax-declared income only
- Age 65+: Self-employment rate 3-7x higher (working past pension age)

**Coverage:** 
- Employee earnings: ASHE 2023 (ONS sample survey)
- Self-employed: HMRC Self Assessment (tax returns, all self-employed with tax obligations)
- Excludes: Cash-in-hand work, informal employment, not yet registered self-employed
- Business owners (Ltd companies): Use separate Corporation Tax data if needed

**Age-based rates:** 
- Self-employment % varies 5% (age 18-24) to 35% (age 65+)
- Single % varies 78% (age 18-24) to 10% (age 65+)
- Employment varies by gender and family status"""
    )

    # Transparent data frame showing the inputs that feed the calculation
    calc_rows = [
        {
            "Step": "Age share of UK adults",
            "Value": f"{age_share * 100:.2f}%",
            "Data source / note": "ONS Census 2021 age distribution"
        },
        {
            "Step": "Ethnicity share (selected)",
            "Value": f"{ethnicity_share * 100:.2f}%",
            "Data source / note": "Census 2021 ethnicity split"
        },
        {
            "Step": "Gender share",
            "Value": f"{gender_share * 100:.2f}%",
            "Data source / note": "Census 2021 gender split"
        },
        {
            "Step": "Adults in slice",
            "Value": f"{total_adults:,}",
            "Data source / note": "UK adults 18+ = 52.6M"
        },
        {
            "Step": "Employment rate (age × gender)",
            "Value": f"{employment_rate_used * 100:.2f}%",
            "Data source / note": "ONS Labour Force Survey 2023"
        },
        {
            "Step": "Employed count",
            "Value": f"{total_employed:,}",
            "Data source / note": "Adults × employment rate"
        },
        {
            "Step": "Single rate (age-specific)",
            "Value": f"{single_rate * 100:.2f}%",
            "Data source / note": "ONS Families & Households 2022"
        },
        {
            "Step": "Single & employed",
            "Value": f"{total_population_single:,}",
            "Data source / note": "Employed × single rate"
        },
        {
            "Step": "Self-employment rate",
            "Value": f"{self_emp_rate_used * 100:.2f}%",
            "Data source / note": "ONS self-employment rates 2023"
        },
        {
            "Step": "Single employees",
            "Value": f"{single_employees:,}",
            "Data source / note": "Single employed × (1 - self-employment)"
        },
        {
            "Step": "Single self-employed",
            "Value": f"{single_self_employed:,}",
            "Data source / note": "Single employed × self-employment"
        },
        {
            "Step": "Income probability (employees)",
            "Value": f"{employee_income_prob * 100:.2f}%",
            "Data source / note": "ASHE 2023 employee income distribution"
        },
        {
            "Step": "Income probability (self-employed)",
            "Value": f"{self_employed_income_prob * 100:.2f}%",
            "Data source / note": "HMRC Self Assessment income distribution"
        },
        {
            "Step": "Expected earning threshold",
            "Value": f"{total_matches:,}",
            "Data source / note": "Income probability × relevant group"
        },
        {
            "Step": "Share of single employed hitting threshold",
            "Value": f"{share_pct:.2f}%",
            "Data source / note": "Total earning ÷ single employed"
        },
    ]

    calc_df = pd.DataFrame(calc_rows)

    st.subheader("Calculation Inputs & Data Used")
    st.dataframe(calc_df, hide_index=True, use_container_width=True)
    st.markdown(
        "This table shows the exact inputs applied in order: age share → ethnicity share → gender split → employment → single rate → self-employment split → income probabilities. Employee income uses ASHE 2023 survey data; self-employed income uses HMRC Self Assessment. Counts are rounded to whole people for readability."
    )

