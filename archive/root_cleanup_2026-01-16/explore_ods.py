"""
Explore ODS file sheets and structure.
"""
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data_cache" / "raw"

def explore_ods_sheets():
    """Explore all sheets in ODS file."""
    ods_file = RAW_DIR / "Table_3.10_2223 Income of individuals with self-employment income 2022 to 2023.ods"
    
    print("="*80)
    print("EXPLORING ODS FILE SHEETS")
    print("="*80)
    
    try:
        # ODS files might have multiple sheets - try to list them
        xl = pd.ExcelFile(ods_file, engine='odf')
        
        print(f"\nSheet names: {xl.sheet_names}")
        
        for sheet_name in xl.sheet_names:
            print(f"\n\n--- Sheet: {sheet_name} ---")
            df = pd.read_excel(ods_file, sheet_name=sheet_name, engine='odf', header=None)
            print(f"Shape: {df.shape}")
            print(f"\nFirst 50 rows:\n{df.head(50)}")
            
            # Look for income brackets
            df_str = df.astype(str)
            for idx, row in df_str.iterrows():
                row_text = ' '.join(row.values)
                if any(keyword in row_text.lower() for keyword in ['£', 'income', 'male', 'female', 'thousand']):
                    if idx < 100:  # Only show first 100 potential matches
                        print(f"\nRow {idx} (potential data): {row.tolist()}")
                        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore_ods_sheets()
