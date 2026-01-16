"""
Extract single (never married) rates by age from ONS marital status data.
Source: marital_status_and_living_arrangements_2002_2024.xlsx
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File path
raw_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/raw/")
input_file = raw_dir / "marital_status_and_living_arrangements_2002_2024.xlsx"
output_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/")

print("=" * 80)
print("EXTRACTING SINGLE RATES BY AGE AND GENDER")
print("=" * 80)

# Read the marital status table
df_all = pd.read_excel(input_file, sheet_name='Table_1_Marital_Status_All', header=None)
df_male = pd.read_excel(input_file, sheet_name='Table_2_Marital_Status_Males', header=None)
df_female = pd.read_excel(input_file, sheet_name='Table_3_Marital_Status_Females', header=None)

def extract_2024_single_rates(df, gender_label):
    """Extract 2024 single rates for each age group."""
    
    # Find the row with headers
    header_row = None
    for i, row in df.iterrows():
        if 'Marital status' in str(row.iloc[0]) and 'Age group' in str(row.iloc[1]):
            header_row = i
            break
    
    if header_row is None:
        print(f"Could not find header row for {gender_label}")
        return None
    
    # Extract headers to find 2024 columns
    headers = df.iloc[header_row].tolist()
    
    # Find 2024 Estimate column
    col_2024 = None
    for i, header in enumerate(headers):
        if '2024' in str(header) and 'Estimate' in str(header):
            col_2024 = i
            break
    
    if col_2024 is None:
        print(f"Could not find 2024 Estimate column for {gender_label}")
        return None
    
    print(f"\n2024 column index for {gender_label}: {col_2024}")
    
    # Extract single rate data
    age_groups = []
    single_rates = []
    
    for i in range(header_row + 1, len(df)):
        marital_status = df.iloc[i, 0]
        age_group = df.iloc[i, 1]
        value = df.iloc[i, col_2024]
        
        # Look for "Never married" rows with age groups
        if 'Never married' in str(marital_status) and age_group and age_group != 'All Ages':
            if age_group not in ['0 to 15', 'All Ages']:  # Skip age 0-15
                try:
                    rate = float(value)
                    age_groups.append(str(age_group))
                    single_rates.append(rate)
                    print(f"  {age_group}: {rate:,.0f}")
                except (ValueError, TypeError):
                    pass
    
    if age_groups:
        return pd.DataFrame({
            'age_group': age_groups,
            f'single_rate_{gender_label.lower()}': single_rates
        })
    return None

# Extract for all, males, and females
df_all_extracted = extract_2024_single_rates(df_all, 'All')
df_male_extracted = extract_2024_single_rates(df_male, 'Male')
df_female_extracted = extract_2024_single_rates(df_female, 'Female')

# Merge the data
print("\n" + "=" * 80)
print("MERGING DATA")
print("=" * 80)

if df_all_extracted is not None:
    result_df = df_all_extracted.copy()
    result_df.rename(columns={'single_rate_all': 'single_rate_total'}, inplace=True)
    print("\nExtracted data:")
    print(result_df)
    
    # Save to CSV
    output_file = output_dir / "single_rate_by_age.csv"
    result_df.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")
else:
    print("\n✗ Failed to extract single rate data")

# Also save male/female breakdown if available
if df_male_extracted is not None and df_female_extracted is not None:
    # Merge them
    merged = df_male_extracted.merge(df_female_extracted, on='age_group', how='inner')
    
    output_file = output_dir / "single_rate_by_age_gender.csv"
    merged.to_csv(output_file, index=False)
    print(f"Saved gender breakdown to {output_file}")
    print("\nGender breakdown:")
    print(merged)
