"""
UK Dating Pool Calculator - Map Visualization Module
Contains map creation functionality
"""

import folium
from data import UK_REGIONS, UK_ADULT_POPULATION


def create_dating_pool_map(total_probability):
    """Create an interactive map showing estimated matches by UK region"""
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
        regional_matches_dict[region] = int(data['adult_pop'] * regional_scale * total_probability)
    
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
        
        # Color gradient: Red (low) -> Orange -> Yellow -> Green -> Blue -> Purple (high)
        if ratio < 0.2:
            color = '#EF5350'  # Red - very low
            radius = 18000
        elif ratio < 0.4:
            color = '#FF7043'  # Orange - low
            radius = 25000
        elif ratio < 0.6:
            color = '#FFA726'  # Amber - medium-low
            radius = 32000
        elif ratio < 0.8:
            color = '#66BB6A'  # Green - medium-high
            radius = 40000
        else:
            color = '#667eea'  # Purple - very high
            radius = 50000
        
        # Add circle marker with modern styling
        folium.Circle(
            location=[data['lat'], data['lon']],
            radius=radius,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.5,
            weight=2,
            opacity=0.8,
            popup=folium.Popup(
                f"""<div style='font-family: "Segoe UI", Arial, sans-serif; width: 240px; padding: 8px;'>
                    <h4 style='margin: 0 0 12px 0; color: {color}; font-weight: 600; font-size: 16px;'>{region}</h4>
                    <div style='background: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid {color};'>
                        <p style='margin: 6px 0; font-size: 14px;'><b style='color: #555;'>Estimated Matches:</b><br>
                        <span style='font-size: 18px; color: {color}; font-weight: 600;'>{regional_matches:,}</span></p>
                        <p style='margin: 6px 0; font-size: 13px; color: #666;'><b>Adult Population:</b> {data['adult_pop']:,}</p>
                        <p style='margin: 6px 0; font-size: 13px; color: #666;'><b>Percentage:</b> {(total_probability * 100):.3f}%</p>
                    </div>
                </div>""",
                max_width=280
            ),
            tooltip=f"<b>{region}</b><br>{regional_matches:,} matches"
        ).add_to(m)
        
        # Add text label
        folium.Marker(
            location=[data['lat'], data['lon']],
            icon=folium.DivIcon(html=f"""
                <div style='font-size: 10pt; color: white; font-weight: bold; 
                     text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
                     white-space: nowrap;'>
                    {region}<br>{regional_matches:,}
                </div>
            """)
        ).add_to(m)
    
    return m
