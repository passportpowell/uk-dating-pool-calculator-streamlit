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

### Visualization & Analysis
- 📈 **Interactive Breakdown**: Visual cascade showing how each filter narrows your dating pool
- 🗺️ **Regional Distribution**: UK map showing geographic distribution of matches
- 📊 **Probability Analysis**: Detailed breakdown of each filter's impact
- 📊 **Probability Cascade**: Understand cumulative filtering effects

### Documentation
- 📚 **Full Source Citations**: Every statistic properly sourced and referenced
- 🔍 **Methodology Explained**: Complete transparency on calculations
- ⚠️ **Limitations Disclosed**: Honest about what the calculator can and cannot predict

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd "UK dating statistic calculator"
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
- **Pandas**: Data manipulation
- **NumPy**: Numerical calculations
- **SciPy**: Statistical distributions (height calculations)

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

- **v1.0.0** (December 2025)
  - Initial release
  - Full UK ONS data integration
  - Multi-select race filter
  - Comprehensive source citations
  - Interactive Streamlit interface

## Contact

For questions, suggestions, or issues, please open an issue on GitHub.

**Connect with me:**
- GitHub: [@passportpowell](https://github.com/passportpowell)
- LinkedIn: [Otis Powell](https://www.linkedin.com/in/otispowell/)

---

**Made with ❤️ using real UK data**
