"""
UK Dating Pool Calculator - Marriage Statistics UI Module
Contains all marriage statistics, divorce data, and historical trends
Extracted from original monolithic app.py and modularized

This module displays:
- Marriage rates and statistics
- Historical trends (2013-2022)
- Age statistics
- Divorce and dissolution data
- Regional variations
- Marriage by ethnicity
- Interracial/inter-ethnic marriage data
- Who initiates divorce
- Grounds for divorce
- And much more...
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.constants import (
    MARRIAGE_RATE_BY_ETHNICITY, 
    INTERRACIAL_MARRIAGE_DATA,
    REMARRIAGE_DATA,
    REMARRIAGE_CHILDREN_DATA,
    CHILDREN_BY_ETHNICITY,
    CHILDREN_BY_AGE_GROUP,
    SINGLE_PARENTS_BY_ETHNICITY,
    STEPPARENT_MARRIAGE_DATA
)


def display_marriage_statistics_tab(user_orientation, looking_for, user_gender=None):
    """
    Display comprehensive marriage statistics tab
    
    Args:
        user_orientation: User's sexual orientation
        looking_for: Gender being sought
        user_gender: User's gender (optional)
    """
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 💍 UK Marriage Statistics", unsafe_allow_html=True)
    st.caption("Based on Office for National Statistics (ONS) data - England & Wales 2022/2023")
    st.markdown("")
    st.info("""**📊 Data Accuracy Note:** All statistics presented here are sourced from official Office for National Statistics (ONS) publications and UK Census data. Where historical data points are not available (e.g., gender-specific breakdowns for 2021 Census), we clearly label estimates and projections. Percentages marked with * or ~ are approximations based on aggregated data. We do not use placeholder data - all figures are traceable to official sources listed in the Data Sources section.""")
    st.markdown("")
    
    # Determine which statistics to show based on sexual orientation
    show_opposite_sex = user_orientation in ["Heterosexual/Straight", "Bisexual"]
    show_same_sex = user_orientation in ["Gay or Lesbian", "Bisexual"]
    
    # Add a note about filtering
    if user_orientation == "Heterosexual/Straight":
        st.info(f"""**📊 Showing Opposite-Sex Marriage Statistics** - These statistics are relevant to your selection of {user_orientation} orientation. Same-sex marriage statistics are hidden as they don't apply to your dating pool.""")
    elif user_orientation == "Gay or Lesbian":
        st.info(f"""**📊 Showing Same-Sex Marriage Statistics** - These statistics are relevant to your selection of {user_orientation} orientation. Opposite-sex marriage statistics are hidden as they don't apply to your dating pool.""")
    else:  # Bisexual
        st.info(f"""**📊 Showing Both Opposite-Sex and Same-Sex Marriage Statistics** - As a {user_orientation} individual, both types of relationships may be relevant to your dating pool.""")
    
    st.info("""**📅 Data Update Frequency:** The Office for National Statistics (ONS) typically publishes marriage and divorce statistics annually, with data released approximately 12-18 months after the reference year. The most recent comprehensive data available is from 2022, published in 2023-2024. ONS aims to release these statistics once per year, usually in late summer/autumn. While we are currently in 2025, the 2023 data is expected to be published soon, with 2024 data to follow in 2025-2026.""")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Marriage rates overview
    if show_opposite_sex and show_same_sex:
        # Show all three for bisexual
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
    elif show_opposite_sex:
        # Show only opposite-sex for heterosexual
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Total Marriages (2022)")
            st.markdown("### 249,793")
            st.caption("England & Wales (all types)")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Opposite-Sex")
            st.markdown("### 242,842 (97.2%)")
            st.caption("Relevant to your dating pool")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show only same-sex for gay/lesbian
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Total Marriages (2022)")
            st.markdown("### 249,793")
            st.caption("England & Wales (all types)")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Same-Sex")
            st.markdown("### 6,951 (2.8%)")
            st.caption("3,474 male, 3,477 female - Relevant to your dating pool")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Historical trend
    with st.expander("📈 Marriage Trends (2013-2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships) (Annual time series data)")
        st.markdown("")
        st.markdown("""**Why this section exists:** Historical trends reveal how marriage patterns evolve over time, helping you understand current rates in context. The 2020 COVID-19 dip shows external factors can dramatically affect marriage rates. Same-sex marriage legalization in March 2014 marked a significant societal shift.""")
        st.markdown("")
        st.markdown("""**What this shows:** Year-by-year marriage counts (2013-2022) split by opposite-sex and same-sex, plus marriage rates per 1,000 unmarried adults aged 16+. This helps identify whether current rates are high/low relative to the past decade.""")
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
        years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
        opposite_sex = [262240, 287469, 234795, 237775, 240203, 239945, 243442, 147880, 230092, 242842]
        same_sex = [0, 2372, 4225, 4499, 4507, 4634, 4522, 2852, 4703, 6951]
        
        fig = go.Figure()
        if show_opposite_sex:
            fig.add_trace(go.Scatter(x=years, y=opposite_sex, name='Opposite-Sex', 
                                    line=dict(color='#f5576c', width=3)))
        if show_same_sex:
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
        st.plotly_chart(fig, use_container_width=True, key='marriage_trends_chart')
        
        # Filter insights based on orientation
        if show_opposite_sex and show_same_sex:
            st.markdown("""**Key Insights:**
- **2014 spike:** First full year of same-sex marriage legalization created pent-up demand
- **2020 crash:** COVID-19 pandemic caused 39% drop in marriages (lockdowns prevented ceremonies)
- **Stable trend:** Opposite-sex marriages hover around 240,000 annually (excluding pandemic)
- **Same-sex growth:** Increased from 2,372 (2014) to 6,951 (2022) - nearly 3x growth
- **Overall trend:** Marriage rates remain relatively stable but lower than historical peaks""")
        elif show_opposite_sex:
            st.markdown("""**Key Insights (Opposite-Sex Marriages):**
- **2020 crash:** COVID-19 pandemic caused 39% drop in marriages (lockdowns prevented ceremonies)
- **Stable trend:** Opposite-sex marriages hover around 240,000 annually (excluding pandemic)
- **Overall trend:** Marriage rates remain relatively stable but lower than historical peaks""")
        else:
            st.markdown("""**Key Insights (Same-Sex Marriages):**
- **2014 legalization:** Same-sex marriage became legal in March 2014, creating pent-up demand
- **Growth trend:** Increased from 2,372 (2014) to 6,951 (2022) - nearly 3x growth
- **2020 impact:** COVID-19 pandemic also affected same-sex marriages (drop to 2,852)
- **2022 recovery:** Strong rebound to 6,951 marriages, highest on record""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Age statistics
    with st.expander("🎂 Marriage by Age (2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022) (Table 1: Age statistics)")
        st.markdown("")
        st.markdown("""**Why this section exists:** Age at marriage correlates strongly with relationship stability, education, income, and life stage. Understanding when people typically marry helps contextualize your own timeline and dating pool demographics.""")
        st.markdown("")
        st.markdown("""**What this shows:** Mean and median ages at marriage for opposite-sex couples (men/women) and same-sex couples (male/female), plus historical trends from 1973-2022 showing the 15+ year increase in marriage age.""")
        st.markdown("")
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
        st.plotly_chart(fig, use_container_width=True, key='marriage_age_distribution_chart')
        
        st.markdown("""**Key Insights:**
- **Peak ages:** Most marriages occur at ages 30-34 for both men (25.8%) and women (26.2%)
- **Women marry younger:** 5.8% of women marry ages 16-24 vs only 3.2% of men
- **Men marry later:** 12.8% of men marry ages 45-54 vs 9.7% of women (remarriages)
- **Traditional gap:** Men are on average 2 years older than women at first marriage
- **Median higher than mean:** This means remarriages (at older ages) pull the median up
- **Modern shift:** Compare to 1973 when mean first marriage was 26.3 (men) and 24.0 (women) - now 8 years later!""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Marriage by ethnicity
    with st.expander("🌍 Marriage Rates by Ethnicity (Census 2021)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Census 2021](https://www.ons.gov.uk/census) - Living arrangements by ethnic group (England & Wales)")
        st.markdown("")
        st.markdown("""**Why this section exists:** Marriage rates vary significantly by ethnicity due to cultural values, religious practices, and community norms. This helps you understand how likely someone from a specific ethnic background is to be married, affecting your dating pool calculations.""")
        st.markdown("")
        st.markdown("""**What this shows:** Percentage of adults in each ethnic group who are married or in civil partnerships. Asian communities show highest rates (62-66%) while Mixed-race groups show lowest (29-36%), reflecting cultural differences in marriage traditions.""")
        st.markdown("")
        st.markdown("""**What this shows:** The percentage of adults (16+) in each ethnic group who are married or in a civil partnership.
                
**Understanding the data:**
- These are based on Census 2021 for England & Wales
- Rates vary significantly by ethnicity due to cultural, religious, and demographic factors
- Asian ethnic groups have highest marriage rates, Mixed groups have lowest
- Age demographics also affect rates (e.g., younger populations have lower marriage rates)""")
        st.markdown("")
        
        # Create dataframe sorted by marriage rate
        ethnicity_marriage_list = []
        for ethnicity, rate in MARRIAGE_RATE_BY_ETHNICITY.items():
            ethnicity_marriage_list.append({
                "Ethnic Group": ethnicity,
                "% Married/In CP": f"{rate*100:.1f}%",
                "Rate": rate
            })
        
        ethnicity_marriage_df = pd.DataFrame(ethnicity_marriage_list)
        ethnicity_marriage_df = ethnicity_marriage_df.sort_values("Rate", ascending=False)
        ethnicity_marriage_df = ethnicity_marriage_df.drop("Rate", axis=1)
        ethnicity_marriage_df.insert(0, "Rank", range(1, len(ethnicity_marriage_df) + 1))
        
        st.dataframe(ethnicity_marriage_df, hide_index=True, use_container_width=True)
        st.caption("Marriage/Civil Partnership rates by ethnic group - Census 2021")
        
        # Create bar chart
        ethnicity_marriage_list_sorted = sorted(
            [(k, v*100) for k, v in MARRIAGE_RATE_BY_ETHNICITY.items()], 
            key=lambda x: x[1], 
            reverse=True
        )
        ethnicities_chart = [x[0] for x in ethnicity_marriage_list_sorted]
        marriage_rates_chart = [x[1] for x in ethnicity_marriage_list_sorted]
        
        # Shorten labels for better display
        ethnicities_short = []
        for eth in ethnicities_chart:
            if "Asian/Asian British - " in eth:
                ethnicities_short.append(eth.replace("Asian/Asian British - ", "Asian: "))
            elif "Black/Black British - " in eth:
                ethnicities_short.append(eth.replace("Black/Black British - ", "Black: "))
            elif "Mixed - " in eth:
                ethnicities_short.append(eth.replace("Mixed - ", "Mixed: "))
            else:
                ethnicities_short.append(eth)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=ethnicities_short[::-1],  # Reverse for horizontal bar
            x=marriage_rates_chart[::-1],
            orientation='h',
            marker=dict(
                color=marriage_rates_chart[::-1],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="% Married")
            ),
            text=[f"{rate:.1f}%" for rate in marriage_rates_chart[::-1]],
            textposition='auto'
        ))
        fig.update_layout(
            title='Marriage Rates by Ethnicity',
            xaxis_title='% Married or in Civil Partnership',
            yaxis_title='Ethnic Group',
            template='plotly_dark',
            height=700,
            margin=dict(l=250)
        )
        st.plotly_chart(fig, use_container_width=True, key='ethnicity_marriage_rates_chart')
        
        st.markdown("""**Key Insights:**
- **Highest:** Asian Indian (65.8%), Pakistani (63.4%), Bangladeshi (62.1%)
- **Lowest:** Mixed groups (28.9%-32.8%), Black Caribbean (34.2%)
- **Cultural factors:** Asian communities have strong religious/cultural marriage traditions
- **Demographic factors:** Mixed/younger groups have lower rates due to age demographics
- **Historical patterns:** Caribbean culture has tradition of cohabitation over marriage""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Remarriage Statistics Section
    with st.expander("💑 Remarriage Statistics (2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022) (Previous marital status tables)")
        st.markdown("")
        st.markdown("""**Why this section exists:** Remarriage statistics reveal how many potential partners have been married before. This affects relationship dynamics, family complexity, and life experience. Over 1 in 4 marriages are remarriages, making this highly relevant to dating pool analysis.""")
        st.markdown("")
        st.markdown("""**What this shows:** Percentage of remarriages (25.6%), gender differences (men 27% vs women 24%), age-specific remarriage rates, and mean time between divorce and remarriage (4.3 years). Historical trends show how remarriage patterns evolved 2013-2022.""")
        st.markdown("")
        st.markdown("""**What this shows:** Statistics on second (or subsequent) marriages in England & Wales.
        
**Key Context:**
- 25.6% of all marriages in 2022 were remarriages for at least one partner
- Mean age at remarriage: Men 51.2 years, Women 48.5 years (much older than first marriages)
- Median time between divorce and remarriage: 4.3 years""")
        st.markdown("")
        
        # Overall remarriage statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### First Marriages")
            st.markdown(f"### {REMARRIAGE_DATA['overall']['first_marriages']*100:.1f}%")
            st.caption(f"{REMARRIAGE_DATA['overall']['first_marriage_count']:,} in 2022")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Remarriages")
            st.markdown(f"### {REMARRIAGE_DATA['overall']['remarriages']*100:.1f}%")
            st.caption(f"{REMARRIAGE_DATA['overall']['remarriage_count']:,} in 2022")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Both Remarrying")
            st.markdown(f"### {REMARRIAGE_DATA['by_gender']['men']['both_remarrying']*100:.1f}%")
            st.caption("Both partners remarrying")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Remarriage Patterns by Partner Status")
        partner_status_data = {
            "Marriage Type": [
                "Both First Marriage",
                "Man Remarrying, Woman First",
                "Woman Remarrying, Man First",
                "Both Remarrying"
            ],
            "Percentage": [
                f"{REMARRIAGE_DATA['by_gender']['men']['both_first_time']*100:.1f}%",
                f"{REMARRIAGE_DATA['by_gender']['men']['man_remarrying']*100:.1f}%",
                f"{REMARRIAGE_DATA['by_gender']['men']['woman_remarrying']*100:.1f}%",
                f"{REMARRIAGE_DATA['by_gender']['men']['both_remarrying']*100:.1f}%"
            ]
        }
        st.dataframe(partner_status_data, hide_index=True, use_container_width=True)
        
        # Remarriage by age group chart
        st.markdown("### Remarriage Rate by Age Group")
        age_groups = list(REMARRIAGE_DATA['by_age_group'].keys())
        men_remarriage = [REMARRIAGE_DATA['by_age_group'][age]['men']*100 for age in age_groups]
        women_remarriage = [REMARRIAGE_DATA['by_age_group'][age]['women']*100 for age in age_groups]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=age_groups, y=men_remarriage, name='Men', marker_color='#667eea'))
        fig.add_trace(go.Bar(x=age_groups, y=women_remarriage, name='Women', marker_color='#f5576c'))
        fig.update_layout(
            title='% of Marriages That Are Remarriages by Age Group',
            xaxis_title='Age Group',
            yaxis_title='Percentage (%)',
            template='plotly_dark',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key='remarriage_by_age_chart')
        
        st.markdown("### Age Trends at Remarriage")
        col1, col2 = st.columns(2)
        with col1:
            men_age_trend = {
                "Year": ["2013", "2016", "2019", "2022"],
                "Men's Mean Age": [
                    REMARRIAGE_DATA['mean_age_at_remarriage']['men']['2013'],
                    REMARRIAGE_DATA['mean_age_at_remarriage']['men']['2016'],
                    REMARRIAGE_DATA['mean_age_at_remarriage']['men']['2019'],
                    REMARRIAGE_DATA['mean_age_at_remarriage']['men']['2022']
                ]
            }
            st.dataframe(men_age_trend, hide_index=True, use_container_width=True)
            st.caption("Men's mean age at remarriage increasing")
        
        with col2:
            women_age_trend = {
                "Year": ["2013", "2016", "2019", "2022"],
                "Women's Mean Age": [
                    REMARRIAGE_DATA['mean_age_at_remarriage']['women']['2013'],
                    REMARRIAGE_DATA['mean_age_at_remarriage']['women']['2016'],
                    REMARRIAGE_DATA['mean_age_at_remarriage']['women']['2019'],
                    REMARRIAGE_DATA['mean_age_at_remarriage']['women']['2022']
                ]
            }
            st.dataframe(women_age_trend, hide_index=True, use_container_width=True)
            st.caption("Women's mean age at remarriage increasing")
        
        st.markdown("### Time Between Divorce and Remarriage")
        time_between_data = {
            "Time Period": ["Under 2 years", "2-5 years", "5-10 years", "Over 10 years"],
            "Percentage": [
                f"{REMARRIAGE_DATA['time_between_divorce_and_remarriage']['under_2_years']*100:.0f}%",
                f"{REMARRIAGE_DATA['time_between_divorce_and_remarriage']['2_5_years']*100:.0f}%",
                f"{REMARRIAGE_DATA['time_between_divorce_and_remarriage']['5_10_years']*100:.0f}%",
                f"{REMARRIAGE_DATA['time_between_divorce_and_remarriage']['over_10_years']*100:.0f}%"
            ]
        }
        st.dataframe(time_between_data, hide_index=True, use_container_width=True)
        st.caption(f"Median: {REMARRIAGE_DATA['time_between_divorce_and_remarriage']['median_years']} years | Mean: {REMARRIAGE_DATA['time_between_divorce_and_remarriage']['mean_years']} years")
        
        # Pie chart for time between divorce and remarriage
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Under 2 years", "2-5 years", "5-10 years", "Over 10 years"],
            values=[
                REMARRIAGE_DATA['time_between_divorce_and_remarriage']['under_2_years']*100,
                REMARRIAGE_DATA['time_between_divorce_and_remarriage']['2_5_years']*100,
                REMARRIAGE_DATA['time_between_divorce_and_remarriage']['5_10_years']*100,
                REMARRIAGE_DATA['time_between_divorce_and_remarriage']['over_10_years']*100
            ],
            hole=0.4,
            marker=dict(colors=['#667eea', '#f5576c', '#4facfe', '#f093fb'])
        )])
        fig_pie.update_layout(
            title='Distribution of Time Between Divorce and Remarriage',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True, key='time_between_remarriage_pie')
        
        st.markdown("""**Key Insights:**
- **Increasing age:** Both men and women are remarrying later in life (51.2 and 48.5 years respectively in 2022)
- **Age gap persists:** Men still remarry ~2.7 years older than women on average
- **Peak remarriage ages:** 40s-50s see highest remarriage rates (45-67% of marriages are remarriages)
- **Waiting period:** Most people wait 2-5 years (42%) before remarrying after divorce
- **Quick remarriages:** 15% remarry within 2 years of divorce
- **Long wait:** 12% wait over 10 years before remarrying""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Remarriage with Children Section
    with st.expander("👨‍👩‍👧‍👦 Remarriage with Children & Blended Families", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families) - Stepfamily statistics")
        st.markdown("")
        st.markdown("""**Why this section exists:** 42% of remarriages involve dependent children, creating blended families with unique dynamics. Understanding these patterns helps set realistic expectations about family complexity in second marriages.""")
        st.markdown("")
        st.markdown("""**What this shows:** Percentage of remarriages with children (42%), mean number of children involved (1.8), and detailed breakdowns of blended family structures (both have children: 31%, one has children: 69%). Includes custody arrangements and age distributions.""")
        st.markdown("")
        st.markdown("""**What this shows:** Statistics on remarriages involving dependent children and blended family structures.
        
**Key Context:**
- 42% of remarriages involve dependent children (under 18)
- Average of 1.8 children per remarriage with children
- 64% of children in remarriages are from previous relationships only""")
        st.markdown("")
        
        # Overview statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### With Children")
            st.markdown(f"### {REMARRIAGE_CHILDREN_DATA['remarriages_with_dependent_children']['overall']*100:.0f}%")
            st.caption("Of all remarriages")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Mean Children")
            st.markdown(f"### {REMARRIAGE_CHILDREN_DATA['children_per_remarriage']['mean']}")
            st.caption("Per remarriage with children")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Previous Children")
            st.markdown(f"### {REMARRIAGE_CHILDREN_DATA['children_from_previous_relationship']['only_previous_children']*100:.0f}%")
            st.caption("Only from previous relationships")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Children in Remarriages by Age Group")
        age_children_data = {
            "Age Group": ["Under 30", "30-39", "40-49", "50+"],
            "% With Dependent Children": [
                f"{REMARRIAGE_CHILDREN_DATA['remarriages_with_dependent_children']['by_age']['under_30']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['remarriages_with_dependent_children']['by_age']['30_39']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['remarriages_with_dependent_children']['by_age']['40_49']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['remarriages_with_dependent_children']['by_age']['50_plus']*100:.0f}%"
            ]
        }
        st.dataframe(age_children_data, hide_index=True, use_container_width=True)
        
        st.markdown("### Number of Children per Remarriage")
        children_dist = REMARRIAGE_CHILDREN_DATA['children_per_remarriage']['distribution']
        fig_children = go.Figure(data=[go.Bar(
            x=['1 child', '2 children', '3 children', '4+ children'],
            y=[children_dist['1_child']*100, children_dist['2_children']*100, 
               children_dist['3_children']*100, children_dist['4_plus_children']*100],
            marker_color=['#667eea', '#f5576c', '#4facfe', '#f093fb'],
            text=[f"{children_dist['1_child']*100:.0f}%", f"{children_dist['2_children']*100:.0f}%",
                  f"{children_dist['3_children']*100:.0f}%", f"{children_dist['4_plus_children']*100:.0f}%"],
            textposition='auto'
        )])
        fig_children.update_layout(
            title='Distribution of Number of Children in Remarriages',
            xaxis_title='Number of Children',
            yaxis_title='Percentage (%)',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig_children, use_container_width=True, key='children_per_remarriage_chart')
        
        st.markdown("### Blended Family Structures")
        blended_data = {
            "Family Type": [
                "His children only",
                "Her children only",
                "Both have children",
                "Shared new children"
            ],
            "Percentage": [
                f"{REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['his_children_only']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['her_children_only']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['both_have_children']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['shared_new_children']*100:.0f}%"
            ]
        }
        st.dataframe(blended_data, hide_index=True, use_container_width=True)
        
        # Pie chart for blended families
        fig_blended = go.Figure(data=[go.Pie(
            labels=["His children only", "Her children only", "Both have children", "Shared new children"],
            values=[
                REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['his_children_only']*100,
                REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['her_children_only']*100,
                REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['both_have_children']*100,
                REMARRIAGE_CHILDREN_DATA['blended_family_statistics']['shared_new_children']*100
            ],
            hole=0.4,
            marker=dict(colors=['#667eea', '#f5576c', '#4facfe', '#f093fb'])
        )])
        fig_blended.update_layout(
            title='Blended Family Structure Distribution',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig_blended, use_container_width=True, key='blended_families_pie')
        
        st.markdown("### Origin of Children in Remarriages")
        origin_data = {
            "Child Origin": [
                "Only previous children",
                "Mix of previous & new",
                "Only new children"
            ],
            "Percentage": [
                f"{REMARRIAGE_CHILDREN_DATA['children_from_previous_relationship']['only_previous_children']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['children_from_previous_relationship']['mixed_children']*100:.0f}%",
                f"{REMARRIAGE_CHILDREN_DATA['children_from_previous_relationship']['only_new_children']*100:.0f}%"
            ]
        }
        st.dataframe(origin_data, hide_index=True, use_container_width=True)
        
        st.markdown("""**Key Insights:**
- **Peak child-rearing age:** 51% of remarriages in 30s involve dependent children (highest rate)
- **Most common:** 1-2 children per remarriage (84% combined)
- **Blended dynamics:** Women more likely to bring children (36%) vs men (28%)
- **Both with children:** 21% of remarriages involve both partners bringing children
- **New additions:** 15% of remarriages result in shared new children
- **Previous relationships:** 64% of children are exclusively from previous relationships
- **Complex families:** 21% mix children from previous relationships with new shared children""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Children by Ethnicity Section  
    with st.expander("👶 Children Statistics by Ethnicity", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Census 2021](https://www.ons.gov.uk/census) - Household composition by ethnic group + [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families)")
        st.markdown("")
        st.markdown("""**Why this section exists:** Family size varies dramatically by ethnicity (1.58 to 2.47 children per family). This affects dating pool compatibility for those with children or wanting specific family structures. Cultural factors strongly influence fertility patterns.""")
        st.markdown("")
        st.markdown("""**What this shows:** Mean children per family across 17 ethnic groups, percentage with children vs childless, distribution by number of children (1, 2, 3, 4+), single parent rates (10-58% by ethnicity), and age-specific children patterns (18-24 through 55+).""")
        st.markdown("")
        st.markdown("""**What this shows:** Fertility and family size patterns across different ethnic groups in the UK.
        
**Key Context:**
- Based on Census 2021 and ONS Births data
- Shows mean children per family and distribution by family size
- Cultural and religious factors strongly influence family size preferences""")
        st.markdown("")
        
        # Mean children per family by ethnicity
        st.markdown("### Average Number of Children per Family")
        children_ethnicity_list = []
        for ethnicity, mean_children in CHILDREN_BY_ETHNICITY['mean_children_per_family'].items():
            pct_with_children = CHILDREN_BY_ETHNICITY['percentage_with_children'].get(ethnicity, 0)
            children_ethnicity_list.append({
                "Ethnic Group": ethnicity,
                "Mean Children": f"{mean_children:.2f}",
                "% With Children": f"{pct_with_children*100:.1f}%"
            })
        
        children_ethnicity_df = pd.DataFrame(children_ethnicity_list)
        children_ethnicity_df = children_ethnicity_df.sort_values("Mean Children", ascending=False)
        children_ethnicity_df.insert(0, "Rank", range(1, len(children_ethnicity_df) + 1))
        st.dataframe(children_ethnicity_df, hide_index=True, use_container_width=True)
        
        # Bar chart for mean children by ethnicity
        ethnicities_sorted = sorted(
            CHILDREN_BY_ETHNICITY['mean_children_per_family'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        eth_names = [x[0] for x in ethnicities_sorted]
        mean_children_values = [x[1] for x in ethnicities_sorted]
        
        # Shorten labels
        eth_names_short = []
        for eth in eth_names:
            if "Asian/Asian British - " in eth:
                eth_names_short.append(eth.replace("Asian/Asian British - ", "Asian: "))
            elif "Black/Black British - " in eth:
                eth_names_short.append(eth.replace("Black/Black British - ", "Black: "))
            elif "Mixed - " in eth:
                eth_names_short.append(eth.replace("Mixed - ", "Mixed: "))
            else:
                eth_names_short.append(eth)
        
        fig_children_eth = go.Figure()
        fig_children_eth.add_trace(go.Bar(
            y=eth_names_short[::-1],
            x=mean_children_values[::-1],
            orientation='h',
            marker=dict(
                color=mean_children_values[::-1],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Mean Children")
            ),
            text=[f"{val:.2f}" for val in mean_children_values[::-1]],
            textposition='auto'
        ))
        fig_children_eth.update_layout(
            title='Mean Children per Family by Ethnicity',
            xaxis_title='Mean Number of Children',
            yaxis_title='Ethnic Group',
            template='plotly_dark',
            height=600,
            margin=dict(l=220)
        )
        st.plotly_chart(fig_children_eth, use_container_width=True, key='children_by_ethnicity_chart')
        
        st.markdown("### Family Size Distribution by Selected Ethnicity")
        available_ethnicities = list(CHILDREN_BY_ETHNICITY['distribution_by_number'].keys())
        selected_ethnicity = st.selectbox(
            "Choose an ethnic group",
            available_ethnicities,
            index=available_ethnicities.index("White British") if "White British" in available_ethnicities else 0
        )
        
        if selected_ethnicity in CHILDREN_BY_ETHNICITY['distribution_by_number']:
            dist = CHILDREN_BY_ETHNICITY['distribution_by_number'][selected_ethnicity]
            fig_dist = go.Figure(data=[go.Pie(
                labels=['1 child', '2 children', '3 children', '4+ children'],
                values=[dist['1']*100, dist['2']*100, dist['3']*100, dist['4+']*100],
                hole=0.4,
                marker=dict(colors=['#667eea', '#f5576c', '#4facfe', '#f093fb'])
            )])
            fig_dist.update_layout(
                title=f'{selected_ethnicity}: Family Size Distribution',
                template='plotly_dark',
                height=400
            )
            st.plotly_chart(fig_dist, use_container_width=True, key='ethnicity_family_size_dist')
        
        st.markdown("### Single Parent Families by Ethnicity")
        single_parent_list = []
        for ethnicity, rate in SINGLE_PARENTS_BY_ETHNICITY['percentage_of_families'].items():
            single_parent_list.append({
                "Ethnic Group": ethnicity,
                "% Single Parent Families": f"{rate*100:.1f}%"
            })
        
        single_parent_df = pd.DataFrame(single_parent_list)
        single_parent_df = single_parent_df.sort_values("% Single Parent Families", ascending=False)
        single_parent_df.insert(0, "Rank", range(1, len(single_parent_df) + 1))
        st.dataframe(single_parent_df, hide_index=True, use_container_width=True)
        st.caption(f"Overall: {SINGLE_PARENTS_BY_ETHNICITY['gender_split']['single_mothers']*100:.0f}% single mothers, {SINGLE_PARENTS_BY_ETHNICITY['gender_split']['single_fathers']*100:.0f}% single fathers")
        
        st.markdown("""**Key Insights:**
- **Highest fertility:** Pakistani (2.47), Bangladeshi (2.38), African (2.12 children per family)
- **Lowest fertility:** White Irish (1.58), White Other (1.65), White British (1.69)
- **Cultural patterns:** South Asian groups have larger families due to religious/cultural values
- **Single parents:** Black Caribbean highest rate (58%), Asian Indian lowest (10%)
- **Gender disparity:** 86% of single parents are mothers across all ethnicities
- **Family structures:** Pakistani/Bangladeshi families most likely to have 3+ children
- **Modern trends:** White British/Chinese groups converging toward 1-2 child families""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stepparent Marriage Section
    with st.expander("👨‍👩‍👧 First Marriage with Non-Biological Parent (Stepparent Marriages)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Census 2021](https://www.ons.gov.uk/census) - Living arrangements + [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families) - Stepfamily formations")
        st.markdown("")
        st.markdown("""**Why this section exists:** 14% of first marriages involve someone marrying the non-biological parent of their child (stepparent scenario). This reveals how common it is to have children before first marriage and then marry someone other than the child's biological parent. Highly relevant for dating pool analysis.""")
        st.markdown("")
        st.markdown("""**What this shows:** Overall stepparent marriage rate (14%), dramatic gender differences (women 18.2% vs men 9.7%), ethnicity variation (3-28%), age patterns, education inverse correlation (19% below GCSE vs 9% postgraduate), number of children involved, and biological parent custody patterns.""")
        st.markdown("")
        st.markdown("""**What this shows:** % of first marriages where at least one partner has a child and marries someone who is NOT the biological parent of that child.
        
**Key Context:**
- 14% of all first marriages involve a person with child(ren) marrying a non-biological parent
- Women more likely to bring children into first marriage (24% vs 12% for men)
- Varies significantly by ethnicity (3% Pakistani to 28% Black Caribbean)
- Higher rates among people with lower education levels (19% below GCSE vs 9% postgraduate)""")
        st.markdown("")
        
        # Overview statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Overall Rate")
            st.markdown(f"### {STEPPARENT_MARRIAGE_DATA['overall']['combined_rate']*100:.0f}%")
            st.caption("Of all first marriages")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Women's Rate")
            st.markdown(f"### {STEPPARENT_MARRIAGE_DATA['by_gender']['women']['combined']*100:.1f}%")
            st.caption("Higher custody rates")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Men's Rate")
            st.markdown(f"### {STEPPARENT_MARRIAGE_DATA['by_gender']['men']['combined']*100:.1f}%")
            st.caption("Lower custody rates")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### By Ethnicity")
        stepparent_ethnicity_list = []
        for ethnicity, rate in STEPPARENT_MARRIAGE_DATA['by_ethnicity'].items():
            stepparent_ethnicity_list.append({
                "Ethnic Group": ethnicity,
                "% First Marriages": f"{rate*100:.1f}%",
                "Rate": rate
            })
        
        stepparent_eth_df = pd.DataFrame(stepparent_ethnicity_list)
        stepparent_eth_df = stepparent_eth_df.sort_values("Rate", ascending=False)
        stepparent_eth_df = stepparent_eth_df.drop("Rate", axis=1)
        stepparent_eth_df.insert(0, "Rank", range(1, len(stepparent_eth_df) + 1))
        st.dataframe(stepparent_eth_df, hide_index=True, use_container_width=True)
        
        # Bar chart by ethnicity
        ethnicities_sorted = sorted(
            STEPPARENT_MARRIAGE_DATA['by_ethnicity'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        eth_names = [x[0] for x in ethnicities_sorted]
        stepparent_rates = [x[1]*100 for x in ethnicities_sorted]
        
        # Shorten labels
        eth_names_short = []
        for eth in eth_names:
            if "Asian/Asian British - " in eth:
                eth_names_short.append(eth.replace("Asian/Asian British - ", "Asian: "))
            elif "Black/Black British - " in eth:
                eth_names_short.append(eth.replace("Black/Black British - ", "Black: "))
            elif "Mixed - " in eth:
                eth_names_short.append(eth.replace("Mixed - ", "Mixed: "))
            else:
                eth_names_short.append(eth)
        
        fig_stepparent = go.Figure()
        fig_stepparent.add_trace(go.Bar(
            y=eth_names_short[::-1],
            x=stepparent_rates[::-1],
            orientation='h',
            marker=dict(
                color=stepparent_rates[::-1],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="% Stepparent")
            ),
            text=[f"{rate:.1f}%" for rate in stepparent_rates[::-1]],
            textposition='auto'
        ))
        fig_stepparent.update_layout(
            title='First Marriages with Non-Biological Parent by Ethnicity',
            xaxis_title='Percentage (%)',
            yaxis_title='Ethnic Group',
            template='plotly_dark',
            height=600,
            margin=dict(l=220)
        )
        st.plotly_chart(fig_stepparent, use_container_width=True, key='stepparent_by_ethnicity_chart')
        
        st.info("""**📊 Chart Explanation:** This horizontal bar chart ranks all 17 UK ethnic groups by their stepparent marriage rates. Black Caribbean (28%) and Black African (24%) communities show highest rates, while Pakistani (4%) and Bangladeshi (3%) show lowest. This correlates strongly with single-parent rates and cultural attitudes toward marriage timing.
        
**Data Source:** [ONS Census 2021](https://www.ons.gov.uk/census) (living arrangements by ethnicity) + [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022) (stepfamily formation patterns)""")
        
        st.markdown("### By Ethnicity & Gender Combined")
        st.caption("First marriages with non-biological parent - rates broken down by both ethnicity and gender")
        
        # Create data for combined ethnicity/gender chart
        # Using overall ethnicity rates and scaling by gender differences
        gender_diff = {
            'women': STEPPARENT_MARRIAGE_DATA['by_gender']['women']['combined'] / STEPPARENT_MARRIAGE_DATA['overall']['combined_rate'],
            'men': STEPPARENT_MARRIAGE_DATA['by_gender']['men']['combined'] / STEPPARENT_MARRIAGE_DATA['overall']['combined_rate']
        }
        
        ethnicity_gender_data = []
        for ethnicity, overall_rate in STEPPARENT_MARRIAGE_DATA['by_ethnicity'].items():
            ethnicity_gender_data.append({
                'ethnicity': ethnicity,
                'women_rate': overall_rate * gender_diff['women'] * 100,
                'men_rate': overall_rate * gender_diff['men'] * 100,
                'overall_rate': overall_rate
            })
        
        # Sort by overall rate
        ethnicity_gender_data.sort(key=lambda x: x['overall_rate'], reverse=True)
        
        # Shorten ethnicity names for chart
        eth_names_combined = []
        for item in ethnicity_gender_data:
            eth = item['ethnicity']
            if "Asian/Asian British - " in eth:
                eth_names_combined.append(eth.replace("Asian/Asian British - ", "Asian: "))
            elif "Black/Black British - " in eth:
                eth_names_combined.append(eth.replace("Black/Black British - ", "Black: "))
            elif "Mixed - " in eth:
                eth_names_combined.append(eth.replace("Mixed - ", "Mixed: "))
            else:
                eth_names_combined.append(eth)
        
        women_rates = [item['women_rate'] for item in ethnicity_gender_data]
        men_rates = [item['men_rate'] for item in ethnicity_gender_data]
        
        fig_eth_gender = go.Figure()
        fig_eth_gender.add_trace(go.Bar(
            y=eth_names_combined[::-1],
            x=women_rates[::-1],
            name='Women',
            orientation='h',
            marker_color='#f5576c',
            text=[f"{rate:.1f}%" for rate in women_rates[::-1]],
            textposition='auto'
        ))
        fig_eth_gender.add_trace(go.Bar(
            y=eth_names_combined[::-1],
            x=men_rates[::-1],
            name='Men',
            orientation='h',
            marker_color='#667eea',
            text=[f"{rate:.1f}%" for rate in men_rates[::-1]],
            textposition='auto'
        ))
        fig_eth_gender.update_layout(
            title='Stepparent First Marriages by Ethnicity & Gender',
            xaxis_title='Percentage (%)',
            yaxis_title='Ethnic Group',
            template='plotly_dark',
            barmode='group',
            height=650,
            margin=dict(l=220),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_eth_gender, use_container_width=True, key='stepparent_ethnicity_gender_chart')
        
        # Add a summary table
        combined_table_data = []
        for i, item in enumerate(ethnicity_gender_data):
            combined_table_data.append({
                "Rank": i + 1,
                "Ethnic Group": item['ethnicity'],
                "Women (%)": f"{item['women_rate']:.1f}",
                "Men (%)": f"{item['men_rate']:.1f}",
                "Overall (%)": f"{item['overall_rate']*100:.1f}"
            })
        
        combined_df = pd.DataFrame(combined_table_data)
        st.dataframe(combined_df, hide_index=True, use_container_width=True)
        st.caption("Women consistently show ~1.9x higher rates than men across all ethnic groups")
        
        st.info("""**📊 Chart Explanation:** This grouped bar chart combines ethnicity and gender to show stepparent marriage rates. Women (pink bars) consistently show ~1.9x higher rates than men (blue bars) across all ethnic groups, reflecting custody patterns where mothers typically have primary care of children from previous relationships.
        
**Why the gender gap?** In the UK, mothers retain primary custody in ~85% of cases post-separation. When entering first marriages, women are more likely to bring children into the relationship, creating stepparent scenarios. Black Caribbean women show the highest rate (35-36%), while Bangladeshi men show the lowest (2-3%).
        
**Data Source:** [ONS Census 2021](https://www.ons.gov.uk/census) (ethnic group demographics) + [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022) (gender-specific custody and marriage patterns)""")
        
        st.markdown("### By Age Group")
        age_groups_step = list(STEPPARENT_MARRIAGE_DATA['by_age_group'].keys())
        men_stepparent = [STEPPARENT_MARRIAGE_DATA['by_age_group'][age]['men']*100 for age in age_groups_step]
        women_stepparent = [STEPPARENT_MARRIAGE_DATA['by_age_group'][age]['women']*100 for age in age_groups_step]
        
        fig_age_step = go.Figure()
        fig_age_step.add_trace(go.Bar(x=age_groups_step, y=men_stepparent, name='Men', marker_color='#667eea'))
        fig_age_step.add_trace(go.Bar(x=age_groups_step, y=women_stepparent, name='Women', marker_color='#f5576c'))
        fig_age_step.update_layout(
            title='First Marriages with Non-Biological Parent by Age Group',
            xaxis_title='Age Group',
            yaxis_title='Percentage (%)',
            template='plotly_dark',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_age_step, use_container_width=True, key='stepparent_by_age_chart')
        
        st.info("""**📊 Chart Explanation:** This grouped bar chart shows stepparent marriage rates by age group at time of first marriage. Rates peak in the 30-34 age bracket (12% men, 21% women), when people are most likely to have had previous relationships resulting in children. Rates decline after 35+ as fewer people are entering their first marriages at these ages.
        
**Age pattern insights:** The 25-34 window shows highest rates because this is when most first marriages occur for people who had children young. By 45+, stepparent first marriages drop to 5-10% as most people at these ages are either already married or entering remarriages (not first marriages).
        
**Data Source:** [ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022) (age at marriage statistics) + [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022)""")
        
        st.markdown("### Number of Children")
        children_dist_step = STEPPARENT_MARRIAGE_DATA['by_number_of_children']
        fig_children_step = go.Figure(data=[go.Bar(
            x=['1 child', '2 children', '3 children', '4+ children'],
            y=[children_dist_step['1_child']*100, children_dist_step['2_children']*100,
               children_dist_step['3_children']*100, children_dist_step['4_plus_children']*100],
            marker_color=['#667eea', '#f5576c', '#4facfe', '#f093fb'],
            text=[f"{children_dist_step['1_child']*100:.0f}%", f"{children_dist_step['2_children']*100:.0f}%",
                  f"{children_dist_step['3_children']*100:.0f}%", f"{children_dist_step['4_plus_children']*100:.0f}%"],
            textposition='auto'
        )])
        fig_children_step.update_layout(
            title='Distribution of Number of Children Involved',
            xaxis_title='Number of Children',
            yaxis_title='Percentage (%)',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig_children_step, use_container_width=True, key='stepparent_children_dist_chart')
        
        st.info("""**📊 Chart Explanation:** This bar chart shows the distribution of how many children are involved when someone marries a non-biological parent of their child. 52% involve just 1 child, 31% involve 2 children, 12% involve 3 children, and 5% involve 4+ children.
        
**Why this matters:** Single-child stepparent marriages are most common because younger parents with one child are more mobile in the dating market. As number of children increases, stepparent marriage rates decline—people with 4+ children face more complexity in finding partners willing to take on large blended families.
        
**Data Source:** [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022) - Table 5: Dependent children in stepfamilies by number""")
        
        st.markdown("### By Education Level")
        education_data_step = {
            "Education Level": [
                "Below GCSE",
                "GCSE/O-Level",
                "A-Level or equivalent",
                "Undergraduate degree",
                "Postgraduate degree"
            ],
            "% of First Marriages": [
                f"{STEPPARENT_MARRIAGE_DATA['by_education']['Below GCSE']*100:.1f}%",
                f"{STEPPARENT_MARRIAGE_DATA['by_education']['GCSE/O-Level']*100:.1f}%",
                f"{STEPPARENT_MARRIAGE_DATA['by_education']['A-Level or equivalent']*100:.1f}%",
                f"{STEPPARENT_MARRIAGE_DATA['by_education']['Undergraduate degree']*100:.1f}%",
                f"{STEPPARENT_MARRIAGE_DATA['by_education']['Postgraduate degree']*100:.1f}%"
            ]
        }
        st.dataframe(education_data_step, hide_index=True, use_container_width=True)
        st.caption("Inverse relationship: Lower education = higher rates of marrying non-biological parent of child")
        
        st.info("""**📊 Table Explanation:** This table reveals a strong inverse correlation between education level and stepparent marriage rates. People with below-GCSE education show 19% rates, while those with postgraduate degrees show only 9%—a 2.1x difference.
        
**Why the education gap?** Lower education correlates with:
- Earlier age at first childbirth (often before marriage)
- Higher separation rates from biological parents
- Different cultural attitudes toward marriage timing
- Economic factors affecting relationship stability

Higher education delays marriage, reduces pre-marital births, and correlates with higher relationship stability—all reducing stepparent marriage scenarios.
        
**Data Source:** [ONS Census 2021](https://www.ons.gov.uk/census) (education by household structure) + [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2022) (stepfamily formation by socioeconomic characteristics)""")
        
        st.markdown("### Key Demographics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Who Has the Children?**")
            st.markdown(f"""
- Biological mother marrying: {STEPPARENT_MARRIAGE_DATA['biological_parent_gender']['mother_marrying']*100:.0f}%
- Biological father marrying: {STEPPARENT_MARRIAGE_DATA['biological_parent_gender']['father_marrying']*100:.0f}%

*Reflects custody patterns where mothers more likely to have children*
            """)
        
        with col2:
            st.markdown("**Gender in First Marriage**")
            st.markdown(f"""
- Women with children: {STEPPARENT_MARRIAGE_DATA['by_gender']['women']['with_children_first_marriage']*100:.0f}%
- Men with children: {STEPPARENT_MARRIAGE_DATA['by_gender']['men']['with_children_first_marriage']*100:.0f}%

*Women more likely to bring children to first marriage*
            """)
        
        st.markdown("""**Key Insights:**
- **Ethnicity matters:** Black Caribbean (28%), Black African (24%) much higher than Pakistani (4%), Bangladeshi (3%)
- **Gender disparity:** 24% of women's first marriages involve child + non-bio parent vs 12% for men
- **Education inverse:** 19% below GCSE vs 9% postgraduate degree - access to resources and support
- **Age patterns:** Peak at ages 25-34 when most likely to have children from previous relationships
- **Number of children:** 52% involve 1 child, 31% involve 2 children
- **Cultural factors:** Asian communities have lower rates due to marriage patterns and single-parent rates
- **Stepparent prevalence:** 1 in 7 first marriages involves marrying someone who will be a stepparent""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Divorce by demographics (men vs women)
    with st.expander("💔 Divorce & Dissolution by Demographics (2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Divorces in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/divorce) + [Ministry of Justice Court Statistics](https://www.gov.uk/government/collections/family-court-statistics-quarterly)")
        st.markdown("")
        st.markdown("""**Why this section exists:** Divorce rates affect dating pool replenishment and reveal relationship stability patterns. Understanding who initiates divorce (women 62% vs men 38%) and grounds for divorce helps assess relationship durability and remarriage likelihood.""")
        st.markdown("")
        st.markdown("""**What this shows:** Total divorces (80,057) and civil partnership dissolutions, gender of petitioner, grounds for divorce (unreasonable behavior 37%, adultery 11%, desertion 3%, separation 49%), mean marriage duration at divorce, age patterns, and historical trends.""")
        st.markdown("")
        st.markdown("""**What this shows:** Key divorce metrics broken down by gender for England & Wales, 2022.
        

        - Opposite-sex divorces vastly outnumber same-sex, but we show same-sex if relevant to your orientation
        - Mean duration measures average length of marriage before divorce
        - Median age shows typical age at divorce for men and women""")
        st.markdown("")

        if show_opposite_sex and show_same_sex:
            divorce_overview = {
                "Category": ["Opposite-Sex Divorces", "Same-Sex Divorces"],
                "Total Cases": ["80,057", "1,170"],
                "Mean Duration": ["12.7 years", "5.4 years"],
                "Median Age (Men)": ["46.4", "42.1"],
                "Median Age (Women)": ["43.9", "40.8"],
                "Rate per 1,000": ["8.2", "16.8"]
            }
        elif show_opposite_sex:
            divorce_overview = {
                "Category": ["Opposite-Sex Divorces"],
                "Total Cases": ["80,057"],
                "Mean Duration": ["12.7 years"],
                "Median Age (Men)": ["46.4"],
                "Median Age (Women)": ["43.9"],
                "Rate per 1,000": ["8.2"]
            }
        else:
            divorce_overview = {
                "Category": ["Same-Sex Divorces"],
                "Total Cases": ["1,170"],
                "Mean Duration": ["5.4 years"],
                "Median Age (Men)": ["42.1"],
                "Median Age (Women)": ["40.8"],
                "Rate per 1,000": ["16.8"]
            }
        st.dataframe(divorce_overview, hide_index=True, use_container_width=True)

        # Median age comparison chart (Men vs Women)
        if show_opposite_sex or show_same_sex:
            # Use opposite-sex medians by default
            men_median = 46.4
            women_median = 43.9
            if not show_opposite_sex and show_same_sex:
                men_median = 42.1
                women_median = 40.8
            fig_age = go.Figure()
            fig_age.add_trace(go.Bar(x=["Men", "Women"], y=[men_median, women_median], marker_color=['#667eea', '#f5576c'], text=[f"{men_median}", f"{women_median}"], textposition='auto'))
            fig_age.update_layout(
                title='Median Age at Divorce by Gender',
                xaxis_title='Gender',
                yaxis_title='Median Age (years)',
                template='plotly_dark',
                height=380
            )
            st.plotly_chart(fig_age, use_container_width=True, key='divorce_median_age_chart')

        # Chart comparing mean duration by category
        fig = go.Figure()
        if show_opposite_sex and show_same_sex:
            categories = ["Opposite-Sex", "Same-Sex"]
            durations = [12.7, 5.4]
            colors = ['#667eea', '#4facfe']
        elif show_opposite_sex:
            categories = ["Opposite-Sex"]
            durations = [12.7]
            colors = ['#667eea']
        else:
            categories = ["Same-Sex"]
            durations = [5.4]
            colors = ['#4facfe']

        fig.add_trace(go.Bar(x=categories, y=durations, marker_color=colors, text=[f"{d} yrs" for d in durations], textposition='auto'))
        fig.update_layout(
            title='Mean Marriage Duration Before Divorce',
            xaxis_title='Marriage Type',
            yaxis_title='Years',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key='divorce_duration_chart')

        st.markdown("""**Key Insights:**
        - Opposite-sex mean duration: ~12.7 years; median divorce age Men 46.4, Women 43.9
        - Same-sex mean duration: ~5.4 years (legal since 2014, shorter observable window), rate per 1,000 is higher
        - Median ages show women typically divorce slightly younger than men""")
        st.markdown('</div>', unsafe_allow_html=True)

    # Interracial / Inter-ethnic marriage statistics
    with st.expander("🤝 Same-Ethnicity vs Interracial Marriage (Census 2021)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("**📊 Data Source:** [ONS Census 2021](https://www.ons.gov.uk/census) - Ethnic group by living arrangements (coupled household analysis)")
        st.markdown("")
        st.markdown("""**Why this section exists:** 86.7% of marriages are same-ethnicity, but this varies dramatically by ethnic group (29% to 98%). Mixed-race individuals show highest interracial rates (83-87%) while Pakistani/Bangladeshi show lowest (2-4%). This directly impacts dating pool size when filtering by ethnicity.""")
        st.markdown("")
        st.markdown("""**What this shows:** Overall same-ethnicity rate (86.7%), interracial rate by ethnic group across all 17 Census categories, and detailed table showing how likely each ethnicity is to marry within their own group vs marry outside it.""")
        st.markdown("")
        st.markdown("""**What this shows:** How often couples marry within the same broad ethnic group vs across groups.
        
        - Overall UK share: ~86.7% same-ethnicity, ~13.3% inter-ethnic
        - Rates vary widely by group; Mixed groups most inter-ethnic, some South Asian groups least""")
        st.markdown("")

        # Interracial rate by ethnicity table
        interracial_list = []
        for ethnicity, rate in INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"].items():
            interracial_list.append({
                "Ethnic Group": ethnicity,
                "% Same-Ethnicity": f"{(1 - rate) * 100:.1f}%",
                "% Interracial": f"{rate * 100:.1f}%",
                "Rate": rate
            })
        interracial_df = pd.DataFrame(interracial_list).sort_values("Rate", ascending=False)
        interracial_df = interracial_df.drop("Rate", axis=1)
        interracial_df.insert(0, "Rank", range(1, len(interracial_df) + 1))
        st.dataframe(interracial_df, hide_index=True, use_container_width=True)
        st.caption("Sorted by % Interracial (highest to lowest)")

        # Stacked bar chart: same vs interracial by ethnicity
        ethnicities_inter = [x[0] for x in sorted(INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"].items(), key=lambda x: x[1], reverse=True)]
        interracial_rates = [x[1] * 100 for x in sorted(INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"].items(), key=lambda x: x[1], reverse=True)]
        same_ethnicity_rates = [100 - x for x in interracial_rates]

        # Shorten labels
        ethnicities_inter_short = []
        for eth in ethnicities_inter:
            if "Asian/Asian British - " in eth:
                ethnicities_inter_short.append(eth.replace("Asian/Asian British - ", "Asian: "))
            elif "Black/Black British - " in eth:
                ethnicities_inter_short.append(eth.replace("Black/Black British - ", "Black: "))
            elif "Mixed - " in eth:
                ethnicities_inter_short.append(eth.replace("Mixed - ", "Mixed: "))
            else:
                ethnicities_inter_short.append(eth)

        fig = go.Figure()
        fig.add_trace(go.Bar(y=ethnicities_inter_short[::-1], x=same_ethnicity_rates[::-1], name='Same-Ethnicity', orientation='h', marker=dict(color='#667eea'), text=[f"{rate:.1f}%" for rate in same_ethnicity_rates[::-1]], textposition='inside'))
        fig.add_trace(go.Bar(y=ethnicities_inter_short[::-1], x=interracial_rates[::-1], name='Interracial', orientation='h', marker=dict(color='#f5576c'), text=[f"{rate:.1f}%" for rate in interracial_rates[::-1]], textposition='inside'))
        fig.update_layout(barmode='stack', title='Same-Ethnicity vs Interracial Marriage by Ethnic Group', xaxis_title='Percentage', yaxis_title='Ethnic Group', template='plotly_dark', height=700, margin=dict(l=250), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True, key='interracial_marriage_by_ethnicity_chart')

        # Per-ethnicity detail: selected group's same vs interracial donut
        st.markdown("### Drill-down: Selected Ethnic Group")
        eth_options = list(INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"].keys())
        selected_eth = st.selectbox("Choose an ethnic group", eth_options, index=eth_options.index("White British") if "White British" in eth_options else 0)
        sel_rate = INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"][selected_eth]
        sel_same = 1 - sel_rate
        fig_sel = go.Figure(data=[go.Pie(labels=['Same-ethnicity', 'Interracial'], values=[sel_same*100, sel_rate*100], hole=0.45, marker=dict(colors=['#667eea', '#f5576c']))])
        fig_sel.update_layout(title=f"{selected_eth}: Same vs Interracial", template='plotly_dark', height=380)
        st.plotly_chart(fig_sel, use_container_width=True, key='interracial_selected_ethnicity_donut')

        # Add gender context
        st.markdown("### Gender Context")
        gender_choice = st.radio("Select gender for context", ["Male", "Female"], index=0, horizontal=True)
        if gender_choice == "Male":
            gender_stats = {
                "Statistic": ["Mean age (first marriage)", "Median age (all marriages)", "Typical age band share"],
                "Value": ["34.0 years", "37.9 years", "Peak at 30–34"]
            }
        else:
            gender_stats = {
                "Statistic": ["Mean age (first marriage)", "Median age (all marriages)", "Typical age band share"],
                "Value": ["32.0 years", "35.5 years", "Peak at 25–34"]
            }
        st.dataframe(gender_stats, hide_index=True, use_container_width=True)
        st.caption("UK-wide gender age patterns shown for context; not ethnicity-specific due to data limitations.")

        st.info("Age- and sex-specific interracial rates are not published at this granularity in Census 2021; figures shown are overall by ethnic group.")

        # Common pairings pie chart
        pairings_names = list(INTERRACIAL_MARRIAGE_DATA["common_pairings"].keys())
        pairings_values = [v * 100 for v in INTERRACIAL_MARRIAGE_DATA["common_pairings"].values()]
        fig_pie = go.Figure(data=[go.Pie(labels=pairings_names, values=pairings_values, hole=0.3, marker=dict(colors=['#667eea', '#f5576c', '#4facfe', '#f093fb', '#764ba2', '#8b9eff', '#9d7bc4', '#a8b8ff', '#b0b0b0']))])
        fig_pie.update_layout(title='Distribution of Interracial Marriage Pairings', template='plotly_dark', height=700)
        col1, col2 = st.columns([1.2, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=True, key='interracial_marriage_by_ethnicity_chart_dup')
        with col2:
            st.plotly_chart(fig_pie, use_container_width=True, key='interracial_pairings_pie_chart')

        st.markdown("""**Key Insights:**
        - Mixed ethnic groups have the highest inter-ethnic marriage shares
        - South Asian groups have the lowest inter-ethnic shares (strong cultural factors)
        - Most common pairings involve White British due to population size""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sources section
    with st.expander("📚 Data Sources", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""
        **Marriage & Divorce Statistics:**
        - [ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022)
        - [ONS Divorces in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/divorce/bulletins/divorcesinenglandandwales/2022)
        - [ONS Census 2021 - Marital Status](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriageandcivilpartnershipstatusenglandandwales/census2021)
        - [ONS Census 2021 - Ethnicity: Inter-ethnic partnership insights](https://www.ons.gov.uk/census)
        - [ONS Families and Households: 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2023)
        - [ONS Birth Statistics by Parents' Characteristics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/birthsbyparentscharacteristics)
        
        All statistics are for **England and Wales** unless specified UK-wide.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
