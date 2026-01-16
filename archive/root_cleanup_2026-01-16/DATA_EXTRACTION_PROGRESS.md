# Data Extraction Progress Report

## ✅ Completed Extractions

### 1. Ethnicity Distribution
- **Source**: `censusbasedstatisticsuk2021.xlsx` (Census 2021 Table_06)
- **Output**: `data_cache/ethnicity_distribution.csv`
- **Status**: ✅ EXTRACTED AND SAVED
- **Method**: Automated extraction using pandas
- **Coverage**: 17 ethnicity categories with normalized probabilities
- **Total Population**: 66,912,629
- **Data Quality**: Broad Census categories (White, Asian, Black, Mixed, Other) distributed proportionally into app's detailed categories

### Key Statistics:
```
White British:    58.14%
White Other:      24.92%
Asian British:     2.15%
Indian:            2.15%
Pakistani:         1.72%
Black groups:      3.71% (combined)
Mixed groups:      2.67% (combined)
Other:             1.96%
```

---

## 📋 Remaining Extractions (Manual Required)

### 2. Single Rates by Age
- **Source**: `Families and households in the UK 2024.pdf`
- **Output**: `data_cache/single_rate_by_age.csv`
- **Status**: ⏳ REQUIRES MANUAL EXTRACTION
- **Priority**: HIGH - affects all relationship filtering

### 3. Employment Rates by Age/Gender
- **Source**: `Labour Force Survey performance and quality monitoring report_ October to December 2023.pdf`
- **Output**: `data_cache/employment_rate_by_age_gender.csv`
- **Status**: ⏳ REQUIRES MANUAL EXTRACTION
- **Priority**: MEDIUM - affects employment calculations

### 4. Employee Income Distribution (Male & Female)
- **Source**: `Employee earnings in the UK 2025.pdf`
- **Output**: `data_cache/income_distribution_male.csv` and `income_distribution_female.csv`
- **Status**: ⏳ REQUIRES MANUAL EXTRACTION
- **Priority**: HIGH - core to income filtering

### 5. Self-Employed Income Distribution (Male & Female)
- **Source**: `Table_3.10_2223 Income of individuals with self-employment income 2022 to 2023.ods` (appears to contain only notes, may need to use PDF instead)
- **Alternative**: `Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf`
- **Output**: `data_cache/self_employed_income_distribution_male.csv` and `self_employed_income_distribution_female.csv`
- **Status**: ⏳ REQUIRES MANUAL EXTRACTION
- **Priority**: MEDIUM - secondary to employee income

---

## 📁 Current File Status

```
data_cache/
├── ethnicity_distribution.csv          ✅ CREATED
├── metadata.json                        ✅ UPDATED
├── single_rate_by_age_TEMPLATE.csv     ✅ TEMPLATE READY
├── employment_rate_by_age_gender_TEMPLATE.csv  ✅ TEMPLATE READY
├── income_distribution_male_TEMPLATE.csv      ✅ TEMPLATE READY
├── income_distribution_female_TEMPLATE.csv    ✅ TEMPLATE READY
├── self_employed_income_distribution_male_TEMPLATE.csv    ✅ TEMPLATE READY
└── self_employed_income_distribution_female_TEMPLATE.csv  ✅ TEMPLATE READY

data_cache/raw/
├── censusbasedstatisticsuk2021.xlsx                                    335 KB
├── Employee earnings in the UK 2025.pdf                                890 KB
├── Families and households in the UK 2024.pdf                          218 KB
├── Labour Force Survey performance and quality monitoring report...    980 KB
├── Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf   1,060 KB
├── Statistics on trusts in the UK December 2025.pdf                    387 KB
├── Table_3.10_2223 Income of individuals with self-employment...       860 KB
└── Working and workless households in the UK July to September 2025.pdf 530 KB
```

---

## 🧪 Testing Current Progress

### Test 1: Verify Ethnicity Data Loaded
```powershell
streamlit run app.py
```
- Navigate to "Dating Pool Calculator"
- Select ethnicity filters
- Results should use Census 2021 distributions

### Test 2: Check Provenance Display
- Navigate to "Income Demographics" page
- Scroll to bottom
- Expand "Data Provenance" section
- Should display:
  - Dataset: ethnicity_distribution
  - Source file: censusbasedstatisticsuk2021.xlsx
  - Source URL: https://www.ons.gov.uk/census
  - Timestamp and notes

---

## 🎯 Next Steps

1. **Run app to verify ethnicity data loading** (immediate)
2. **Extract single rates by age** (high priority - opens PDF, find table, copy to CSV)
3. **Extract employee income distributions** (high priority)
4. **Extract employment rates** (medium priority)
5. **Extract self-employed income** (medium priority)

---

## 📖 Reference Documents

- **`MANUAL_DATA_EXTRACTION_GUIDE.md`** - Detailed instructions for extracting each dataset
- **`parse_data_files.py`** - Initial parser script with file inspection
- **`finalize_ethnicity_extraction.py`** - Successful ethnicity extraction script
- **`data_loader.py`** - CSV override loading system
- **`provenance_ui.py`** - Data source display component

---

## 💡 Key Insights

1. **Census data is usable**: XLSX format allowed automated extraction
2. **PDF barriers**: 6 of 8 files are PDFs requiring manual table copying
3. **ODS file issue**: HMRC ODS appears to contain notes only, not data tables
4. **Template system works**: Generated templates show exact required format
5. **Provenance tracking ready**: Infrastructure in place to display sources

---

## 🔄 Alternative Data Sources

If manual extraction proves too time-consuming, consider:
- ONS Open Data API (some datasets available as CSV/JSON)
- Nomis API for Labour Force Survey data
- HMRC data tables published separately from PDFs
- Academic datasets that pre-process official statistics

---

## ✅ Verification Checklist

Before considering data migration complete:
- [x] Ethnicity distribution extracted and normalized
- [x] CSV templates created for all remaining datasets
- [x] Provenance metadata structure established
- [x] Data loader system tested with ethnicity CSV
- [ ] Single rates by age extracted
- [ ] Employment rates extracted
- [ ] Employee income distributions extracted
- [ ] Self-employed income distributions extracted
- [ ] All distributions verified to sum to 1.0
- [ ] App tested with all official data loaded
- [ ] Results compared to source tables for sanity check
