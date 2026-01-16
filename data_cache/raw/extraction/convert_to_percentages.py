"""
Convert single rate counts to percentages for use in app.
Single rates extracted from ONS are population counts by age.
This script converts them to percentages suitable for the app.
"""

import pandas as pd
import numpy as np
from pathlib import Path

cache_dir = Path("e:/OneDrive/Github/UK dating statistic calculator zbook/data_cache/")

# Load single rate data (population counts)
df_single = pd.read_csv(cache_dir / "single_rate_by_age.csv")

print("=" * 80)
print("CONVERTING SINGLE RATE POPULATION COUNTS TO PERCENTAGES")
print("=" * 80)

# Load population data (UK Census 2021 by age group)
# From uk_population_timeseries file
population_by_age = {
    "16 to 19": 2_900_000,      # Approximate from Census
    "20 to 24": 3_800_000,
    "25 to 29": 3_400_000,
    "30 to 34": 3_300_000,
    "35 to 39": 3_100_000,
    "40 to 44": 3_100_000,
    "45 to 49": 3_100_000,
    "50 to 54": 3_300_000,
    "55 to 59": 3_200_000,
    "60 to 64": 2_800_000,
    "65 to 69": 2_300_000,
    "70 to 74": 1_900_000,
    "75 to 79": 1_300_000,
    "80 to 84": 900_000,
    "85 and over": 700_000,
}

print("\nCalculating percentages...")
print(f"\n{'Age Band':<15} {'Single Count':<15} {'Pop. Est':<15} {'Single %':<10}")
print("-" * 55)

rates = {}
for _, row in df_single.iterrows():
    age_band = row['age_group']
    single_count = row['single_rate_total']
    
    # Get population estimate (may need to update with actual Census data)
    pop_est = population_by_age.get(age_band)
    
    if pop_est and single_count > 0:
        single_pct = single_count / pop_est
        rates[age_band] = single_pct
        print(f"{age_band:<15} {single_count:>14,.0f} {pop_est:>14,.0f} {single_pct:>9.2%}")
    else:
        print(f"{age_band:<15} {single_count:>14,.0f} {'UNKNOWN':<14} {'ERROR':<10}")

# Normalize to match expected age bands in data.py
normalized_rates = {}
normalized_rates["16-24"] = np.mean([rates.get("16 to 19", 0.78), rates.get("20 to 24", 0.78)])
normalized_rates["25-34"] = np.mean([rates.get("25 to 29", 0.50), rates.get("30 to 34", 0.50)])
normalized_rates["35-44"] = np.mean([rates.get("35 to 39", 0.32), rates.get("40 to 44", 0.32)])
normalized_rates["45-54"] = np.mean([rates.get("45 to 49", 0.25), rates.get("50 to 54", 0.25)])
normalized_rates["55-64"] = np.mean([rates.get("55 to 59", 0.20), rates.get("60 to 64", 0.20)])
normalized_rates["65+"] = np.mean([rates.get("65 to 69", 0.10), rates.get("70 to 74", 0.10), 
                                    rates.get("75 to 79", 0.10), rates.get("80 to 84", 0.10),
                                    rates.get("85 and over", 0.10)])

print("\n" + "=" * 80)
print("NORMALIZED TO APP AGE BANDS")
print("=" * 80)
for age_band, rate in normalized_rates.items():
    print(f"{age_band:<10} = {rate:.4f}  (Python: {rate})")

# Save as CSV for data_loader
output_df = pd.DataFrame({
    'key': list(normalized_rates.keys()),
    'value': list(normalized_rates.values())
})

output_file = cache_dir / "single_rate_by_age.csv"
output_df.to_csv(output_file, index=False)
print(f"\nSaved normalized rates to {output_file}")

# NOTE: Still need actual population totals by age from UK Census/ONS
print("\n" + "=" * 80)
print("TODO: Get accurate population counts by age from UK Census 2021")
print("=" * 80)
