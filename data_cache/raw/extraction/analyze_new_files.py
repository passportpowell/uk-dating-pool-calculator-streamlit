"""
Analyze new files added to data_cache/raw/
"""
import pandas as pd
from pathlib import Path
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("data_cache/raw")

# New files to check
new_files = [
    "19682025.xlsx",  # Weird name - probably population data
    "Annual-Summary-Headline-Tables-2024.ods",  # Looks like employment summary
    "employmentselfemploymentbyagegroupsexjd11tojd22.xlsx",  # Employment by age/sex - PERFECT!
    "maritalstatuslivingarrangements2002to2024englandandwales.xlsx",  # Marital status - PERFECT!
    "regionalemploymentbyage.xlsx",  # Employment by age - could be useful
    "TS021-2021-1.csv",  # ONS code - likely demographic
    "TS021-2021-1.xlsx",  # Same data
    "Table_3.10_2223.ods",  # Duplicate?
]

print("="*80)
print("ANALYZING NEW FILES")
print("="*80)

for filename in new_files:
    filepath = RAW_DIR / filename
    if filepath.exists():
        print(f"\n[{filename}]")
        try:
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(filepath, nrows=10)
                print(f"  Sheets/Size: {df.shape}")
                print(f"  Columns: {df.columns.tolist()[:5]}")
                print(f"  First value: {df.iloc[0, 0] if len(df) > 0 else 'N/A'}")
                
            elif filename.endswith('.ods'):
                df = pd.read_excel(filepath, engine='odf', nrows=10)
                print(f"  Size: {df.shape}")
                print(f"  Columns: {df.columns.tolist()[:5]}")
                
            elif filename.endswith('.csv'):
                df = pd.read_csv(filepath, nrows=10)
                print(f"  Size: {df.shape}")
                print(f"  Columns: {df.columns.tolist()[:5]}")
                
        except Exception as e:
            print(f"  Error: {str(e)[:80]}")

print("\n" + "="*80)
print("FILES THAT SHOULD BE RENAMED")
print("="*80)

weird_names = {
    "19682025.xlsx": "uk_population_timeseries_1968_2025.xlsx",
    "employmentselfemploymentbyagegroupsexjd11tojd22.xlsx": "employment_self_employment_by_age_and_sex.xlsx",
    "maritalstatuslivingarrangements2002to2024englandandwales.xlsx": "marital_status_living_arrangements_2002_2024.xlsx",
    "regionalemploymentbyage.xlsx": "regional_employment_by_age.xlsx",
    "TS021-2021-1.csv": "census_2021_demographic_table_TS021.csv",
    "TS021-2021-1.xlsx": "census_2021_demographic_table_TS021.xlsx",
}

for old_name, new_name in weird_names.items():
    filepath = RAW_DIR / old_name
    if filepath.exists():
        print(f"\n{old_name}")
        print(f"  → RENAME TO: {new_name}")
