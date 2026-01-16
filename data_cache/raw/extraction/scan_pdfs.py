"""
Extract tables from ONS PDFs using pdfplumber
Searches for marital status, employment rates, and self-employment data
"""
import pdfplumber
import pandas as pd
from pathlib import Path
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("data_cache/raw")
EXTRACTION_DIR = RAW_DIR / "extraction"
OUTPUT_DIR = Path("data_cache")

print("="*80)
print("PDF TABLE EXTRACTION - ONS Documents")
print("="*80)

# Track what we find
findings = {
    'single_rates': None,
    'employment_rates': None,
    'self_employed_income': None,
}

# ============================================================================
# 1. FAMILIES AND HOUSEHOLDS - Extract Single Rates by Age
# ============================================================================

print("\n" + "="*80)
print("1. EXTRACTING SINGLE RATES BY AGE")
print("   Source: Families and households in the UK 2024.pdf")
print("="*80)

families_pdf = RAW_DIR / "Families and households in the UK 2024.pdf"

if families_pdf.exists():
    print(f"\nOpening: {families_pdf.name}")
    
    with pdfplumber.open(families_pdf) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        single_data = []
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            if tables:
                print(f"\nPage {page_num}: Found {len(tables)} table(s)")
                
                for table_idx, table in enumerate(tables):
                    # Convert to DataFrame to inspect
                    if len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        
                        # Check if this looks like marital status/living arrangements by age
                        table_str = df.to_string()
                        col_str = str(df.columns).lower()
                        
                        if any(keyword in table_str.lower() for keyword in ['single', 'never married', 'marital', 'living arrangements']):
                            print(f"  Table {table_idx}: Potential marital status data found")
                            print(f"  Columns: {list(df.columns)[:8]}")  # First 8 cols
                            print(f"  Shape: {df.shape}")
                            print(f"  First few rows:")
                            print(df.head(3).to_string())
                            
                            # Try to extract single rates
                            # Look for rows with age bands (16-24, 25-34, etc.)
                            age_patterns = ['16-24', '16-', '20-24', '25-34', '35-44', '45-54', '55-64', '65', 'All ages']
                            
                            for idx, row in df.iterrows():
                                row_str = str(row.iloc[0]).lower() if pd.notna(row.iloc[0]) else ""
                                
                                # Check if row contains age or marital status keywords
                                if any(age in str(row.iloc[0]) for age in age_patterns) or 'single' in row_str:
                                    print(f"    Row {idx}: {row.tolist()[:5]}")

else:
    print(f"File not found: {families_pdf}")

# ============================================================================
# 2. LABOUR FORCE SURVEY - Extract Employment Rates by Age/Gender
# ============================================================================

print("\n\n" + "="*80)
print("2. EXTRACTING EMPLOYMENT RATES BY AGE/GENDER")
print("   Source: Labour Force Survey performance and quality monitoring report_")
print("           October to December 2023.pdf")
print("="*80)

lfs_pdf = RAW_DIR / "Labour Force Survey performance and quality monitoring report_ October to December 2023.pdf"

if lfs_pdf.exists():
    print(f"\nOpening: {lfs_pdf.name}")
    
    with pdfplumber.open(lfs_pdf) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            if tables:
                print(f"\nPage {page_num}: Found {len(tables)} table(s)")
                
                for table_idx, table in enumerate(tables):
                    if len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        
                        table_str = df.to_string()
                        col_str = str(df.columns).lower()
                        
                        # Look for employment rate data by age and gender
                        if any(keyword in table_str.lower() for keyword in ['employment', 'male', 'female', 'age']) or \
                           any(keyword in col_str for keyword in ['male', 'female', 'gender']):
                            
                            print(f"  Table {table_idx}: Potential employment data")
                            print(f"  Columns: {list(df.columns)[:10]}")
                            print(f"  Shape: {df.shape}")
                            print(f"  First few rows:")
                            print(df.head(3).to_string())

else:
    print(f"File not found: {lfs_pdf}")

# ============================================================================
# 3. HMRC - Extract Self-Employment Income
# ============================================================================

print("\n\n" + "="*80)
print("3. EXTRACTING SELF-EMPLOYMENT INCOME DATA")
print("   Source: Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf")
print("="*80)

hmrc_pdf = RAW_DIR / "Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf"

if hmrc_pdf.exists():
    print(f"\nOpening: {hmrc_pdf.name}")
    
    with pdfplumber.open(hmrc_pdf) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            if tables:
                print(f"\nPage {page_num}: Found {len(tables)} table(s)")
                
                for table_idx, table in enumerate(tables):
                    if len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        
                        table_str = df.to_string()
                        
                        # Look for self-employment income tables
                        if any(keyword in table_str.lower() for keyword in ['self-employment', 'self employed', 'income', '£', 'thousand']):
                            
                            print(f"  Table {table_idx}: Potential self-employment data")
                            print(f"  Columns: {list(df.columns)[:10]}")
                            print(f"  Shape: {df.shape}")
                            print(f"  First few rows:")
                            print(df.head(3).to_string())

else:
    print(f"File not found: {hmrc_pdf}")

print("\n\n" + "="*80)
print("SUMMARY")
print("="*80)
print("""
Extraction complete. Check output above for found tables.

Next steps:
1. Review the tables found for each PDF
2. Identify which tables contain the data we need
3. If tables found are correct, create extraction_processor.py to:
   - Parse the identified tables
   - Extract specific columns
   - Clean data (decimals, formatting)
   - Save to CSV files

Files to be created (if successful):
  - data_cache/single_rate_by_age.csv
  - data_cache/employment_rate_by_age_gender.csv
  - data_cache/self_employed_income_distribution_male.csv
  - data_cache/self_employed_income_distribution_female.csv
""")
