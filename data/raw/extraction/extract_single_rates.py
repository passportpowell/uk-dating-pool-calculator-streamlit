"""
Extract single rates by age from marital status file
"""
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("../")  # data_cache/raw/
OUT_DIR = Path("../../")  # data_cache/

file_path = RAW_DIR / "marital_status_and_living_arrangements_2002_2024.xlsx"

print("="*80)
print("EXTRACTING SINGLE RATES BY AGE")
print("="*80)

# Read the marital status file - it has sheets for different breakdowns
xl = pd.ExcelFile(file_path)
print(f"\nAvailable sheets: {xl.sheet_names}")

# Read Table 1: Marital Status for All (has both male and female data)
df_all = pd.read_excel(file_path, sheet_name="Table_1_Marital_Status_All", header=None)

print(f"\nTable 1 shape: {df_all.shape}")
print(f"\nFirst 30 rows:")
print(df_all.head(30))

# Find the 2024 data and age bands
print("\n" + "="*80)
print("SEARCHING FOR 2024 DATA AND AGE BANDS")
print("="*80)

# Look for 2024 and age band rows
for idx, row in df_all.iterrows():
    row_str = str(row.values).lower()
    if any(keyword in row_str for keyword in ['2024', 'age', '16', '25', '35']):
        if idx < 100:
            print(f"Row {idx}: {row.tolist()[:10]}")
