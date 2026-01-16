"""
Analyze the new ASHE Table 8 and Labour Force Survey quality update files
"""
import pandas as pd
from pathlib import Path
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("data_cache/raw")

print("="*80)
print("ASHE TABLE 8 - INCOME DATA EXPLORATION")
print("="*80)

# Check the annual pay files - these will have income distribution
ashe_file = RAW_DIR / "Home Geography Table 8.7a   Annual pay - Gross 2024.xlsx"

if ashe_file.exists():
    print(f"\n[ASHE Table 8.7a - Annual pay - Gross 2024]")
    try:
        df = pd.read_excel(ashe_file)
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {df.columns.tolist()}")
        print(f"\n  First 25 rows:")
        print(df.head(25).to_string())
        
        # Check structure
        print(f"\n  Data types: {df.dtypes.tolist()}")
        
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "="*80)
print("LABOUR FORCE SURVEY QUALITY UPDATE")
print("="*80)

lfs_file = RAW_DIR / "Labour Force Survey quality update September 2025.pdf"
if lfs_file.exists():
    size_kb = lfs_file.stat().st_size / 1024
    print(f"\n[File exists: Labour Force Survey quality update September 2025.pdf]")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Type: PDF quality/methodology document")
    print(f"  May contain: references to detailed data tables, quality notes, age breakdowns")
else:
    print("File not found")

print("\n" + "="*80)
print("ASSESSMENT")
print("="*80)

print("""
ASHE Table 8.7a - Annual pay (Gross 2024):
  This is EXCELLENT for income data!
  - Shows actual earnings values by geography/local authority
  - May have gender breakdowns
  - Need to extract distribution across income brackets
  
Labour Force Survey quality update September 2025:
  This is a REFERENCE document
  - Explains methodology, quality notes, data collection
  - May point to where detailed employment tables are
  - Might reference employment by age/gender tables
""")
