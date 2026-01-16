# Manual Data Extraction Guide

## Status

✅ **COMPLETED**: Ethnicity Distribution  
- Source: `censusbasedstatisticsuk2021.xlsx` (Census 2021 Table_06)
- Output: `data_cache/ethnicity_distribution.csv`
- Extracted: 17 ethnicity categories with probabilities

## Remaining Extractions (PDFs)

### 1. Single Rates by Age
**Source File**: `Families and households in the UK 2024.pdf`

**What to Extract**: Living arrangements by age table showing percentage/count of single (never married) individuals

**Expected CSV Format**: `data_cache/single_rate_by_age.csv`
```csv
age_band,single_rate
16-24,0.92
25-34,0.50
35-44,0.25
45-54,0.18
55-64,0.14
65+,0.10
```

**Steps**:
1. Open the PDF and search for "living arrangements" or "marital status by age"
2. Find table with age bands and percentages for "Single (never married)"
3. Copy data to Excel with columns: `age_band`, `single_rate`
4. Convert percentages to decimals (e.g., 50% = 0.50)
5. Save as CSV to `data_cache/single_rate_by_age.csv`

---

### 2. Employment Rates by Age and Gender
**Source File**: `Labour Force Survey performance and quality monitoring report_ October to December 2023.pdf`

**What to Extract**: Employment rates broken down by age band and gender

**Expected CSV Format**: `data_cache/employment_rate_by_age_gender.csv`
```csv
age_band,gender,rate
16-24,Male,0.65
16-24,Female,0.62
25-34,Male,0.88
25-34,Female,0.80
35-44,Male,0.90
35-44,Female,0.82
45-54,Male,0.88
45-54,Female,0.83
55-64,Male,0.73
55-64,Female,0.68
65+,Male,0.12
65+,Female,0.08
```

**Steps**:
1. Open PDF and search for "employment rate" or "economic activity"
2. Find table showing employment rates by age and gender
3. Copy to Excel with columns: `age_band`, `gender`, `rate`
4. Ensure gender values are exactly "Male" or "Female"
5. Convert percentages to decimals
6. Save as CSV

---

### 3. Employee Income Distribution (Male)
**Source File**: `Employee earnings in the UK 2025.pdf` (ASHE data)

**What to Extract**: Annual earnings distribution for male employees

**Expected CSV Format**: `data_cache/income_distribution_male.csv`
```csv
income_bracket,probability
Under £10k,0.05
£10k-£20k,0.15
£20k-£30k,0.20
£30k-£40k,0.25
£40k-£50k,0.15
£50k-£75k,0.12
£75k-£100k,0.05
Over £100k,0.03
```

**Steps**:
1. Open PDF and find "Annual earnings" or "Gross annual pay" table
2. Look for male-specific data or overall percentile distribution
3. Map percentiles to income brackets:
   - Under £10k: bottom percentile
   - £10k-£20k: ~10th-25th percentile
   - £20k-£30k: ~25th-50th percentile
   - £30k-£40k: ~50th-65th percentile
   - £40k-£50k: ~65th-75th percentile
   - £50k-£75k: ~75th-85th percentile
   - £75k-£100k: ~85th-95th percentile
   - Over £100k: top 5%
4. Calculate probabilities (difference between percentiles)
5. Normalize so probabilities sum to 1.0
6. Save as CSV

---

### 4. Employee Income Distribution (Female)
**Source File**: `Employee earnings in the UK 2025.pdf` (ASHE data)

**What to Extract**: Annual earnings distribution for female employees (same format as male)

**Expected CSV Format**: `data_cache/income_distribution_female.csv`
(Same structure as male version)

---

### 5. Self-Employed Income Distribution (Male)
**Source File**: `Table_3.10_2223 Income of individuals with self-employment income 2022 to 2023.ods` OR `Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf`

**What to Extract**: Income distribution for self-employed males

**Expected CSV Format**: `data_cache/self_employed_income_distribution_male.csv`
```csv
income_bracket,probability
Under £10k,0.25
£10k-£20k,0.20
£20k-£30k,0.18
£30k-£40k,0.15
£40k-£50k,0.10
£50k-£75k,0.08
£75k-£100k,0.03
Over £100k,0.01
```

**Steps**:

**For ODS file** (if odfpy installed):
1. Open with LibreOffice Calc or Excel
2. Find table with self-employment income brackets
3. Extract male-specific columns
4. Map to standard brackets and normalize

**For PDF file**:
1. Search for "self-employment income" tables
2. Find gender-specific data if available
3. Copy to Excel and format as above

---

### 6. Self-Employed Income Distribution (Female)
**Source File**: Same as above

**Expected CSV Format**: `data_cache/self_employed_income_distribution_female.csv`
(Same structure as male version)

---

## Quick Commands

After creating CSVs, verify with:
```powershell
Get-ChildItem "data_cache\*.csv"
```

Check CSV content:
```powershell
Get-Content "data_cache\single_rate_by_age.csv"
```

Test app loading:
```powershell
streamlit run app.py
```

Check provenance display:
- Navigate to Income Demographics page
- Expand "Data Provenance" section at bottom
- Should show ethnicity_distribution with Census 2021 source

---

## Semi-Automated: HMRC ODS File

The HMRC ODS file can potentially be parsed automatically. Run:

```powershell
python extract_data.py 2>&1 | Select-Object -First 300
```

This will show the structure of the ODS file. If income brackets are clearly visible, we can create a parser to extract them automatically.

---

## Notes

- All PDFs are official ONS/HMRC publications
- Data is typically in tables with clear labels
- Use Ctrl+F in PDF to search for key terms
- Age bands may not exactly match - use closest mapping
- Income brackets may need interpolation between percentiles
- Ensure all probabilities sum to 1.0 (normalize if needed)

## Testing After Extraction

Once you've created the CSVs:

1. **Verify Files Exist**:
   ```powershell
   Get-ChildItem data_cache\*.csv | Select-Object Name, Length
   ```

2. **Check Data Format**:
   Open each CSV in notepad/Excel to verify column names match expected format

3. **Run App**:
   ```powershell
   streamlit run app.py
   ```

4. **Verify Provenance**:
   - Go to pages/2_Income_Demographics.py
   - Scroll to bottom and expand "Data Provenance"
   - Should show ethnicity_distribution with source file and timestamp

5. **Check Calculations**:
   - Use Dating Pool Calculator with specific filters
   - Results should reflect the official data distributions
   - Compare percentages to original PDF tables for sanity check

## Priority Order

If time-limited, extract in this order:

1. **Single rates by age** - affects all relationship status filtering
2. **Employee income (male & female)** - core to income filtering
3. **Employment rates** - affects employment calculations
4. **Self-employed income** - secondary to employee income
