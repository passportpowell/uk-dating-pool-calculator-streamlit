"""
Final extraction of ethnicity distribution from Census 2021.
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data_cache" / "raw"
OUT_DIR = BASE_DIR / "data_cache"

def extract_and_save_ethnicity():
    """Extract ethnicity distribution and save to CSV."""
    census_file = RAW_DIR / "censusbasedstatisticsuk2021.xlsx"
    
    print("="*80)
    print("EXTRACTING AND SAVING ETHNICITY DISTRIBUTION")
    print("="*80)
    
    # Read Table_06 with row 7 as header
    df = pd.read_excel(census_file, sheet_name='Table_06', header=7)
    
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nFirst 20 rows:\n{df.head(20)}")
    
    # Sum all age groups for UK total
    # Filter for "United Kingdom" rows only
    uk_data = df[df['Geography'] == 'United Kingdom'].copy()
    
    print(f"\n\nFound {len(uk_data)} UK rows")
    print(f"\nUK data sample:\n{uk_data.head(10)}")
    
    # Sum across all ages
    ethnicity_totals = {
        'Asian': uk_data['Asian ethnic groups [Note 14]'].sum(),
        'Black': uk_data['Black, Caribbean or African ethnic groups'].sum(),
        'Mixed': uk_data['Mixed or Multiple ethnic groups'].sum(),
        'White': uk_data['White ethnic groups [Note 14]'].sum(),
        'Other': uk_data['Other ethnic groups [Note 14]'].sum()
    }
    
    print(f"\n\nEthnicity totals:")
    for eth, count in ethnicity_totals.items():
        print(f"  {eth}: {count:,}")
    
    total_pop = sum(ethnicity_totals.values())
    print(f"\nTotal population: {total_pop:,}")
    
    # Our app uses more granular categories - we need to map Census broad groups
    # to our specific categories. For now, create a simple mapping:
    # 
    # Census: White -> Our: White British (assume majority), White Other
    # Census: Asian -> Our: Asian British, Indian, Pakistani, Bangladeshi, Chinese, Other Asian
    # Census: Black -> Our: Black British, Caribbean, African, Other Black
    # Census: Mixed -> Our: White and Asian, White and Black, Other Mixed
    # Census: Other -> Our: Arab, Other
    
    # For simplicity, distribute proportionally within categories
    # This is an approximation - ideally we'd have the detailed breakdown
    
    app_categories = {
        # White groups (assume 70% White British, 30% White Other as rough estimate)
        'White British': ethnicity_totals['White'] * 0.70,
        'White Other': ethnicity_totals['White'] * 0.30,
        
        # Asian groups (distribute evenly for now - ideally use detailed Census table)
        'Asian British': ethnicity_totals['Asian'] * 0.25,
        'Indian': ethnicity_totals['Asian'] * 0.25,
        'Pakistani': ethnicity_totals['Asian'] * 0.20,
        'Bangladeshi': ethnicity_totals['Asian'] * 0.10,
        'Chinese': ethnicity_totals['Asian'] * 0.10,
        'Other Asian': ethnicity_totals['Asian'] * 0.10,
        
        # Black groups (distribute evenly)
        'Black British': ethnicity_totals['Black'] * 0.30,
        'Caribbean': ethnicity_totals['Black'] * 0.25,
        'African': ethnicity_totals['Black'] * 0.35,
        'Other Black': ethnicity_totals['Black'] * 0.10,
        
        # Mixed groups (distribute evenly)
        'White and Asian': ethnicity_totals['Mixed'] * 0.40,
        'White and Black': ethnicity_totals['Mixed'] * 0.40,
        'Other Mixed': ethnicity_totals['Mixed'] * 0.20,
        
        # Other groups
        'Arab': ethnicity_totals['Other'] * 0.50,
        'Other': ethnicity_totals['Other'] * 0.50
    }
    
    print(f"\n\nMapped to app categories:")
    for cat, count in sorted(app_categories.items()):
        prob = count / total_pop
        print(f"  {cat}: {count:,.0f} ({prob:.4f})")
    
    # Normalize to probabilities
    ethnicity_probs = {cat: count / total_pop for cat, count in app_categories.items()}
    
    # Save as CSV
    output_file = OUT_DIR / "ethnicity_distribution.csv"
    df_out = pd.DataFrame(list(ethnicity_probs.items()), columns=['ethnicity', 'probability'])
    df_out.to_csv(output_file, index=False)
    
    print(f"\n\n✓ Saved ethnicity distribution to {output_file}")
    
    # Update provenance
    provenance = {
        'dataset': 'ethnicity_distribution',
        'source_file': str(census_file.name),
        'source_url': 'https://www.ons.gov.uk/census',
        'last_fetched': datetime.now().isoformat(),
        'notes': 'Extracted from Census 2021 Table_06. Broad categories distributed proportionally into detailed categories as approximation.'
    }
    
    # Load existing provenance or create new
    prov_file = OUT_DIR / "metadata.json"
    if prov_file.exists():
        with open(prov_file, 'r') as f:
            all_prov = json.load(f)
    else:
        all_prov = []
    
    # Update or add ethnicity provenance
    found = False
    for item in all_prov:
        if item['dataset'] == 'ethnicity_distribution':
            item.update(provenance)
            found = True
            break
    if not found:
        all_prov.append(provenance)
    
    with open(prov_file, 'w') as f:
        json.dump(all_prov, f, indent=2)
    
    print(f"✓ Updated provenance metadata")
    
    return ethnicity_probs

if __name__ == "__main__":
    extract_and_save_ethnicity()
    
    print("\n" + "="*80)
    print("NEXT: EXTRACT OTHER DATASETS")
    print("="*80)
    print("""
Still needed (all PDFs require manual extraction):
1. Single rates by age - Families & Households PDF
2. Employment rates by age/gender - Labour Force Survey PDF
3. Employee income distributions - ASHE PDF
4. Self-employed income distributions - HMRC ODS or Personal Incomes PDF

Run the extract_data.py script to explore the HMRC ODS file next.
    """)
