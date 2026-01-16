# Data Extraction Progress Summary

## Successfully Extracted Files

### 1. Single Rate by Age (from marital_status_and_living_arrangements_2002_2024.xlsx)
- **File**: `single_rate_by_age.csv` 
- **Data**: Never-married rates by age band (2024)
- **Age Groups**: 16-19 through 85+
- **Source**: ONS Marital Status and Living Arrangements survey
- **Status**: ✓ COMPLETE

Example:
```
age_group,single_rate_total
16 to 19,2945228
20 to 24,3602975
25 to 29,3364373
```

### 2. Single Rate by Age & Gender (from same source)
- **File**: `single_rate_by_age_gender.csv`
- **Data**: Never-married rates by age band AND gender (2024)
- **Status**: ✓ COMPLETE

Example:
```
age_group,single_rate_male,single_rate_female
16 to 19,1518038,1427190
20 to 24,1873172,1729803
```

### 3. Employment by Age & Gender (from employment_by_age_and_sex.xlsx)
- **File**: `employment_by_age_gender.csv`
- **Data**: Employment counts by age band and gender (2011 APS data)
- **Age Groups**: 16-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+
- **Source**: ONS Annual Population Survey 2011-2022
- **Status**: ✓ COMPLETE

Example:
```
age_group,employment_male,employment_female
16 to 29,3236710,3147842
30 to 39,3015086,2693458
```

## Already Extracted (from Previous Sessions)

### 1. Ethnicity Distribution
- **File**: `ethnicity_distribution.csv`
- **Source**: Census 2021 Table_06
- **Categories**: 17 ethnic groups
- **Status**: ✓ COMPLETE

### 2. Income Distribution - Male
- **File**: `income_distribution_male.csv`
- **Source**: ASHE 2024 Table 8.7a
- **Brackets**: 8 income brackets
- **Status**: ✓ COMPLETE

### 3. Income Distribution - Female
- **File**: `income_distribution_female.csv`
- **Source**: ASHE 2024 Table 8.7a
- **Brackets**: 8 income brackets
- **Status**: ✓ COMPLETE

## Raw Files Analysis

### Analyzed & Not Needed (Lower Priority / Duplicate Data)
- **UK Population Timeseries 1968-2025.xlsx**: Population totals (already have recent Census data)
- **Annual-Summary-Headline-Tables-2024.ods**: Labour Force Survey summary (already have employment data from more detailed source)
- **Census 2021 Demographic Table TS021**: Demographic table (already using ethnicity data)
- **Table_3.10_2223.ods**: Self-employment income by income range (lower priority - would need age breakdown)

### Unused PDF Files
- Employee earnings in the UK 2025.pdf
- Families and households in the UK 2024.pdf
- Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf
- Labour Force Survey quality update September 2025.pdf
- Statistics on trusts in the UK December 2025.pdf
- Working and workless households in the UK July to September 2025.pdf
- Labour Force Survey performance and quality monitoring report

### Additional ASHE Tables (Technical Use)
- Home Geography Tables 8.1a-8.11b: Additional ASHE pay breakdown by geography/categories (already extracted percentile data)

## Next Steps

1. ✓ Update data_loader.py to load new CSV files
2. ✓ Test app with all new data loaded
3. ✓ Verify data provenance display works correctly
4. Optional: Extract self-employment income distribution by age (would require additional data processing)

## File Metadata for Provenance System

```python
# single_rate_by_age.csv
{
    'name': 'Never-married population by age',
    'source': 'ONS Marital Status and Living Arrangements Survey',
    'file': 'marital_status_and_living_arrangements_2002_2024.xlsx',
    'sheet': 'Table_1_Marital_Status_All',
    'year': 2024,
    'url': 'https://www.ons.gov.uk/peoplepopulationandcommunity/householdcharacteristics/maritalstatusandlivingrarrangements/datasets/maritalstatuslivingarrangements',
    'timestamp': datetime.now(),
    'notes': 'Population counts (not rates) from Annual Household Survey'
}

# employment_by_age_gender.csv
{
    'name': 'Employment by age and gender',
    'source': 'ONS Annual Population Survey',
    'file': 'employment_by_age_and_sex.xlsx',
    'sheet': 'Employment by age group',
    'year': 2011,  # or 2022 depending on column used
    'url': 'https://www.ons.gov.uk/employmentandlabourmarket/peopleandwork/employmentandemployeetypes/datasets/employmentbyageandsex',
    'timestamp': datetime.now(),
    'notes': 'Employment counts by age band and gender from APS 2011-2022'
}
```

## Integration Notes

All new CSV files follow the template format:
- First row contains headers
- Data rows contain actual values
- Files are UTF-8 encoded
- Ready to be loaded by data_loader.py

The extracted data uses population counts rather than percentages/rates to allow flexible calculation in the application.
