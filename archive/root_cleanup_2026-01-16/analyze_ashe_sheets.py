"""
Check all sheets in ASHE Table 8 files to find income distribution data
"""
import pandas as pd
from pathlib import Path
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("data_cache/raw")

# ASHE Table 8 has multiple files
ashe_files = sorted([f for f in RAW_DIR.glob("Home Geography Table 8*") if f.suffix == '.xlsx'])

print("="*80)
print("ASHE TABLE 8 FILES - SHEET NAMES")
print("="*80)

for filepath in ashe_files:
    print(f"\n{filepath.name}:")
    try:
        xl = pd.ExcelFile(filepath)
        print(f"  Sheets: {xl.sheet_names[:10]}")  # First 10 sheet names
        if len(xl.sheet_names) > 10:
            print(f"  ... and {len(xl.sheet_names) - 10} more")
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "="*80)
print("CHECKING TABLE 8.7a (ANNUAL PAY) SHEETS IN DETAIL")
print("="*80)

ashe_annual = RAW_DIR / "Home Geography Table 8.7a   Annual pay - Gross 2024.xlsx"
if ashe_annual.exists():
    xl = pd.ExcelFile(ashe_annual)
    print(f"\nTotal sheets: {len(xl.sheet_names)}")
    
    for i, sheet in enumerate(xl.sheet_names[:15]):  # Check first 15 sheets
        df = pd.read_excel(ashe_annual, sheet_name=sheet, header=None)
        print(f"\n  Sheet {i}: '{sheet}'")
        print(f"    Shape: {df.shape}")
        
        # Show first few rows to identify content
        if df.shape[0] > 0:
            first_row = df.iloc[0].tolist()
            print(f"    First row: {str(first_row)[:100]}")
        
        # Look for key terms
        df_str = df.astype(str).to_string()
        if any(keyword in df_str.lower() for keyword in ['male', 'female', 'gender', '10th', 'percentile', 'median']):
            print(f"    ** CONTAINS EARNINGS/GENDER DATA **")

print("\nDone!")
