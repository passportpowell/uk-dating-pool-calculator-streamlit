# UK Dating Pool Calculator - Refactored Structure

## Overview

This project has been reorganized into a professional, modular structure with:
- **AI Features**: OpenAI ChatGPT integration for statistics Q&A (NEW!)
- **Organized Modules**: Logical grouping of calculations, UI, data, and utilities
- **Separate Data Management**: Raw data sources separated from processed CSVs
- **Clean Package Structure**: Python package best practices with `__init__.py` files

## Project Structure

```
.
├── app.py                           # Main Streamlit entry point (home page)
├── requirements.txt                 # Python dependencies
├── test_imports.py                  # Import verification script
├── 1_dating_pool.py                 # Streamlit page: Dating Pool Calculator
├── 2_income_demographics.py          # Streamlit page: Income Statistics
├── 3_marriage_statistics.py          # Streamlit page: Marriage Statistics
├── 4_baby_health.py                  # Streamlit page: Baby & Child Health
├── 5_ai_assistant.py                 # Streamlit page: AI Assistant (NEW!)
│
├── src/                              # Main source package
│   ├── __init__.py                  # Package initialization
│   │
│   ├── ai/                          # AI module (NEW!)
│   │   ├── __init__.py
│   │   └── assistant.py             # OpenAI ChatGPT integration
│   │
│   ├── calculations/                # Core calculations
│   │   ├── __init__.py
│   │   └── dating_pool.py           # Probability calculation functions
│   │
│   ├── data/                        # Data management
│   │   ├── __init__.py
│   │   ├── constants.py             # Statistical data & constants
│   │   ├── loader.py                # CSV data loader
│   │   └── provenance.py            # Data source tracking
│   │
│   ├── ui/                          # Streamlit UI components
│   │   ├── __init__.py
│   │   ├── sidebar.py               # Sidebar input controls
│   │   ├── results.py               # Results display
│   │   ├── marriage_stats.py        # Marriage statistics display
│   │   ├── income_stats.py          # Income demographics display
│   │   └── baby_stats.py            # Baby health statistics display
│   │
│   └── utils/                       # Utilities
│       ├── __init__.py
│       ├── styles.py                # Streamlit CSS styling
│       └── maps.py                  # Folium map visualization
│
├── data/                            # Data files (external to code)
│   ├── processed/                   # Processed CSV data
│   │   ├── single_rate_by_age.csv
│   │   ├── employment_rate_by_age_gender.csv
│   │   ├── ethnicity_distribution.csv
│   │   ├── income_distribution_male.csv
│   │   ├── income_distribution_female.csv
│   │   └── ... (other CSVs)
│   │
│   └── raw/                         # Raw source files (kept for reference)
│       ├── ONS_*.xlsx
│       ├── NHS_*.csv
│       └── ... (raw source data)
│
├── archive/                         # Old/archived files
│   ├── old_root_files/              # Original root-level Python files
│   ├── old_structure/               # Previous directory structure
│   └── ... (other archived items)
│
└── docs/                            # Documentation (optional)
    ├── ARCHITECTURE.md              # System architecture
    ├── SETUP_GUIDE.md               # Installation & running
    └── AI_FEATURES.md               # AI capabilities
```

## Key Changes

### 1. **New AI Features** ✨
- **File**: `src/ai/assistant.py`
- **Capabilities**: Ask questions about UK dating statistics, get instant AI-powered answers
- **Integration**: Available from AI Assistant page and sidebar on all pages
- **API**: OpenAI GPT-4o-mini (cost-efficient)
- **Status**: ✅ Fully integrated and functional

### 2. **Modular Organization**
- **`src/calculations/`**: Pure calculation functions (no UI logic)
- **`src/data/`**: All statistical data and constants
- **`src/ui/`**: Streamlit-specific UI rendering functions
- **`src/utils/`**: Maps, styling, and helper functions
- **`src/ai/`**: AI assistant functionality (NEW)

### 3. **Data Management**
- **`data/processed/`**: CSV overrides and processed data (5 files)
- **`data/raw/`**: Raw source files (44+ files) kept for reference
- **`data_cache/`**: No longer used (files migrated to `data/` folder)

### 4. **Clean Root Level**
- Only essential files at root: `app.py`, `requirements.txt`, and Streamlit pages
- Old module files archived in `archive/old_root_files/`
- Streamlit expects pages at root, which are now linked to `src/` imports

## Running the Application

### Setup (First Time)
```bash
# Install dependencies
pip install -r requirements.txt

# Test imports (verify structure is correct)
python test_imports.py

# Should show: ✅ All 5 imports PASSED!
```

### Run Application
```bash
# Start the Streamlit app
streamlit run app.py

# Opens at: http://localhost:8501
```

### Available Pages
1. **Home Page** (`app.py`) - Navigation and overview
2. **Dating Pool Calculator** (`1_dating_pool.py`) - Main calculator
3. **Income Demographics** (`2_income_demographics.py`) - Income statistics
4. **Marriage Statistics** (`3_marriage_statistics.py`) - Marriage/family data
5. **Baby & Child Health** (`4_baby_health.py`) - Health statistics
6. **AI Assistant** (`5_ai_assistant.py`) - AI-powered Q&A (NEW!)

## Data Management

### CSV Override System
The application loads CSV data with an override mechanism:

1. **Default data**: Hard-coded in `src/data/constants.py`
2. **Overrides**: Load from `data/processed/` CSVs if they exist
3. **Loading**: `src/data/loader.py` handles CSV loading
4. **Path**: Updated to use `data/processed/` directory

### Supported Override Files
- `single_rate_by_age.csv`
- `employment_rate_by_age_gender.csv`
- `ethnicity_distribution.csv`
- `income_distribution_male.csv`
- `income_distribution_female.csv`

## API Keys & Configuration

### OpenAI (Required for AI Features)
Set your OpenAI API key before running:

```bash
# On Windows PowerShell:
$env:OPENAI_API_KEY = "your-api-key-here"

# On Linux/Mac:
export OPENAI_API_KEY="your-api-key-here"
```

The AI Assistant will use `gpt-4o-mini` for cost-efficient responses.

## Imports Reference

### For UI Components
```python
from src.ui.sidebar import create_sidebar
from src.ui.results import display_results
from src.ui.marriage_stats import display_marriage_statistics_tab
```

### For Data
```python
from src.data.constants import UK_ADULT_POPULATION, AGE_DISTRIBUTION
```

### For Calculations
```python
from src.calculations.dating_pool import calculate_age_probability
```

### For AI
```python
from src.ai.assistant import AIAssistant, render_ai_chat
```

### For Utilities
```python
from src.utils.styles import CUSTOM_CSS
from src.utils.maps import create_dating_pool_map
```

## Testing

Run the import verification script:
```bash
python test_imports.py
```

Expected output:
```
Testing imports...

✓ Styles
✓ Data constants
✓ Calculations
✓ AI assistant
✓ UI sidebar

==================================================
✅ All 5 imports PASSED!
```

## Troubleshooting

### Import Errors
1. Ensure you're running from the project root directory
2. Check that all files in `src/` have been properly copied
3. Verify `__init__.py` files exist in all `src/` subdirectories
4. Run `python test_imports.py` to diagnose import issues

### Data Not Loading
1. Check that CSV files exist in `data/processed/` if overrides are needed
2. Verify path in `src/data/loader.py` points to correct directory
3. Check console output for any file not found errors

### AI Assistant Not Working
1. Verify `OPENAI_API_KEY` environment variable is set
2. Check OpenAI API key is valid and has available credits
3. Ensure `openai>=1.3.0` is installed: `pip install openai`

## Migration Notes

This project was recently refactored from a monolithic structure to a modular one:

**What Changed:**
- ✅ Files organized into `src/` subdirectories
- ✅ Data moved to `data/` directory (separate from code)
- ✅ Old files archived in `archive/`
- ✅ All imports updated to use new paths
- ✅ `__init__.py` files created for package structure
- ✅ AI features added with OpenAI integration
- ✅ Requirements updated with `openai>=1.3.0`

**What's Same:**
- ✅ All core functionality preserved
- ✅ Same data sources (ONS, NHS, etc.)
- ✅ Same UI and visualizations
- ✅ Same Streamlit pages (now with AI)

## Dependencies

Key packages (see `requirements.txt` for full list):
- `streamlit` - UI framework
- `pandas` - Data manipulation
- `plotly` - Visualizations
- `folium` - Maps
- `scipy` - Statistical functions
- `openai>=1.3.0` - AI assistant (NEW!)

## License & Attribution

All statistical data is sourced from official UK government sources (ONS, NHS, etc.) as documented in the code.

---

**Last Updated**: January 2025
**Structure Version**: 2.0 (Refactored with AI)
