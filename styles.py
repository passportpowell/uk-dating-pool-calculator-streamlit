"""
UK Dating Pool Calculator - Styles Module
Contains all CSS styling for the Streamlit app
"""

# Custom CSS - Premium Glassmorphism Theme (Dark Mode Optimized)
CUSTOM_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
    
    /* Apply font family globally */
    .stApp {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Custom background color to support dark glass look */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #1e1b29 0%, #0c0a0f 100%);
    }

    /* Main header - premium styling with subtle text shadow */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 3.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #ff8b94 0%, #ff8ba7 20%, #9d7bc4 70%, #8b9eff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        filter: drop-shadow(0px 2px 10px rgba(157, 123, 196, 0.15));
        animation: fadeIn 1.2s ease-in-out;
    }
    
    /* Sub-header - lighter color with tracking */
    .sub-header {
        text-align: center;
        color: #bfaabf;
        font-size: 1.25rem;
        margin-bottom: 2.5rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        animation: fadeIn 1.5s ease-in-out;
    }
    
    /* Result box - premium gradient with soft inner shadow and bright neon glow */
    .result-box {
        background: linear-gradient(135deg, rgba(255, 139, 148, 0.15) 0%, rgba(118, 75, 162, 0.25) 100%);
        backdrop-filter: blur(15px);
        padding: 3.5rem 2.5rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.15),
                    0 0 30px rgba(118, 75, 162, 0.2);
        border: 1px solid rgba(255, 139, 148, 0.25);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .result-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.25),
                    0 0 40px rgba(118, 75, 162, 0.35);
        border-color: rgba(255, 139, 148, 0.4);
    }
    
    .result-percentage {
        font-size: 5.5rem;
        font-weight: 800;
        margin: 0.8rem 0;
        background: linear-gradient(135deg, #ff8b94 0%, #ff8ba7 50%, #8b9eff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0px 2px 8px rgba(255, 139, 148, 0.4));
    }
    
    .result-count {
        font-size: 1.95rem;
        opacity: 0.95;
        font-weight: 600;
        letter-spacing: -0.2px;
        color: #f3e8ff;
    }
    
    /* Info cards - beautiful premium glassmorphism */
    .info-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        margin-bottom: 1.8rem;
        border: 1px solid rgba(139, 158, 255, 0.1);
        transition: border-color 0.3s ease, background 0.3s ease;
    }
    
    .info-card:hover {
        border-color: rgba(139, 158, 255, 0.25);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .info-card h3 {
        color: #ff8ba7;
        margin-top: 0;
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.2px;
    }
    
    /* Metric highlights - brighter for dark mode */
    .metric-highlight {
        background: linear-gradient(135deg, #ff8b94 0%, #764ba2 100%);
        color: white;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
        box-shadow: 0 4px 12px rgba(255, 139, 148, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Progress bars customization */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #ff8b94 0%, #764ba2 100%) !important;
    }
    
    /* Sidebar styling for dark mode */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 23, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ff8ba7 !important;
        font-weight: 700;
    }
    
    /* Make sidebar widgets more visible */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] .stNumberInput label {
        color: #e2d9ec !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Improve dataframe styling for dark mode */
    .dataframe {
        font-size: 0.95rem;
        color: #e2d9ec;
    }
    
    /* Make dataframes more readable in dark mode */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid rgba(139, 158, 255, 0.1);
    }
    
    /* Improve tab styling to look very premium and custom */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 8px 12px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 12px 24px !important;
        font-weight: 600;
        font-size: 1.05rem !important;
        border: 1px solid rgba(139, 158, 255, 0.08);
        transition: all 0.3s ease;
        color: #b0a5c0 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.06);
        color: #fff !important;
        border-color: rgba(139, 158, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff8b94 0%, #764ba2 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 139, 148, 0.3);
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.25);
    }
    
    /* Improve expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(139, 158, 255, 0.1);
        font-weight: 600;
        font-size: 1.05rem;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(139, 158, 255, 0.25);
    }
    
    /* Better text contrast */
    p, li, span, div {
        color: #dfd7e7;
    }
    
    /* Markdown headers */
    h1, h2, h3, h4 {
        color: #f1ecf6;
        font-weight: 700;
    }
    
    /* Caption text should be lighter but readable */
    .caption {
        color: #a496b5 !important;
    }
    
    /* Links should be visible */
    a {
        color: #ff8ba7 !important;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: #ffb3c6 !important;
        text-decoration: underline;
    }
    
    /* Make metric values stand out */
    [data-testid="stMetricValue"] {
        color: #ff8ba7 !important;
        font-weight: 700;
    }
    
    /* Keyframe animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Custom CSS tooltips & warnings */
    .stAlert {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    </style>
"""

