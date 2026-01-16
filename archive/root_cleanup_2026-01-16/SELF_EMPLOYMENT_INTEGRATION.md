# Self-Employment Features - Quick Integration Guide

## What's New

The Income Demographics tab now includes **employment type filtering** to separately analyze:
- ✅ **Employees** (PAYE/salary) - ASHE 2023 data
- ✅ **Self-employed** (sole traders/partnerships) - HMRC Self Assessment data  
- ✅ **Any** - Blended employee + self-employed

---

## User-Facing Changes

### New UI Element: Employment Type Filter
```
Employment type (radio buttons):
  • Any           - All employment (blend by prevalence)
  • Employees     - PAYE/salary only
  • Self-employed - Sole traders/partnerships only
  • Business owners [future] - Ltd companies [placeholder]
```

### Updated Metrics Display
```
Before: "Earning £X+ | 12,345 matches"
After:  "Earning £X+ | 12,345 matches [Employment type indicator]"
```

### Updated Gender Breakdown Table
Columns now reflect employment type:
- **Employees:** Shows "Employee Single" column separately
- **Self-employed:** Shows "Self-employed Single" column separately
- **Any:** Shows both "Employees" and "Self-employed" columns

### Updated Documentation
- Info box now explains self-employment rates by age
- Cites HMRC Self Assessment as additional source
- Explains key differences in income distribution

---

## Data Changes

### New in data.py
```python
# Self-employment rates by age band and gender (ONS LFS 2023)
SELF_EMPLOYMENT_RATE_BY_AGE_GENDER = {
    "18-24": {"Male": 0.06, "Female": 0.05},
    # ... etc ...
    "65+": {"Male": 0.35, "Female": 0.28},
}

# Self-employed income distribution (normalized)
SELF_EMPLOYED_INCOME_DISTRIBUTION_MALE = { ... }
SELF_EMPLOYED_INCOME_DISTRIBUTION_FEMALE = { ... }

OVERALL_SELF_EMPLOYMENT_RATE = 0.13  # ~13% of UK workforce
```

---

## Code Changes

### New Functions in calculations.py
```python
# Calculate probability self-employed earns at/above threshold
calculate_self_employed_income_probability(min_income, gender)

# Get self-employment rate for age range (blended gender)
get_self_employment_rate_by_age(age_min, age_max)

# Get self-employment rate for specific age range & gender
get_self_employment_rate_by_age_gender(age_min, age_max, gender)
```

### Updated Logic in ui_income_stats_content.py
```python
# Employment type filtering
if employment_type == "Any":
    # Blend employee and self-employed calculations
    
elif employment_type == "Self-employed":
    # Use HMRC Self Assessment income distribution
    
else:  # Employees
    # Use ASHE 2023 income distribution (filter out self-employed)
```

---

## Key Differences: Employee vs Self-Employed

| Metric | Employee | Self-Employed | Source |
|--------|----------|---------------|--------|
| % Workforce | 87% | 13% | ONS LFS 2023 |
| Under £20k | 25% | 35% | ASHE vs HMRC |
| £50k+ | 19% | 16% | ASHE vs HMRC |
| £100k+ | 2% | 2% | ASHE vs HMRC |
| Peak age | 35-45 | 55+ | ONS LFS 2023 |

**Why different income distributions?**
- Self-employed have more below £20k (includes part-time, side hustles, startup phase)
- Both similar at higher incomes (successful businesses vs senior employees)

---

## Testing Checklist

- [ ] Employment type filter works (Any/Employees/Self-employed)
- [ ] Metrics update when filter changes
- [ ] Gender breakdown table shows correct columns
- [ ] Income threshold chart uses correct distribution
- [ ] Self-employment rates are reasonable (5% at age 18-24, 35% at 65+)
- [ ] "Any" blends both types correctly
- [ ] Help text mentions employment type in income label

---

## Example Queries Now Possible

**Before:** "How many single females earning £100k+ age 35-45?"
**Now:** "How many single **self-employed** females earning £100k+ age 35-45?"

**Before:** Blended ASHE data only
**Now:** Can separately see:
- PAYE employees earning threshold
- Self-employed earning threshold
- Breakdown in gender table

---

## Configuration Files Modified

1. **data.py** - Added self-employment data (new dictionaries, no breaking changes)
2. **calculations.py** - Added helper functions (no breaking changes to existing)
3. **ui_income_stats_content.py** - New employment type filter, updated calculations

## Backward Compatibility

✅ All changes are additive - no existing functionality removed
✅ Existing calculations still work (employment_type defaults to "Any")
✅ UI gracefully handles missing employment_type parameter

---

## Data Coverage

### What's Included
- ✅ PAYE employees (ASHE 2023)
- ✅ Self-employed sole traders (HMRC Self Assessment)
- ✅ Self-employed partnerships (HMRC Self Assessment)
- ✅ Self-employment by age, gender, region [future]

### What's NOT Included
- ❌ Ltd company directors/business owners
- ❌ Gig workers (depends on tax classification)
- ❌ Informal/cash-in-hand work
- ❌ Unreported self-employed (no tax return)

---

## Future Enhancement: Business Owners

Placeholder for Ltd company data (future):
```python
# In ui_income_stats_content.py:
elif employment_type == "Business owners":
    # Use Corporation Tax data (HMRC)
    # Income from company directors with Ltd structure
```

Requires:
- HMRC Corporation Tax Liabilities data
- Payroll tax data (employers with employees)
- Director salary ranges by company size
