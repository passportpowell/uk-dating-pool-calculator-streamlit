"""
UI Component for Baby & Child Health Statistics
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.constants import BABY_HEALTH_DATA


def display_baby_statistics_tab():
    """Display comprehensive baby and child health statistics"""
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 👶 UK Baby & Child Health Statistics", unsafe_allow_html=True)
    st.caption("Based on Office for National Statistics (ONS), NHS Digital, and Department of Health data")
    st.markdown("")
    st.info("""**📊 Data Accuracy Note:** All statistics presented are from official UK government sources including ONS, NHS Digital, and public health surveys. These track maternal and child health outcomes over time. Data represents England & Wales or UK-wide depending on the dataset.""")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # COMPREHENSIVE OVERVIEW - Age Comparison
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Overview: All Pregnancy Outcomes by Maternal Age", unsafe_allow_html=True)
    st.markdown("""**Compare everything at a glance:** This comprehensive table and chart show how maternal age affects all major pregnancy outcomes and risks.""")
    st.info("**📖 Sources:** ONS Birth Statistics, MBRRACE-UK Reports, PHE Congenital Anomaly Statistics, HFEA Fertility Data")
    st.markdown("")
    
    # Prepare comprehensive data
    complications = BABY_HEALTH_DATA["birth_complications_by_maternal_age"]
    fertility_data = BABY_HEALTH_DATA["fertility_and_conception"]
    genetic_risks = BABY_HEALTH_DATA["genetic_conditions_risk_by_maternal_age"]
    
    age_groups = ["Under 20", "20-29", "30-34", "35-39", "40+"]
    age_groups_chart = ["<20", "20-29", "30-34", "35-39", "40+"]
    
    # Compile all data into comprehensive table
    comprehensive_data = {
        "Age Group": age_groups,
        "Miscarriage %": [
            fertility_data["miscarriage_rates"]["by_age"]["under_30"],
            fertility_data["miscarriage_rates"]["by_age"]["under_30"],
            fertility_data["miscarriage_rates"]["by_age"]["30_34"],
            fertility_data["miscarriage_rates"]["by_age"]["35_39"],
            fertility_data["miscarriage_rates"]["by_age"]["40_44"],
        ],
        "Stillbirth (per 1,000)": [
            complications["under_20"]["stillbirth_rate"],
            complications["20_29"]["stillbirth_rate"],
            complications["30_34"]["stillbirth_rate"],
            complications["35_39"]["stillbirth_rate"],
            complications["40_plus"]["stillbirth_rate"],
        ],
        "Preterm Birth %": [
            complications["under_20"]["preterm_birth"],
            complications["20_29"]["preterm_birth"],
            complications["30_34"]["preterm_birth"],
            complications["35_39"]["preterm_birth"],
            complications["40_plus"]["preterm_birth"],
        ],
        "C-Section %": [
            complications["under_20"]["c_section_rate"],
            complications["20_29"]["c_section_rate"],
            complications["30_34"]["c_section_rate"],
            complications["35_39"]["c_section_rate"],
            complications["40_plus"]["c_section_rate"],
        ],
        "Down Syndrome Risk": [
            "1 in 1,500",
            "1 in 1,250",
            "1 in 952",
            "1 in 378",
            "1 in 106",
        ],
        "All Chromosomal Risk": [
            "1 in 526",
            "1 in 476",
            "1 in 385",
            "1 in 192",
            "1 in 66",
        ],
        "IVF Success % (per cycle)": [
            "32%",
            "32%",
            "25%",
            "19%",
            "11-4%",
        ],
        "Risk Level": [
            "🟡 Moderate",
            "🟢 Low (Optimal)",
            "🟢 Low",
            "🟠 Moderate-High",
            "🔴 High",
        ]
    }
    
    df_comprehensive = pd.DataFrame(comprehensive_data)
    
    st.markdown("### 📋 Complete Comparison Table and Chart")
    
    col_table, col_chart = st.columns([1, 1])
    
    with col_table:
        st.dataframe(df_comprehensive, hide_index=True, use_container_width=True)
        st.caption("⭐ **Optimal age range: 20-34** - Lowest risks across all metrics")
    
    with col_chart:
        # Create comprehensive multi-line chart
        miscarriage_rates = [10.0, 10.0, 12.0, 18.0, 34.0]
        stillbirth_rates = [4.8, 3.5, 3.7, 4.5, 6.4]
        preterm_rates = [8.5, 7.2, 7.5, 8.2, 9.8]
        csection_rates = [28.0, 30.5, 35.2, 42.8, 54.3]
        
        # Create numeric chromosomal risk (convert "1 in X" to percentage)
        chromosomal_risk_numeric = [
            100/526,  # Under 20: 1 in 526
            100/476,  # 20-29: 1 in 476
            100/385,  # 30-34: 1 in 385
            100/192,  # 35-39: 1 in 192
            100/66,   # 40+: 1 in 66
        ]
        
        downs_risk_numeric = [
            100/1500,  # Under 20: 1 in 1,500
            100/1250,  # 20-29: 1 in 1,250
            100/952,   # 30-34: 1 in 952
            100/378,   # 35-39: 1 in 378
            100/106,   # 40+: 1 in 106
        ]
        
        fig = go.Figure()
        
        # Add traces for each metric
        fig.add_trace(go.Scatter(
            x=age_groups_chart,
            y=miscarriage_rates,
            name='Miscarriage Rate (%)',
            line=dict(color='#f5576c', width=3),
            marker=dict(size=10),
            mode='lines+markers',
            hovertemplate='Age: %{x}<br>Miscarriage: %{y}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=age_groups_chart,
            y=preterm_rates,
            name='Preterm Birth (%)',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10),
            mode='lines+markers',
            hovertemplate='Age: %{x}<br>Preterm Birth: %{y}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=age_groups_chart,
            y=stillbirth_rates,
            name='Stillbirth (per 1,000)',
            line=dict(color='#f093fb', width=3),
            marker=dict(size=10),
            mode='lines+markers',
            hovertemplate='Age: %{x}<br>Stillbirth: %{y} per 1,000<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=age_groups_chart,
            y=[r*10 for r in chromosomal_risk_numeric],  # Scale up for visibility
            name='All Chromosomal Abnormalities (% × 10)',
            line=dict(color='#4facfe', width=3, dash='dash'),
            marker=dict(size=10),
            mode='lines+markers',
            hovertemplate='Age: %{x}<br>Chromosomal Risk: %{y:.2f}% (scaled)<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=age_groups_chart,
            y=[r*10 for r in downs_risk_numeric],  # Scale up for visibility
            name='Down Syndrome (% × 10)',
            line=dict(color='#764ba2', width=3, dash='dot'),
            marker=dict(size=10),
            mode='lines+markers',
            hovertemplate='Age: %{x}<br>Down Syndrome: %{y:.2f}% (scaled)<extra></extra>'
        ))
        
        fig.update_layout(
            title='Pregnancy Risks by Maternal Age',
            xaxis_title='Maternal Age Group',
            yaxis_title='Percentage / Rate',
            template='plotly_dark',
            height=550,
            hovermode='x unified',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(0,0,0,0.5)"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, key='comprehensive_age_comparison_chart')
    
    st.markdown("""
    **📊 Key Insights from Age Comparison:**
    
    **Optimal Age (20-34):**
    - ✅ Lowest miscarriage rates (10-12%)
    - ✅ Lowest stillbirth rates (3.5-3.7 per 1,000)
    - ✅ Lowest chromosomal abnormality risk
    - ✅ Lowest preterm birth rates
    - ✅ Moderate C-section rates (30-35%)
    
    **Age 35-39 (Increased Risk):**
    - ⚠️ Miscarriage rises to 18% (+50% vs 20-29)
    - ⚠️ Stillbirth increases to 4.5 per 1,000 (+29%)
    - ⚠️ Chromosomal risk doubles (1 in 192 vs 1 in 385)
    - ⚠️ Down syndrome risk triples (1 in 378 vs 1 in 952)
    - ⚠️ C-section rate 43% (vs 31% at 20-29)
    
    **Age 40+ (Significantly Higher Risk):**
    - 🔴 Miscarriage jumps to 34% (3.4x higher than 20-29)
    - 🔴 Stillbirth 6.4 per 1,000 (83% higher than 20-29)
    - 🔴 Chromosomal risk 1 in 66 (6x higher than 30-34)
    - 🔴 Down syndrome 1 in 106 (9x higher than 30-34)
    - 🔴 C-section majority at 54%
    - 🔴 Preterm birth 9.8% (36% higher than 20-29)
    
    **Teen Mothers (<20):**
    - ⚠️ Higher stillbirth (4.8 per 1,000)
    - ⚠️ Higher preterm birth (8.5%)
    - ⚠️ Lower chromosomal risk (due to younger eggs)
    - ⚠️ Social/economic challenges increase other risks
    
    **The "Fertility Cliff" after 35:**
    - Sharp increase in all complications after age 35
    - Risk acceleration continues, especially after 40
    - Modern prenatal care mitigates but doesn't eliminate age-related risks
    """)
    
    st.markdown("")
    st.markdown("### 🔄 C-Section Rates by Age")
    
    # C-section specific chart
    fig_csection = go.Figure()
    fig_csection.add_trace(go.Bar(
        x=age_groups_chart,
        y=csection_rates,
        marker=dict(
            color=csection_rates,
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="C-Section %")
        ),
        text=[f"{r}%" for r in csection_rates],
        textposition='auto',
        hovertemplate='Age: %{x}<br>C-Section Rate: %{y}%<extra></extra>'
    ))
    
    fig_csection.update_layout(
        title='C-Section Rate by Maternal Age',
        xaxis_title='Maternal Age Group',
        yaxis_title='C-Section Rate (%)',
        template='plotly_dark',
        height=400
    )
    
    st.plotly_chart(fig_csection, use_container_width=True, key='csection_by_age_chart')
    
    st.info("""**💡 Why C-sections increase with age:**
    - Decreased uterine muscle elasticity
    - Higher rates of complications (placenta previa, fetal distress)
    - Slower/stalled labor progression
    - Previous C-sections more common in older mothers
    - Medical caution with "precious pregnancy" (IVF, long-awaited)
    - Higher rates of twins/multiples (especially IVF)""")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Maternal Mortality Trends
    with st.expander("🏥 Maternal Mortality Trends (2011-2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** Maternal deaths per 100,000 live births - women who die during pregnancy or within 42 days of giving birth.
        
        **Understanding the data:**
        - UK has one of the lowest maternal mortality rates globally
        - Significant improvement over past decade
        - Target: Reduce to below 7 per 100,000""")
        st.info("**📖 Source:** [MBRRACE-UK Maternal Mortality Reports](https://www.npeu.ox.ac.uk/mbrrace-uk) - Confidential Enquiry into Maternal Deaths")
        st.markdown("")
        
        # Create dataframe
        maternal_data = BABY_HEALTH_DATA["maternal_mortality"]
        parental_age_data = BABY_HEALTH_DATA["parental_age_statistics"]
        
        years = ["2011-2013", "2014-2016", "2017-2019", "2020", "2021", "2022"]
        years_numeric = [2012, 2015, 2018, 2020, 2021, 2022]  # Mid-point for plotting
        rates = [maternal_data["2011-2013"], maternal_data["2014-2016"], 
                maternal_data["2017-2019"], maternal_data["2020"], 
                maternal_data["2021"], maternal_data["2022"]]
        
        # Get maternal age data for corresponding years
        mother_ages = [30.0, 30.7, 31.0, 31.2, 31.4, 31.5]
        mothers_over_35_pct = [23.8, 27.3, 28.5, 29.4, 30.2, 31.0]
        
        df_maternal = pd.DataFrame({
            "Period": years,
            "Deaths per 100,000": rates,
            "Avg Mother Age": mother_ages,
            "Mothers 35+ %": mothers_over_35_pct,
            "Trend": ["Baseline", "Improving", "Improving", "COVID Impact", "Recovering", "Record Low"]
        })
        
        col_table, col_chart = st.columns([1, 1])
        
        with col_table:
            st.dataframe(df_maternal, hide_index=True, use_container_width=True)
            st.caption("📊 Note: Average maternal age has increased from 30.0 to 31.5 years, while mortality decreased")
        
        with col_chart:
            # Chart with dual axis
            fig = go.Figure()
            
            # Maternal mortality rate
            fig.add_trace(go.Scatter(
                x=years,
                y=rates,
                name='Maternal Mortality',
                mode='lines+markers',
                line=dict(color='#f5576c', width=3),
                marker=dict(size=10),
                yaxis='y'
            ))
            
            # Average mother age
            fig.add_trace(go.Scatter(
                x=years,
                y=mother_ages,
                name='Average Mother Age',
                mode='lines+markers',
                line=dict(color='#4facfe', width=2, dash='dash'),
                marker=dict(size=8),
                yaxis='y2'
            ))
            
            # % mothers over 35
            fig.add_trace(go.Scatter(
                x=years,
                y=mothers_over_35_pct,
                name='Mothers 35+ (%)',
                mode='lines+markers',
                line=dict(color='#ffa726', width=2, dash='dot'),
                marker=dict(size=8),
                yaxis='y3'
            ))
            
            fig.update_layout(
                title='Maternal Mortality vs Age',
                xaxis_title='Year',
                template='plotly_dark',
                height=500,
                yaxis=dict(
                    title=dict(text='Deaths per 100,000', font=dict(color='#f5576c')),
                    tickfont=dict(color='#f5576c')
                ),
                yaxis2=dict(
                    title=dict(text='Average Age (years)', font=dict(color='#4facfe')),
                    tickfont=dict(color='#4facfe'),
                    overlaying='y',
                    side='right',
                    position=0.85
                ),
                yaxis3=dict(
                    title=dict(text='Mothers 35+ (%)', font=dict(color='#ffa726')),
                    tickfont=dict(color='#ffa726'),
                    overlaying='y',
                    side='right'
                ),
                legend=dict(x=0.01, y=0.99)
            )
            st.plotly_chart(fig, use_container_width=True, key='maternal_mortality_chart')
        
        st.markdown("""**Key Insights:**
        - **Major improvement:** 30% reduction from 12.2 (2011-2013) to 8.5 (2022)
        - **COVID-19 impact:** Slight increase in 2020 (10.7) due to pandemic complications
        - **Recovery:** Strong recovery post-COVID with record low in 2022
        - **Target:** WHO recommends below 7 per 100,000 - UK approaching this goal
        - **Leading causes:** Cardiovascular disease, thromboembolism, mental health issues, sepsis""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stillbirth Rates
    with st.expander("💔 Stillbirth Rates (2010-2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** Stillbirths per 1,000 total births - babies born with no signs of life at or after 24 weeks gestation.
        
        **Understanding the data:**
        - Stillbirth = death before or during birth (after 24 weeks)
        - UK has one of the lowest stillbirth rates globally
        - Cinfo("**📖 Source:** [ONS Child Mortality Statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/bulletins/childhoodinfantandperinatalmortalityinenglandandwales/latest) - Annual Stillbirth Data")
        st.ontinuous improvement through better antenatal care""")
        st.markdown("")
        
        stillbirth_data = BABY_HEALTH_DATA["stillbirth_rates"]
        parental_age_data = BABY_HEALTH_DATA["parental_age_statistics"]
        
        years_still = ["2010", "2015", "2019", "2020", "2021", "2022"]
        rates_still = [stillbirth_data["2010"], stillbirth_data["2015"], 
                      stillbirth_data["2019"], stillbirth_data["2020"], 
                      stillbirth_data["2021"], stillbirth_data["2022"]]
        
        # Get maternal age data
        mother_ages = [parental_age_data["mother_mean_age"]["2010"],
                      parental_age_data["mother_mean_age"]["2015"],
                      31.0, 31.2, 31.4,
                      parental_age_data["mother_mean_age"]["2022"]]
        mothers_over_35 = [parental_age_data["mothers_over_35"]["2010"],
                          parental_age_data["mothers_over_35"]["2015"],
                          28.5, 29.4, 30.2,
                          parental_age_data["mothers_over_35"]["2022"]]
        
        df_stillbirth = pd.DataFrame({
            "Year": years_still,
            "Stillbirths per 1,000": rates_still,
            "Avg Mother Age": mother_ages,
            "Mothers 35+ %": mothers_over_35,
            "Change from 2010": [0, -9.6, -25.0, -21.2, -23.1, -26.9]
        })
        
        col_table, col_chart = st.columns([1, 1])
        
        with col_table:
            st.dataframe(df_stillbirth, hide_index=True, use_container_width=True)
            st.caption("📊 Despite rising maternal age (30.0→31.5 yrs) and more mothers 35+ (23.8%→31.0%), stillbirth rates declined through improved prenatal care")
        
        with col_chart:
            # Chart with quad axis (stillbirth, age, mothers 35+, births)
            fig = go.Figure()
            
            # Birth counts (in thousands) for each year
            births_thousands = [723, 697, 640, 613, 624, 605]
            
            # Stillbirth rate
            fig.add_trace(go.Scatter(
                x=years_still,
                y=rates_still,
                name='Stillbirth Rate',
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)',
                yaxis='y'
            ))
            
            # Average mother age
            fig.add_trace(go.Scatter(
                x=years_still,
                y=mother_ages,
                name='Average Mother Age',
                mode='lines+markers',
                line=dict(color='#4facfe', width=2, dash='dash'),
                marker=dict(size=8),
                yaxis='y2'
            ))
            
            # % mothers over 35
            fig.add_trace(go.Scatter(
                x=years_still,
                y=mothers_over_35,
                name='Mothers 35+ (%)',
                mode='lines+markers',
                line=dict(color='#ffa726', width=2, dash='dot'),
                marker=dict(size=8),
                yaxis='y3'
            ))
            
            # Birth count line
            fig.add_trace(go.Scatter(
                x=years_still,
                y=births_thousands,
                name='Births (thousands)',
                mode='lines+markers',
                line=dict(color='#90ee90', width=2, dash='dashdot'),
                marker=dict(size=7),
                yaxis='y4',
                hovertemplate='Year: %{x}<br>Births: %{y}k<extra></extra>'
            ))
            
            fig.update_layout(
                title='Stillbirth Rate vs Age & Birth Volume',
                xaxis_title='Year',
                template='plotly_dark',
                height=500,
                yaxis=dict(
                    title=dict(text='Stillbirths per 1,000', font=dict(color='#667eea')),
                    tickfont=dict(color='#667eea'),
                    domain=[0, 0.7]
                ),
                yaxis2=dict(
                    title=dict(text='Avg Age (yrs)', font=dict(color='#4facfe')),
                    tickfont=dict(color='#4facfe'),
                    overlaying='y',
                    side='right',
                    anchor='free',
                    position=0.93
                ),
                yaxis3=dict(
                    title=dict(text='Mothers 35+ (%)', font=dict(color='#ffa726')),
                    tickfont=dict(color='#ffa726'),
                    overlaying='y',
                    side='right',
                    anchor='x'
                ),
                yaxis4=dict(
                    title=dict(text='Births (k)', font=dict(color='#90ee90')),
                    tickfont=dict(color='#90ee90'),
                    anchor='free',
                    overlaying='y',
                    side='left',
                    position=0.05
                ),
                legend=dict(x=0.15, y=0.99, bgcolor='rgba(0,0,0,0.7)')
            )
            st.plotly_chart(fig, use_container_width=True, key='stillbirth_chart')
        
        st.markdown("""**Key Insights:**
        - **Dramatic improvement:** 27% reduction from 5.2 (2010) to 3.8 (2022)
        - **Current rate:** 3.8 per 1,000 = 1 in 263 births
        - **COVID impact:** Slight increase in 2020-2021, now recovered
        - **Best in world:** UK among top 5 countries for low stillbirth rates
        - **Risk factors:** Maternal age >40, obesity, smoking, diabetes
        - **Prevention:** Improved antenatal screening, growth monitoring, placental function tests""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Infant Mortality
    with st.expander("👼 Infant Mortality (Under 1 Year) - 2010-2022", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** Deaths of babies under 1 year per 1,000 live births.
        
        **Categories:**
        - **Neonatal:** Deaths 0-28 days (most critical period)
        - **Post-neonatal:** Deaths 28 days to 1 year
        - *info("**📖 Source:** [ONS Child Mortality Statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/bulletins/childhoodinfantandperinatalmortalityinenglandandwales/latest) - Infant & Neonatal Deaths")
        st.*Total infant mortality:** Combined rate""")
        st.markdown("")
        
        infant_data = BABY_HEALTH_DATA["infant_mortality"]
        parental_age_data = BABY_HEALTH_DATA["parental_age_statistics"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Overall Infant Mortality Trend")
            years_infant = ["2010", "2015", "2020", "2021", "2022"]
            rates_infant = [infant_data["2010"], infant_data["2015"], 
                           infant_data["2020"], infant_data["2021"], infant_data["2022"]]
            
            # Get maternal age data
            mother_ages = [parental_age_data["mother_mean_age"]["2010"],
                          parental_age_data["mother_mean_age"]["2015"],
                          parental_age_data["mother_mean_age"]["2020"],
                          31.4,
                          parental_age_data["mother_mean_age"]["2022"]]
            
            df_infant = pd.DataFrame({
                "Year": years_infant,
                "Deaths per 1,000": rates_infant,
                "Avg Mother Age": mother_ages,
                "Deaths per Year (approx)": [2819, 2339, 2280, 2220, 2100]
            })
            st.dataframe(df_infant, hide_index=True, use_container_width=True)
            st.caption("📊 Infant mortality declined as maternal age increased")
        
        with col2:
            st.markdown("#### Neonatal vs Post-Neonatal")
            neo_years = ["2010", "2015", "2020", "2021"]
            df_breakdown = pd.DataFrame({
                "Year": neo_years,
                "Neonatal (0-28 days)": [3.3, 2.5, 2.3, 2.2],
                "Post-neonatal (28d-1yr)": [1.4, 1.4, 1.5, 1.5],
            })
            st.dataframe(df_breakdown, hide_index=True, use_container_width=True)
        
        # Chart with triple axis (mortality, age, births)
        fig = go.Figure()
        
        # Birth counts (in thousands) for each year
        births_thousands = [688, 677, 613, 624, 605]
        
        # Infant mortality bars
        fig.add_trace(go.Bar(
            x=years_infant,
            y=rates_infant,
            name='Infant Mortality',
            marker_color='#f093fb',
            text=rates_infant,
            textposition='auto',
            yaxis='y'
        ))
        
        # Average mother age line
        fig.add_trace(go.Scatter(
            x=years_infant,
            y=mother_ages,
            name='Average Mother Age',
            mode='lines+markers',
            line=dict(color='#4facfe', width=3, dash='dash'),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        # Birth count line
        fig.add_trace(go.Scatter(
            x=years_infant,
            y=births_thousands,
            name='Births (thousands)',
            mode='lines+markers',
            line=dict(color='#ffa726', width=2, dash='dot'),
            marker=dict(size=8),
            yaxis='y3',
            hovertemplate='Year: %{x}<br>Births: %{y}k<extra></extra>'
        ))
        
        fig.update_layout(
            title='Infant Mortality vs Maternal Age Trends',
            xaxis_title='Year',
            template='plotly_dark',
            height=500,
            yaxis=dict(
                title=dict(text='Deaths per 1,000 Live Births', font=dict(color='#f093fb')),
                tickfont=dict(color='#f093fb')
            ),
            yaxis2=dict(
                title=dict(text='Average Mother Age (years)', font=dict(color='#4facfe')),
                tickfont=dict(color='#4facfe'),
                overlaying='y',
                side='right',
                position=0.85
            ),
            yaxis3=dict(
                title=dict(text='Births (thousands)', font=dict(color='#ffa726')),
                tickfont=dict(color='#ffa726'),
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig, use_container_width=True, key='infant_mortality_chart')
        
        st.markdown("""**Key Insights:**
        - **Steady improvement:** 26% reduction from 4.7 (2010) to 3.5 (2022)
        - **Current rate:** 3.5 per 1,000 = 1 in 286 babies
        - **Neonatal deaths:** Account for ~63% of infant deaths (most vulnerable period)
        - **Leading causes:** Congenital anomalies, prematurity, birth asphyxia, infections
        - **Comparison:** UK rate similar to France (3.5), better than US (5.4), lower than Japan (1.8)""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Parental Age Trends
    with st.expander("👨‍👩‍👧 Parental Age Trends (1990-2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** How the average age of parents at childbirth has changed over 32 years.
        
        **Key trends:**
        - Parents having children later in life
        - Women over 35 now account for 1 in 3 births
        - Tinfo("**📖 Source:** [ONS Birth Statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths) - Births by Parents' Characteristics")
        st.een pregnancies declining dramatically""")
        st.markdown("")
        
        parent_age_data = BABY_HEALTH_DATA["parental_age_statistics"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Mean Parental Age Over Time")
            years_parent = ["1990", "2000", "2010", "2015", "2020", "2022"]
            mother_ages = [28.8, 29.5, 30.0, 30.7, 31.2, 31.5]
            father_ages = [31.8, 32.5, 33.2, 33.9, 34.4, 34.7]
            
            df_parent_age = pd.DataFrame({
                "Year": years_parent,
                "Mother Mean Age": mother_ages,
                "Father Mean Age": father_ages,
                "Age Gap": [3.0, 3.0, 3.2, 3.2, 3.2, 3.2]
            })
            st.dataframe(df_parent_age, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### Births by Maternal Age Category")
            df_age_cat = pd.DataFrame({
                "Category": ["Mothers >35", "Mothers >40", "Teen Mothers <20"],
                "1990 %": [15.2, 3.2, 8.1],
                "2022 %": [31.0, 12.5, 1.5],
                "Change": ["+104%", "+291%", "-81%"]
            })
            st.dataframe(df_age_cat, hide_index=True, use_container_width=True)
        
        # Dual line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years_parent,
            y=mother_ages,
            name='Mother',
            line=dict(color='#f5576c', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=years_parent,
            y=father_ages,
            name='Father',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            title='Mean Parental Age at Childbirth',
            xaxis_title='Year',
            yaxis_title='Age',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key='parent_age_chart')
        
        st.markdown("""**Key Insights:**
        - **Mother age increase:** +2.7 years since 1990 (28.8 → 31.5)
        - **Father age increase:** +2.9 years since 1990 (31.8 → 34.7)
        - **Mothers over 35:** Now 31% of births (was 15.2% in 1990) - more than DOUBLED
        - **Mothers over 40:** Now 12.5% (was 3.2% in 1990) - nearly QUADRUPLED
        - **Teen pregnancies:** Collapsed from 8.1% to 1.5% - **81% reduction**
        - **Why the shift?** Education, careers, financial stability, contraception access, IVF availability
        - **Risks:** Advanced maternal age increases complications but prenatal care has improved""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Birth Defects and Chromosomal Disorders
    with st.expander("🧬 Chromosomal & Genetic Disorders", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** Prevalence of chromosomal disorders and congenital anomalies.
        
        **Iinfo("**📖 Sources:** [PHE Congenital Anomaly Statistics](https://www.gov.uk/government/collections/congenital-anomaly-statistics), NHS Fetal Anomaly Screening Programme, National Down Syndrome Cytogenetic Register")
        st.mportant note:** Many of these are now detected prenatally through screening""")
        st.markdown("")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Chromosomal Disorders")
            chrom_data = BABY_HEALTH_DATA["birth_defects"]["chromosomal_disorders"]
            df_chrom = pd.DataFrame({
                "Disorder": list(chrom_data.keys()),
                "Rate per 1,000 Births": list(chrom_data.values()),
                "Approx 1 in N": ["1 in 695", "1 in 1,316", "1 in 1,818", "1 in 2,128", "1 in 1,064"]
            })
            st.dataframe(df_chrom, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### Structural Birth Defects (Top 5)")
            struct_data = BABY_HEALTH_DATA["birth_defects"]["structural_defects"]
            df_struct = pd.DataFrame({
                "Defect": ["Congenital heart defects", "Limb defects", "Cleft lip/palate", "Neural tube defects", "Gastroschisis"],
                "Rate per 1,000": [0.86, 0.16, 0.17, 0.06, 0.04],
                "Approx 1 in N": ["1 in 116", "1 in 625", "1 in 588", "1 in 1,667", "1 in 2,500"]
            })
            st.dataframe(df_struct, hide_index=True, use_container_width=True)
        
        st.markdown("")
        st.markdown("#### Risk by Maternal Age - Down Syndrome & All Chromosomal Abnormalities")
        
        risk_data = BABY_HEALTH_DATA["genetic_conditions_risk_by_maternal_age"]
        df_risk = pd.DataFrame({
            "Maternal Age": ["20", "25", "30", "35", "40", "45"],
            "Down Syndrome Risk": list(risk_data["downs_syndrome_risk"].values()),
            "All Chromosomal Abnormalities": list(risk_data["all_chromosomal_abnormalities"].values())
        })
        
        col_risk_table, col_risk_chart = st.columns([1, 1])
        
        with col_risk_table:
            st.dataframe(df_risk, hide_index=True, use_container_width=True)
            st.caption("Risk increases dramatically after age 35")
        
        with col_risk_chart:
            # Convert risk ratios to percentages for chart
            ages = [20, 25, 30, 35, 40, 45]
            downs_percentages = [100/1500, 100/1250, 100/952, 100/378, 100/106, 100/30]
            all_chrom_percentages = [100/526, 100/476, 100/385, 100/192, 100/66, 100/21]
            
            fig_risk = go.Figure()
            
            fig_risk.add_trace(go.Scatter(
                x=ages,
                y=downs_percentages,
                name='Down Syndrome Risk',
                mode='lines+markers',
                line=dict(color='#764ba2', width=3),
                marker=dict(size=10),
                hovertemplate='Age: %{x}<br>Risk: %{y:.3f}%<extra></extra>'
            ))
            
            fig_risk.add_trace(go.Scatter(
                x=ages,
                y=all_chrom_percentages,
                name='All Chromosomal Abnormalities',
                mode='lines+markers',
                line=dict(color='#4facfe', width=3),
                marker=dict(size=10),
                hovertemplate='Age: %{x}<br>Risk: %{y:.2f}%<extra></extra>'
            ))
            
            fig_risk.update_layout(
                title='Chromosomal Risk by Maternal Age',
                xaxis_title='Maternal Age (years)',
                yaxis_title='Risk Percentage (%)',
                template='plotly_dark',
                height=450,
                hovermode='x unified',
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="rgba(0,0,0,0.5)"
                )
            )
            
            st.plotly_chart(fig_risk, use_container_width=True, key='chromosomal_risk_chart')
        
        st.markdown("""**Key Insights:**
        - **Overall rate:** 2.5% of births have major congenital anomalies
        - **Most common:** Congenital heart defects (0.86 per 1,000 = ~1 in 116 babies)
        - **Down syndrome:** Most common chromosomal disorder (0.144 per 1,000)
        - **Age effect:** Risk of Down syndrome increases 50x from age 20 to 45
        - **Screening:** 98% of pregnant women in UK offered screening; many choose termination
        - **Survival:** Many conditions now treatable with surgery/medical intervention
        - **Prenatal detection:** ~90% of Down syndrome cases detected prenatally""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Child Mental Health
    with st.expander("🧠 Child Mental Health Trends (2004-2022)", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** Prevalence of mental health disorders in children aged 5-15.
        
        **Ainfo("**📖 Source:** [NHS Digital Mental Health of Children and Young People in England Survey](https://digital.nhs.uk/data-and-information/publications/statistical/mental-health-of-children-and-young-people-in-england) - Longitudinal studies 2004-2022")
        st.larming trend:** Significant increase, especially post-COVID-19 pandemic""")
        st.markdown("")
        
        mental_data = BABY_HEALTH_DATA["child_mental_health"]
        parental_age_data = BABY_HEALTH_DATA["parental_age_statistics"]
        
        st.markdown("#### Overall Disorder Prevalence (%)")
        overall = mental_data["overall_disorder_prevalence"]
        years_mental = ["2004", "2014", "2017", "2022"]
        overall_rates = [overall["2004"], overall["2014"], overall["2017"], overall["2022"]]
        
        # Get parental age data for corresponding years
        parent_ages = [29.0, 30.5, 30.9, 31.5]  # Approximate maternal ages
        
        df_overall_mental = pd.DataFrame({
            "Year": years_mental,
            "Prevalence %": overall_rates,
            "Avg Mother Age": parent_ages,
            "Approx Children (millions)": [0.86, 1.02, 1.07, 1.37]
        })
        st.dataframe(df_overall_mental, hide_index=True, use_container_width=True)
        st.caption("📊 59% increase since 2004; 29% increase since 2017 (COVID impact). Note: Maternal age also increased but mental health trends driven primarily by social factors")
        
        st.markdown("")
        st.markdown("#### Breakdown by Disorder Type")
        
        disorder_types = ["Anxiety Disorders", "Depression", "Conduct Disorders", "ADHD", "Autism Spectrum Disorder"]
        rates_2004 = [3.9, 0.9, 5.4, 2.2, 0.5]
        rates_2017 = [4.8, 1.5, 5.1, 2.8, 1.2]
        rates_2022 = [7.1, 2.4, 6.2, 3.4, 1.8]
        
        df_disorders = pd.DataFrame({
            "Disorder": disorder_types,
            "2004 %": rates_2004,
            "2017 %": rates_2017,
            "2022 %": rates_2022,
            "Change 2004-2022": ["+82%", "+167%", "+15%", "+55%", "+260%"]
        })
        st.dataframe(df_disorders, hide_index=True, use_container_width=True)
        
        # Chart with dual axis
        fig = go.Figure()
        
        # Mental health disorders
        for disorder, r_2004, r_2017, r_2022 in zip(disorder_types, rates_2004, rates_2017, rates_2022):
            fig.add_trace(go.Scatter(
                x=["2004", "2017", "2022"],
                y=[r_2004, r_2017, r_2022],
                name=disorder.replace(" Disorder", ""),
                mode='lines+markers',
                line=dict(width=2.5),
                marker=dict(size=8),
                yaxis='y'
            ))
        
        # Add maternal age trend
        fig.add_trace(go.Scatter(
            x=["2004", "2014", "2017", "2022"],
            y=[29.0, 30.5, 30.9, 31.5],
            name='Avg Mother Age',
            mode='lines+markers',
            line=dict(color='#ffffff', width=3, dash='dash'),
            marker=dict(size=10, symbol='diamond'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Child Mental Health vs Maternal Age Trends',
            xaxis_title='Year',
            template='plotly_dark',
            height=500,
            yaxis=dict(
                title=dict(text='Mental Health Prevalence (%)', font=dict(color='#ff6b9d')),
                tickfont=dict(color='#ff6b9d')
            ),
            yaxis2=dict(
                title=dict(text='Average Mother Age (years)', font=dict(color='#ffffff')),
                tickfont=dict(color='#ffffff'),
                overlaying='y',
                side='right',
                range=[28, 32]
            ),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.5)')
        )
        st.plotly_chart(fig, use_container_width=True, key='mental_health_chart')
        
        st.markdown("""**Key Insights:**
        - **Overall increase:** From 9.6% (2004) to 15.3% (2022) - **59% increase**
        - **COVID-19 impact:** Accelerated growth from 11.9% (2017) to 15.3% (2022)
        - **Anxiety disorders:** Largest increase - from 3.9% to 7.1% (**82% increase**)
        - **Depression:** Tripled from 0.9% to 2.4% (**167% increase**)
        - **Autism diagnosis:** Nearly quadrupled from 0.5% to 1.8% (**260% increase** - partly better detection)
        - **Now:** 1 in 6.5 children has a diagnosable mental health disorder
        - **Causes:** Social media, academic pressure, economic stress, COVID-19 isolation, screen time
        - **Gender gap:** Girls more likely to have anxiety/depression; boys more likely to have ADHD/autism""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Child Physical Health
    with st.expander("🏃 Child Physical Health (Obesity, Asthma, Allergies)", expanded=False):
        st.info("**📖 Sources:** [NHS Digital National Child Measurement Programme](https://digital.nhs.uk/data-and-information/publications/statistical/national-child-measurement-programme) (obesity), [NHS Health Survey for England](https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england) (asthma, allergies), Public Health England Oral Health Surveys (dental)")
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** Prevalence of common childhood physical health conditions.""")
        st.markdown("")
        
        physical_data = BABY_HEALTH_DATA["child_physical_health"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Childhood Obesity (Age 11)")
            obesity_data = physical_data["childhood_obesity"]
            years_obesity = ["2009-10", "2015", "2020", "2022"]
            obesity_rates = [31.5, 34.2, 35.8, 38.3]
            
            df_obesity = pd.DataFrame({
                "Year": years_obesity,
                "% Overweight/Obese": obesity_rates,
                "Change from 2009": [0, +2.7, +4.3, +6.8]
            })
            st.dataframe(df_obesity, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### Asthma & Allergies")
            df_conditions = pd.DataFrame({
                "Condition": ["Asthma", "Eczema/Allergies", "Dental Decay (age 5)"],
                "2010 %": [8.5, 15.3, 31.0],
                "2022 %": [10.1, 18.5, 21.5],
                "Trend": ["Increasing", "Increasing", "Improving"]
            })
            st.dataframe(df_conditions, hide_index=True, use_container_width=True)
        
        # Obesity chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=years_obesity,
            y=obesity_rates,
            marker=dict(
                color=obesity_rates,
                colorscale='Reds',
                showscale=True
            ),
            text=[f"{r}%" for r in obesity_rates],
            textposition='auto'
        ))
        fig.update_layout(
            title='Childhood Obesity Trend (% Overweight/Obese by Age 11)',
            xaxis_title='Year',
            yaxis_title='Percentage',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key='obesity_chart')
        
        st.markdown("""**Key Insights:**
        - **Obesity crisis:** 38.3% of 11-year-olds overweight/obese in 2022 - **more than 1 in 3**
        - **COVID impact:** 2.5 percentage point increase during lockdowns (less exercise, more snacking)
        - **Social inequality:** Children from deprived areas have 2x higher obesity rates
        - **Asthma increase:** From 8.5% to 10.1% - now **1 in 10 children**
        - **Allergies/eczema:** Rising from 15.3% to 18.5% - nearly **1 in 5 children**
        - **Dental health:** One success story - decay down from 31% to 21.5%
        - **Long-term impact:** Childhood obesity predicts adult obesity, diabetes, heart disease
        - **Causes:** Processed food, sedentary lifestyle, screen time, socioeconomic factors""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Preterm Births
    with st.expander("⏰ Preterm Birth Rates", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** Babies born before full term (37 weeks gestation).
        
        **Categories:**
        - **Overall preterm:** Before 37 weeks (most common)
        - *info("**📖 Sources:** [ONS Birth Statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths) (preterm rates), National Neonatal Research Database, EPICure Studies (survival rates)")
        st.*Very preterm:** Before 32 weeks (serious risks)
        - **Extremely preterm:** Before 28 weeks (highest risk)""")
        st.markdown("")
        
        preterm_data = BABY_HEALTH_DATA["pre_term_birth"]
        
        df_preterm = pd.DataFrame({
            "Category": ["Overall Preterm (<37 weeks)", "Very Preterm (<32 weeks)", "Extremely Preterm (<28 weeks)"],
            "2010 %": [7.3, 1.5, 0.4],
            "2022 %": [7.9, 1.6, 0.5],
            "Approx 1 in N (2022)": ["1 in 13", "1 in 63", "1 in 200"]
        })
        st.dataframe(df_preterm, hide_index=True, use_container_width=True)
        
        st.markdown("")
        st.markdown("#### NICU Survival Rates by Gestational Age")
        
        nicu_data = BABY_HEALTH_DATA["neonatal_intensive_care"]["survival_rates_by_gestation"]
        df_survival = pd.DataFrame({
            "Gestation (weeks)": ["22", "23", "24", "25", "26", "27", "28", "32+"],
            "Survival Rate %": [10, 26, 55, 72, 82, 88, 92, 98],
            "Interpretation": [
                "Extremely low",
                "Low",
                "Moderate",
                "Good",
                "Very good",
                "High",
                "Very high",
                "Near-certain"
            ]
        })
        st.dataframe(df_survival, hide_index=True, use_container_width=True)
        
        # Survival chart
        weeks = [22, 23, 24, 25, 26, 27, 28, 32]
        survival = [10, 26, 55, 72, 82, 88, 92, 98]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[str(w) for w in weeks],
            y=survival,
            marker=dict(
                color=survival,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Survival %")
            ),
            text=[f"{s}%" for s in survival],
            textposition='auto'
        ))
        fig.update_layout(
            title='NICU Survival Rates by Gestational Age',
            xaxis_title='Weeks Gestation',
            yaxis_title='Survival Rate (%)',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key='nicu_survival_chart')
        
        st.markdown("""**Key Insights:**
        - **Overall rate:** 7.9% of births are preterm (1 in 13)
        - **Slight increase:** Up from 7.3% in 2010 - may reflect better detection
        - **Very preterm:** 1.6% (1 in 63) - require intensive neonatal care
        - **Extremely preterm:** 0.5% (1 in 200) - highest risk for complications
        - **Survival improving:** 28-week babies now have 92% survival (vs ~60% in 1990s)
        - **NICU admissions:** 14.2% of babies need neonatal intensive care
        - **Risk factors:** Multiple births, maternal age >40, IVF, smoking, infections
        - **Long-term:** Preterm babies at higher risk for disabilities, learning difficulties""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fertility and IVF
    with st.expander("🧪 Fertility, IVF & Miscarriage Rates", expanded=False):
        st.info("**📖 Sources:** [HFEA Fertility Treatment Data](https://www.hfea.gov.uk/about-us/publications/research-and-data/) (IVF success rates), Tommy's National Miscarriage Research Centre, Royal College of Obstetricians and Gynaecologists (RCOG)")
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** IVF success rates and miscarriage statistics by age.""")
        st.markdown("")
        
        fertility_data = BABY_HEALTH_DATA["fertility_and_conception"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### IVF Success Rates by Age")
            st.markdown("**Per cycle success rate (%)**")
            df_ivf = pd.DataFrame({
                "Age Group": ["Under 35", "35-37", "38-39", "40-42", "Over 42"],
                "Success Rate %": [32.0, 25.0, 19.0, 11.0, 4.0],
                "Approx 1 in N Cycles": ["1 in 3", "1 in 4", "1 in 5", "1 in 9", "1 in 25"]
            })
            st.dataframe(df_ivf, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### Miscarriage Rates by Age")
            st.markdown("**% of known pregnancies**")
            miscarriage = fertility_data["miscarriage_rates"]["by_age"]
            df_miscarriage = pd.DataFrame({
                "Age Group": list(miscarriage.keys()),
                "Miscarriage Rate %": list(miscarriage.values()),
                "Risk Level": ["Low", "Low", "Moderate", "High", "Very High"]
            })
            st.dataframe(df_miscarriage, hide_index=True, use_container_width=True)
        
        # Combined chart
        ages_chart = ["<30", "30-34", "35-39", "40-44", "45+"]
        ivf_rates = [32, 25, 19, 11, 4]
        miscarriage_rates = [10, 12, 18, 34, 53]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ages_chart,
            y=ivf_rates,
            name='IVF Success Rate',
            line=dict(color='#4facfe', width=3),
            marker=dict(size=10),
            yaxis='y'
        ))
        fig.add_trace(go.Scatter(
            x=ages_chart,
            y=miscarriage_rates,
            name='Miscarriage Rate',
            line=dict(color='#f5576c', width=3),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='IVF Success vs Miscarriage Risk by Maternal Age',
            xaxis_title='Maternal Age',
            yaxis=dict(title='IVF Success Rate (%)', side='left'),
            yaxis2=dict(title='Miscarriage Rate (%)', side='right', overlaying='y'),
            template='plotly_dark',
            height=450,
            legend=dict(x=0.7, y=0.95)
        )
        st.plotly_chart(fig, use_container_width=True, key='fertility_chart')
        
        st.markdown("""**Key Insights:**
        - **IVF cycles:** 68,700 cycles in 2022 (recovered from COVID dip)
        - **Age is critical:** IVF success drops 8x from under-35 (32%) to over-42 (4%)
        - **Overall miscarriage:** 15% of known pregnancies
        - **Age effect:** Miscarriage risk quintuples from under-30 (10%) to 45+ (53%)
        - **Biological cliff:** Sharp decline after 35 for both fertility and miscarriage risk
        - **Multiple attempts:** Most successful IVF patients undergo 2-3 cycles
        - **Cost:** Average £5,000 per cycle; NHS coverage varies by region
        - **Egg quality:** Primary factor in age-related decline""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Maternal Complications by Age
    with st.expander("⚠️ Birth Complications by Maternal Age", expanded=False):
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""**What this shows:** How birth complication rates vary by mother's age.""")
        st.info("**📖 Sources:** [NHS Maternity Statistics](https://digital.nhs.uk/data-and-information/publications/statistical/nhs-maternity-statistics) (C-sections, complications), ONS Birth Characteristics (age-related outcomes), MBRRACE-UK Reports")
        st.markdown("")
        
        complications = BABY_HEALTH_DATA["birth_complications_by_maternal_age"]
        parental_age_data = BABY_HEALTH_DATA["parental_age_statistics"]
        maternal_compl_data = BABY_HEALTH_DATA["maternal_complications"]
        
        age_groups = ["Under 20", "20-29", "30-34", "35-39", "40+"]
        preterm_rates = [8.5, 7.2, 7.5, 8.2, 9.8]
        stillbirth_rates = [4.8, 3.5, 3.7, 4.5, 6.4]
        csection_rates = [28.0, 30.5, 35.2, 42.8, 54.3]
        
        st.markdown("#### Complication Rates by Current Maternal Age")
        df_complications = pd.DataFrame({
            "Age Group": age_groups,
            "Preterm Birth %": preterm_rates,
            "Stillbirth (per 1,000)": stillbirth_rates,
            "C-Section Rate %": csection_rates
        })
        st.dataframe(df_complications, hide_index=True, use_container_width=True)
        st.caption("Current snapshot: How complications vary by maternal age group")
        
        st.markdown("")
        st.markdown("#### Historical Trend: Gestational Diabetes vs Maternal Age (2010-2022)")
        
        # Add historical gestational diabetes trend with maternal age
        gest_diab = maternal_compl_data["gestational_diabetes"]
        years_gest = ["2010", "2015", "2020", "2022"]
        gest_diab_rates = [gest_diab["2010"], gest_diab["2015"], gest_diab["2020"], gest_diab["2022"]]
        mother_ages_gest = [parental_age_data["mother_mean_age"]["2010"],
                           parental_age_data["mother_mean_age"]["2015"],
                           parental_age_data["mother_mean_age"]["2020"],
                           parental_age_data["mother_mean_age"]["2022"]]
        
        df_gest_trend = pd.DataFrame({
            "Year": years_gest,
            "Gestational Diabetes %": gest_diab_rates,
            "Avg Mother Age": mother_ages_gest
        })
        st.dataframe(df_gest_trend, hide_index=True, use_container_width=True)
        st.caption("📊 Gestational diabetes has nearly doubled (3.2%→6.1%) as maternal age increased (30.0→31.5 years)")
        
        # Multiple line chart for current age groups
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=age_groups,
            y=preterm_rates,
            name='Preterm Birth %',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=age_groups,
            y=stillbirth_rates,
            name='Stillbirth Rate (per 1,000)',
            line=dict(color='#f5576c', width=3),
            marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=age_groups,
            y=[r/10 for r in csection_rates],  # Scale down for visibility
            name='C-Section Rate % (÷10)',
            line=dict(color='#f093fb', width=3, dash='dash'),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title='Birth Complications by Maternal Age (Current)',
            xaxis_title='Maternal Age Group',
            yaxis_title='Rate',
            template='plotly_dark',
            height=450
        )
        st.plotly_chart(fig, use_container_width=True, key='complications_chart')
        
        # Add gestational diabetes trend chart
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=years_gest,
            y=gest_diab_rates,
            name='Gestational Diabetes',
            mode='lines+markers',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=10),
            yaxis='y'
        ))
        fig2.add_trace(go.Scatter(
            x=years_gest,
            y=mother_ages_gest,
            name='Average Mother Age',
            mode='lines+markers',
            line=dict(color='#4facfe', width=3, dash='dash'),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig2.update_layout(
            title='Gestational Diabetes vs Maternal Age Trends',
            xaxis_title='Year',
            template='plotly_dark',
            height=450,
            yaxis=dict(
                title=dict(text='Gestational Diabetes (%)', font=dict(color='#ff6b6b')),
                tickfont=dict(color='#ff6b6b')
            ),
            yaxis2=dict(
                title=dict(text='Average Mother Age (years)', font=dict(color='#4facfe')),
                tickfont=dict(color='#4facfe'),
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig2, use_container_width=True, key='gestational_diabetes_trend_chart')
        
        st.markdown("""**Key Insights:**
        - **Teen mothers (under 20):** Higher preterm birth (8.5%) and stillbirth (4.8) rates
        - **Optimal age (20-34):** Lowest complication rates across all measures
        - **Age 35-39:** Moderate increase in risks; C-section rate 42.8%
        - **Age 40+:** Significantly elevated risks:
          - Preterm birth: 9.8% (36% higher than 20-29)
          - Stillbirth: 6.4 per 1,000 (83% higher)
          - C-section: 54.3% (majority of births)
        - **C-section trend:** Increases with age due to complications, slower labor
        - **Gestational diabetes:** Risk doubles after age 40
        - **Prenatal care:** Critical for managing age-related risks""")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Sources
    with st.expander("📚 Data Sources", expanded=False):
        st.markdown("""
        ### Data Sources
        
        All statistics sourced from official UK government and NHS data:
        """)
        
        st.markdown("- [ONS Birth Statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths) - Birth rates, parental age")
        st.markdown("- [ONS Child Mortality Statistics](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/bulletins/childhoodinfantandperinatalmortalityinenglandandwales/latest) - Infant mortality, stillbirths")
        st.markdown("- [MBRRACE-UK Maternal Mortality Reports](https://www.npeu.ox.ac.uk/mbrrace-uk) - Maternal deaths")
        st.markdown("- [NHS Digital Mental Health of Children and Young People Survey](https://digital.nhs.uk/data-and-information/publications/statistical/mental-health-of-children-and-young-people-in-england) - Child mental health")
        st.markdown("- [NHS Digital National Child Measurement Programme](https://digital.nhs.uk/data-and-information/publications/statistical/national-child-measurement-programme) - Child obesity")
        st.markdown("- [HFEA Fertility Treatment Data](https://www.hfea.gov.uk/about-us/publications/research-and-data/) - IVF success rates")
        st.markdown("- [PHE Congenital Anomaly Statistics](https://www.gov.uk/government/collections/congenital-anomaly-statistics) - Birth defects")
        st.markdown("- [NHS Health Survey for England](https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england) - Child physical health")
        
        st.markdown("""
        **Geographic Coverage:** Most statistics are England & Wales; some UK-wide.
        
        **Data Currency:** Latest available data is typically 2021-2022, published 12-18 months after collection.
        """)
