"""
Extract ethnicity distribution from Census 2021 Table_06.
"""
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data_cache" / "raw"
OUT_DIR = BASE_DIR / "data_cache"

def extract_ethnicity():
    """Extract ethnicity data from Census Table_06."""
    census_file = RAW_DIR / "censusbasedstatisticsuk2021.xlsx"
    
    print("="*80)
    print("EXTRACTING ETHNICITY DATA FROM CENSUS 2021")
    print("="*80)
    
    # Read Table_06 with more rows to see structure
    df = pd.read_excel(census_file, sheet_name='Table_06', header=None)
    
    print(f"\nFull table shape: {df.shape}")
    print(f"\nFirst 50 rows:")
    print(df.head(50))
    
    # The actual data starts after the header rows
    # Look for row with ethnicity category headers
    for idx in range(50):
        row = df.iloc[idx]
        row_str = ' '.join([str(v) for v in row.values if pd.notna(v)])
        if 'White' in row_str or 'Asian' in row_str or 'Black' in row_str:
            print(f"\n*** Found potential ethnicity categories at row {idx} ***")
            print(f"Row {idx}: {row.tolist()}")
    
    # Try to find the header row and data rows
    print("\n\nSearching for age breakdowns with ethnicity data...")
    for idx in range(10, min(100, len(df))):
        row = df.iloc[idx]
        if any('White' in str(v) for v in row.values if pd.notna(v)):
            print(f"\nRow {idx}: {row.tolist()}")

if __name__ == "__main__":
    extract_ethnicity()
