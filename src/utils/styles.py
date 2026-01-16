"""
UK Dating Pool Calculator - Styles Module
Contains all CSS styling for the Streamlit app
"""

# Custom CSS - Dark Mode Optimized
CUSTOM_CSS = """
    <style>
    /* Main header - bright gradient for visibility in dark mode */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #8b9eff 0%, #9d7bc4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    /* Sub-header - lighter color for dark mode */
    .sub-header {
        text-align: center;
        color: #b0b0b0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Result box - vibrant gradient that works in dark mode */
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(139, 158, 255, 0.3);
    }
    
    .result-percentage {
        font-size: 5rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
    }
    
    .result-count {
        font-size: 1.8rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Info cards - theme aware with semi-transparent background */
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        border-left: 4px solid #8b9eff;
        border: 1px solid rgba(139, 158, 255, 0.2);
    }
    
    .info-card h3 {
        color: #8b9eff;
        margin-top: 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    /* Metric highlights - brighter for dark mode */
    .metric-highlight {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
        box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling for dark mode */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.2);
    }
    
    /* Make sidebar widgets more visible */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] .stNumberInput label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    /* Improve dataframe styling for dark mode */
    .dataframe {
        font-size: 0.95rem;
    }
    
    /* Make dataframes more readable in dark mode */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid rgba(139, 158, 255, 0.2);
    }
    
    /* Improve tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        border: 1px solid rgba(139, 158, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: 1px solid rgba(139, 158, 255, 0.5);
    }
    
    /* Improve expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border: 1px solid rgba(139, 158, 255, 0.2);
        font-weight: 500;
    }
    
    /* Better text contrast */
    p, li, span, div {
        color: inherit;
    }
    
    /* Markdown headers */
    h1, h2, h3, h4 {
        color: #e0e0e0;
    }
    
    /* Caption text should be lighter but readable */
    .caption {
        color: #b0b0b0 !important;
    }
    
    /* Links should be visible */
    a {
        color: #8b9eff !important;
    }
    
    a:hover {
        color: #a8b8ff !important;
    }
    
    /* Make metric values stand out */
    [data-testid="stMetricValue"] {
        color: #8b9eff;
    }
    </style>
"""
