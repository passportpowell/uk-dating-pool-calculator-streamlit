"""
Extract actual data from downloaded files into normalized CSVs.
"""
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data_cache" / "raw"
OUT_DIR = BASE_DIR / "data_cache"

def explore_census_file():
    """Explore Census XLSX file structure to find ethnicity data."""
    census_file = RAW_DIR / "censusbasedstatisticsuk2021.xlsx"
    
    print("\n" + "="*80)
    print("EXPLORING CENSUS 2021 FILE")
    print("="*80)
    
    xl = pd.ExcelFile(census_file)
    
    # Check each table sheet
    for sheet_name in xl.sheet_names:
        if 'Table' in sheet_name:
            print(f"\n--- {sheet_name} ---")
            df = pd.read_excel(census_file, sheet_name=sheet_name, nrows=20)
            print(f"Columns: {df.columns.tolist()}")
            print(f"First few rows:\n{df.head(10)}")
            
            # Look for ethnicity-related keywords
            df_str = df.to_string()
            if any(keyword in df_str.lower() for keyword in ['ethnic', 'white', 'asian', 'black', 'mixed']):
                print(f"   ^^^ LIKELY CONTAINS ETHNICITY DATA ^^^")

def explore_ods_file():
    """Explore HMRC self-employment ODS file."""
    ods_file = RAW_DIR / "Table_3.10_2223 Income of individuals with self-employment income 2022 to 2023.ods"
    
    print("\n" + "="*80)
    print("EXPLORING HMRC SELF-EMPLOYMENT ODS FILE")
    print("="*80)
    
    try:
        # Try to read with odfpy engine
        df = pd.read_excel(ods_file, engine='odf')
        print(f"\nColumns: {df.columns.tolist()}")
        print(f"\nShape: {df.shape}")
        print(f"\nFirst 30 rows:\n{df.head(30)}")
        print(f"\nLast 10 rows:\n{df.tail(10)}")
        
        # Save raw extract for inspection
        raw_output = OUT_DIR / "raw_self_employment_extract.csv"
        df.to_csv(raw_output, index=False)
        print(f"\n✓ Saved raw extract to {raw_output}")
        
    except Exception as e:
        print(f"Error reading ODS: {e}")

def extract_self_employment_income():
    """Extract self-employment income distribution from ODS file."""
    ods_file = RAW_DIR / "Table_3.10_2223 Income of individuals with self-employment income 2022 to 2023.ods"
    
    print("\n" + "="*80)
    print("EXTRACTING SELF-EMPLOYMENT INCOME DATA")
    print("="*80)
    
    try:
        # Read the full file
        df = pd.read_excel(ods_file, engine='odf')
        
        # Look for rows with income ranges and gender columns
        # Typical structure: Income range | Total | Male | Female
        print("\nSearching for income brackets and gender splits...")
        
        # Find rows containing income bracket patterns (e.g., "£10,000-£20,000")
        df_str = df.astype(str)
        income_rows = []
        
        for idx, row in df_str.iterrows():
            row_text = ' '.join(row.values)
            if '£' in row_text and ('-' in row_text or 'under' in row_text.lower() or 'over' in row_text.lower()):
                income_rows.append(idx)
        
        if income_rows:
            print(f"\nFound {len(income_rows)} potential income bracket rows")
            print(f"Row indices: {income_rows[:10]}...")
            
            # Show some sample rows
            for idx in income_rows[:5]:
                print(f"\nRow {idx}: {df.iloc[idx].tolist()}")
        else:
            print("\nNo obvious income bracket rows found - may need manual inspection")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Explore files to understand their structure
    explore_census_file()
    explore_ods_file()
    extract_self_employment_income()
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("""
Based on the exploration above:

1. Identify which Census table contains ethnicity data
2. Extract the relevant columns from that table
3. Map to our ethnicity categories (White British, White Other, etc.)
4. Normalize to probabilities

For ODS file:
1. Identify the income bracket columns
2. Find male/female split columns
3. Extract and normalize to match our income ranges

For PDFs (6 files):
- Manual extraction remains necessary
- Open PDFs, find tables, copy to Excel, format as templates show
    """)
