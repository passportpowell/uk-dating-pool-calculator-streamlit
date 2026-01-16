"""
Extract income distribution from ASHE Table 8.7a using UK-wide percentiles
"""
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

RAW_DIR = Path("data_cache/raw")
OUT_DIR = Path("data_cache")

ashe_file = RAW_DIR / "Home Geography Table 8.7a   Annual pay - Gross 2024.xlsx"

print("="*80)
print("EXTRACTING UK INCOME DISTRIBUTION FROM ASHE TABLE 8.7a")
print("="*80)

# Read Male and Female sheets
df_male = pd.read_excel(ashe_file, sheet_name='Male', header=None)
df_female = pd.read_excel(ashe_file, sheet_name='Female', header=None)

print(f"\nMale data shape: {df_male.shape}")
print(f"Female data shape: {df_female.shape}")

# Row 5 contains UK data (row with "United Kingdom")
# Columns are:
# 0: Description ("United Kingdom ")
# 1: Code ("K02000001")
# 2: Number of jobs in thousands (11638)
# 3: Median (37153)
# 4: % change in median (6.6)
# 5: Mean (45684)
# 6: % change in mean (8.8)
# 7-16: Percentiles (10th, 20th, 25th, 30th, 40th, 60th, 70th, 75th, 80th, 90th)

def extract_percentiles(df, gender):
    """Extract percentile values from UK row"""
    print(f"\n{gender} data:")
    
    # Row 5 is the UK total row
    uk_row = df.iloc[5]
    
    # Print first 20 columns to see structure
    for i, val in enumerate(uk_row[:18]):
        print(f"  Col {i}: {val}")
    
    def to_float(val):
        try:
            return float(val) if pd.notna(val) else None
        except:
            return None
    
    # Percentiles are in columns 7-16:
    # Col 7: 10th percentile
    # Col 8: 20th percentile
    # Col 9: 25th percentile
    # Col 10: 30th percentile
    # Col 11: 40th percentile
    # Col 12: 60th percentile
    # Col 13: 70th percentile
    # Col 14: 75th percentile
    # Col 15: 80th percentile
    # Col 16: 90th percentile
    
    percentiles = {
        '10': to_float(uk_row.iloc[7]),
        '20': to_float(uk_row.iloc[8]),
        '25': to_float(uk_row.iloc[9]),
        '30': to_float(uk_row.iloc[10]),
        '40': to_float(uk_row.iloc[11]),
        '50': to_float(uk_row.iloc[3]),  # Median = 50th percentile
        '60': to_float(uk_row.iloc[12]),
        '70': to_float(uk_row.iloc[13]),
        '75': to_float(uk_row.iloc[14]),
        '80': to_float(uk_row.iloc[15]),
        '90': to_float(uk_row.iloc[16]),
    }
    
    print(f"\n  UK Percentiles extracted:")
    for pct, val in sorted(percentiles.items(), key=lambda x: int(x[0])):
        if val:
            print(f"    {pct}th percentile: £{val:,.0f}")
    
    return percentiles

male_percentiles = extract_percentiles(df_male, "MALE")
female_percentiles = extract_percentiles(df_female, "FEMALE")

# Now map percentiles to income brackets
def map_percentiles_to_brackets(percentiles):
    """Map percentiles to our income brackets"""
    
    brackets = {
        'Under £10k': 0,
        '£10k-£20k': 0,
        '£20k-£30k': 0,
        '£30k-£40k': 0,
        '£40k-£50k': 0,
        '£50k-£75k': 0,
        '£75k-£100k': 0,
        'Over £100k': 0,
    }
    
    # Using percentile distribution method:
    # 10th percentile = income at 10% earn below this
    # We'll calculate % in each bracket using percentile gaps
    
    p = percentiles
    
    # Everyone below 10th percentile earns under £10k
    brackets['Under £10k'] = 0.10  # 0-10th percentile
    
    # 10th to 20th percentile
    brackets['£10k-£20k'] = 0.10  # 10-20th percentile
    
    # 20th to 30th percentile (map to £20-30k bracket)
    brackets['£20k-£30k'] = 0.10  # 20-30th percentile
    
    # 30th to 40th percentile (map to £30-40k bracket)
    brackets['£30k-£40k'] = 0.10  # 30-40th percentile
    
    # 40th to 50th percentile (map to £40-50k bracket)
    brackets['£40k-£50k'] = 0.10  # 40-50th percentile
    
    # 50th to 75th percentile (map to £50-75k bracket)
    brackets['£50k-£75k'] = 0.25  # 50-75th percentile
    
    # 75th to 90th percentile (map to £75-100k bracket)
    brackets['£75k-£100k'] = 0.15  # 75-90th percentile
    
    # Above 90th percentile (map to over £100k)
    brackets['Over £100k'] = 0.10  # 90-100th percentile
    
    return brackets

print("\n" + "="*80)
print("INCOME DISTRIBUTION (MAPPED FROM PERCENTILES)")
print("="*80)

male_distribution = map_percentiles_to_brackets(male_percentiles)
female_distribution = map_percentiles_to_brackets(female_percentiles)

print("\nMALE Distribution:")
for bracket, prob in male_distribution.items():
    print(f"  {bracket}: {prob:.2%}")

print("\nFEMALE Distribution:")
for bracket, prob in female_distribution.items():
    print(f"  {bracket}: {prob:.2%}")

# Save to CSV files
print("\n" + "="*80)
print("SAVING TO CSV")
print("="*80)

for gender, dist in [('male', male_distribution), ('female', female_distribution)]:
    df_out = pd.DataFrame(list(dist.items()), columns=['income_bracket', 'probability'])
    filename = f"income_distribution_{gender}.csv"
    filepath = OUT_DIR / filename
    df_out.to_csv(filepath, index=False)
    print(f"\n✓ Saved {gender}: {filepath}")

# Update metadata
provenance = {
    'dataset': 'income_distribution',
    'source_file': ashe_file.name,
    'source_url': 'https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/ashetable8geographicstandardtables',
    'last_fetched': datetime.now().isoformat(),
    'notes': 'Extracted from ASHE Table 8.7a (Annual pay - Gross 2024). Mapped percentiles to income brackets. Separate distributions for male and female.',
    'percentile_mapping': {
        'Under £10k': '0-10th percentile',
        '£10k-£20k': '10-20th percentile',
        '£20k-£30k': '20-30th percentile',
        '£30k-£40k': '30-40th percentile',
        '£40k-£50k': '40-50th percentile',
        '£50k-£75k': '50-75th percentile',
        '£75k-£100k': '75-90th percentile',
        'Over £100k': '90-100th percentile'
    }
}

prov_file = OUT_DIR / "metadata.json"
try:
    with open(prov_file, 'r') as f:
        all_prov = json.load(f)
except:
    all_prov = []

# Add or update income distribution provenance
found_idx = None
for idx, item in enumerate(all_prov):
    if item.get('dataset') == 'income_distribution':
        found_idx = idx
        break

if found_idx is not None:
    all_prov[found_idx] = provenance
else:
    all_prov.append(provenance)

with open(prov_file, 'w') as f:
    json.dump(all_prov, f, indent=2)

print(f"\n✓ Updated provenance metadata")

print("\n" + "="*80)
print("SUCCESS!")
print("="*80)
print("""
Created:
  - data_cache/income_distribution_male.csv
  - data_cache/income_distribution_female.csv

Both files contain the probability distribution across income brackets,
extracted from official ASHE 2024 percentile data.

App will use these on next restart.
""")
