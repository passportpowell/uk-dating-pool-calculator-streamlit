"""
Debug ASHE file structure to find actual percentile values
"""
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data_cache/raw")
ashe_file = RAW_DIR / "Home Geography Table 8.7a   Annual pay - Gross 2024.xlsx"

df_male = pd.read_excel(ashe_file, sheet_name='Male', header=None)

print("Rows 0-10 of Male sheet:")
for i in range(11):
    row_vals = df_male.iloc[i, :8].tolist()
    print(f"Row {i}: {row_vals}")

print("\n" + "="*80)
print("Looking for UK data row and actual percentile values...")
print("="*80)

for i in range(30):
    val0 = df_male.iloc[i, 0]
    val1 = df_male.iloc[i, 1]
    val3 = df_male.iloc[i, 3]  # Should be median value
    
    if val0 == "United Kingdom" and pd.notna(val3):
        print(f"\nFound UK row at index {i}:")
        for j in range(20):
            print(f"  Col {j}: {df_male.iloc[i, j]}")
        break
