"""
UK Dating Pool Calculator - Map Visualization Module
Contains map creation functionality
"""

import folium
from src.data.constants import UK_REGIONS, UK_ADULT_POPULATION


def create_dating_pool_map(total_probability):
    """Create an interactive map showing estimated matches by UK region.

    Circles scale with estimated matches and include popups showing counts.
    """
    # Create base map centered on UK with aesthetic CartoDB Positron tiles
    m = folium.Map(
        location=[54.5, -3.5],
        zoom_start=6,
        tiles='CartoDB positron',
        attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    )
    
    # Calculate regional scaling factor to ensure regional totals match UK total
    total_regional_adults = sum(data['adult_pop'] for data in UK_REGIONS.values())
    regional_scale = UK_ADULT_POPULATION / total_regional_adults
    
    # Calculate all regional matches first to determine color scaling
    regional_matches_dict = {}
    for region, data in UK_REGIONS.items():
        regional_matches_dict[region] = max(0, int(round(data['adult_pop'] * regional_scale * total_probability)))
    
    # Get min and max for color scaling
    max_matches = max(regional_matches_dict.values())
    min_matches = min(regional_matches_dict.values())
    
    # Add markers for each region
    for region, data in UK_REGIONS.items():
        regional_matches = regional_matches_dict[region]
        
        # Calculate color based on relative position
        if max_matches > min_matches:
            ratio = (regional_matches - min_matches) / (max_matches - min_matches)
        else:
            ratio = 0.5
        
        # Color gradient: Red (low) -> Orange -> Yellow -> Green -> Purple (high)
        if ratio < 0.2:
            color = '#EF5350'  # Red - very low
        elif ratio < 0.4:
            color = '#FF7043'  # Orange - low
        elif ratio < 0.6:
            color = '#FFA726'  # Amber - medium-low
        elif ratio < 0.8:
            color = '#66BB6A'  # Green - medium-high
        else:
            color = '#667eea'  # Purple - very high

        # Radius scales with sqrt of matches; further reduced for smaller circles (meters)
        radius = 3000
        if max_matches > 0:
            radius = max(3000, int(3000 + 15000 * (regional_matches / max_matches) ** 0.5))
        
        # Tooltip shows info on hover; popup also shows counts on click
        popup_text = f"{region}<br>Estimated matches: {regional_matches:,}"
        hover_text = f"{region} — {regional_matches:,} estimated matches"
        
        folium.Circle(
            location=[data['lat'], data['lon']],
            radius=radius,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.5,
            weight=2,
            opacity=0.8,
            popup=folium.Popup(popup_text, max_width=200),
            tooltip=hover_text
        ).add_to(m)
    
    return m
