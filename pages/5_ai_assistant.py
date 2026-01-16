"""
AI Assistant Page - Accessible from main navigation
Full-featured AI chat interface for exploring UK dating statistics
"""

import streamlit as st

# Use the src package import to avoid module resolution issues
from src.ai.assistant import render_ai_chat, initialize_session_state

# Page configuration
st.set_page_config(
    page_title="AI Assistant - UK Dating Calculator",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Header
st.markdown("# 🤖 AI Assistant")
st.markdown("Ask questions about UK dating statistics, demographics, income distribution, and more!")

# Render the chat interface
render_ai_chat()

# Footer with tips
st.markdown("---")
st.markdown("""
### 💡 Tips for better questions:

- **Be specific**: Instead of "Tell me about dating", try "What percentage of UK adults aged 25-34 are single?"
- **Ask about demographics**: "Compare marriage rates between different ethnicities" or "Income distribution by age and gender"
- **Request comparisons**: "How has marriage rate changed over time?" or "Gender differences in employment?"
- **Ask for explanations**: "Why is the employment rate lower at 55-64?" or "What factors affect dating pool size?"

### 📊 Related Pages:

- **Dating Pool Calculator**: Calculate your specific dating pool based on criteria
- **Income Demographics**: Explore UK income distribution
- **Marriage Statistics**: Comprehensive marriage and family data
- **Baby & Child Health**: Child health statistics and trends
""")

# Files used for AI responses (data footprint)
with st.expander("Files Used (AI Assistant Context)", expanded=False):
    st.markdown(
        """
- data/raw/censusbasedstatisticsuk2021.xlsx (population by age and sex)
- data/raw/Home Geography Table 8.7a   Annual pay - Gross 2024.xlsx (ASHE earnings percentiles)
- data/raw/marital_status_and_living_arrangements_2002_2024.xlsx (marital status trends)
- data/processed/employment_rate_by_age_gender.csv (employment rates)
- data/processed/single_rate_by_age.csv (single / never married rates)
- data/processed/income_distribution_male.csv and data/processed/income_distribution_female.csv (income distributions)
        """
    )
