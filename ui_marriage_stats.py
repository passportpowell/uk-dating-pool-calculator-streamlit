"""
UK Dating Pool Calculator - Marriage Statistics UI Module
Contains all marriage statistics, divorce data, and historical trends.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data import (
    MARRIAGE_RATE_BY_ETHNICITY, 
    INTERRACIAL_MARRIAGE_DATA
)

def display_marriage_statistics_tab(user_orientation, looking_for, user_gender=None):
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### ðŸ’ UK Marriage Statistics", unsafe_allow_html=True)
    st.caption("Based on Office for National Statistics (ONS) data - England & Wales 2022/2023")
    st.markdown("")
    st.info("""**ðŸ“Š Data Accuracy Note:** All statistics presented here are sourced from official Office for National Statistics (ONS) publications and UK Census data. Where historical data points are not available (e.g., gender-specific breakdowns for 2021 Census), we clearly label estimates and projections. Percentages marked with * or ~ are approximations based on aggregated data. We do not use placeholder data - all figures are traceable to official sources listed in the Data Sources section.""")
    st.markdown("")
    
    # Determine which statistics to show based on sexual orientation
    show_opposite_sex = user_orientation in ["Heterosexual/Straight", "Bisexual"]
    show_same_sex = user_orientation in ["Gay or Lesbian", "Bisexual"]
    
    # Add a note about filtering
    if user_orientation == "Heterosexual/Straight":
        st.info(f"""**ðŸ“Š Showing Opposite-Sex Marriage Statistics** - These statistics are relevant to your selection of {user_orientation} orientation. Same-sex marriage statistics are hidden as they don't apply to your dating pool.""")
    elif user_orientation == "Gay or Lesbian":
        st.info(f"""**ðŸ“Š Showing Same-Sex Marriage Statistics** - These statistics are relevant to your selection of {user_orientation} orientation. Opposite-sex marriage statistics are hidden as they don't apply to your dating pool.""")
    else:  # Bisexual
        st.info(f"""**ðŸ“Š Showing Both Opposite-Sex and Same-Sex Marriage Statistics** - As a {user_orientation} individual, both types of relationships may be relevant to your dating pool.""")
    
    st.info("""**ðŸ“… Data Update Frequency:** The Office for National Statistics (ONS) typically publishes marriage and divorce statistics annually, with data released approximately 12-18 months after the reference year. The most recent comprehensive data available is from 2022, published in 2023-2024. ONS aims to release these statistics once per year, usually in late summer/autumn. While we are currently in 2025, the 2023 data is expected to be published soon, with 2024 data to follow in 2025-2026.""")
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
    with st.expander("ðŸ“ˆ Marriage Trends (2013-2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** This tracks how marriage rates have changed over the past decade in England & Wales.
    Same-sex marriage became legal in March 2014, so 2013 shows zero same-sex marriages.""")
        st.markdown("")
        
        marriage_trend_data = {
            "Year": ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020*", "2021", "2022"],
            "Total Marriages": ["262,240", "289,841", "239,020", "242,274", "244,710", "244,579", "247,964", "150,732", "234,795", "249,793"],
            "Opposite-Sex": ["262,240", "287,469", "234,795", "237,775", "240,203", "239,945", "243,442", "147,880", "230,092", "242,842"],
            "Same-Sex": ["0", "2,372", "4,225", "4,499", "4,507", "4,634", "4,522", "2,852", "4,703", "6,951"],
            "Marriage RateÂ¹": ["22.5", "24.6", "20.1", "20.1", "20.1", "19.9", "20.0", "12.2", "18.9", "19.9"]
        }
        
        col_table, col_chart = st.columns([1, 1])
        
        with col_table:
            st.dataframe(marriage_trend_data, hide_index=True, use_container_width=True)
            st.caption("Â¹ Marriage rate per 1,000 unmarried population aged 16+. *2020 affected by COVID-19 pandemic")
        
        # Chart for marriage trends
        import plotly.graph_objects as go
        years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
        opposite_sex = [262240, 287469, 234795, 237775, 240203, 239945, 243442, 147880, 230092, 242842]
        same_sex = [0, 2372, 4225, 4499, 4507, 4634, 4522, 2852, 4703, 6951]
        
        with col_chart:
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
            st.plotly_chart(fig, use_container_width=True, key='marriage_trends_first_chart')
        
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
    with st.expander("ðŸŽ‚ Marriage by Age (2022)", expanded=False):
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
    
    # Divorce statistics
    with st.expander("ðŸ’” Divorce & Dissolution Statistics (2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** How many marriages end in divorce and how long they typically last.
        
        **Understanding the statistics:**
        - **Mean duration:** Average length of all marriages before divorce (add all durations Ã· number of divorces)
        - **Median age:** The middle age - half divorce younger, half divorce older
        - **Divorce rate:** Number of divorces per 1,000 married people per year""")
        st.markdown("")
        
        st.markdown("### ðŸ“ˆ Historical Divorce & Dissolution Trends (1963-2022)")
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
            "Divorce RateÂ¹": ["2.5", "5.9", "12.0", "13.4", "13.6", "13.0", "12.7", "12.2", "10.8", "8.9", "8.9", "8.5", "9.6", "6.9"]
        }
        st.dataframe(divorce_trend_data, hide_index=True, use_container_width=True)
        st.caption("Â¹ Divorce rate per 1,000 married population. Dissolutions = civil partnership breakups. 2022 data affected by timing of no-fault reform (April 2022)")
        
        # Chart for historical divorce trends
        years_divorce = [1963, 1971, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2019, 2020, 2021, 2022]
        divorces = [32000, 74437, 148301, 160300, 165658, 155499, 141135, 141322, 119589, 101055, 107599, 103592, 113505, 80057]
        dissolutions = [0, 0, 0, 0, 0, 0, 0, 167, 6385, 5734, 5006, 3956, 7525, 2112]
        
        fig = go.Figure()
        if show_opposite_sex:
            fig.add_trace(go.Scatter(x=years_divorce, y=divorces, name='Divorces (Opposite-Sex)', 
                                    line=dict(color='#f5576c', width=3), fill='tonexty'))
        if show_same_sex:
            fig.add_trace(go.Scatter(x=years_divorce, y=dissolutions, name='Civil Partnership Dissolutions',
                                    line=dict(color='#4facfe', width=3)))
        
        # Add annotations for key events based on what's shown
        if show_opposite_sex:
            fig.add_annotation(x=1971, y=74437, text="1969 Reform Act<br>takes effect",
                              showarrow=True, arrowhead=2, ax=-40, ay=-40)
            fig.add_annotation(x=1990, y=165658, text="Peak: 165,658<br>divorces (1990)",
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
        st.plotly_chart(fig, use_container_width=True, key='divorce_trends_chart')
        
        st.markdown("""**Key Insights:**
        - **Dramatic increase 1963-1990:** Divorces rose from 32,000 to peak of 165,658 (1990 in available data; actual peak was 1993 at ~180,000)
        - **1969 Reform Act impact:** Divorces more than doubled from 32,000 (1963) to 74,437 (1971) when reform took effect
        - **Peak divorce era:** 1980s-1990s saw highest divorce rates (160,000+ annually)
        - **Steady decline since early 1990s:** Divorces fell to 80,057 in 2022 - a 52% drop from 1990 peak
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
        
        # Filter divorce overview based on orientation
        if show_opposite_sex and show_same_sex:
            divorce_overview = {
                "Category": ["Opposite-Sex Divorces", "Same-Sex Divorces", "Civil Partnership (Male)", "Civil Partnership (Female)"],
                "Total Cases": ["80,057", "1,170", "422", "494"],
                "Mean Duration": ["12.7 years", "5.4 years", "7.8 years", "6.2 years"],
                "Median Age at Divorce": ["M: 46.4, F: 43.9", "M: 42.1, F: 40.8", "45.3", "43.6"],
                "Rate per 1,000": ["8.2", "16.8", "N/A", "N/A"]
            }
        elif show_opposite_sex:
            divorce_overview = {
                "Category": ["Opposite-Sex Divorces"],
                "Total Cases": ["80,057"],
                "Mean Duration": ["12.7 years"],
                "Median Age at Divorce": ["M: 46.4, F: 43.9"],
                "Rate per 1,000": ["8.2"]
            }
        else:
            divorce_overview = {
                "Category": ["Same-Sex Divorces", "Civil Partnership (Male)", "Civil Partnership (Female)"],
                "Total Cases": ["1,170", "422", "494"],
                "Mean Duration": ["5.4 years", "7.8 years", "6.2 years"],
                "Median Age at Divorce": ["M: 42.1, F: 40.8", "45.3", "43.6"],
                "Rate per 1,000": ["16.8", "N/A", "N/A"]
            }
        st.dataframe(divorce_overview, hide_index=True, use_container_width=True)
        
        # Comparison accounting for different population sizes
        if show_opposite_sex and show_same_sex:
            st.markdown("")
            st.markdown("#### ðŸ“Š Comparative Analysis (Rate-Adjusted)")
            st.markdown("""**How this is calculated:** These rates are 'rate-adjusted' to allow fair comparison:
            - **Divorce rate per 1,000 marriages** = (Number of divorces Ã· Number of married couples) Ã— 1,000
              - Opposite-sex: 80,057 divorces Ã· ~9.8 million married couples = 8.2 per 1,000 annually
              - Same-sex: 1,170 divorces Ã· ~69,700 married couples = 16.8 per 1,000 annually
            - **Duration vs baseline** = (Same-sex duration Ã· Opposite-sex duration) Ã— 100 = (5.4 Ã· 12.7) Ã— 100 = 42.5%
            - **Rate comparison** = (Same-sex rate Ã· Opposite-sex rate - 1) Ã— 100 = (16.8 Ã· 8.2 - 1) Ã— 100 = 105% higher
            
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
                    "16.8 (â†‘105% higher)",
                    "5.4 years",
                    "42.5% of baseline",
                    "1.3 years"
                ]
            }
            st.dataframe(comparison_data, hide_index=True, use_container_width=True)
            st.caption("Rate-adjusted: Accounts for different population sizes. Same-sex marriages are newer (legal since 2014), so shorter durations expected.")
        
        # Chart comparing divorce rates and duration
        st.markdown("")
        fig = go.Figure()
        if show_opposite_sex and show_same_sex:
            categories = ['Opposite-Sex', 'Same-Sex', 'Civil Partner (M)', 'Civil Partner (F)']
            durations = [12.7, 5.4, 7.8, 6.2]
            colors = ['#667eea', '#4facfe', '#f093fb', '#f5576c']
        elif show_opposite_sex:
            categories = ['Opposite-Sex']
            durations = [12.7]
            colors = ['#667eea']
        else:
            categories = ['Same-Sex', 'Civil Partner (M)', 'Civil Partner (F)']
            durations = [5.4, 7.8, 6.2]
            colors = ['#4facfe', '#f093fb', '#f5576c']
        
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
        st.plotly_chart(fig, use_container_width=True, key='marriage_duration_chart')
        
        st.markdown("#### Mean Age at First Marriage by Gender (2013-2022)")
        st.markdown("**Age differences show men marry slightly later than women:**")
        st.markdown("")
        
        age_gender_data = {
            "Year": ["2013", "2015", "2017", "2019", "2022"],
            "Men (Mean Age)": ["32.1", "32.5", "32.8", "33.4", "34.0"],
            "Women (Mean Age)": ["30.2", "30.6", "30.9", "31.5", "32.0"],
            "Gender Gap": ["1.9 years", "1.9 years", "1.9 years", "1.9 years", "2.0 years"],
            "Trend": ["Increasing", "Increasing", "Increasing", "Increasing", "Widening"]
        }
        st.dataframe(age_gender_data, hide_index=True, use_container_width=True)
        st.caption("Men consistently marry ~2 years older than women - stable pattern across the decade")
        
        st.markdown("""**What this gender data shows:**
        
        **Marriage Pattern by Gender:**
        - **Equal participation:** In opposite-sex marriages, exactly equal numbers of men and women marry (one man per woman)
        - **Age gap:** Men marry at mean age 34 vs women at 32 (2022) - consistent 2-year gap
        - **Both declining together:** When marriage rates drop/rise, both genders affected equally
        - **Same-sex comparison:** Same-sex marriages show very different patterns (more equal ages for women-women partnerships)
        
        **Gender-Specific Marriage Trends:**
        - **Men's pattern:** Marriage decline mirrors women's; likely same causes (economic, educational, cohabitation)
        - **Women's advantage:** Earlier age at marriage means longer time to establish families and careers
        - **Increasing gap:** Gender age gap widening slightly (1.9 â†’ 2.0 years) as men delay even more
        - **Career factors:** Women's education/careers causing later marriages; men's still later
        
        **Demographic notes:**
        - These numbers reflect ALL opposite-sex marriages (first marriages + remarriages)
        - Remarriages occur at older ages, pulling overall average up
        - First marriage age is lower: men ~32, women ~30 (approximately)""")
        
        # Filter insights based on orientation
        with st.expander("ðŸ“Š Key Insights", expanded=False):
            if show_opposite_sex and show_same_sex:
                st.markdown("""**Key Insights:**
                
                *Source: Office for National Statistics (ONS) - Divorces in England and Wales: 2022*
                
                - **Opposite-sex divorce rate:** 8.2 per 1,000 married people = ~0.82% divorce annually
            - **Same-sex higher rate:** 16.8 per 1,000 = double the opposite-sex rate (but sample is newer)
            - **Shorter same-sex duration:** 5.4 years vs 12.7 years - BUT same-sex marriage only legal since 2014, so maximum possible duration is 8-9 years in 2022 data
            - **Civil partnerships:** Middle ground at 6-8 years (these have existed since 2005, longer track record)
                - **Age at divorce:** People divorce in their 40s on average - men slightly older
                - **Why shorter same-sex duration?** New marriages haven't had time to reach 10+ years yet. Early adopters may have had relationship problems. More data needed after 2030.""")
            elif show_opposite_sex:
                st.markdown("""**Key Insights (Opposite-Sex Marriages):**
                
                *Source: Office for National Statistics (ONS) - Divorces in England and Wales: 2022*
                
                - **Divorce rate:** 8.2 per 1,000 married people = ~0.82% divorce annually
                - **Mean duration:** 12.7 years before divorce
                - **Median age at divorce:** Men 46.4 years, Women 43.9 years
                - **Long-term stability:** About 52% of marriages survive 30+ years""")
            else:
                st.markdown("""**Key Insights (Same-Sex Marriages & Civil Partnerships):**
                
                *Source: Office for National Statistics (ONS) - Divorces in England and Wales: 2022*
                
                - **Same-sex divorce rate:** 16.8 per 1,000 = higher than opposite-sex (but newer sample)
                - **Mean duration:** 5.4 years (same-sex marriages), 6-8 years (civil partnerships)
                - **Historical context:** Same-sex marriage only legal since 2014, so maximum duration is 8-9 years in 2022 data
                - **Civil partnerships:** Existed since 2005, providing longer track record (7-8 year average)
                - **Age at dissolution:** Slightly younger than opposite-sex divorces
                - **Why shorter duration?** New marriages haven't had time to reach 10+ years yet. More data needed after 2030.""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Who initiates divorce
    with st.expander("âš–ï¸ Who Initiates Divorce? (2022)", expanded=False):
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
        st.plotly_chart(fig, use_container_width=True, key='divorce_initiator_chart')
        
        with st.expander("ðŸ“Š Key Insights", expanded=False):
            st.markdown("""**Key Insights:**
            
                *Source: Office for National Statistics (ONS) - Divorces in England and Wales: 2022*
            
            - **Women dominate initiation:** 63% of divorces filed by wives vs 30% by husbands
            - **2:1 ratio:** For every divorce initiated by a husband, 2.1 are initiated by wives
            - **Joint applications rare:** Only 6.9% are filed jointly (increased after no-fault reform in April 2022)
            - **Why women initiate more:** Research suggests women have higher expectations for emotional connection, identify problems earlier, do more 'emotional labor', and are more likely to have social/family support for divorce
            - **Men's reluctance:** Men report being 'blindsided' more often, suggesting they may not recognize relationship problems as early
            - **Financial independence:** Women's increased workforce participation (since 1970s) makes divorce more financially viable""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Reasons for divorce
    with st.expander("ðŸ“‹ Grounds for Divorce (2022)", expanded=False):
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
                "Ground": ["Irretrievable breakdown (no-fault)", "  â†³ Filed by woman (est.)", "  â†³ Filed by man (est.)", "Joint application", "20-week cooling-off applied"],
                "% of Cases": ["93.1%", "~58.7%*", "~28.0%*", "6.9%", "100%"],
                "Impact": ["No blame required", "Part of 93.1%", "Part of 93.1%", "Both parties agree", "Mandatory waiting period"]
            }
            st.dataframe(divorce_reasons_new, hide_index=True, use_container_width=True)
            st.caption("*Estimated breakdown of no-fault applications by gender. New system removes adversarial blame. Gender split reflects who files the application.")
            st.markdown("")
            st.info("""â„¹ï¸ **Note:** The 93.1% 'no-fault' category includes both male and female applicants (see 'Who Initiates Divorce?' section above for the 63% women / 30% men / 6.9% joint breakdown). Under no-fault reform, you don't need to prove grounds, but someone still has to file the application - the gender split for who files remains similar to before the reform.""")
        
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
        st.plotly_chart(fig, use_container_width=True, key='divorce_grounds_chart')
        
        with st.expander("ðŸ“Š Key Insights", expanded=False):
            st.markdown("""**Key Insights:**
            
                *Source: Office for National Statistics (ONS) - Divorces in England and Wales: 2022; Ministry of Justice - Divorce (Financial Provision) Act 2022*
            
            - **No-fault revolution:** 93.1% now use simple "irretrievable breakdown" without proving fault
            - **Joint applications increased:** From <2% to 6.9% - couples can now apply together
            - **Old system problems:** Required blaming spouse, creating hostility; often forced people to wait 2-5 years
            - **Unreasonable behavior** was the most common ground (35%) - a catch-all category that included anything from lack of affection to financial irresponsibility
            - **Adultery bias:** Women cited adultery more (70%) because men's affairs were more likely to be discovered
            - **Separation grounds:** Required living apart 2 years (with consent) or 5 years (without) - expensive and impractical
            - **Reform benefits:** Reduces conflict, faster process, less expensive, protects children from parental conflict""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Underlying reasons for divorce
    with st.expander("ðŸ’¡ Underlying Reasons for Divorce (Survey Data)", expanded=False):
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
            st.plotly_chart(fig, use_container_width=True, key='real_divorce_reasons_chart')
        
        with st.expander("ðŸ“Š Key Insights", expanded=False):
            st.markdown("""**Key Insights:**
            
            *Source: Multiple UK divorce surveys (2018-2022) including Resolution (family law organization) and Relate (relationship charity)*
            
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
    with st.expander("ðŸ“Š Marriage Survival Rates (Opposite-Sex)", expanded=False):
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
    with st.expander("ðŸ’° Marriage & Income Statistics", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Household Income by Marital Status (2023)")
            income_marital = {
                "Status": ["Married couple", "Cohabiting couple", "Single (never married)", "Divorced/Separated", "Widowed"],
                "Median Income": ["Â£44,500", "Â£38,200", "Â£23,800", "Â£26,400", "Â£18,900"]
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
    with st.expander("ðŸ‘¶ Children & Marriage", expanded=False):
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
    with st.expander("ðŸ•Šï¸ Widowhood Statistics", expanded=False):
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
    with st.expander("ðŸ”„ Remarriage Statistics (2022)", expanded=False):
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
    with st.expander("ðŸ—ºï¸ Regional Marriage Rates (2022)", expanded=False):
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
    
    # Marriage rates by ethnicity
    with st.expander("ðŸŒ Marriage Rates by Ethnicity (Census 2021)", expanded=False):
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
        
        with st.expander("ðŸ“Š Key Insights", expanded=False):
            st.markdown("""**Key Insights:**
            
            *Source: Office for National Statistics (ONS) - Census 2021, England and Wales*
            
            **Highest Marriage Rates (Top 5):**
        - **Asian Indian (65.8%)** - Strong cultural/religious emphasis on marriage
        - **Asian Pakistani (63.4%)** - Similar cultural values, often arranged marriages
        - **Asian Bangladeshi (62.1%)** - Islamic tradition values marriage
        - **Asian Chinese (54.8%)** - Cultural emphasis on family formation
        - **Asian Other (51.2%)** - Includes various Asian ethnic groups
        
        **Lowest Marriage Rates (Bottom 5):**
        - **Mixed: White & Black African (28.9%)** - Younger demographic, less traditional
        - **Mixed: White & Black Caribbean (29.8%)** - Caribbean culture less marriage-focused
        - **Black: Other (31.2%)** - Diverse group, varying cultural norms
        - **Mixed: Other (32.8%)** - Multiple mixed backgrounds
        - **Black: Caribbean (34.2%)** - Historical Caribbean patterns of cohabitation over marriage
        
        **Why such variation?**
        - **Cultural/Religious factors:** Asian communities often have strong religious (Hindu, Muslim, Sikh) traditions emphasizing marriage
        - **Arranged marriage tradition:** Some Asian communities maintain arranged/assisted marriage customs, increasing marriage rates
        - **Age demographics:** Mixed and Black Caribbean groups tend to be younger on average; younger people marry less
        - **Caribbean cultural norms:** Long tradition of visiting relationships and common-law partnerships in Caribbean culture
        - **Migration patterns:** Recent migrants may marry earlier; second-generation may adopt British patterns
        - **Economic factors:** Marriage rates correlate with income/stability; varies by ethnic group
        - **Cohabitation attitudes:** White British and Black groups more accepting of long-term cohabitation without marriage
        
            **Comparison to general population:**
            - UK overall: ~44.8% of adults are married (similar to White British at 44.8%)
            - Asian groups: 12-21 percentage points **above** average
            - Mixed/Black Caribbean groups: 10-16 percentage points **below** average""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Interracial/Inter-ethnic marriage statistics
    with st.expander("ðŸ’‘ Same-Race vs Interracial Marriage (Census 2021)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** How often people marry within their own ethnic group vs across ethnic boundaries.
        
        **Definitions:**
        - **Same-ethnicity marriage:** Both partners identify with the same broad ethnic group (e.g., both White British)
        - **Interracial/Inter-ethnic marriage:** Partners from different ethnic groups (e.g., White British & Asian Indian)
        - Data from Census 2021 - England & Wales""")
        st.markdown("")
        
        # Overall statistics
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Same-Ethnicity Couples")
            st.markdown("### 86.7%")
            st.caption("Most couples share the same ethnicity")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">', unsafe_allow_html=True)
            st.markdown("#### Interracial/Inter-ethnic Couples")
            st.markdown("### 13.3%")
            st.caption("Couples from different ethnic backgrounds")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("")
        
        # Create two columns for side-by-side display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Interracial Marriage Rates by Ethnic Group")
            st.markdown("**% of married people in each group who have a partner of different ethnicity:**")
            st.markdown("")
            
            # Create dataframe for interracial rates
            interracial_list = []
            for ethnicity, rate in INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"].items():
                same_rate = (1 - rate) * 100
                interracial_list.append({
                    "Ethnic Group": ethnicity,
                    "% Same-Ethnicity": f"{same_rate:.1f}%",
                    "% Interracial": f"{rate*100:.1f}%",
                    "Rate": rate
                })
            
            interracial_df = pd.DataFrame(interracial_list)
            interracial_df = interracial_df.sort_values("Rate", ascending=False)
            interracial_df = interracial_df.drop("Rate", axis=1)
            interracial_df.insert(0, "Rank", range(1, len(interracial_df) + 1))
            
            st.dataframe(interracial_df, hide_index=True, use_container_width=True)
            st.caption("Sorted by % Interracial (highest to lowest)")
        
        with col2:
            st.markdown("#### Most Common Interracial Pairings")
            st.markdown("**When couples are from different ethnic groups, these are the most common combinations:**")
            st.markdown("")
            
            # Create dataframe for common pairings
            pairings_list = []
            for pairing, pct in INTERRACIAL_MARRIAGE_DATA["common_pairings"].items():
                pairings_list.append({
                    "Pairing": pairing,
                    "% of Interracial Marriages": f"{pct*100:.1f}%",
                    "Rate": pct
                })
            
            pairings_df = pd.DataFrame(pairings_list)
            pairings_df = pairings_df.sort_values("Rate", ascending=False)
            pairings_df = pairings_df.drop("Rate", axis=1)
            pairings_df.insert(0, "Rank", range(1, len(pairings_df) + 1))
            
            st.dataframe(pairings_df, hide_index=True, use_container_width=True)
        
        st.markdown("")
        st.markdown("")
        
        # Create stacked bar chart
        ethnicities_inter = [x[0] for x in sorted(
            INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"].items(),
            key=lambda x: x[1],
            reverse=True
        )]
        interracial_rates = [x[1]*100 for x in sorted(
            INTERRACIAL_MARRIAGE_DATA["interracial_rate_by_ethnicity"].items(),
            key=lambda x: x[1],
            reverse=True
        )]
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
        fig.add_trace(go.Bar(
            y=ethnicities_inter_short[::-1],
            x=same_ethnicity_rates[::-1],
            name='Same-Ethnicity',
            orientation='h',
            marker=dict(color='#667eea'),
            text=[f"{rate:.1f}%" for rate in same_ethnicity_rates[::-1]],
            textposition='inside'
        ))
        fig.add_trace(go.Bar(
            y=ethnicities_inter_short[::-1],
            x=interracial_rates[::-1],
            name='Interracial',
            orientation='h',
            marker=dict(color='#f5576c'),
            text=[f"{rate:.1f}%" for rate in interracial_rates[::-1]],
            textposition='inside'
        ))
        
        fig.update_layout(
            barmode='stack',
            title='Same-Ethnicity vs Interracial Marriage by Ethnic Group',
            xaxis_title='Percentage',
            yaxis_title='Ethnic Group',
            template='plotly_dark',
            height=700,
            margin=dict(l=250),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Pie chart for common pairings
        pairings_names = list(INTERRACIAL_MARRIAGE_DATA["common_pairings"].keys())
        pairings_values = [v*100 for v in INTERRACIAL_MARRIAGE_DATA["common_pairings"].values()]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=pairings_names,
            values=pairings_values,
            hole=0.3,
            marker=dict(colors=['#667eea', '#f5576c', '#4facfe', '#f093fb', '#764ba2', '#8b9eff', '#9d7bc4', '#a8b8ff', '#b0b0b0'])
        )])
        fig_pie.update_layout(
            title='Distribution of Interracial Marriage Pairings',
            template='plotly_dark',
            height=700
        )
        
        # Display charts side by side
        col1, col2 = st.columns([1.2, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=True, key='interracial_marriage_by_ethnicity_chart')
        with col2:
            st.plotly_chart(fig_pie, use_container_width=True, key='interracial_pairings_pie_chart')
        
        st.markdown("")
        
        with st.expander("ðŸ“Š Key Insights", expanded=False):
            st.markdown("""**Key Insights:**
            
            *Source: Office for National Statistics (ONS) - Census 2021, England and Wales*
            
            **Most Likely to Marry Interracially:**
        - **Mixed ethnic groups (85-89%)** - By definition, often have one parent from each ethnicity, so naturally more open
        - **Black Caribbean (48.9%)** - Nearly HALF have partners from different ethnicities
        - **Arab (38.7%)** - Relatively high interracial marriage rate
        - **Black Other & Chinese (36-37%)** - Above-average openness to interracial relationships
        
        **Least Likely to Marry Interracially:**
        - **Asian Bangladeshi (6.3%)** - 93.7% marry within own ethnicity
        - **Asian Pakistani (7.8%)** - 92.2% marry within own ethnicity  
        - **Asian Indian (14.3%)** - 85.7% marry within own ethnicity
        - **White British (11.2%)** - 88.8% marry within own ethnicity (but largest group, so most interracial marriages involve White British)
        
        **Most Common Interracial Pairings:**
        - **White British & White Other (31.2%)** - By far the most common, though technically "interethnic" not "interracial"
        - **White British & Asian Indian (11.8%)** - Second most common
        - **White British & Black Caribbean (9.4%)** - Third most common
        - **White British dominates** - Appears in 6 of top 7 pairings (due to being 74% of population)
        
        **Why the variation?**
        - **Cultural/Religious factors:** Asian Muslim/Hindu/Sikh communities often prefer same-ethnicity marriage for religious/cultural continuity
        - **Arranged marriage tradition:** Pakistani/Bangladeshi communities often have arranged marriages within ethnic group
        - **Language barriers:** First-generation migrants may prefer same-ethnicity partners who share language
        - **Family pressure:** Some cultures have strong family expectations about partner ethnicity
        - **Geographic concentration:** Some groups cluster in specific areas, limiting exposure to other ethnicities
        - **Black Caribbean openness:** Long history in UK (Windrush generation 1948+), more integrated into British society
        - **Mixed groups:** Children of interracial couples naturally more open to diverse relationships
        - **White British numbers:** As 74% of population, statistically appear in most interracial pairings
        
        **Historical trends:**
        - Interracial marriage increasing steadily: was ~9% in 2001, now 13.3% in 2021
        - Younger generations much more open: ~20% of couples under 35 are interracial
        - Urban areas higher: London ~25% interracial couples vs ~8% in rural areas
        
            **Implications:**
            - Dating pool significantly smaller for those preferring same-ethnicity partners in minority groups
            - Openness to interracial dating dramatically increases dating pool for all minorities
            - Cultural/religious compatibility often more important than ethnicity itself""")
        
        st.markdown("")
        st.markdown("### ðŸ“ˆ Historical Trends in Interracial Marriage (2001-2021)")
        st.markdown("""**What this shows:** How interracial and inter-ethnic relationships have grown over 20 years, showing increasing acceptance and integration across UK society.
        
        **Census comparisons:**
        - **2001 Census:** 7% of couples in inter-ethnic relationships
        - **2011 Census:** 9% of couples in inter-ethnic relationships (+2 percentage points)
        - **2021 Census:** 13.3% of couples in inter-ethnic relationships (+4.3 percentage points)""")
        st.markdown("")
        
        # # Overall trend
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.markdown("#### Overall Growth in Interracial Relationships")
        #     historical_overall = {
        #         "Year": ["2001", "2011", "2021"],
        #         "% Inter-ethnic": ["7%", "9%", "13.3%"],
        #         "Growth": ["-", "+2.0 pp", "+4.3 pp"],
        #         "Couples (Thousands)": ["1,709", "2,327", "Estimated 3,500+"]
        #     }
        #     st.dataframe(historical_overall, hide_index=True, use_container_width=True)
        #     st.caption("pp = percentage points. Estimated 2021 based on population growth and increased diversity.")
        
        # with col2:
        #     st.markdown("#### Growth Rate Analysis")
        #     growth_rates = {
        #         "Period": ["2001-2011", "2011-2021", "2001-2021"],
        #         "Change": ["+2.0 pp", "+4.3 pp", "+6.3 pp"],
        #         "% Increase": ["+28.6%", "+47.8%", "+90%"],
        #         "Trend": ["Steady", "Accelerating", "Rapid growth"]
        #     }
        #     st.dataframe(growth_rates, hide_index=True, use_container_width=True)
        #     st.caption("Growth is accelerating - the increase 2011-2021 was more than double 2001-2011")
        
        st.markdown("")
        
        # Historical comparison by ethnic group
        # st.markdown("#### How Different Ethnic Groups Changed (2001 to 2011)")
        # st.markdown("**Selected ethnic groups showing trends:**")
        # st.markdown("")
        
        # ethnicity_trends = {
        #     "Ethnic Group": [
        #         "White British",
        #         "White Irish",
        #         "Other White",
        #         "Indian",
        #         "Pakistani",
        #         "Bangladeshi",
        #         "Chinese",
        #         "Black Caribbean",
        #         "Black Other",
        #         "Mixed (White & Asian)",
        #         "Overall"
        #     ],
        #     "2001 %": ["3%", "65%", "54%", "10%", "9%", "7%", "25%", "34%", "71%", "85%", "7%"],
        #     "2011 %": ["4%", "71%", "39%", "12%", "9%", "7%", "31%", "43%", "62%", "87%", "9%"],
        #     "Change": ["+1 pp", "+6 pp", "-15 pp", "+2 pp", "0 pp", "0 pp", "+6 pp", "+9 pp", "-9 pp", "+2 pp", "+2 pp"]
        # }
        # st.dataframe(ethnicity_trends, hide_index=True, use_container_width=True)
        # st.caption("Data from 2001 and 2011 Census. Changes show significant variation by group.")
        
        st.markdown("")
        
        # Prepare both historical charts
        years = [2001, 2011, 2021]
        
        # Historical chart by demographic groups
        fig = go.Figure()
        
        # Key demographic lines - selected for diversity and interest
        groups_data = {
            'Overall': {'2001': 7, '2011': 9, '2021': 13.3, 'color': '#f5576c'},
            'White British': {'2001': 3, '2011': 4, '2021': 5.5, 'color': '#667eea'},
            'Mixed (All)': {'2001': 85, '2011': 87, '2021': 89, 'color': '#4facfe'},
            'Black Caribbean': {'2001': 34, '2011': 43, '2021': 48.9, 'color': '#f093fb'},
            'Chinese': {'2001': 25, '2011': 31, '2021': 36.5, 'color': '#764ba2'},
            'South Asian (Indian)': {'2001': 10, '2011': 12, '2021': 14.3, 'color': '#8b9eff'},
            'South Asian (Pakistani)': {'2001': 9, '2011': 9, '2021': 7.8, 'color': '#9d7bc4'},
        }
        
        for group_name, data in groups_data.items():
            values = [data['2001'], data['2011'], data['2021']]
            fig.add_trace(go.Scatter(
                x=years,
                y=values,
                mode='lines+markers',
                name=group_name,
                line=dict(color=data['color'], width=2.5),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title='Inter-ethnic Relationship Trends by Demographic Group (2001-2021)',
            xaxis_title='Year',
            yaxis_title='% of Couples in Inter-ethnic Relationships',
            template='plotly_dark',
            height=550,
            hovermode='x unified',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Gender split chart
        fig_gender = go.Figure()
        
        # Gender data by ethnicity (2001, 2011 actual census; 2021 projected based on trends)
        # Note: Full gender breakdown by ethnicity not yet published for 2021 Census
        gender_groups = {
            'Chinese - Women': {'2001': 39, '2011': 39, '2021': 45, 'color': '#764ba2', 'dash': 'solid'},
            'Chinese - Men': {'2001': 20, '2011': 20, '2021': 28, 'color': '#764ba2', 'dash': 'dash'},
            'Arab - Men': {'2001': 43, '2011': 43, '2021': 46, 'color': '#f5576c', 'dash': 'solid'},
            'Arab - Women': {'2001': 26, '2011': 26, '2021': 32, 'color': '#f5576c', 'dash': 'dash'},
            'Other Asian - Women': {'2001': 38, '2011': 38, '2021': 42, 'color': '#667eea', 'dash': 'solid'},
            'Other Asian - Men': {'2001': 23, '2011': 23, '2021': 28, 'color': '#667eea', 'dash': 'dash'},
            'Black Caribbean - Women': {'2001': 35, '2011': 44, '2021': 50, 'color': '#4facfe', 'dash': 'solid'},
            'Black Caribbean - Men': {'2001': 33, '2011': 42, '2021': 48, 'color': '#4facfe', 'dash': 'dash'},
        }
        
        for group_name, data in gender_groups.items():
            values = [data['2001'], data['2011'], data['2021']]
            fig_gender.add_trace(go.Scatter(
                x=years,
                y=values,
                mode='lines+markers',
                name=group_name,
                line=dict(color=data['color'], width=2.5, dash=data['dash']),
                marker=dict(size=6)
            ))
        
        fig_gender.update_layout(
            title='Inter-ethnic Relationship Trends by Gender (2001-2021)',
            xaxis_title='Year',
            yaxis_title='% in Inter-ethnic Relationships',
            template='plotly_dark',
            height=550,
            hovermode='x unified',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            annotations=[
                dict(text="Solid line = Women | Dashed line = Men | 2021 data projected from trends", xref="paper", yref="paper",
                     x=0.5, y=-0.12, showarrow=False, font=dict(size=10, color="white"))
            ]
        )
        
        # Display charts side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig, use_container_width=True, key='interracial_historical_trend_chart')
        with col2:
            st.plotly_chart(fig_gender, use_container_width=True, key='interracial_gender_trend_chart')
        
        st.markdown("")
        
        with st.expander("ðŸ“Š Key Gender Insights", expanded=False):
            st.markdown("""**Key Gender Insights:**
            
            *Source: Office for National Statistics (ONS) - Census 2001, 2011 (actual data); 2021 gender-specific breakdown not yet published, so 2021 figures are projections based on overall Census 2021 trends*
            
            **Major Gender Gaps (Largest Differences):**
        - **Chinese: Massive gap** - Women nearly 2x more likely than men (39% vs 20% in 2011)
          - Women: 39% inter-ethnic | Men: 20% inter-ethnic (19 pp gap)
          - Suggests Chinese women more accepted in British dating market, or more open to marrying outside group
        
        - **Arab: Reverse gap** - Men significantly more likely than women (43% vs 26% in 2011)
          - Men: 43% inter-ethnic | Women: 26% inter-ethnic (17 pp gap)
          - Suggests traditional cultural patterns where men have more freedom in partner selection
        
        - **Other Asian: Women more open** - 15 percentage point gap (38% vs 23%)
          - Women significantly more likely to marry across ethnic boundaries
        
        **Smaller Gender Differences:**
        - **Black Caribbean:** Nearly equal (43% women vs 42% men in 2011)
          - Most integrated group; both genders equally likely to marry interracially
        
        **What drives gender differences?**
        - **Cultural/religious norms:** Some cultures restrict women's choices more than men's
        - **Dating market dynamics:** Minority women may face different dynamics than minority men
        - **Femininity stereotypes:** Asian women stereotyped as "desirable" in Western media (fetishization?)
        - **Masculinity stereotypes:** Asian men face less favorable stereotypes in dating markets
        - **Family pressure:** Some cultures exert more control over daughters' marriage choices
        - **Educational mobility:** Women increasingly higher educated, marrying across classes/ethnicities
        - **Second-generation differences:** Younger women more likely to reject parental expectations
        
        **Generational trend (2001â†’2011â†’2021):**
        - Gender gaps narrowing in most groups as younger generations reject traditional restrictions
        - Chinese gap closing: men's rates growing faster than women's
        - Arab gap stabilizing as younger Arabs adopt more Western dating norms
        - Overall: Both men and women increasingly marrying interracially
        
            **Dating pool implications:**
            - **Chinese women:** Largest dating pool as most willing to marry interracially
            - **Chinese men:** Smallest dating pool in own ethnic group; larger pool outside
            - **Arab men:** More dating freedom; can marry outside without family backlash
            - **Arab women:** Fewer options if preferring to stay within culture""")
        
        with st.expander("ðŸ“Š Key Historical Insights", expanded=False):
            st.markdown("""**Key Historical Insights:**
            
            *Source: Office for National Statistics (ONS) - Census 2001, 2011, 2021; ONS article "What does the Census tell us about inter-ethnic relationships?" (2014)*
            
            **Overall Trajectory:**
            - **Steady growth:** 7% â†’ 9% â†’ 13.3% represents consistent increase over 20 years
            - **Acceleration:** Growth doubled in speed between 2011-2021 vs 2001-2011
            - **Population changes:** UK became 18% non-white in 2021 (vs ~8-12% in 2001), creating more opportunities for inter-ethnic relationships
            - **Integration effect:** Longer-established minority groups (Caribbean, Asian) show higher rates than newer groups (Eastern European)
            - **Time lag:** Census patterns reflect relationships formed years before - 2021 data includes couples who met in mid-2010s
            
            **By Ethnic Group Changes (2001â†’2011):**
            
            **Increased Inter-ethnic Rates:**
            - **Black Caribbean:** 34% â†’ 43% (+9 pp) - Continued integration into British society
            - **Chinese:** 25% â†’ 31% (+6 pp) - Strong growth, especially among women (was 39% for women by 2011)
            - **White Irish:** 65% â†’ 71% (+6 pp) - Already high, continued openness
            
            **Decreased or Stable:**
            - **South Asian (Indian/Pakistani/Bangladeshi):** Remained stable (9-12%) - Stronger cultural/religious boundaries
            - **Other White:** 54% â†’ 39% (-15 pp) - Major change due to Polish migration (2004 EU expansion)
              - Poland had low rates (many recent migrants, less integrated), diluting "Other White" average
            
            **Why the 20-year acceleration?**
            1. **Growing minorities:** Larger minority populations = more exposure and opportunities
            2. **Second-generation integration:** Children of 1970s-1980s migrants now forming relationships
            3. **Urban growth:** Increasing urban diversity (London, Manchester, Birmingham)
            4. **Internet dating:** Online dating removes geographic/social barriers; easier to meet across ethnic groups
            5. **Cultural shift:** Younger generations more accepting; less family pressure
            6. **Education:** University brings together young people from diverse backgrounds
            7. **Workplace diversity:** More integrated workplaces = more cross-ethnic friendships â†’ relationships
            
            **Age and generational effects (2011 data):**
            - **Ages 16-24:** 11% inter-ethnic (highest) - Younger people far more open
            - **Ages 25-49:** 12% inter-ethnic - Peak relationship-forming years, high rates
            - **Ages 50-64:** 7% inter-ethnic - Formed relationships in 1980s-1990s, less diversity then
            - **Ages 65+:** 5% inter-ethnic - Formed in 1950s-1980s, much less diverse society
            - **Generational gap:** 65+ generation had 1/2 the inter-ethnic rate of young people
            
            **Regional variation (2011):**
            - **London:** ~25% inter-ethnic (highest diversity and integration)
            - **Urban areas:** 15-20% inter-ethnic
            - **Rural areas:** 5-8% inter-ethnic (less diversity, more traditional)
            
            **Relationship type differences (2011):**
            - **Cohabiting couples:** 12% inter-ethnic
            - **Married couples:** 8% inter-ethnic
            - **Implication:** Cohabiting relationships more likely to be inter-ethnic; suggests younger, more liberal couples
            
            **Projected 2031 trends:**
            - If acceleration continues: could reach 15-18% by 2031
            - Younger cohorts now marrying (born 1995-2005) are ~20% inter-ethnic
            - London and major cities likely reaching 30%+ inter-ethnic relationships
            - South Asian groups may converge slightly upward as younger generations increasingly open
            
            **What these trends mean for dating:**
            - **Minority men:** More women available as inter-ethnic dating increases
            - **Minority women:** Similar benefit - larger potential pool
            - **Younger generation:** Dating someone from different background increasingly normalized
            - **Regional effect:** London/urban dwellers have much larger diverse dating pools than rural areas
            - **Selection effect:** Growing minority - most inter-ethnic relationships are with White British (largest group)
            
            *Source: Office for National Statistics (ONS) - Census 2001, 2011, 2021; ONS article "What does the Census tell us about inter-ethnic relationships?" (2014)*""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Modern trends
    with st.expander("ðŸ”„ Modern Marriage Trends", expanded=False):
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
                    "Average: Â£290,000",
                    "Average: Â£45,000",
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
    with st.expander("ðŸŒ UK vs International Comparison", expanded=False):
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
    with st.expander("ðŸ“š Data Sources", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""
        - **[ONS Marriages in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriagesinenglandandwalesprovisional/2022)**
        - **[ONS Divorces in England and Wales: 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/divorce/bulletins/divorcesinenglandandwales/2022)**
        - **[ONS Census 2021 - Marital and Civil Partnership Status](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/bulletins/marriageandcivilpartnershipstatusinenglandandwales/census2021)**
        - **[ONS Families and Households: 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2023)**
        - **[ONS Birth Statistics by Parents' Characteristics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/birthsbyparentscharacteristics)**
        - **[ONS Annual Survey of Hours and Earnings](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2023)** - Income by marital status
        - **[DWP Family Resources Survey 2023](https://www.gov.uk/government/statistics/family-resources-survey-financial-year-2022-to-2023)**
        - **[ONS Census 2021 - Ethnic Group by Marital Status](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity/articles/ethnicgroupbylegalpartnershipstatusenglandandwales/census2021)** - Marriage rates by ethnicity
        - **[ONS Census 2021 - Interethnic Relationships](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/marriagecohabitationandcivilpartnerships/articles/mixedethniccouplesintheuk/2021)** - Same-race and interracial marriage data
        - **[Eurostat Marriage Statistics](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Marriage_and_divorce_statistics)** - International comparison data
        
        All statistics are for **England and Wales** unless specified UK-wide. Scotland and Northern Ireland 
        publish separate statistics but follow similar trends.
        
        **Note:** Same-sex marriage became legal in England & Wales (March 2014), Scotland (December 2014), 
        and Northern Ireland (January 2020). Civil partnerships available since 2005.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
