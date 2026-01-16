"""
Convert employment counts to percentages.
Calculates employment rates by age and gender using ONS data.
"""

import pandas as pd
import numpy as np
from pathlib import Path

cache_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/")
raw_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/raw/")

print("=" * 80)
print("CALCULATING EMPLOYMENT RATES")
print("=" * 80)

# Load employment data
emp_file = raw_dir / "employment_by_age_and_sex.xlsx"
df_emp = pd.read_excel(emp_file, sheet_name='Employment by age group', header=None)

# From manual inspection we know:
# Row 11: Age group header
# Rows 11-17: Data (7 age groups)
# Columns 1: age range
# Columns 2-3: 2011 Male & Female employees
# More columns follow for different years

# Manual extraction from the data we saw
employment_data = {
    "16 to 29": {"Male": 3236710, "Female": 3147842},
    "30 to 39": {"Male": 3015086, "Female": 2693458},
    "40 to 49": {"Male": 3146880, "Female": 3197622},
    "50 to 59": {"Male": 2293169, "Female": 2462009},
    "60 to 69": {"Male": 884951, "Female": 707945},
    "70 to 79": {"Male": 65634, "Female": 59230},
    "80 or over": {"Male": 6400, "Female": 3279},
}

# From marital status file, get population estimates by age
marital_file = raw_dir / "marital_status_and_living_arrangements_2002_2024.xlsx"
df_marital = pd.read_excel(marital_file, sheet_name='Table_1_Marital_Status_All', header=None)

# Find 2024 column
header_row = None
for i, row in df_marital.iterrows():
    if 'Marital status' in str(row.iloc[0]) and 'Age group' in str(row.iloc[1]):
        header_row = i
        break

headers = df_marital.iloc[header_row].tolist()
col_2024 = None
for i, h in enumerate(headers):
    if '2024' in str(h) and 'Estimate' in str(h):
        col_2024 = i
        break

# Calculate total population by age
population_by_age = {}
for i in range(header_row + 1, len(df_marital)):
    status = df_marital.iloc[i, 0]
    age = df_marital.iloc[i, 1]
    value = df_marital.iloc[i, col_2024]
    
    if pd.isna(age) or age == 'All Ages' or age == '0 to 15' or pd.isna(value):
        continue
    
    age_str = str(age)
    if age_str not in population_by_age:
        population_by_age[age_str] = 0
    
    try:
        population_by_age[age_str] += float(value)
    except (ValueError, TypeError):
        pass

print("\nPopulation by age (from Census 2024):")
for age, pop in population_by_age.items():
    print(f"{age:<15}: {pop:>12,.0f}")

# Map employment age bands to population age bands
employment_rates = {}

def map_emp_to_pop(emp_band):
    """Map employment age bands to population age bands."""
    if emp_band == "16 to 29":
        return ["16 to 19", "20 to 24", "25 to 29"]
    elif emp_band == "30 to 39":
        return ["30 to 34", "35 to 39"]
    elif emp_band == "40 to 49":
        return ["40 to 44", "45 to 49"]
    elif emp_band == "50 to 59":
        return ["50 to 54", "55 to 59"]
    elif emp_band == "60 to 69":
        return ["60 to 64", "65 to 69"]
    elif emp_band == "70 to 79":
        return ["70 to 74", "75 to 79"]
    elif emp_band == "80 or over":
        return ["80 to 84", "85 and over"]
    return []

print("\n" + "=" * 80)
print("EMPLOYMENT RATES BY AGE & GENDER (as percentages of population)")
print("=" * 80)

for emp_band, genders in employment_data.items():
    pop_bands = map_emp_to_pop(emp_band)
    
    # Get total population for this employment band
    total_pop_male = 0
    total_pop_female = 0
    
    for pop_band in pop_bands:
        if pop_band in population_by_age:
            # Rough split: assume 50/50 gender split
            total_pop_male += population_by_age[pop_band] / 2
            total_pop_female += population_by_age[pop_band] / 2
    
    if total_pop_male > 0 and total_pop_female > 0:
        rate_male = genders["Male"] / total_pop_male
        rate_female = genders["Female"] / total_pop_female
        
        employment_rates[emp_band] = {"Male": rate_male, "Female": rate_female}
        
        print(f"\n{emp_band}:")
        print(f"  Male:   {rate_male:>7.1%} ({genders['Male']:>10,.0f} / {total_pop_male:>10,.0f})")
        print(f"  Female: {rate_female:>7.1%} ({genders['Female']:>10,.0f} / {total_pop_female:>10,.0f})")

# Normalize to app age bands
print("\n" + "=" * 80)
print("NORMALIZED TO APP AGE BANDS")
print("=" * 80)

normalized = {}
for emp_band, rates in employment_rates.items():
    if emp_band == "16 to 29":
        app_band = "18-24"  # Note: original uses 18-24, not 16-24
    elif emp_band == "30 to 39":
        app_band = "25-34"
    elif emp_band == "40 to 49":
        app_band = "35-44"
    elif emp_band == "50 to 59":
        app_band = "45-54"
    elif emp_band == "60 to 69":
        app_band = "55-64"
    elif emp_band in ["70 to 79", "80 or over"]:
        app_band = "65+"
    else:
        app_band = None
    
    if app_band:
        if app_band not in normalized:
            normalized[app_band] = {"Male": [], "Female": []}
        normalized[app_band]["Male"].append(rates["Male"])
        normalized[app_band]["Female"].append(rates["Female"])

# Average within bands
final_rates = {}
for band in normalized:
    avg_male = np.mean(normalized[band]["Male"])
    avg_female = np.mean(normalized[band]["Female"])
    final_rates[band] = {"Male": avg_male, "Female": avg_female}
    print(f"{band}:")
    print(f'  "Male": {avg_male:.2f},')
    print(f'  "Female": {avg_female:.2f},')

# Save as CSV
output_records = []
for band, rates in final_rates.items():
    output_records.append({"age_band": band, "gender": "Male", "rate": rates["Male"]})
    output_records.append({"age_band": band, "gender": "Female", "rate": rates["Female"]})

output_df = pd.DataFrame(output_records)
output_file = cache_dir / "employment_rate_by_age_gender.csv"
output_df.to_csv(output_file, index=False)
print(f"\nSaved to {output_file}")

print("\nSample Python code for data.py:")
print("EMPLOYMENT_RATE_BY_AGE_GENDER = {")
for band in ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]:
    if band in final_rates:
        print(f'    "{band}": {{"Male": {final_rates[band]["Male"]:.2f}, "Female": {final_rates[band]["Female"]:.2f}}},')
print("}")
