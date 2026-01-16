"""
UK Dating Pool Calculator - Home Page
Welcome page with navigation to different sections

Structure:
- src/ai/: AI integration (OpenAI ChatGPT)
- src/calculations/: Probability calculation functions
- src/data/: Statistical data and constants (ONS, NHS, HMRC)
- src/ui/: Streamlit UI components
- src/utils/: Maps, styling, and utilities

Pages:
- 1_dating_pool.py: Main dating pool calculator
- 2_income_demographics.py: Income statistics explorer
- 3_marriage_statistics.py: Marriage and family statistics
- 4_baby_health.py: Baby and child health data
- 5_ai_assistant.py: AI-powered Q&A about statistics
- 6_cost_of_living.py: Family lifestyle cost calculator

Data:
- data/processed/: CSV overrides for statistical data
- data/raw/: Original source files from ONS, NHS, HMRC
"""

import streamlit as st
from src.utils.styles import CUSTOM_CSS
from src.ai.assistant import render_ai_sidebar

# Page configuration
st.set_page_config(
    page_title="UK Dating Pool Calculator",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def main():
    # Render AI sidebar on all pages
    render_ai_sidebar()
    
    # Header
    st.markdown('<div class="main-header">UK Dating Pool Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Calculate your realistic dating pool size using real UK statistics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">United Kingdom includes England, Scotland, Wales, and Northern Ireland (NOT Republic of Ireland)</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Welcome section
    st.markdown("""
    ## Welcome! 👋
    
    This calculator helps you understand your realistic dating pool size in the UK based on your preferences and criteria.
    
    ### 🎯 What You Can Do:
    
    Use the navigation sidebar (👈) or click the links below to explore different sections:
    """)
    
    # Navigation cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 15px 0;">🎯 Dating Pool Calculator</h3>
            <p style="margin: 0 0 15px 0;">Enter your dating criteria and calculate your realistic dating pool size. Get detailed breakdowns by each filter, geographic distribution maps, and probability analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; border-radius: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 15px 0;">💍 Marriage Statistics</h3>
            <p style="margin: 0 0 15px 0;">Comprehensive UK marriage and divorce statistics including remarriage rates, stepfamily data, interracial marriage patterns, and historical trends.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; border-radius: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 15px 0;">💷 Income Demographics</h3>
            <p style="margin: 0 0 15px 0;">Explore UK income distribution by age, gender, ethnicity, and employment type. See how many people earn above specific thresholds in different demographics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 30px; border-radius: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 15px 0;">👶 Baby & Child Health</h3>
            <p style="margin: 0 0 15px 0;">UK health statistics for babies and children including birth rates, health conditions, developmental milestones, and demographic patterns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Third row with remaining pages
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: white; padding: 30px; border-radius: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 15px 0;">🤖 AI Assistant</h3>
            <p style="margin: 0 0 15px 0;">Ask questions about UK dating statistics using AI. Get instant answers, insights, and data interpretations powered by OpenAI GPT.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #ff9a56 0%, #ffca3a 100%); color: white; padding: 30px; border-radius: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 15px 0;">💰 Cost of Living Calculator</h3>
            <p style="margin: 0 0 15px 0;">Calculate the annual household income needed to support your desired lifestyle including housing, education, retirement, and children's future.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key features
    st.markdown("""
    ## ✨ Key Features
    
    - **Real UK Data**: All statistics from official ONS Census 2021, NHS surveys, and government sources
    - **Comprehensive Filters**: Age, height, income, education, ethnicity, body type, children, marriage history, and more
    - **Interactive Visualizations**: Charts, maps, and breakdowns showing how each criterion affects your pool
    - **Demographic Insights**: Understand UK population patterns across income, marriage, and family structures
    - **AI-Powered Insights**: Ask questions and get instant answers about dating statistics
    - **Transparent Methodology**: Full source citations and explanations for all data points
    
    ## 📊 Data Sources
    
    All statistics are based on official UK government data:
    
    - **ONS Census 2021** - Population demographics, ethnicity, living arrangements
    - **ONS Labour Force Survey 2023** - Employment and income data
    - **NHS Health Survey for England 2021** - Height, weight, and health statistics
    - **ONS Marriages & Divorces 2022** - Marriage rates, divorce patterns
    - **ONS Families and Households 2022** - Children, stepfamilies, household composition
    - **HMRC Income Tax Statistics** - Self-employment income distributions
    
    ## 🚀 Getting Started
    
    1. **Navigate to "Dating Pool Calculator"** using the sidebar (👈) or menu
    2. **Enter your dating criteria** (age, height, income, etc.)
    3. **Click "Calculate"** to see your dating pool size
    4. **Explore detailed breakdowns** with probability analysis and maps
    5. **Check other sections** for deeper demographic insights
    6. **Ask the AI Assistant** for insights about specific demographics
    
    ---
    
    ### 📅 Data Currency
    
    Most recent comprehensive data available is from 2021-2023. ONS typically releases annual statistics with 12-18 month lag.
    We are currently in 2025; 2023 data has been published, 2024 data expected in 2025-2026.
    """)
    
    # Footer
    st.markdown("---")
    st.caption("UK Dating Pool Calculator | Based on official ONS and NHS statistics | Last updated: 2025")


if __name__ == "__main__":
    main()
