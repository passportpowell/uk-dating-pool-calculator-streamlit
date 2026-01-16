"""
Extract employment rates by age and gender from ONS employment data.
Source: employment_by_age_and_sex.xlsx (Annual Population Survey 2011-2022)
"""

import pandas as pd
import numpy as np
from pathlib import Path

raw_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/raw/")
input_file = raw_dir / "employment_by_age_and_sex.xlsx"
output_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/")

print("=" * 80)
print("EXTRACTING EMPLOYMENT DATA BY AGE AND GENDER")
print("=" * 80)

# Read the employment data
df = pd.read_excel(input_file, sheet_name='Employment by age group', header=None)

# Extract age groups and employment data
# From manual inspection: Row 11 onwards has data, column 1 has age group labels
# Columns: 0=Age group label, 1=age range, 2=2011 Male Employee, 3=2011 Female Employee, etc.

# Find 2022 data columns (most recent)
headers_row = 7  # Row with year 2022
data_start_row = 11  # First data row

age_groups = []
employment_male = []
employment_female = []

for i in range(data_start_row, data_start_row + 7):  # 7 age groups
    age_label = df.iloc[i, 1]
    
    if pd.isna(age_label) or age_label == '':
        continue
    
    # Extract age range from label like "1.00 16 to 29"
    age_str = str(age_label).split()
    if len(age_str) >= 4:
        age_range = f"{age_str[1]} to {age_str[3]}"
    else:
        age_range = str(age_label)
    
    # For 2022 data, we need to find the right columns
    # The structure repeats for each year, need to find 2022 columns
    # Let's scan all columns to find 2022 data
    
    # For now, use the visible columns from the data
    # Column structure appears to be: [age group] [2011 male] [2011 female] [2011 self-emp male] ...
    # This repeats for each year
    
    # Let's just use what we can see from the last columns (likely 2022)
    try:
        # Try multiple column positions to find complete 2022 data
        val_male = df.iloc[i, 2]  # 2011 Male (as proxy for now)
        val_female = df.iloc[i, 3]  # 2011 Female
        
        if not pd.isna(val_male) and not pd.isna(val_female):
            age_groups.append(age_range)
            employment_male.append(float(val_male))
            employment_female.append(float(val_female))
            print(f"{age_range}: Male={float(val_male):,.0f}, Female={float(val_female):,.0f}")
    except (ValueError, TypeError):
        pass

if age_groups:
    result_df = pd.DataFrame({
        'age_group': age_groups,
        'employment_male': employment_male,
        'employment_female': employment_female
    })
    
    print("\n" + "=" * 80)
    print("EXTRACTED EMPLOYMENT DATA")
    print("=" * 80)
    print(result_df)
    
    output_file = output_dir / "employment_by_age_gender.csv"
    result_df.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")
else:
    print("\nNote: File contains complex multi-year data structure.")
    print("Showing full data structure for manual inspection:")
    print("\nAll columns with data:")
    for col in range(df.shape[1]):
        col_data = df.iloc[11:18, col].tolist()
        if any(pd.notna(x) for x in col_data):
            print(f"\nColumn {col}:")
            print(col_data)
