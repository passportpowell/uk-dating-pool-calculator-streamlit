# SPECIFIC DATA EXTRACTION REQUIREMENTS

## 1. SINGLE RATES BY AGE - VERY HIGH PRIORITY

**Source File**: `data_cache/raw/Families and households in the UK 2024.pdf`

**What to Find**:
- Look for table titled "Living arrangements by age" OR "Marital status by age" OR "Family status by age"
- Should show age bands (e.g., 16-24, 25-34, 35-44, 45-54, 55-64, 65+)
- Should have a column for "Single" or "Never married"
- Need the PERCENTAGE (not count)

**Exact CSV Format Required**:
```
age_band,single_rate
16-24,0.92
25-34,0.50
35-44,0.25
45-54,0.18
55-64,0.14
65+,0.10
```

**Instructions**:
1. Open PDF → Use Ctrl+F to search for "living arrangements" or "marital status"
2. Find the table with age bands (columns) and marital status categories (rows)
3. Locate the row for "Single" or "Never married" 
4. Read the percentage for each age band
5. Convert % to decimal (e.g., 92% = 0.92)
6. Create CSV with two columns: `age_band` and `single_rate`
7. Save as: `data_cache/single_rate_by_age.csv`

**File will be used for**: Filtering by "single" relationship status in dating pool

---

## 2. EMPLOYMENT RATES BY AGE AND GENDER - HIGH PRIORITY

**Source File**: `data_cache/raw/Labour Force Survey performance and quality monitoring report_ October to December 2023.pdf`

**What to Find**:
- Look for table with "Employment rate" by age and gender
- Should have:
  - Column headers: Age bands (16-24, 25-34, 35-44, 45-54, 55-64, 65+)
  - Row headers: Male, Female (or separate tables for each)
- Need PERCENTAGE employed for each age/gender combination

**Exact CSV Format Required**:
```
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

**Instructions**:
1. Open PDF → Use Ctrl+F to search for "employment rate by age" or "economic activity by age"
2. Find the table with employment data broken down by age bands AND gender
3. For EACH age band, read:
   - Male employment rate (as %)
   - Female employment rate (as %)
4. Convert % to decimal (e.g., 65% = 0.65)
5. Create CSV with three columns: `age_band`, `gender`, `rate`
6. Gender column must be exactly "Male" or "Female" (capitalized)
7. Age bands should match: 16-24, 25-34, 35-44, 45-54, 55-64, 65+
8. Save as: `data_cache/employment_rate_by_age_gender.csv`

**File will be used for**: Calculating probability of person being employed

**Note**: The XLS files you downloaded show overall employment rates (one number), NOT broken by age. This PDF should have the age breakdown.

---

## 3. SELF-EMPLOYED INCOME BY GENDER - LOWER PRIORITY

**Source File**: Either:
- `data_cache/raw/Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf`
- `data_cache/raw/Table_3.10_2223 Income of individuals with self-employment income 2022 to 2023.ods`

**What to Find**:
- Table showing self-employment income distribution
- Should have income brackets with counts/percentages for males and females
- OR percentile data similar to ASHE (10th, 20th, 25th, etc. percentiles)

**Exact CSV Format Required** (two separate files):
```
# self_employed_income_distribution_male.csv
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

```
# self_employed_income_distribution_female.csv
[Same format as above]
```

**Instructions**:
1. Try the ODS file first (open with LibreOffice Calc or Excel)
   - Look for table with self-employment income brackets
   - Find male and female columns
   - Extract data
2. If ODS doesn't have usable data, try the PDF:
   - Search for "self-employment income" table
   - Look for income ranges (£0-10k, £10k-20k, etc.)
   - Find counts or percentages for each gender
   - Calculate probability distribution
3. Save as two files:
   - `data_cache/self_employed_income_distribution_male.csv`
   - `data_cache/self_employed_income_distribution_female.csv`

**File will be used for**: Self-employed income filtering (secondary - less commonly used)

---

## PRIORITY ORDER (Do in this sequence)

1. **FIRST** (10 mins): Single rates by age
   - Most impactful for filtering
   - Should be a simple straightforward table
   - Easy to extract

2. **SECOND** (15 mins): Employment rates by age/gender
   - Important for probability calculations
   - More complex table but clearly structured
   - May be split into male/female sections

3. **THIRD** (10 mins): Self-employed income
   - Only if you have time
   - Lower impact feature
   - Can use placeholder if needed

---

## VERIFICATION CHECKLIST

After extracting each CSV, verify:

**Single Rates**:
- [ ] File exists: `data_cache/single_rate_by_age.csv`
- [ ] Has 2 columns: age_band, single_rate
- [ ] Has 6 rows (one per age band)
- [ ] All values are decimals between 0 and 1
- [ ] Values make sense (younger should have higher single rates)

**Employment Rates**:
- [ ] File exists: `data_cache/employment_rate_by_age_gender.csv`
- [ ] Has 3 columns: age_band, gender, rate
- [ ] Has 12 rows (6 age bands × 2 genders)
- [ ] Gender is exactly "Male" or "Female"
- [ ] All rates are decimals between 0 and 1
- [ ] Female rates generally lower than male (statistical pattern)
- [ ] Younger and middle-age higher than 65+

**Self-Employed Income**:
- [ ] Files exist: `self_employed_income_distribution_male.csv` and `_female.csv`
- [ ] Each has 2 columns: income_bracket, probability
- [ ] Each has 8 rows (one per bracket)
- [ ] All probabilities are decimals between 0 and 1
- [ ] Probabilities sum to 1.0 for each file

---

## TESTING AFTER EXTRACTION

Once you've created the CSVs:

```powershell
# Verify files exist
Get-ChildItem data_cache\*.csv

# Check single rates format
Get-Content data_cache\single_rate_by_age.csv

# Check employment rates format
Get-Content data_cache\employment_rate_by_age_gender.csv

# Restart app
streamlit run app.py
```

Then in the app:
1. Go to Dating Pool Calculator
2. Try filtering by:
   - Age (should use employment rates)
   - Single/Relationship status (should use single rates)
3. Check "Data Provenance" on Income Demographics page - should show all 3 datasets
4. Results should reflect official data

---

## STUCK? Here's Help

**Can't find the right table in the PDF?**
- Try different search terms: "age", "employment", "single", "marital", "living arrangements"
- Check the table of contents at the start of the PDF
- Look for appendices or detailed tables sections

**Data has different age bands?**
- Use closest match (e.g., if PDF has 16-19, 20-24 but you need 16-24, take average)
- Add a note in the CSV with `#` comments explaining any adjustments

**Percentages don't sum to 100% in marital status table?**
- Might be showing only selected categories
- Sum just the "single" row alone - that's your single_rate
- Or may show all statuses (single, married, divorced, widowed, etc.) separately

**Multiple tables in the same document?**
- Extract from the UK-wide table (not regional breakdowns)
- Use the most recent data year
- Prefer "actual" or "observed" over "forecast" or "projected"
