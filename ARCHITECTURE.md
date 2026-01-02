# Module Architecture Diagram

## Project Structure

```
UK dating statistic calculator/
│
├── 📄 app.py (Main Entry Point - 13 KB)
│   └── Orchestrates all modules, handles user flow
│
├── 📦 Data Layer
│   └── data.py (9.5 KB)
│       ├── Population statistics
│       ├── Distributions (age, income, ethnicity, etc.)
│       ├── Regional data
│       └── Marriage/relationship stats
│
├── 🧮 Logic Layer
│   └── calculations.py (10.7 KB)
│       ├── Age probability
│       ├── Height probability (normal distribution)
│       ├── Income probability
│       ├── Education probability
│       ├── Ethnicity probability
│       ├── Body type probability
│       ├── Orientation compatibility
│       ├── Children probability
│       ├── Marriage history probability
│       ├── Baldness probability
│       └── Utility functions (cm ↔ feet/inches)
│
├── 🎨 Presentation Layer
│   ├── styles.py (5 KB)
│   │   └── All CSS styling
│   │
│   ├── ui_sidebar.py (11.7 KB)
│   │   ├── User gender & orientation
│   │   ├── Looking for gender
│   │   ├── Age range selector
│   │   ├── Height input (metric/imperial)
│   │   ├── Body type multiselect
│   │   ├── Income selector
│   │   ├── Education selector
│   │   ├── Ethnicity multiselect
│   │   ├── Relationship status
│   │   ├── Children preference
│   │   ├── Marriage history
│   │   └── Baldness preference
│   │
│   ├── ui_results.py (12 KB)
│   │   ├── display_results() - Main result box
│   │   ├── display_probability_breakdown_tab() - Tab 1
│   │   ├── display_criteria_tab() - Tab 2
│   │   └── display_map_tab() - Tab 3
│   │
│   └── map_visualization.py (4.1 KB)
│       └── create_dating_pool_map() - Interactive UK map
│
└── 💾 Backup Files
    ├── app_old_monolithic.py (Original 192 KB)
    ├── app copy.py (Original backup)
    └── app_original_full.py (Reference backup)
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                         (Streamlit App)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ui_sidebar.py                            │
│                   Collects User Inputs                          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ • Gender & Orientation  • Age Range   • Height            │ │
│  │ • Body Type            • Income       • Education         │ │
│  │ • Ethnicity            • Relationship • Children          │ │
│  │ • Marriage History     • Baldness     • Calculate Button  │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                           app.py                                │
│                   Main Calculation Logic                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  For each filter:                                         │ │
│  │  1. Call calculation function from calculations.py       │ │
│  │  2. Get data from data.py                                │ │
│  │  3. Calculate individual probability                     │ │
│  │                                                           │ │
│  │  Then:                                                    │ │
│  │  • Multiply all probabilities                            │ │
│  │  • Calculate estimated matches                           │ │
│  │  • Pass results to UI components                         │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│ calculations │    │    data.py   │    │  ui_results.py   │
│     .py      │◄───┤              │    │                  │
│              │    │ • UK_ADULT_  │    │ • display_       │
│ • calculate_ │    │   POPULATION │    │   results()      │
│   age_prob   │    │ • AGE_       │    │ • display_       │
│ • calculate_ │    │   DISTRIBUTION│   │   probability_   │
│   height_    │    │ • INCOME_    │    │   breakdown()    │
│   prob       │    │   DISTRIBUTION│   │ • display_       │
│ • calculate_ │    │ • ETHNICITY_ │    │   criteria()     │
│   income_    │    │   DISTRIBUTION│   │ • display_map()  │
│   prob       │    │ • etc...     │    │                  │
│ • etc...     │    │              │    │                  │
└──────────────┘    └──────────────┘    └──────────────────┘
                                                  │
                                                  │
                                                  ▼
                                        ┌──────────────────┐
                                        │ map_            │
                                        │ visualization   │
                                        │      .py        │
                                        │                 │
                                        │ • create_       │
                                        │   dating_pool_  │
                                        │   map()         │
                                        │                 │
                                        │ Uses data.py:   │
                                        │ • UK_REGIONS    │
                                        └──────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESULTS DISPLAY                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Tab 1: Probability Breakdown (Cascade Table)            │ │
│  │  Tab 2: Your Selected Criteria (Summary)                 │ │
│  │  Tab 3: Geographic Distribution (Map + Regional Table)   │ │
│  │  Tab 4: Marriage Statistics (From original file)         │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                        ┌──────────┐
                        │  styles  │
                        │   .py    │
                        │          │
                        │ Applied  │
                        │ globally │
                        └──────────┘
```

## Import Dependency Graph

```
app.py
  │
  ├─► data.py (no further dependencies)
  │
  ├─► styles.py (no further dependencies)
  │
  ├─► calculations.py
  │     └─► data.py
  │           ├─ AGE_DISTRIBUTION
  │           ├─ MALE_HEIGHT_MEAN/STD
  │           ├─ FEMALE_HEIGHT_MEAN/STD
  │           ├─ INCOME_DISTRIBUTION_MALE/FEMALE
  │           ├─ EDUCATION_DISTRIBUTION
  │           ├─ ETHNICITY_DISTRIBUTION
  │           ├─ BODY_TYPE_DISTRIBUTION_MALE/FEMALE
  │           ├─ CHILDREN_DISTRIBUTION
  │           ├─ MARRIAGE_HISTORY
  │           ├─ BALDNESS_BY_AGE
  │           └─ SEXUAL_ORIENTATION_DISTRIBUTION
  │
  ├─► ui_sidebar.py
  │     ├─► data.py
  │     │     ├─ ETHNICITY_DISTRIBUTION (for dropdown)
  │     │     ├─ MIN_WAGE_ANNUAL
  │     │     ├─ MEDIAN_SALARY
  │     │     └─ AVERAGE_SALARY
  │     └─► calculations.py
  │           └─ cm_to_feet_inches() - utility function
  │
  ├─► ui_results.py
  │     ├─► data.py
  │     │     ├─ UK_ADULT_POPULATION
  │     │     └─ UK_REGIONS
  │     ├─► calculations.py
  │     │     └─ cm_to_feet_inches() - for display
  │     └─► map_visualization.py
  │           └─ create_dating_pool_map()
  │
  └─► map_visualization.py
        └─► data.py
              ├─ UK_REGIONS (lat/lon/population)
              └─ UK_ADULT_POPULATION (for scaling)
```

## Calculation Flow

```
User Input → Sidebar → app.py main()
                          │
                          ▼
              ┌───────────────────────┐
              │  Calculate 12 filters │
              └───────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
  [Gender Prob]                       [Age Prob]
  49.2% or 50.8%                      calculate_age_probability()
        │                                   │
        ▼                                   ▼
  [Height Prob]                       [Body Type Prob]
  calculate_height_probability()      calculate_body_type_probability()
        │                                   │
        ▼                                   ▼
  [Income Prob]                       [Education Prob]
  calculate_income_probability()      calculate_education_probability()
        │                                   │
        ▼                                   ▼
  [Ethnicity Prob]                    [Orientation Prob]
  calculate_ethnicity_probability()   calculate_orientation_probability()
        │                                   │
        ▼                                   ▼
  [Single Prob]                       [Children Prob]
  SINGLE_RATE or 1.0                  calculate_children_probability()
        │                                   │
        ▼                                   ▼
  [Marriage Prob]                     [Baldness Prob]
  calculate_marriage_probability()    calculate_baldness_probability()
        │                                   │
        └───────────────┬───────────────────┘
                        │
                        ▼
              ┌───────────────────────┐
              │  Multiply All Probs   │
              │  Total = P1×P2×...×P12│
              └───────────────────────┘
                        │
                        ▼
              ┌───────────────────────┐
              │  Estimated Matches =  │
              │  UK_Adult_Pop × Total │
              └───────────────────────┘
                        │
                        ▼
              ┌───────────────────────┐
              │   Display Results     │
              │   (ui_results.py)     │
              └───────────────────────┘
```

## Benefits of Modular Structure

### Before (Monolithic)
```
app.py (3390 lines, 192 KB)
├─ Data definitions (lines 1-700)
├─ Helper functions (lines 700-1000)
├─ Calculation functions (lines 1000-1500)
├─ UI sidebar code (lines 1500-2000)
├─ Results display (lines 2000-2500)
├─ Marriage statistics (lines 2500-3200)
└─ Data sources (lines 3200-3390)

❌ Hard to navigate
❌ Difficult to maintain
❌ Can't reuse components
❌ Testing is challenging
```

### After (Modular)
```
📁 Project Root
├─ app.py (270 lines, 13 KB) ✅ Easy to understand
├─ data.py (240 lines, 9.5 KB) ✅ Single source of truth
├─ calculations.py (285 lines, 10.7 KB) ✅ Pure functions, testable
├─ ui_sidebar.py (310 lines, 11.7 KB) ✅ Isolated UI component
├─ ui_results.py (320 lines, 12 KB) ✅ Reusable display logic
├─ map_visualization.py (120 lines, 4.1 KB) ✅ Independent visualization
└─ styles.py (160 lines, 5 KB) ✅ Centralized styling

✅ Clear organization
✅ Easy maintenance
✅ Reusable components
✅ Testable functions
✅ Each file < 15 KB
```

---

**Legend:**
- 📄 = Python file
- 📦 = Data module
- 🧮 = Logic module
- 🎨 = Presentation module
- 💾 = Backup/archive
