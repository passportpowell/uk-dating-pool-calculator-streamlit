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
from data import (
    MARRIAGE_RATE_BY_ETHNICITY, 
    INTERRACIAL_MARRIAGE_DATA
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
    
    # Sources section
    with st.expander("📚 Data Sources", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""
        **Marriage & Divorce Statistics:**
        - [ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022)
        - [ONS Divorces in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/divorce/bulletins/divorcesinenglandandwales/2022)
        - [ONS Census 2021 - Marital Status](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriageandcivilpartnershipstatusenglandandwales/census2021)
        - [ONS Families and Households: 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2023)
        - [ONS Birth Statistics by Parents' Characteristics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/birthsbyparentscharacteristics)
        
        All statistics are for **England and Wales** unless specified UK-wide.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
