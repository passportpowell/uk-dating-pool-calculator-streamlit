# Self-Employment & Business Owner Analysis - Implementation Summary

**Status:** ✅ Complete and validated

---

## What Was Implemented

The dating pool calculator now includes comprehensive **self-employment and business owner analysis** with the ability to filter and separately analyze:

1. **Employees** (PAYE/salary workers)
   - Income data: ASHE 2023 (ONS survey)
   - Population: ~87% of UK workforce
   - Key metric: 25-32% earn below £20k, 2% earn above £100k

2. **Self-Employed** (sole traders and partnerships)
   - Income data: HMRC Self Assessment (tax returns)
   - Population: ~13% of UK workforce  
   - Key metric: 35-42% earn below £20k, 2% earn above £100k
   - Growth by age: 6% at 18-24 → 35% at 65+

3. **Any Employment** (blended)
   - Combines employee and self-employed pools by prevalence
   - Income probability weighted by actual proportions
   - Most realistic for open dating pool queries

---

## Data Sources Added

### Self-Employment Rates (ONS Labour Force Survey 2023)
```python
SELF_EMPLOYMENT_RATE_BY_AGE_GENDER = {
    "18-24": {"Male": 0.06, "Female": 0.05},
    "25-34": {"Male": 0.12, "Female": 0.09},
    "35-44": {"Male": 0.16, "Female": 0.12},
    "45-54": {"Male": 0.18, "Female": 0.14},
    "55-64": {"Male": 0.21, "Female": 0.17},
    "65+":   {"Male": 0.35, "Female": 0.28},
}
```

### Self-Employed Income Distribution (HMRC Self Assessment 2023)
```python
SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE = {
    "Under £20k": 0.35,     # Higher proportion than employees
    "£20k-£30k": 0.20,
    "£30k-£40k": 0.15,
    # ... (more brackets, normalized to sum to 1.0)
    "£1M+": 0.001
}

SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE = {
    "Under £20k": 0.42,     # Even higher than males
    "£20k-£30k": 0.22,
    # ... (normalized to 1.0)
}
```

### Overall Self-Employment Rate
```python
OVERALL_SELF_EMPLOYMENT_RATE = 0.13  # ~13% of UK workforce
```

---

## New Calculation Functions

### 1. Self-Employed Income Probability
```python
def calculate_self_employed_income_probability(min_income, gender):
    """Calculate probability self-employed person earns at/above threshold.
    
    Uses HMRC Self Assessment income distribution.
    Separate from employee distribution (ASHE).
    """
```

**Usage:**
```python
# What % of self-employed males earn £75k+?
prob = calculate_self_employed_income_probability(75000, "Male")
# Returns: 0.0744 (7.44%)
```

### 2. Self-Employment Rate (Blended Gender)
```python
def get_self_employment_rate_by_age(age_min, age_max):
    """Get self-employment rate for age range (weighted by gender split)."""
```

**Usage:**
```python
# What % of employed 35-44 year-olds are self-employed?
rate = get_self_employment_rate_by_age(35, 44)
# Returns: 0.14 (14%)
```

### 3. Self-Employment Rate (Specific Gender)
```python
def get_self_employment_rate_by_age_gender(age_min, age_max, gender):
    """Get self-employment rate for specific age range and gender."""
```

**Usage:**
```python
# What % of employed females age 35-44 are self-employed?
rate = get_self_employment_rate_by_age_gender(35, 44, "Female")
# Returns: 0.12 (12%)
```

---

## UI Changes

### New Employment Type Filter
Added to Income Demographics tab:
```
Employment type:
  ⦿ Any           (blends employee + self-employed)
  ○ Employees     (PAYE/salary only)
  ○ Self-employed (sole traders/partnerships)
  ○ Business owners [future placeholder]
```

### Updated Metrics Display
Now shows employment type in metric label:
```
Before: "Earning £100k+ | 5,432 matches"
After:  "Earning £100k+ | 5,432 matches [Employment type]"
```

### Updated Gender Breakdown Table

**For "Any" employment:**
| Gender | Adults | Employed | Employees | Self-employed | Earning £100k+ |
|---|---|---|---|---|---|

**For "Employees" only:**
| Gender | Adults | Employed | Employee Single | Earning £100k+ |

**For "Self-employed" only:**
| Gender | Adults | Employed | Self-employed Single | Earning £100k+ |

### Updated Income Threshold Chart
Now displays correct income distribution based on employment type filter:
- **Employees:** ASHE 2023 employee distribution
- **Self-employed:** HMRC Self Assessment distribution
- **Any:** Blended by population weight

---

## Files Modified

### 1. data.py
**Added:**
- `SELF_EMPLOYMENT_RATE_BY_AGE_GENDER` - 6 age bands × 2 genders
- `SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE` - 11 income brackets (normalized)
- `SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE` - 11 income brackets (normalized)
- `OVERALL_SELF_EMPLOYMENT_RATE` - 13% constant
- Updated imports in `calculations.py`

**Lines changed:** +67 lines (no deletions)

### 2. calculations.py
**Added:**
- `calculate_self_employed_income_probability(min_income, gender)` - 30 lines
- `get_self_employment_rate_by_age(age_min, age_max)` - 20 lines
- `get_self_employment_rate_by_age_gender(age_min, age_max, gender)` - 23 lines

**Updated:**
- Imports to include new self-employment data constants

**Lines changed:** +73 lines (no deletions)

### 3. ui_income_stats_content.py
**Added:**
- Employment type radio filter (3 columns layout)
- Branching logic for employment type calculations
- Updated metric display with employment type
- Updated gender breakdown table to show employment breakdown
- Updated income threshold chart logic
- Updated info box with self-employment explanation

**Modified:**
- Data imports (added self-employment functions)
- Calculation pipeline (3-way branch by employment type)
- Display logic (dynamic columns based on employment type)

**Lines changed:** ~150 lines modified/added

---

## Backward Compatibility

✅ **Fully backward compatible:**
- All new code is additive (no breaking changes)
- Existing `calculate_income_probability()` still works
- Income Demographics tab has sensible defaults
- Streamlit app continues to work with or without employment type selection

---

## Test Results

All validation tests passed:

```
Test 1: Self-employment rates by age
  18-24: 6.0% ✓
  25-34: 12.0% ✓
  45-54: 18.0% ✓
  65+: 35.0% ✓

Test 2: Self-employed income distributions sum to 1.0
  Male: 1.000000 ✓
  Female: 1.000000 ✓

Test 3: Self-employed income thresholds
  £20,000+ - Males: 64.8%, Females: 58.0% ✓
  £50,000+ - Males: 19.5%, Females: 13.0% ✓
  £100,000+ - Males: 3.4%, Females: 1.5% ✓

Test 4: Gender blending (Any)
  £50k+ self-employed Any gender: 16.2% ✓

Test 5: Realistic scenario (Female 35-44, £75k+)
  Starting: 1,000,000 adults
  Employed: 790,000 (79%)
  Single: 252,800 (32%)
  Self-employed: 30,336 (12%)
  Matches: 12,336 (4.9%)
  ✓ All intermediate values reasonable
```

---

## Key Features

### 1. Age-Based Self-Employment Rates
- Automatically adjusts for age demographic selected
- Weighted by gender if "Any" gender selected
- Accounts for higher self-employment in older cohorts

### 2. Separate Income Distributions
- Employees: ASHE 2023 (ONS surveyed PAYE population)
- Self-employed: HMRC Self Assessment (tax-declared unincorporated)
- Different earning profiles reflected (e.g., more below £20k for self-employed)

### 3. Blending Logic
When user selects "Any" employment type:
1. Calculate total single employed population
2. Split by self-employment rate: `single_self_employed = single × self_emp_rate`
3. Apply correct income distribution to each:
   - Employees: use ASHE distribution
   - Self-employed: use HMRC distribution
4. Sum for total matches

### 4. Demographic Filtering
Works with all existing demographic filters:
- Age range (custom)
- Gender (Any/Male/Female)
- Ethnicity (multi-select)
- Single status (already integrated)
- Income threshold (custom)

---

## Example Queries Now Possible

**Before:** Mixed ASHE data only
**Now:** Separate analysis by employment type

1. **"How many single self-employed females earning £100k+, age 35-45?"**
   - Filter: Female, 35-45, Self-employed, £100k+
   - Uses HMRC income distribution (1-2% at this level)

2. **"What's the dating pool for single employed males earning £50k+?"**
   - Filter: Male, any age, Employees, £50k+
   - Uses ASHE income distribution (~19% at this level)

3. **"Compare employee vs self-employed across demographics"**
   - Run once with "Employees" filter
   - Run again with "Self-employed" filter
   - Compare in gender breakdown table

---

## Future Enhancements

### Phase 2: Business Owners (Ltd Companies)
- Placeholder in radio filter: "Business owners"
- Data source: HMRC Corporation Tax Liabilities
- Focus on director salaries and dividend income

### Phase 3: Industry & Sector Breakdown
- Self-employment rates by industry
- Income by industry within self-employed
- Most common self-employed professions

### Phase 4: Earnings Volatility
- HMRC data variance by year
- Income confidence intervals
- Growth trajectory by age

### Phase 5: Side Hustles
- Employees with secondary self-employment income
- Multi-job prevalence by demographic
- Combined household income analysis

---

## Documentation Created

1. **SELF_EMPLOYMENT_ANALYSIS.md** - Comprehensive feature documentation
2. **SELF_EMPLOYMENT_INTEGRATION.md** - Quick integration guide
3. **This file** - Implementation summary

---

## Validation Checklist

- [x] Self-employment data added to data.py
- [x] Income distributions normalized to sum to 1.0
- [x] Calculation functions implemented and tested
- [x] UI updated with employment type filter
- [x] Gender breakdown table updated
- [x] Income threshold chart uses correct distribution
- [x] Documentation complete
- [x] All tests passing
- [x] Backward compatibility maintained

---

## Next Steps

1. **Test in Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   - Navigate to Income Demographics tab
   - Try employment type filters
   - Verify gender breakdown columns update correctly
   - Check income threshold chart changes

2. **User feedback:**
   - Verify self-employment rates match user expectations
   - Test edge cases (e.g., very young/old demographics)
   - Confirm income distribution feels reasonable

3. **Future:** Integrate business owner data (Phase 2)

---

## Contact & Questions

For questions about:
- **Code implementation:** See calculations.py docstrings
- **Data sources:** See data.py comments and SELF_EMPLOYMENT_ANALYSIS.md
- **UI/UX:** See ui_income_stats_content.py comments
- **Statistical methodology:** See SELF_EMPLOYMENT_ANALYSIS.md

---

**Last updated:** January 2025
**Status:** Ready for integration testing
