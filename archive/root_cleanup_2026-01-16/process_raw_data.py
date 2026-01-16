"""
Helper script to process downloaded ONS/HMRC files into normalized data_cache/ CSVs.
Place your raw files in data_cache/raw/ and run this script to extract the needed tables.
"""

import os
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent / "data_cache" / "raw"
CACHE_DIR = Path(__file__).parent / "data_cache"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def normalize_dict(d: dict) -> dict:
    """Normalize dict values to sum to 1.0"""
    s = sum(d.values())
    if s > 0:
        return {k: v/s for k, v in d.items()}
    return d


def process_ethnicity_census():
    """
    Extract ethnicity distribution from Census 2021 files.
    Expected: CSV/XLSX with ethnicity categories and counts/shares.
    Output: ethnicity_distribution.csv with columns: key, value
    """
    # Look for census ethnicity file
    candidates = list(RAW_DIR.glob("*census*ethnicity*.csv")) + \
                 list(RAW_DIR.glob("*census*ethnicity*.xlsx"))
    
    if not candidates:
        print("❌ Missing: Census 2021 ethnicity file")
        print("   Need: Table with ethnicity categories and population counts/shares")
        print("   From: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/censusbasedstatisticsuk2021")
        return
    
    # Parse first candidate
    file = candidates[0]
    print(f"✓ Found: {file.name}")
    # TODO: Add specific parsing logic once we know the file structure
    print("   → Manual review needed: check column names and structure")


def process_families_households():
    """
    Extract single rates by age from Families & Households bulletin.
    Expected: Table with age bands and single/never married percentages.
    Output: single_rate_by_age.csv with columns: key, value
    """
    candidates = list(RAW_DIR.glob("*families*households*.csv")) + \
                 list(RAW_DIR.glob("*families*households*.xlsx")) + \
                 list(RAW_DIR.glob("*families*households*.ods"))
    
    if not candidates:
        print("❌ Missing: Families & Households 2024 data")
        print("   Need: Table with age bands and single/unmarried rates")
        print("   From: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/bulletins/familiesandhouseholds/2024")
        return
    
    file = candidates[0]
    print(f"✓ Found: {file.name}")
    print("   → Manual review needed: extract single rates by age band")


def process_employment_lfs():
    """
    Extract employment rates by age & gender from Labour Force Survey.
    Expected: Table with age bands, gender, and employment rates.
    Output: employment_rate_by_age_gender.csv with columns: age_band, gender, rate
    """
    candidates = list(RAW_DIR.glob("*lfs*.csv")) + \
                 list(RAW_DIR.glob("*lfs*.xlsx")) + \
                 list(RAW_DIR.glob("*labour*force*.csv")) + \
                 list(RAW_DIR.glob("*labour*force*.xlsx"))
    
    if not candidates:
        print("❌ Missing: Labour Force Survey employment data")
        print("   Need: Employment rates by age band and gender")
        print("   From: https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes")
        return
    
    file = candidates[0]
    print(f"✓ Found: {file.name}")
    print("   → Manual review needed: extract employment rates by age/gender")


def process_ashe_income():
    """
    Extract employee income distribution from ASHE (Annual Survey of Hours and Earnings).
    Expected: Tables with income brackets and percentages for males/females.
    Output: income_distribution_male.csv, income_distribution_female.csv
    """
    candidates = list(RAW_DIR.glob("*ashe*.csv")) + \
                 list(RAW_DIR.glob("*ashe*.xlsx")) + \
                 list(RAW_DIR.glob("*earnings*.csv")) + \
                 list(RAW_DIR.glob("*earnings*.xlsx"))
    
    if not candidates:
        print("❌ Missing: ASHE 2025 employee income data")
        print("   Need: Income distribution by brackets, separate for male/female")
        print("   From: https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2025")
        return
    
    file = candidates[0]
    print(f"✓ Found: {file.name}")
    print("   → Manual review needed: extract income brackets by gender")


def process_hmrc_self_employed():
    """
    Extract self-employed income distribution from HMRC data.
    Expected: Tables with income brackets and counts/percentages for self-employed.
    Output: self_employed_income_distribution_male.csv, self_employed_income_distribution_female.csv
    """
    candidates = list(RAW_DIR.glob("*hmrc*.csv")) + \
                 list(RAW_DIR.glob("*hmrc*.xlsx")) + \
                 list(RAW_DIR.glob("*self*employ*.csv")) + \
                 list(RAW_DIR.glob("*self*employ*.xlsx")) + \
                 list(RAW_DIR.glob("*personal*income*.csv")) + \
                 list(RAW_DIR.glob("*personal*income*.xlsx"))
    
    if not candidates:
        print("❌ Missing: HMRC self-employed income data")
        print("   Need: Self-employment income distribution by brackets and gender")
        print("   From: https://www.gov.uk/government/statistics/personal-incomes-statistics-for-the-tax-year-2022-to-2023")
        return
    
    file = candidates[0]
    print(f"✓ Found: {file.name}")
    print("   → Manual review needed: extract self-employed income by gender")


def main():
    print("=" * 70)
    print("DATA FILE PROCESSOR")
    print("=" * 70)
    print()
    print("Checking for downloaded files in data_cache/raw/...")
    print()
    
    # Check what files exist
    raw_files = list(RAW_DIR.glob("*"))
    if not raw_files:
        print("⚠️  No files found in data_cache/raw/")
        print()
        print("INSTRUCTIONS:")
        print("1. Download the following datasets:")
        print()
    
    # Process each dataset
    process_ethnicity_census()
    print()
    process_families_households()
    print()
    process_employment_lfs()
    print()
    process_ashe_income()
    print()
    process_hmrc_self_employed()
    print()
    
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Move your downloaded CSV/XLSX/ODS files to: data_cache/raw/")
    print("2. Run this script again to see what's detected")
    print("3. For detected files, manually extract the needed tables:")
    print("   - Open the file in Excel/LibreOffice")
    print("   - Find the relevant table (e.g., ethnicity shares, income brackets)")
    print("   - Export as CSV with headers: key,value (or age_band,gender,rate)")
    print("   - Save to data_cache/ with the expected filename")
    print()
    print("Expected output files in data_cache/:")
    print("  - ethnicity_distribution.csv")
    print("  - single_rate_by_age.csv")
    print("  - employment_rate_by_age_gender.csv")
    print("  - income_distribution_male.csv")
    print("  - income_distribution_female.csv")
    print("  - self_employed_income_distribution_male.csv")
    print("  - self_employed_income_distribution_female.csv")


if __name__ == "__main__":
    main()
