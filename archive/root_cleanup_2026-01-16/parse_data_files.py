"""
Parse downloaded ONS/HMRC files and generate normalized CSVs for data_cache/.
Run this after placing raw files in data_cache/raw/
"""

import os
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

RAW_DIR = Path(__file__).parent / "data_cache" / "raw"
CACHE_DIR = Path(__file__).parent / "data_cache"


def normalize_dict(d: dict) -> dict:
    """Normalize dict values to sum to 1.0"""
    s = sum(d.values())
    if s > 0:
        return {k: v/s for k, v in d.items()}
    return d


def parse_census_ethnicity():
    """
    Parse censusbasedstatisticsuk2021.xlsx for ethnicity distribution.
    Look for ethnicity population counts and convert to shares.
    """
    file = RAW_DIR / "censusbasedstatisticsuk2021.xlsx"
    if not file.exists():
        return None
    
    try:
        # Try to find ethnicity sheet - Census files often have multiple sheets
        xl = pd.ExcelFile(file)
        print(f"Census sheets: {xl.sheet_names}")
        
        # Look for ethnicity-related sheet
        ethnicity_sheets = [s for s in xl.sheet_names if 'ethnic' in s.lower() or 'ethnicity' in s.lower()]
        
        if ethnicity_sheets:
            df = pd.read_excel(file, sheet_name=ethnicity_sheets[0])
        else:
            # Try first sheet
            df = pd.read_excel(file, sheet_name=0)
        
        print(f"Census columns: {df.columns.tolist()}")
        print(f"First few rows:\n{df.head()}")
        
        # Manual extraction needed - structure varies by Census release
        # For now, use curated data and note source
        return {
            "source": "Census 2021 (manual extraction needed)",
            "file": file.name,
            "note": "Complex multi-sheet file - requires manual table identification"
        }
        
    except Exception as e:
        print(f"Error parsing census: {e}")
        return None


def parse_families_households_pdf():
    """
    Parse Families and households PDF for single rates by age.
    PDFs require manual extraction - note that tables are present.
    """
    file = RAW_DIR / "Families and households in the UK 2024.pdf"
    if not file.exists():
        return None
    
    return {
        "source": "ONS Families & Households 2024",
        "file": file.name,
        "note": "PDF format - manual extraction required. Look for 'Living arrangements by age' table."
    }


def parse_labour_force_pdf():
    """
    Parse Labour Force Survey PDF for employment rates.
    PDFs require manual extraction.
    """
    file = RAW_DIR / "Labour Force Survey performance and quality monitoring report_ October to December 2023.pdf"
    if not file.exists():
        return None
    
    return {
        "source": "ONS Labour Force Survey Q4 2023",
        "file": file.name,
        "note": "PDF format - manual extraction required. Look for employment rates by age/gender."
    }


def parse_workless_households_pdf():
    """
    Parse Working and workless households PDF for employment data.
    """
    file = RAW_DIR / "Working and workless households in the UK July to September 2025.pdf"
    if not file.exists():
        return None
    
    return {
        "source": "ONS Working/Workless Households Q3 2025",
        "file": file.name,
        "note": "PDF format - contains household employment data, may supplement LFS"
    }


def parse_employee_earnings_pdf():
    """
    Parse Employee earnings (ASHE) PDF for income distribution.
    """
    file = RAW_DIR / "Employee earnings in the UK 2025.pdf"
    if not file.exists():
        return None
    
    return {
        "source": "ONS ASHE 2025",
        "file": file.name,
        "note": "PDF format - manual extraction required. Look for income percentiles by gender."
    }


def parse_self_employment_ods():
    """
    Parse HMRC self-employment income ODS file.
    ODS can be read with pandas if odfpy is installed.
    """
    file = RAW_DIR / "Table_3.10_2223 Income of individuals with self-employment income 2022 to 2023.ods"
    if not file.exists():
        return None
    
    try:
        # Try to read ODS file
        try:
            df = pd.read_excel(file, engine='odf')
            print(f"Self-employment ODS columns: {df.columns.tolist()}")
            print(f"First few rows:\n{df.head(10)}")
            
            # Look for income brackets and counts/percentages
            # Structure needs to be examined
            return {
                "source": "HMRC Self-Employment Income 2022-2023",
                "file": file.name,
                "note": "ODS readable - manual mapping needed to extract income brackets by gender"
            }
        except ImportError:
            return {
                "source": "HMRC Self-Employment Income 2022-2023",
                "file": file.name,
                "note": "ODS format - install odfpy to read: pip install odfpy"
            }
            
    except Exception as e:
        print(f"Error parsing self-employment ODS: {e}")
        return None


def parse_personal_incomes_pdf():
    """
    Parse Personal Incomes Statistics PDF from HMRC.
    """
    file = RAW_DIR / "Personal Incomes Statistics 2022 to 2023 Summary Statistics.pdf"
    if not file.exists():
        return None
    
    return {
        "source": "HMRC Personal Incomes Statistics 2022-2023",
        "file": file.name,
        "note": "PDF format - contains tax data, can supplement income distributions"
    }


def parse_trusts_pdf():
    """
    Parse Statistics on trusts PDF.
    """
    file = RAW_DIR / "Statistics on trusts in the UK December 2025.pdf"
    if not file.exists():
        return None
    
    return {
        "source": "HMRC Trusts Statistics Dec 2025",
        "file": file.name,
        "note": "PDF format - trust data, likely not directly relevant to dating pool"
    }


def create_example_csvs():
    """
    Create example CSV templates showing the expected format for manual data entry.
    """
    # Example ethnicity distribution
    ethnicity_example = pd.DataFrame({
        'key': ['White British', 'White Irish', 'White Other', 'Asian/Asian British - Indian'],
        'value': [0.744, 0.009, 0.062, 0.030]
    })
    ethnicity_example.to_csv(CACHE_DIR / "ethnicity_distribution_TEMPLATE.csv", index=False)
    
    # Example single rate by age
    single_example = pd.DataFrame({
        'key': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
        'value': [0.78, 0.50, 0.32, 0.25, 0.20, 0.10]
    })
    single_example.to_csv(CACHE_DIR / "single_rate_by_age_TEMPLATE.csv", index=False)
    
    # Example employment rate
    employment_example = pd.DataFrame({
        'age_band': ['18-24', '18-24', '25-34', '25-34'],
        'gender': ['Male', 'Female', 'Male', 'Female'],
        'rate': [0.62, 0.60, 0.85, 0.80]
    })
    employment_example.to_csv(CACHE_DIR / "employment_rate_by_age_gender_TEMPLATE.csv", index=False)
    
    # Example income distribution
    income_example = pd.DataFrame({
        'key': ['Under £20k', '£20k-£30k', '£30k-£40k', '£40k-£50k', '£50k-£75k'],
        'value': [0.25, 0.22, 0.18, 0.13, 0.14]
    })
    income_example.to_csv(CACHE_DIR / "income_distribution_male_TEMPLATE.csv", index=False)
    
    print("✓ Created CSV templates in data_cache/")


def main():
    print("=" * 80)
    print("PARSING DOWNLOADED DATA FILES")
    print("=" * 80)
    print()
    
    provenance = []
    
    # Parse each file
    print("1. Census 2021 ethnicity...")
    result = parse_census_ethnicity()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    print("2. Families & Households 2024...")
    result = parse_families_households_pdf()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    print("3. Labour Force Survey Q4 2023...")
    result = parse_labour_force_pdf()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    print("4. Working/Workless Households Q3 2025...")
    result = parse_workless_households_pdf()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    print("5. ASHE Employee Earnings 2025...")
    result = parse_employee_earnings_pdf()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    print("6. HMRC Self-Employment Income 2022-2023...")
    result = parse_self_employment_ods()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    print("7. HMRC Personal Incomes 2022-2023...")
    result = parse_personal_incomes_pdf()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    print("8. HMRC Trusts Dec 2025...")
    result = parse_trusts_pdf()
    if result:
        provenance.append(result)
        print(f"   → {result.get('note', 'Processed')}")
    print()
    
    # Save provenance
    meta_path = CACHE_DIR / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    print(f"✓ Saved provenance to {meta_path}")
    print()
    
    # Create templates
    create_example_csvs()
    print()
    
    print("=" * 80)
    print("NEXT STEPS: MANUAL DATA EXTRACTION")
    print("=" * 80)
    print()
    print("Most files are PDFs requiring manual extraction:")
    print()
    print("1. Open each PDF and find the relevant tables")
    print("2. Copy data to Excel/LibreOffice")
    print("3. Format as shown in the _TEMPLATE.csv files")
    print("4. Save to data_cache/ with correct filename (remove _TEMPLATE)")
    print()
    print("Required output files:")
    print("  ✓ ethnicity_distribution.csv")
    print("  ✓ single_rate_by_age.csv")
    print("  ✓ employment_rate_by_age_gender.csv")
    print("  ✓ income_distribution_male.csv")
    print("  ✓ income_distribution_female.csv")
    print("  ✓ self_employed_income_distribution_male.csv")
    print("  ✓ self_employed_income_distribution_female.csv")
    print()
    print("Once files are ready, the app will automatically load them on next run.")
    print("Check 'Data Provenance' expander in the app to verify sources.")


if __name__ == "__main__":
    main()
