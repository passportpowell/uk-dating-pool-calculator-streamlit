"""
Extract income distribution data from ASHE Table 8.7a (Annual pay - Gross 2024)
"""
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("data_cache/raw")
OUT_DIR = Path("data_cache")

ashe_file = RAW_DIR / "Home Geography Table 8.7a   Annual pay - Gross 2024.xlsx"

print("="*80)
print("EXTRACTING INCOME DISTRIBUTIONS FROM ASHE TABLE 8.7a")
print("="*80)

if ashe_file.exists():
    # Read Male and Female sheets
    df_male = pd.read_excel(ashe_file, sheet_name='Male')
    df_female = pd.read_excel(ashe_file, sheet_name='Female')
    
    print(f"\nMale data shape: {df_male.shape}")
    print(f"Female data shape: {df_female.shape}")
    
    # Look at the structure
    print("\n" + "="*80)
    print("MALE DATA STRUCTURE")
    print("="*80)
    print(f"\nColumns: {df_male.columns.tolist()}")
    print(f"\nFirst 30 rows to identify structure:")
    print(df_male.head(30).to_string())
    
    print("\n" + "="*80)
    print("FEMALE DATA STRUCTURE")
    print("="*80)
    print(f"\nColumns: {df_female.columns.tolist()}")
    print(f"\nFirst 30 rows to identify structure:")
    print(df_female.head(30).to_string())
    
    # Look for percentile rows
    print("\n" + "="*80)
    print("SEARCHING FOR PERCENTILE ROWS")
    print("="*80)
    
    for idx, row in df_male.iterrows():
        row_str = str(row.iloc[0]).lower() if pd.notna(row.iloc[0]) else ""
        if any(keyword in row_str for keyword in ['percentile', '10th', '20th', '25th', 'median', '75th', '90th']):
            print(f"\nRow {idx}: {row.tolist()[:5]}")  # Show first 5 cols
            if idx > 30:  # Stop after finding some
                break

else:
    print("File not found!")

print("\n" + "="*80)
print("NOTE")
print("="*80)
print("""
This file contains earnings by local authority (geography), not income brackets.
To get income DISTRIBUTION, we need to:
1. Identify which columns contain percentile information
2. Map these to our income brackets (Under 10k, 10-20k, etc.)
3. Or look for a different ASHE table with percentile distributions

Alternative: Look in 'Employee earnings in the UK 2025.pdf' for percentile tables.
""")
