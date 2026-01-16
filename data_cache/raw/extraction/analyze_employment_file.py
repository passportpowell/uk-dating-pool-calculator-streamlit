"""
Extract employment rates by age and gender from ONS employment data.
Source: employment_by_age_and_sex.xlsx
Data: Annual Population Survey 2011-2022
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File path
raw_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/raw/")
input_file = raw_dir / "employment_by_age_and_sex.xlsx"
output_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/")

print("=" * 80)
print("EXTRACTING EMPLOYMENT RATES BY AGE AND GENDER")
print("=" * 80)

# Read the employment data
xls = pd.ExcelFile(input_file)
print(f"\nAvailable sheets: {xls.sheet_names}")

# Try the most likely sheet names
sheet_name = 'Employment by age group' if 'Employment by age group' in xls.sheet_names else xls.sheet_names[0]
df = pd.read_excel(input_file, sheet_name=sheet_name, header=None)

print(f"\nUsing sheet: {sheet_name}")
print(f"Data shape: {df.shape}")
print("\nFirst 30 rows:")
print(df.iloc[:30, :10])

# Find the header row containing year data
header_row = None
for i in range(min(10, len(df))):
    row_str = str(df.iloc[i].tolist())
    if '2022' in row_str or 'Year' in row_str.upper():
        header_row = i
        print(f"\nPotential header row {i}: {df.iloc[i, :5].tolist()}")

# Look for age group column
print("\nSearching for data structure...")
print("\nFirst 20 rows with content:")
for i in range(min(20, len(df))):
    print(f"Row {i}: {df.iloc[i, :5].tolist()}")
