"""
UK Dating Pool Calculator - Results Display Module
Contains results display and all tabs (breakdown, criteria, map, marriage stats)
Note: Marriage statistics tab content is extensive and located in app.py lines 1290-3200
This module imports from other modules for cleaner separation
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_folium import st_folium
from src.data.constants import UK_ADULT_POPULATION, UK_REGIONS
from src.calculations.dating_pool import cm_to_feet_inches
from src.utils.maps import create_dating_pool_map


def display_results(inputs, probabilities, estimated_matches, percentage):
    """Display the main results box"""
    st.markdown(f"""
        <div class="result-box">
            <h2 style="margin: 0 0 1rem 0; font-size: 1.8rem; opacity: 0.95;">🎯 Your Dating Pool</h2>
            <div class="result-percentage">{percentage:.3f}%</div>
            <div class="result-count">≈ {estimated_matches:,} people in the UK</div>
            <p style="margin-top: 1.5rem; font-size: 1rem; opacity: 0.9;">
                Out of {UK_ADULT_POPULATION:,} UK adults
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Reality check banner
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if percentage < 0.1:
            st.error("🔥 Extremely selective criteria! Your dating pool is very small for the population.")
        elif percentage < 1:
            st.warning("🔥 Extremely selective criteria! Your dating pool is very small for the population.")
        elif percentage < 5:
            st.info("🔥 Extremely selective criteria! Your dating pool is very small for the population.")
        else:
            st.success("✨ Relatively broad criteria. You have plenty of options!")


def display_probability_breakdown_tab(inputs, probabilities, estimated_matches, percentage):
    """Display the probability breakdown tab"""
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### Filter Cascade", unsafe_allow_html=True)
    st.caption("Each filter progressively narrows down the pool")
    
    # Unpack probabilities
    (gender_prob, age_prob, height_prob, body_type_prob, income_prob,
     education_prob, ethnicity_prob, orientation_prob, single_prob,
     children_prob, marriage_prob, baldness_prob) = probabilities
    
    breakdown_data = {
        "Criterion": ["Gender", "Age Range", "Height Range", "Body Type", "Income", 
                    "Education", "Ethnicity", "Orientation", "Single/Available", 
                    "Children", "Marriage History", "Baldness", "**TOTAL**"],
        "Probability": [
            f"{gender_prob*100:.1f}%",
            f"{age_prob*100:.1f}%",
            f"{height_prob*100:.1f}%",
            f"{body_type_prob*100:.1f}%",
            f"{income_prob*100:.1f}%",
            f"{education_prob*100:.1f}%",
            f"{ethnicity_prob*100:.1f}%",
            f"{orientation_prob*100:.1f}%",
            f"{single_prob*100:.1f}%",
            f"{children_prob*100:.1f}%",
            f"{marriage_prob*100:.1f}%",
            f"{baldness_prob*100:.1f}%",
            f"**{percentage:.3f}%**"
        ],
        "Remaining Pool": [
            f"{int(UK_ADULT_POPULATION * gender_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob * children_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob * children_prob * marriage_prob):,}",
            f"{int(UK_ADULT_POPULATION * gender_prob * age_prob * height_prob * body_type_prob * income_prob * education_prob * ethnicity_prob * orientation_prob * single_prob * children_prob * marriage_prob * baldness_prob):,}",
            f"**{estimated_matches:,}**"
        ]
    }
    st.dataframe(breakdown_data, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def display_criteria_tab(inputs):
    """Display the selected criteria tab"""
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### Selected Filters", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**👤 Your Gender:** {inputs['user_gender']}")
        st.markdown(f"**🔍 Looking for:** {inputs['looking_for']}")
        st.markdown(f"**🏳️‍🌈 Orientation:** {inputs['user_orientation']}")
        
        age_range = inputs['age_range']
        if age_range == (18, 99):
            st.markdown(f"**🎂 Age:** <span class='metric-highlight'>Any (18+)</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**🎂 Age:** <span class='metric-highlight'>{age_range[0]}-{age_range[1]} years</span>", unsafe_allow_html=True)
        
        # Format height display
        min_height_cm = inputs['min_height_cm']
        max_height_cm = inputs['max_height_cm']
        if min_height_cm == 140 and max_height_cm == 210:
            st.markdown(f"**📏 Height:** <span class='metric-highlight'>Any</span>", unsafe_allow_html=True)
        else:
            min_f, min_i = cm_to_feet_inches(min_height_cm)
            max_f, max_i = cm_to_feet_inches(max_height_cm)
            st.markdown(f"**📏 Height:** <span class='metric-highlight'>{min_height_cm:.0f}-{max_height_cm:.0f} cm ({min_f}'{min_i}\" - {max_f}'{max_i}\")</span>", unsafe_allow_html=True)
        
        min_income = inputs['min_income']
        if min_income > 0:
            st.markdown(f"**💰 Min Income:** <span class='metric-highlight'>£{min_income:,}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**💰 Min Income:** <span class='metric-highlight'>Any</span>", unsafe_allow_html=True)
    
    with col_b:
        st.markdown(f"**🏋️ Body Type:** <span class='metric-highlight'>{len(inputs['selected_body_types'])} type(s)</span>", unsafe_allow_html=True)
        st.markdown(f"**🎓 Education:** <span class='metric-highlight'>{inputs['education_level']} and above</span>", unsafe_allow_html=True)
        st.markdown(f"**🌍 Ethnicity:** <span class='metric-highlight'>{len(inputs['selected_ethnicities'])} group(s)</span>", unsafe_allow_html=True)
        st.markdown(f"**💑 Status:** <span class='metric-highlight'>{'Single only' if inputs['must_be_single'] else 'Any'}</span>", unsafe_allow_html=True)
        st.markdown(f"**👶 Children:** <span class='metric-highlight'>{len(inputs['acceptable_children'])} option(s)</span>", unsafe_allow_html=True)
        st.markdown(f"**💍 Marriage History:** <span class='metric-highlight'>{len(inputs['acceptable_marriage_history'])} option(s)</span>", unsafe_allow_html=True)
        if inputs['looking_for'] == "Male" or inputs['looking_for'] == "Any":
            st.markdown(f"**👨 Baldness:** <span class='metric-highlight'>{inputs['baldness_preference']}</span>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_map_tab(total_probability, estimated_matches):
    """Display the geographic distribution map tab"""
    if estimated_matches < 1:
        st.info("Dating pool is extremely small with the current filters — no regional map to display.")
        return

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Geographic Distribution of Potential Matches", unsafe_allow_html=True)
    st.markdown("""
    **Interactive Map:** Explore where your potential matches are located across the UK. 
    Each circle represents a region, with size and color indicating match density.
    """)
    st.markdown("")
    
    # Legend
    col_leg1, col_leg2, col_leg3 = st.columns(3)
    with col_leg1:
        st.markdown("🔴 **Low Density** - Fewer matches per capita")
    with col_leg2:
        st.markdown("🟣 **High Density** - More matches per capita")
    with col_leg3:
        st.markdown("⭕ **Circle Size** - Total estimated matches")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    
    # Create and display the map
    dating_map = create_dating_pool_map(total_probability)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Convert map to HTML to avoid JSON serialization issues
        import streamlit.components.v1 as components
        map_html = dating_map._repr_html_()
        components.html(map_html, width=1000, height=900, scrolling=True)
    
    st.markdown("")

    st.caption(
        "Estimates per region = regional adult population × (UK adult pop scaling) × your overall match probability. "
        "Adult populations come from ONS regional figures; probability comes from your filters applied to the whole UK. "
        "Circles are scaled by the estimated counts; hover to see the region and its estimated matches."
    )
    
    # Regional breakdown table
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Regional Breakdown Analysis", unsafe_allow_html=True)
    st.markdown("""
    **Understanding the numbers:** This table shows how your potential matches are distributed 
    across UK regions.
    """)
    st.markdown("")
    
    # Calculate regional data
    total_regional_adults = sum(data['adult_pop'] for data in UK_REGIONS.values())
    regional_scale = UK_ADULT_POPULATION / total_regional_adults
    
    regional_data = []
    for region, data in UK_REGIONS.items():
        regional_matches = int(round(data['adult_pop'] * regional_scale * total_probability))
        regional_data.append({
            "Region": region,
            "Adult Population": data['adult_pop'],
            "Estimated Matches": regional_matches,
            "% of Region": total_probability * 100,
        })

    regional_df = pd.DataFrame(regional_data)
    regional_df = regional_df.sort_values("Estimated Matches", ascending=False).reset_index(drop=True)

    # Build rank labels for display
    rank_labels = ['🥇 1st', '🥈 2nd', '🥉 3rd'] + [f"{i}th" for i in range(4, len(regional_df) + 1)]

    # Format numbers for display
    regional_df_display = regional_df.copy()
    regional_df_display["Match Rank"] = rank_labels
    regional_df_display["Adult Population"] = regional_df_display["Adult Population"].map(lambda x: f"{x:,}")
    regional_df_display["Estimated Matches"] = regional_df_display["Estimated Matches"].map(lambda x: f"{x:,}")
    regional_df_display["% of Region"] = regional_df_display["% of Region"].map(lambda x: f"{x:.3f}%")
    regional_df_display = regional_df_display[['Match Rank', 'Region', 'Adult Population', 'Estimated Matches', '% of Region']]
    
    st.dataframe(regional_df_display, hide_index=True, use_container_width=True)
    
    # Summary statistics
    st.markdown("")
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    top_region = regional_df.iloc[0]
    with col_sum1:
        st.metric("Top Region", top_region['Region'], f"{top_region['Estimated Matches']:,} matches")
    
    with col_sum2:
        total_matches = int(regional_df['Estimated Matches'].sum())
        st.metric("Total UK Matches", f"{total_matches:,}", f"{(total_probability * 100):.3f}% of population")
    
    with col_sum3:
        avg_regional_pct = total_probability * 100
        st.metric("Average Regional Rate", f"{avg_regional_pct:.3f}%", "Consistent across regions")
    
    st.markdown("")
    st.caption("💡 **Insight:** While absolute numbers vary by population, your probability of finding a match is consistent across all regions.")
    st.markdown('</div>', unsafe_allow_html=True)
