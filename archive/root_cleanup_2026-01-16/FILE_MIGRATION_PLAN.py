"""
File organization structure for UK Dating Pool Calculator

Project structure (post-reorganization):
```
UK dating statistic calculator zbook/
├── app.py                          # Main entry point
├── requirements.txt                # Dependencies
├── .streamlit/                     # Streamlit config
├── .gitignore                      
├── README.md                       # Project documentation
├── src/                            # Source code
│   ├── __init__.py
│   ├── ai/                         # AI features
│   │   ├── __init__.py
│   │   └── assistant.py            # OpenAI integration
│   ├── calculations/               # Core calculation logic
│   │   ├── __init__.py
│   │   └── dating_pool.py          # Calculation functions
│   ├── data/                       # Data management
│   │   ├── __init__.py
│   │   ├── loader.py               # Load from data_cache CSV
│   │   ├── constants.py            # Data constants & overrides
│   │   └── provenance.py           # Data source tracking
│   ├── ui/                         # Streamlit UI components
│   │   ├── __init__.py
│   │   ├── sidebar.py              # Sidebar controls
│   │   ├── results.py              # Results display
│   │   ├── marriage_stats.py       # Marriage statistics UI
│   │   ├── income_stats.py         # Income demographics UI
│   │   └── baby_stats.py           # Baby health UI
│   ├── utils/                      # Utility functions
│   │   ├── __init__.py
│   │   ├── styles.py               # CSS styling
│   │   ├── maps.py                 # Map visualization
│   │   └── helpers.py              # Helper functions
│   └── pages/                      # Streamlit pages
│       ├── __init__.py
│       ├── 1_dating_pool.py
│       ├── 2_income_demographics.py
│       ├── 3_marriage_statistics.py
│       ├── 4_baby_health.py
│       └── 5_ai_assistant.py
├── data/                           # Data directory
│   ├── raw/                        # Raw source files
│   │   └── [kept outside archive for reference]
│   └── processed/                  # Extracted CSV files
│       ├── single_rate_by_age.csv
│       ├── employment_rate_by_age_gender.csv
│       ├── ethnicity_distribution.csv
│       ├── income_distribution_male.csv
│       └── income_distribution_female.csv
├── docs/                           # Documentation
│   ├── DATA_SOURCES.md
│   ├── ARCHITECTURE.md
│   ├── SETUP_GUIDE.md
│   └── AI_FEATURES.md
└── archive/                        # Deprecated files
    ├── old_scripts/
    ├── extracted_docs/
    └── tests/
```

File mapping for reorganization:
- calculations.py          → src/calculations/dating_pool.py
- data.py                  → src/data/constants.py
- data_loader.py           → src/data/loader.py
- provenance_ui.py         → src/data/provenance.py
- ai_assistant.py          → src/ai/assistant.py
- map_visualization.py      → src/utils/maps.py
- styles.py                → src/utils/styles.py
- ui_sidebar.py            → src/ui/sidebar.py
- ui_results.py            → src/ui/results.py
- ui_marriage_stats_content.py → src/ui/marriage_stats.py
- ui_income_stats_content.py   → src/ui/income_stats.py
- ui_baby_stats_content.py     → src/ui/baby_stats.py
- pages/*                  → src/pages/
- data_cache/*             → data/processed/

Files to archive (no longer needed):
- Various analysis scripts (analyze_*.py, extract_*.py, parse_*.py)
- Old documentation files (*_SUMMARY.md, *_CHECKLIST.md, etc.)
- Backup files (app copy.py, *_old.py)
- Temporary test files
- __pycache__/
"""

import os
import shutil
from pathlib import Path

def print_migration_plan():
    """Print the file migration plan."""
    print("=" * 80)
    print("FILE MIGRATION PLAN FOR UK DATING POOL CALCULATOR")
    print("=" * 80)
    
    print("""
PHASE 1: CORE LOGIC FILES (Move to src/)
  calculations.py          → src/calculations/dating_pool.py
  data.py                  → src/data/constants.py
  data_loader.py           → src/data/loader.py
  provenance_ui.py         → src/data/provenance.py
  map_visualization.py      → src/utils/maps.py
  styles.py                → src/utils/styles.py

PHASE 2: UI COMPONENT FILES (Move to src/ui/)
  ui_sidebar.py            → src/ui/sidebar.py
  ui_results.py            → src/ui/results.py
  ui_marriage_stats_content.py → src/ui/marriage_stats.py
  ui_income_stats_content.py   → src/ui/income_stats.py
  ui_baby_stats_content.py     → src/ui/baby_stats.py

PHASE 3: AI FILES (Move to src/ai/)
  ai_assistant.py          → src/ai/assistant.py

PHASE 4: PAGE FILES (Move to src/pages/)
  pages/1_Dating_Pool_Calculator.py     → src/pages/1_dating_pool.py
  pages/2_Income_Demographics.py        → src/pages/2_income_demographics.py
  pages/3_Marriage_Statistics.py        → src/pages/3_marriage_statistics.py
  pages/4_Baby_And_Child_Health.py      → src/pages/4_baby_health.py
  pages/5_AI_Assistant.py               → src/pages/5_ai_assistant.py

PHASE 5: DATA FILES (Move to data/)
  data_cache/*.csv         → data/processed/
  data_cache/raw/*         → data/raw/

PHASE 6: CLEANUP (Move to archive/)
  Analysis scripts:
    - analyze_*.py
    - debug_*.py
    - extract_*.py (except data extraction scripts)
    - parse_*.py
    - process_*.py
    - fetch_*.py
  
  Backup files:
    - app copy.py
    - *_old.py
    - *_copy.*
  
  Documentation (keep best, archive rest):
    - *_SUMMARY.md
    - *_CHECKLIST.md
    - *_FIXES.md
    - IMPLEMENTATION_*.md
    - REFACTORING_*.md
  
  Temporary files:
    - Otis 6 jan 2026.txt
    - *.bak
    - __pycache__/
    
PHASE 7: KEEP AT ROOT
  - app.py (updated with new imports)
  - requirements.txt
  - README.md
  - .gitignore
  - .streamlit/
  - .git/
  - LICENSE (if exists)

NEW DOCUMENTATION (to create)
  - docs/DATA_SOURCES.md
  - docs/ARCHITECTURE.md
  - docs/SETUP_GUIDE.md
  - docs/AI_FEATURES.md
  - docs/DATA_INTEGRITY.md
""")
    
    print("\nDIRECTORY STRUCTURE SUMMARY:")
    print("""
Before: Root directory with 50+ loose files
After:  Organized into logical modules with clear separation of concerns

Key improvements:
✓ Source code organized by function (calculations, ui, data, ai, utils)
✓ Data clearly separated (raw vs processed)
✓ Pages in dedicated directory following Streamlit convention
✓ Old/unused files archived rather than deleted
✓ Clear entry point (app.py at root)
✓ Documentation in dedicated docs/ folder
""")

if __name__ == "__main__":
    print_migration_plan()
    print("\n" + "=" * 80)
    print("USE THIS GUIDE TO ORGANIZE FILES MANUALLY OR WITH MOVE SCRIPTS")
    print("=" * 80)
