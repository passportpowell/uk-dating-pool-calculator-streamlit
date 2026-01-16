# UK Dating Pool Calculator

A Streamlit web application that calculates your realistic dating pool size using real UK government statistics from ONS (Office for National Statistics), NHS, HMRC, and other official sources.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge)](http://99.81.223.163:32768/)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌐 Live Application

**[Launch Calculator →](http://99.81.223.163:32768/)**

## ✨ Key Features

### Calculator Features
- 🎯 **Real UK Statistics**: All data sourced from ONS, NHS, HMRC, and official UK government sources with hyperlinked references
- 📊 **Comprehensive Filters**: 
  - Age range selection (18-65+)
  - Height preferences with metric & imperial (cm, feet/inches)
  - Body type (BMI categories from NHS data)
  - **Income levels** (£0 to £1M+ millionaires, includes self-employed & business owners from HMRC data)
  - **Education** (minimum level + all above - e.g., "GCSE" includes A-Level, Undergraduate, Postgraduate)
  - Multiple ethnicity selection (Census 2021)
  - Sexual orientation compatibility
  - Relationship status
  - Children preferences
  - Marriage history
  - Male pattern baldness (age-adjusted prevalence)

### 💍 Marriage & Relationship Statistics (Always Visible)
**Explore comprehensive UK marriage data before or after using the calculator:**
- 📈 Marriage trends (2013-2022) with COVID-19 impact analysis
- 💔 Divorce statistics including no-fault reform (April 2022)
- 🧭 Interracial marriage drill-down by ethnic group with same vs cross-ethnicity splits
- 👥 Gender context in drill-down (male/female marriage age patterns) and divorce median-age comparison chart
- ⚖️ Who initiates divorce (63% women, 30% men, 6.9% joint)
- 📋 Grounds for divorce (pre and post reform comparison)
- 🎂 Marriage age demographics
- 🔄 Remarriage statistics and success rates
- 🗺️ Regional marriage variations across UK
- 🌍 International comparisons
- 💰 Income and education correlations with marriage
- 👶 Children and family statistics
- All sections collapsible for easy navigation

### New Features (December 2025 Update)
- 💍 **Always-Visible Marriage Stats**: Comprehensive marriage data accessible before calculator use
- 💰 **Millionaire Income Bracket**: Now includes £1M+ earners with HMRC Self Assessment data
- 🏢 **Business Owners Included**: High-income data accounts for self-employed, directors, dividend income
- 🎓 **Smart Education Filter**: Select minimum level, automatically includes all higher qualifications (no more accidentally excluding degrees!)
- 📏 **Dual Height Units**: Displays both cm and feet/inches (e.g., 175.3cm = 5'9")
- 🔗 **Fully Sourced**: Every statistic has valid hyperlinks to official ONS, NHS, HMRC, WHO, and academic sources
- 📅 **Data Freshness Info**: Know when ONS updates statistics (annual releases ~12-18 months after reference year)

### New Features (January 2026 Update)
- � **AI Assistant**: ChatGPT-powered Q&A about UK statistics (requires OpenAI API key)
- 🤝 Interracial marriage drill-down with per-ethnicity same vs cross-ethnicity shares and pairing breakdowns
- 👥 Divorce demographics: gender median-age comparison plus contextual gender stats in drill-down
- 🏗️ **Complete Refactoring**: Modular src/ architecture with 6 sub-packages
- 📦 **Professional Structure**: Clean separation of AI, calculations, data, UI, and utilities
- 🗂️ **Data Organization**: Separate data/ directory with processed/ and raw/ subdirectories
- 🔧 Import cleanup and archiving of unused modules

### Visualization & Analysis
- 📈 **Interactive Breakdown**: Visual cascade showing how each filter narrows your dating pool
- 🗺️ **Regional Distribution**: UK map showing geographic distribution of matches
- 📊 **Probability Analysis**: Detailed breakdown of each filter's impact
- 📊 **Probability Cascade**: Understand cumulative filtering effects

### Documentation
- 📚 **Full Source Citations**: Every statistic properly sourced and referenced
- 🔍 **Methodology Explained**: Complete transparency on calculations
- ⚠️ **Limitations Disclosed**: Honest about what the calculator can and cannot predict

## 🏗️ Project Architecture

This project features a **professional, modular architecture** with AI capabilities:

```
📦 UK dating statistic calculator/
├── 📄 app.py                       # Main application entry (home page)
├── 📄 1_dating_pool.py             # Dating Pool Calculator page
├── 📄 2_income_demographics.py     # Income Statistics page  
├── 📄 3_marriage_statistics.py     # Marriage Statistics page
├── 📄 4_baby_health.py             # Baby & Child Health page
├── 📄 5_ai_assistant.py            # AI Assistant page (NEW!)
├── 📄 requirements.txt             # Python dependencies
│
├── 📁 src/                         # Main source package
│   ├── 📁 ai/                      # AI integration (NEW!)
│   │   └── assistant.py            # OpenAI ChatGPT integration
│   ├── 📁 calculations/            # Core calculations
│   │   └── dating_pool.py          # Probability calculation functions
│   ├── 📁 data/                    # Data management
│   │   ├── constants.py            # Statistical data & constants (ONS, NHS, HMRC)
│   │   ├── loader.py               # CSV data loader from data/processed/
│   │   └── provenance.py           # Data source tracking
│   ├── 📁 ui/                      # Streamlit UI components
│   │   ├── sidebar.py              # Sidebar input controls
│   │   ├── results.py              # Results display & tabs
│   │   ├── marriage_stats.py       # Marriage statistics display
│   │   ├── income_stats.py         # Income demographics display
│   │   └── baby_stats.py           # Baby health statistics display
│   └── 📁 utils/                   # Utilities
│       ├── styles.py               # CSS styling & UI themes
│       └── maps.py                 # Geographic distribution maps (Folium)
│
├── 📁 data/                        # Data files (external to code)
│   ├── processed/                  # Processed CSV data (5 overrides)
│   │   ├── single_rate_by_age.csv
│   │   ├── employment_rate_by_age_gender.csv
│   │   ├── ethnicity_distribution.csv
│   │   ├── income_distribution_male.csv
│   │   └── income_distribution_female.csv
│   └── raw/                        # Raw source files (44+ files, preserved for reference)
│       ├── ONS_*.xlsx              # Office for National Statistics data
│       ├── NHS_*.csv               # NHS Health Survey data
│       └── HMRC_*.xlsx             # HMRC Self Assessment data
│
└── 📁 archive/                     # Old/archived files (not in use)
    ├── old_pages/                  # Previous pages directory
    ├── old_root_files/             # Original root-level modules
    └── old_structure/              # Prior directory structure
```

### Module Overview

**Pages (Streamlit Multi-Page App)**:
- **app.py**: Home page with navigation and overview
- **1_dating_pool.py**: Main dating pool calculator with filters
- **2_income_demographics.py**: Income statistics by age, gender, ethnicity
- **3_marriage_statistics.py**: Marriage, divorce, interracial marriage data
- **4_baby_health.py**: Baby and child health statistics
- **5_ai_assistant.py**: AI-powered Q&A about UK statistics (NEW!)

**Source Modules (src/)**:
- **ai/assistant.py**: OpenAI ChatGPT integration for statistics Q&A (NEW!)
- **calculations/dating_pool.py**: Pure calculation functions (no UI logic)
- **data/constants.py**: All statistical data (ONS, NHS, HMRC) with CSV overrides
- **data/loader.py**: Loads data from data/processed/ directory
- **data/provenance.py**: Tracks data source metadata
- **ui/*.py**: Streamlit-specific UI rendering functions (5 modules)
- **utils/styles.py**: Custom CSS styling and themes
- **utils/maps.py**: Folium-based geographic distribution maps

**Data (data/)**:
- **processed/**: CSV files that override default data (5 files currently used)
- **raw/**: Original source files from ONS, NHS, HMRC (44+ files preserved)
- **ui_results.py**: Results visualization, breakdown tables, criteria display
- **map_visualization.py**: Folium-based UK regional distribution maps

📚 **Full documentation:** See [ARCHITECTURE.md](ARCHITECTURE.md), [MODULAR_STRUCTURE.md](MODULAR_STRUCTURE.md), and [QUICK_START.md](QUICK_START.md)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone https://github.com/passportpowell/uk-dating-pool-calculator-streamlit.git
cd uk-dating-pool-calculator-streamlit
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## How It Works

The calculator uses **independent probability multiplication** to estimate your dating pool:

```
P(match) = P(gender) × P(age) × P(height) × P(income) × P(education) × P(ethnicity) × P(single)
```

### Example Calculation

If you're looking for:
- **Gender**: Female (50% of population)
- **Age**: 25-35 (18.7% of adults)
- **Height**: 160-175cm (60% of females)
- **Income**: £30k+ (45% of females)
- **Education**: Degree or higher (41% of adults)
- **Ethnicity**: Any (100%)
- **Single**: Yes (35% of adults)

**Result**: 0.50 × 0.187 × 0.60 × 0.45 × 0.41 × 1.0 × 0.35 = **0.362%** or ~190,000 people in the UK

## Data Sources

All statistics are based on official UK data:

1. **Population Data**
   - [ONS Mid-2022 Population Estimates](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates)
   - Total UK Adult Population: ~52.6 million

2. **Ethnicity Distribution**
   - [ONS Census 2021](https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity)
   - England and Wales ethnic groups

3. **Height Distribution**
   - [NHS Health Survey for England](https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england)
   - Academic research on UK anthropometrics

4. **Income Statistics**
   - [ONS ASHE 2023](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours)
   - Annual Survey of Hours and Earnings

5. **Education Levels**
   - [ONS Education Statistics 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare)

6. **Relationship Status**
   - [ONS Families and Households 2022](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families)

## Features Breakdown

### Filters Available

- **Gender Selection**: Male or Female
- **Age Range**: 18-80 years (slider)
- **Height Range**: 140-210cm with conversions to feet
- **Minimum Income**: £0 to £100k+ brackets
- **Education Levels**: Multi-select from 5 qualification levels
- **Ethnicity**: Multi-select from 5 census categories
- **Relationship Status**: Toggle for single/available only

### Visual Features

- Clean, modern UI with gradient result displays
- Real-time probability breakdown table
- Criteria summary panel
- Reality check warnings based on selectivity
- Expandable data sources section with full methodology

## Important Notes

### Assumptions
- All criteria are treated as **independent** (some correlations exist in reality)
- Geographic distribution is **uniform** (actual distribution varies by region)
- Does not account for **mutual attraction** or **compatibility**

### Limitations
- Statistical model only - real dating success depends on many unquantifiable factors
- Does not consider local dating markets or social circles
- Some correlations between variables (e.g., education and income) are simplified
- Attractiveness and personality are not included

**Remember**: This is an educational tool. Your dating success isn't determined by statistics!

## Technical Stack

- **Streamlit**: Web framework
- **OpenAI API**: AI-powered statistics Q&A (gpt-4o-mini)
- **Pandas**: Data manipulation
- **NumPy**: Numerical calculations
- **SciPy**: Statistical distributions (height calculations)
- **Plotly**: Interactive visualizations
- **Folium**: Geographic map rendering

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/passportpowell/uk-dating-pool-calculator.git
   cd uk-dating-pool-calculator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API Key** (for AI features):
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY = "your-api-key-here"
   
   # Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access at**: http://localhost:8501

## Testing

Verify all imports are working:
```bash
python test_imports.py
```

Expected output: ✅ All 5 imports PASSED!

## Screenshots

### Main Interface
Select your preferences in the sidebar and click "Calculate" to see your dating pool size.

### Results Display
- Large percentage display
- Estimated number of matches
- Detailed probability breakdown
- Criteria summary

### Data Sources
Full transparency with expandable sources section including methodology and references.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas for improvement:

- Add regional breakdowns (London, Scotland, Wales, etc.)
- Include more demographic factors
- Add data visualization charts
- Mobile responsive improvements
- Additional statistics sources

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This calculator is for **educational and entertainment purposes only**. All statistics are based on official UK government data, but the model makes simplifying assumptions. Real-world dating success depends on countless factors beyond demographics, including personality, timing, compatibility, and individual circumstances.

## Version History

- **v3.0.0** (January 2026)
  - 🤖 **AI Assistant**: OpenAI ChatGPT integration for Q&A
  - 🏗️ **Major Refactoring**: Professional modular architecture (src/ with 6 sub-packages)
  - 📦 **Package Structure**: Clean separation (ai, calculations, data, ui, utils)
  - 🗂️ **Data Organization**: Separate data/ directory (processed/, raw/)
  - 📚 **Updated Documentation**: RESTRUCTURE_GUIDE.md, FIX_SUMMARY.md
  - 🔧 **Import System**: All modules use src.* imports
  - 🤝 Interracial marriage drill-down with detailed ethnicity pairings
  - 👥 Divorce demographics with gender analysis

- **v2.0.0** (January 2026)
  - ✨ **Major Refactoring**: Modular architecture (7 separate modules)
  - 📂 Clean separation of concerns for maintainability
  - 📚 Comprehensive documentation (ARCHITECTURE.md, MODULAR_STRUCTURE.md)
  - 👶 Added Baby & Fertility Statistics tab
  - 🗺️ Enhanced UK regional mapping
  - 🔧 Improved code organization and testability

- **v1.0.0** (December 2025)
  - 🚀 Initial release
  - 💍 Full UK ONS data integration
  - 🔗 Multi-select ethnicity filter
  - 📊 Comprehensive source citations
  - 🎨 Interactive Streamlit interface
  - 💰 Millionaire income bracket with HMRC data

## Contact

For questions, suggestions, or issues, please open an issue on GitHub.

**Connect with me:**
- GitHub: [@passportpowell](https://github.com/passportpowell)
- LinkedIn: [Otis Powell](https://www.linkedin.com/in/otispowell/)

---

**Made with ❤️ using real UK data**
