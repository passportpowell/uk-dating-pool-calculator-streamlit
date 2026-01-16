# Self-Employment & Business Owner Analysis

## New Features Added

This document describes the self-employment analysis features that have been added to the dating pool calculator's Income Demographics tab.

---

## Data Sources

### Self-Employment Rates
- **Source:** ONS Labour Force Survey 2023
- **Coverage:** By age band and gender
- **Key finding:** Self-employment rates vary from 5-6% (age 18-24) to 28-35% (age 65+)

### Self-Employed Income Distribution  
- **Source:** HMRC Self Assessment Data + ONS Self-Employment Trends
- **Coverage:** Tax-declared income from self-employed population
- **Key differences from employees:**
  - Higher proportion earning below £20k (35-42% vs 25-32% for employees)
  - Higher proportion earning above £150k (greater variability in earnings)
  - Reflects actual tax returns, not sample surveys

---

## Filtering Options

### Employment Type Filter
Users can now filter by three employment types:

1. **Any** - Blends employee and self-employed income distributions
   - Employees: Use ASHE 2023 distribution
   - Self-employed: Use HMRC Self Assessment distribution
   - Weighted by actual prevalence (~87% employees, ~13% self-employed)

2. **Employees** - PAYE/salary workers only
   - Income from ONS ASHE 2023 (sample survey)
   - Excludes sole traders and partnerships
   - ~87% of UK workforce

3. **Self-employed** - Sole traders and partnerships only
   - Income from HMRC Self Assessment (tax returns)
   - Excludes incorporated companies/Ltd
   - ~13% of UK workforce

### Demographic Filters (Existing)
- Age range (18-75)
- Gender (Male, Female, Any)
- Ethnicity (multi-select from Census 2021 categories)
- Income threshold (slider or text input)

---

## Calculation Pipeline

### For "Any" Employment Type:
1. Adults in demographic: age + gender + ethnicity (Census 2021)
2. Total employed: Adults × employment rate by age/gender (ONS LFS 2023)
3. Single employed: Employed × single rate by age (ONS F&H 2022)
4. Split by employment type: Single × self-employment rate
5. Income match: 
   - Employees: Single employees × probability from ASHE 2023
   - Self-employed: Single self-employed × probability from HMRC
6. Total: Employee matches + Self-employed matches

### For "Self-employed" Type:
1. Adults in demographic (Census 2021)
2. Total employed (ONS LFS 2023)
3. Single employed (ONS F&H 2022)
4. Self-employed only: Single × self-employment rate
5. Income match: Self-employed × HMRC income probability

### For "Employees" Type:
1. Adults in demographic (Census 2021)
2. Total employed (ONS LFS 2023)
3. Single employed (ONS F&H 2022)
4. Employees only: Single × (1 - self-employment rate)
5. Income match: Employees × ASHE income probability

---

## Self-Employment Rates by Age & Gender

```
Age Band | Male | Female
---------|------|-------
18-24    |  6%  |  5%
25-34    | 12%  |  9%
35-44    | 16%  | 12%
45-54    | 18%  | 14%
55-64    | 21%  | 17%
65+      | 35%  | 28%
```

**Key insight:** Self-employment increases with age, particularly after age 55. By 65+, 28-35% of the employed population is self-employed (many working past standard retirement age).

---

## Income Distribution Comparison

### Employees (ASHE 2023) vs Self-Employed (HMRC)

| Income Band | Employees (%) | Self-Employed (%) | Difference |
|---|---|---|---|
| Under £20k | 25% | 35% | +10pp |
| £20k-£30k | 22% | 20% | -2pp |
| £30k-£40k | 18% | 15% | -3pp |
| £40k-£50k | 13% | 10% | -3pp |
| £50k-£75k | 14% | 12% | -2pp |
| £75k-£100k | 5% | 4% | -1pp |
| £100k-£150k | 2% | 2% | - |
| £150k-£250k | 0.7% | 0.8% | +0.1pp |
| £250k+ | 0.3% | 0.4% | +0.1pp |

**Key findings:**
- Self-employed have 10 percentage points more in "Under £20k" band
- Self-employed have higher representation at top income levels (£150k+)
- Reflects different earning volatility and tax planning

---

## Display Changes

### Metrics Card
Now shows:
- Earning threshold count (with employment type label)
- Share of single employed
- Total employed singles
- Total employed (not single)

### Gender Breakdown Table
Columns change based on employment type:

**Any:**
- Gender | Adults | Employed | Employees | Self-employed | Earning £X+

**Employees:**
- Gender | Adults | Employed | Employee Single | Earning £X+

**Self-employed:**
- Gender | Adults | Employed | Self-employed Single | Earning £X+

### Income Threshold Chart
Now uses appropriate income distribution:
- Employees: ASHE 2023
- Self-employed: HMRC Self Assessment
- Any: Blended

---

## Implementation Files

### data.py
- Added `SELF_EMPLOYMENT_RATE_BY_AGE_GENDER` dictionary
- Added `SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE` (normalized)
- Added `SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE` (normalized)
- Added `OVERALL_SELF_EMPLOYMENT_RATE` (13%)

### calculations.py
- Added `calculate_self_employed_income_probability()` function
- Added `get_self_employment_rate_by_age()` function
- Added `get_self_employment_rate_by_age_gender()` function
- Updated imports to include self-employment data

### ui_income_stats_content.py
- Added "Employment type" radio filter (Any/Employees/Self-employed)
- Updated calculation logic to branch by employment type
- Updated metrics display to show employment type
- Updated gender breakdown table to show employment breakdown
- Updated income threshold chart to use correct distribution
- Updated documentation to explain self-employment analysis

---

## Data Notes

### ASHE (Employee Income)
- Source: ONS Annual Survey of Hours and Earnings 2023
- Coverage: ~180,000 private sector employees + public sector employees
- Represents: PAYE/salary workers only
- Notes: Excludes self-employed, directors' salaries treated as employees

### HMRC Self Assessment (Self-Employed Income)
- Source: HMRC Tax Statistics 2023
- Coverage: ~3.5 million self-employed individuals/partnerships
- Represents: Tax-declared income from unincorporated businesses
- Notes: Only captures those with tax obligations; excludes unreported/informal work

### ONS Labour Force Survey (Employment & Self-Employment)
- Source: ONS Labour Force Survey 2023
- Coverage: ~42,000 households quarterly
- Represents: Employment status and self-employment classification
- Notes: Self-employed includes sole traders, partners, directors not on payroll

---

## Limitations & Future Enhancements

### Current Limitations
1. **Business owners excluded** - Separate Ltd company data (Corporation Tax) not yet integrated
2. **Informal work excluded** - Cash-in-hand, unregistered self-employed not captured
3. **Gig workers unclear** - Some classified as self-employed, some as employees depending on tax status
4. **Income volatility not shown** - HMRC data shows average, not variance across years

### Future Enhancements
1. Add Corporation Tax data for Ltd company directors
2. Add partnership income breakdown
3. Show income variance/confidence intervals
4. Add industry breakdown by employment type
5. Add side-hustle prevalence (employees with secondary income)
6. Integrate HMRC high-income data (1000+ earners)

---

## Examples

### Example 1: Professional Female, Age 35-45, £100k+
**Employees only:**
- Adults: 500,000 (hypothetical)
- Employed: 395,000 (79%)
- Single employed: 126,400 (32%)
- Earning £100k+: 2,528 (2% of employees)

**Self-employed:**
- Same employed count
- Self-employed single: 15,168 (12% of single)
- Earning £100k+: 303 (2% of self-employed)

**Any employment:**
- Total £100k+: 2,831 (match rate 2.2%)

### Example 2: Young Male, Age 25-34, £50k+
**Employees only:**
- Single employed: 450,000
- Earning £50k+: 76,500 (17% of employees)

**Self-employed:**
- Single employed: 450,000
- Self-employed single: 45,900 (10% self-employed rate)
- Earning £50k+: 7,309 (16% of self-employed)

**Any employment:**
- Total £50k+: 83,809 (match rate 16%)

---

## Questions & Support

For questions about:
- **Employee income data:** See ASHE documentation
- **Self-employed rates:** See ONS LFS Q3 2023
- **Self-employed income:** See HMRC Tax Statistics
- **Single rates by age:** See ONS Families & Households 2022
- **Calculation methodology:** See calculations.py docstrings
