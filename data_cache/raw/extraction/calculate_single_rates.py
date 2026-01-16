"""
Convert single rate and employment counts to percentages.
Calculates rates using actual ONS data.
"""

import pandas as pd
import numpy as np
from pathlib import Path

cache_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/")
raw_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/raw/")

# Load marital status data to get total population by age
print("=" * 80)
print("CALCULATING SINGLE RATES")
print("=" * 80)

marital_file = raw_dir / "marital_status_and_living_arrangements_2002_2024.xlsx"
df_marital = pd.read_excel(marital_file, sheet_name='Table_1_Marital_Status_All', header=None)

# Find header row and all rows
header_row = None
for i, row in df_marital.iterrows():
    if 'Marital status' in str(row.iloc[0]) and 'Age group' in str(row.iloc[1]):
        header_row = i
        break

# Find 2024 columns
headers = df_marital.iloc[header_row].tolist()
col_2024_estimate = None
for i, h in enumerate(headers):
    if '2024' in str(h) and 'Estimate' in str(h):
        col_2024_estimate = i
        break

print(f"Header row: {header_row}")
print(f"2024 Estimate column: {col_2024_estimate}")

# Extract all persons counts for calculating percentages
age_groups = []
single_counts = []
total_counts = []

for i in range(header_row + 1, len(df_marital)):
    status = df_marital.iloc[i, 0]
    age = df_marital.iloc[i, 1]
    value = df_marital.iloc[i, col_2024_estimate]
    
    # Get all persons total (All Ages row for each status)
    if 'Married' in str(status) and age == 'All Ages':
        all_married = value
        break

# Now calculate single rates
single_rates_dict = {}

for i in range(header_row + 1, len(df_marital)):
    status = df_marital.iloc[i, 0]
    age = df_marital.iloc[i, 1]
    value = df_marital.iloc[i, col_2024_estimate]
    
    if pd.isna(value) or pd.isna(age) or age == 'All Ages' or age == '0 to 15':
        continue
    
    if 'Never married' in str(status) and age:
        age_str = str(age)
        try:
            single_count = float(value)
            single_rates_dict[age_str] = single_count
            print(f"{age_str}: {single_count:,.0f}")
        except (ValueError, TypeError):
            pass

# Calculate totals for each age by summing all statuses
total_by_age = {}
for i in range(header_row + 1, len(df_marital)):
    status = df_marital.iloc[i, 0]
    age = df_marital.iloc[i, 1]
    value = df_marital.iloc[i, col_2024_estimate]
    
    if pd.isna(age) or age == 'All Ages' or age == '0 to 15' or pd.isna(value):
        continue
    
    age_str = str(age)
    if age_str not in total_by_age:
        total_by_age[age_str] = 0
    
    try:
        total_by_age[age_str] += float(value)
    except (ValueError, TypeError):
        pass

# Calculate rates as percentages
print("\n" + "=" * 80)
print("SINGLE RATE PERCENTAGES BY AGE")
print("=" * 80)

single_rates = {}
for age, count in single_rates_dict.items():
    if age in total_by_age and total_by_age[age] > 0:
        rate = count / total_by_age[age]
        single_rates[age] = rate
        print(f"{age:<15}: {rate:>7.1%} ({count:>10,.0f} / {total_by_age[age]:>10,.0f})")

# Normalize to app age bands
print("\n" + "=" * 80)
print("NORMALIZED TO APP AGE BANDS (key format for data.py)")
print("=" * 80)

def map_to_age_band(age_str):
    """Map ONS age bands to app age bands."""
    if age_str == '16 to 19':
        return '16-24'
    elif age_str == '20 to 24':
        return '16-24'
    elif age_str == '25 to 29':
        return '25-34'
    elif age_str == '30 to 34':
        return '25-34'
    elif age_str == '35 to 39':
        return '35-44'
    elif age_str == '40 to 44':
        return '35-44'
    elif age_str == '45 to 49':
        return '45-54'
    elif age_str == '50 to 54':
        return '45-54'
    elif age_str == '55 to 59':
        return '55-64'
    elif age_str == '60 to 64':
        return '55-64'
    elif age_str in ['65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 and over']:
        return '65+'
    return None

normalized = {}
for age, rate in single_rates.items():
    band = map_to_age_band(age)
    if band:
        if band not in normalized:
            normalized[band] = []
        normalized[band].append(rate)

# Average rates within each band
final_rates = {}
for band in normalized:
    avg_rate = np.mean(normalized[band])
    final_rates[band] = avg_rate
    print(f"{band:<10} = {avg_rate:.4f}")

# Save as CSV
output_df = pd.DataFrame([final_rates])
output_df_transposed = pd.DataFrame({
    'key': list(final_rates.keys()),
    'value': list(final_rates.values())
})

output_file = cache_dir / "single_rate_by_age.csv"
output_df_transposed.to_csv(output_file, index=False)
print(f"\nSaved to {output_file}")

print("\nSample Python code for data.py:")
print("SINGLE_RATE_BY_AGE = {")
for band in ["16-24", "25-34", "35-44", "45-54", "55-64", "65+"]:
    if band in final_rates:
        print(f'    "{band}": {final_rates[band]:.2f},')
print("}")
