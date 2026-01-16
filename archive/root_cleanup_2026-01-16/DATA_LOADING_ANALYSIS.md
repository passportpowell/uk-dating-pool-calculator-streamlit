# Data Loading Architecture Analysis Report

**Generated**: January 16, 2026  
**Workspace**: e:\OneDrive\Github\UK dating statistic calculator zbook

---

## Executive Summary

The application follows a **hybrid architecture** with:
- **Primary data source**: `data.py` with hardcoded constants
- **Override mechanism**: `data_loader.py` for CSV-based overrides from `data_cache/`
- **Data processing scripts**: Standalone extraction/conversion utilities that don't use the formal loading pipeline

### Key Findings:
✅ **Main app properly uses data.py**  
✅ **UI modules properly import from data.py**  
⚠️ **data_loader.py has minimal usage** (only referenced in data.py itself)  
⚠️ **Data extraction scripts operate independently** (they generate the CSV files)  
⚠️ **Inconsistent data loading pattern** - data_loader provides fallback mechanism but isn't actively imported

---

## 1. Files That Properly Use data.py

These files import from `data.py` and use the constants directly. This is the **correct and intended pattern**.

### UI & Display Modules:
- **ui_sidebar.py** ✅
  - Imports: `ETHNICITY_DISTRIBUTION, MIN_WAGE_ANNUAL, MEDIAN_SALARY, AVERAGE_SALARY`
  - Purpose: Display options in sidebar filters
  
- **ui_results.py** ✅
  - Imports: `UK_ADULT_POPULATION, UK_REGIONS`
  - Purpose: Display breakdown and maps

- **ui_marriage_stats_content.py** ✅
  - Imports: Multiple marriage/children/family constants
  - Purpose: Display marriage statistics

- **ui_income_stats_content.py** ✅
  - Imports: Income distribution constants
  - Purpose: Display income demographics

- **ui_baby_stats_content.py** ✅
  - Imports: `BABY_HEALTH_DATA`
  - Purpose: Display baby/child health statistics

- **map_visualization.py** ✅
  - Imports: `UK_REGIONS, UK_ADULT_POPULATION`
  - Purpose: Create regional distribution maps

- **calculations.py** ✅
  - Imports: 12+ distribution constants (ages, heights, income, ethnicity, etc.)
  - Purpose: Calculate probabilities based on data constants
  - **Note**: Has multiple local imports in functions (lines 154, 387, 413, 453)

### Pages (Streamlit):
- **pages/1_Dating_Pool_Calculator.py** ✅
  - Imports: `UK_ADULT_POPULATION`
  - Purpose: Main calculator interface

- **pages/2_Income_Demographics.py** ✅
  - No direct data imports (uses ui modules)

- **pages/3_Marriage_Statistics.py** ✅
  - No direct data imports (uses ui modules)

- **pages/4_Baby_And_Child_Health.py** ✅
  - No direct data imports (uses ui modules)

- **pages/5_AI_Assistant.py** ✅
  - No direct data imports (uses ai_assistant module)

### Entry Point:
- **app.py** ✅
  - No direct data imports (imports from styles and ai_assistant)
  - Purpose: Main Streamlit home page

### Other Modules:
- **styles.py** ✅
  - No data imports (pure CSS/styling)

- **ai_assistant.py** ✅
  - No direct data imports (queries data from calculations dynamically)

---

## 2. Files That Use data_loader.py

**VERY LIMITED USAGE** - This is a concern:

### Direct Imports:
- **data.py** (line 335) ✅
  ```python
  from data_loader import load_override_data
  ```
  - This is the only direct import of `data_loader`
  - **Purpose**: data.py's module-level code attempts to load overrides from `data_cache/`
  - **Status**: This is correct architecture - data.py is the gatekeeper

### Indirect Usage:
- **No other files directly import from data_loader**
- All other files import from `data.py` which internally uses `data_loader`

---

## 3. Files That Load Data From Files Independently

These files **BYPASS the formal data loading system** and directly read from files. This is acceptable for **data extraction/processing scripts** but not for the main app.

### Data Extraction & Processing Scripts (Legitimate):
- **parse_data_files.py** ✅ (Acceptable)
  - Reads: `pd.read_excel()` (lines 42, 45, 137)
  - Purpose: Parse raw ONS/HMRC files and generate CSVs
  - **Status**: Standalone data processing utility - OK to bypass loader

- **finalize_ethnicity_extraction.py** ✅ (Acceptable)
  - Reads: `pd.read_excel()` (line 22)
  - Reads/Writes: `open()` (lines 118, 133)
  - Purpose: Final ethnicity data extraction
  - **Status**: Data processing utility - OK to bypass loader

- **fetch_sources.py** ✅ (Acceptable)
  - Reads: API endpoints and `open()` file operations (lines 26, 32, 95)
  - Reads: `pd.read_csv()`, `pd.read_excel()` from network responses (lines 100, 102)
  - Purpose: Download and cache datasets
  - **Status**: Data fetching utility - OK to bypass loader

- **extract_income_distribution.py** ✅ (Acceptable)
  - Reads: `pd.read_excel()` (lines 19-20)
  - Writes: `open()` (lines 184, 201)
  - Purpose: Extract ASHE income data
  - **Status**: Data extraction utility - OK to bypass loader

- **extract_ethnicity.py** ✅ (Acceptable)
  - Reads: `pd.read_excel()` (line 20)
  - Purpose: Extract Census ethnicity data
  - **Status**: Data extraction utility - OK to bypass loader

- **extract_data.py** ✅ (Acceptable)
  - Reads: `pd.read_excel()` (lines 26, 45, 69)
  - Purpose: Extract Census and ODS data
  - **Status**: Data extraction utility - OK to bypass loader

- **process_raw_data.py** ✅ (Acceptable)
  - Reads: Multiple `pd.read_excel()` calls throughout
  - Purpose: Process downloaded files into normalized CSVs
  - **Status**: Data processing utility - OK to bypass loader

- **explore_ods.py** ✅ (Acceptable)
  - Reads: `pd.read_excel()` (line 26)
  - Purpose: Exploration/debugging script
  - **Status**: Dev utility - OK to bypass loader

- **debug_ashe.py** ✅ (Acceptable)
  - Reads: `pd.read_excel()` (line 10)
  - Purpose: Debugging script
  - **Status**: Dev utility - OK to bypass loader

### Other Utilities:
- **data_loader.py** itself uses `open()` (lines 17, 40, 136) ✅
  - Purpose: Load CSV overrides
  - **Status**: Legitimate for this module

- **data_cache/raw/extraction/ scripts**
  - Various scripts use `pd.read_excel()`, `pd.read_csv()`, and `pdfplumber.open()`
  - **Status**: Raw data processing - OK to bypass loader

---

## 4. Inconsistencies & Issues

### ⚠️ ISSUE 1: data_loader.py Underutilized

**Current State:**
- `data_loader.py` exists and provides `load_override_data()` function
- Only called once: in `data.py` at module initialization
- No other files import from it

**Risk:**
- If main logic in `data.py` fails to call `data_loader`, overrides are never loaded
- Other files can't independently use `data_loader` to get overrides

**Recommendation:**
- ✅ Current architecture is acceptable IF data.py properly initializes overrides on import
- Should verify `load_override_data()` is actually being called and working

### ⚠️ ISSUE 2: data.py Internal Calls

**Current State:**
- `calculations.py` has local imports within functions (lines 154, 387, 413, 453)
  ```python
  from data import GENDER_SPLIT  # Inside function
  ```

**Risk:**
- Local imports inside functions bypass module-level initialization
- If override data needs to be loaded before use, these could fail
- Performance: importing on each function call

**Recommendation:**
- Move local imports to module-level (top of file)
- Use global import pattern like other modules

### ⚠️ ISSUE 3: Lack of Data Provenance Tracking

**Current State:**
- `data_loader.py` doesn't track which CSV files were loaded or their timestamps
- `fetch_sources.py` generates metadata but it's not integrated with data loading
- `provenance_ui.py` looks for `DATA_PROVENANCE` from `data.py` but catches exceptions

**Risk:**
- Users/developers don't know if they're using curated or override data
- No audit trail of which datasets are actually loaded

**Recommendation:**
- Enhance `data_loader.py` to track loaded files
- Store metadata in `data.py` for display in UI

### ⚠️ ISSUE 4: Multiple Entry Points for Override Data

**Current State:**
- Data can come from:
  1. Hardcoded constants in `data.py`
  2. CSV files in `data_cache/` (via `data_loader.py`)
  3. Various extraction scripts that regenerate CSVs

**Risk:**
- Unclear which source is authoritative
- Manual extraction scripts don't automatically update `data_cache/`
- No validation that extracted CSVs are properly formatted for `data_loader`

**Recommendation:**
- Document expected CSV formats for `data_loader.py`
- Ensure extraction scripts output in correct format
- Add schema validation

---

## 5. Data Loader Details

### data_loader.py Functions:

1. **`_load_simple_kv_csv(path)`** 
   - Format: CSV with columns `key, value`
   - Returns: Dict with normalized values (sum = 1.0)
   - Used for: Age distribution, ethnicity, education, etc.

2. **`_load_employment_csv(path)`**
   - Format: CSV with columns `age_band, gender, rate`
   - Returns: Dict[age_band -> Dict[gender -> rate]]
   - Used for: Employment rates, self-employment rates

3. **`_load_income_csv(path)`**
   - Format: CSV with columns `income_band, gender, count/rate`
   - Returns: Dict[income_band -> rate]
   - Used for: Income distributions by gender

4. **`load_override_data()`** (Main entry point)
   - Attempts to load all CSV overrides from `data_cache/`
   - Returns: Dict of loaded distributions
   - **Called from**: `data.py` module initialization

---

## 6. Summary Table

| Category | Files | Status | Pattern |
|----------|-------|--------|---------|
| **Main App Entry** | app.py | ✅ | Uses styles/ai_assistant |
| **Pages** | 1-5_*.py | ✅ | Import from data.py (indirectly via UI modules) |
| **Calculations** | calculations.py | ⚠️ | Uses local imports in functions |
| **UI Modules** | ui_*.py | ✅ | Direct data.py imports |
| **Utilities** | map_visualization.py, styles.py | ✅ | Direct data.py imports or none |
| **Data Loading** | data.py | ✅ | Calls data_loader.py on init |
| **Data Processing** | fetch_sources.py, parse_data_files.py, extract_*.py | ✅ | Legitimate direct file access |
| **Data Override** | data_loader.py | ⚠️ | Only used by data.py |
| **Development** | explore_ods.py, debug_ashe.py | ✅ | Acceptable for dev scripts |

---

## 7. Recommendations

### High Priority:
1. **Verify data_loader initialization**: Confirm `load_override_data()` is actually being called in `data.py` and logging results
2. **Fix calculations.py local imports**: Move them to module-level
3. **Add data loading validation**: Log which data sources (hardcoded vs. CSV) are being used

### Medium Priority:
4. **Document CSV schemas**: Ensure extraction scripts output correctly-formatted CSVs
5. **Enhance provenance tracking**: Track which CSVs were loaded in `DATA_PROVENANCE`
6. **Add data source validation**: Validate CSV formats before loading

### Low Priority:
7. **Consolidate extraction scripts**: Consider merging similar extraction utilities
8. **Add tests for data_loader**: Unit tests for CSV parsing edge cases

---

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         Streamlit App Entry Points          │
│  (app.py, pages/1-5_*.py)                  │
└──────────────────┬──────────────────────────┘
                   │
                   ├─→ UI Modules (ui_*.py) ──┐
                   │                           │
                   └─→ calculations.py ────────┤
                                               │
                   ┌───────────────────────────┘
                   │
                   ↓
            ┌──────────────┐
            │  data.py     │ ← Main data source
            │              │
            │  - Constants │
            │  - Calls     │
            │    data_     │
            │    loader()  │
            └──────────────┘
                   ↑
                   │
            ┌──────────────────────────┐
            │  data_loader.py          │
            │  (Override mechanism)    │
            │  Loads: data_cache/*.csv │
            └──────────────────────────┘
                   ↑
                   │
         ┌─────────┴──────────┐
         │                    │
    ┌────────────┐    ┌──────────────────┐
    │ fetch_     │    │ parse_data_      │
    │ sources.py │    │ files.py, etc.   │
    │ (Download) │    │ (Extract & CSV)  │
    └────────────┘    └──────────────────┘
         ↓                    ↓
    ┌──────────────────────────────────┐
    │  data_cache/ (CSV files)         │
    │  - *.csv override files          │
    │  - metadata.json                 │
    └──────────────────────────────────┘
```

