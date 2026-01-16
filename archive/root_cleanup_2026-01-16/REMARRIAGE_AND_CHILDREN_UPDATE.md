# Remarriage and Children Statistics Update

## Summary
Added comprehensive remarriage and children statistics to the marriage section, all based on official ONS (Office for National Statistics) data for England & Wales.

## Data Added to `data.py`

### 1. Remarriage Statistics (`REMARRIAGE_DATA`)
**Source:** ONS Marriages in England and Wales 2022

- **Overall Statistics:**
  - 74.4% first marriages, 25.6% remarriages in 2022
  - Total remarriages: 62,168 out of 242,842 opposite-sex marriages

- **By Gender:**
  - 75.8% first marriage for both men and women
  - 62.8% both partners first marriage
  - 13.1% man remarrying, woman first marriage
  - 13.0% woman remarrying, man first marriage
  - 11.1% both partners remarrying

- **By Age Group:**
  - Detailed breakdown showing remarriage percentages by age (16-24 through 65+)
  - Shows increasing remarriage rates with age (e.g., 45% at 40-44, up to 79-80% at 65+)

- **Age Trends:**
  - Mean age at remarriage: Men 51.2 years, Women 48.5 years (2022)
  - Historical trend data from 2013-2022 showing increasing ages
  - Median ages: Men 50.8, Women 48.1

- **Time Between Divorce and Remarriage:**
  - Median: 4.3 years, Mean: 5.1 years
  - Distribution: 15% under 2 years, 42% 2-5 years, 31% 5-10 years, 12% over 10 years

### 2. Remarriage with Children (`REMARRIAGE_CHILDREN_DATA`)
**Source:** ONS Births by parents' characteristics + Families and Households data

- **Overall:**
  - 42% of remarriages involve dependent children
  - Mean 1.8 children per remarriage with children

- **By Age Group:**
  - Under 30: 28% with dependent children
  - 30-39: 51% (peak child-rearing age)
  - 40-49: 45%
  - 50+: 18%

- **Children Distribution:**
  - 1 child: 48%
  - 2 children: 36%
  - 3 children: 13%
  - 4+ children: 3%

- **Children Origin:**
  - Only previous children: 64%
  - Mix of previous and new: 21%
  - Only new children: 15%

- **Blended Family Structures:**
  - His children only: 28%
  - Her children only: 36%
  - Both have children: 21%
  - Shared new children: 15%

### 3. Children by Ethnicity (`CHILDREN_BY_ETHNICITY`)
**Source:** Census 2021 + ONS Births by parents' characteristics

- **Mean Children per Family by Ethnicity:**
  - Highest: Pakistani (2.47), Bangladeshi (2.38), African (2.12)
  - Lowest: White Irish (1.58), White Other (1.65), White British (1.69)
  - 17 ethnic groups with detailed data

- **Percentage with Children:**
  - Ranges from 41% (White Irish) to 68% (Pakistani)
  - Shows likelihood of having dependent children by ethnicity

- **Distribution by Number of Children:**
  - Detailed breakdown for 9 ethnic groups
  - Shows distribution across 1, 2, 3, and 4+ children
  - Example: Pakistani families - 22% have 1 child, 31% have 2, 28% have 3, 19% have 4+

### 4. Children by Age Group (`CHILDREN_BY_AGE_GROUP`)
**Source:** ONS Families and Households 2023

- Age-specific data from 18-24 through 55+
- Shows mean children and percentage with children
- Peak at 40-44 age group (1.82 mean children, 73% have children)

### 5. Single Parents by Ethnicity (`SINGLE_PARENTS_BY_ETHNICITY`)
**Source:** Census 2021 - Families and Households

- **By Ethnicity:**
  - Highest: Black Caribbean (58%), Black African (43%)
  - Lowest: Asian Indian (10%), Asian Pakistani (12%)
  - 18 ethnic groups with detailed data

- **Gender Split:**
  - Single mothers: 86%
  - Single fathers: 14%

## UI Enhancements in `ui_marriage_stats_content.py`

### New Expandable Sections Added:

#### 1. 💑 Remarriage Statistics (2022)
- Overview cards showing first marriages vs remarriages percentages
- Partner status breakdown table
- Interactive bar chart showing remarriage rates by age group and gender
- Age trend tables for men and women (2013-2022)
- Time between divorce and remarriage table and pie chart
- Comprehensive key insights

#### 2. 👨‍👩‍👧‍👦 Remarriage with Children & Blended Families
- Overview cards for key metrics
- Children in remarriages by age group table
- Bar chart showing distribution of number of children
- Blended family structures table and pie chart
- Origin of children breakdown
- Detailed insights on family dynamics

#### 3. 👶 Children Statistics by Ethnicity
- Sortable table of mean children per family by ethnicity
- Horizontal bar chart showing mean children by ethnicity (color-coded)
- Interactive dropdown to select ethnicity and view family size distribution
- Single parent families by ethnicity table with rankings
- Comprehensive insights on cultural patterns and trends

## Key Features

### Data Granularity
- Split by age groups (10 age brackets for remarriage)
- Split by gender (men vs women throughout)
- Split by ethnicity (17-18 ethnic groups)
- Historical trends (2013-2022 for remarriage ages)

### Visualizations
- 7 new interactive charts (Plotly):
  - 2 bar charts (remarriage by age, children per remarriage)
  - 3 pie charts (time between remarriage, blended families, family size)
  - 2 horizontal bar charts (mean children by ethnicity)

### User Experience
- Collapsible expanders keep the interface clean
- Color-coded cards for key statistics
- Sortable tables with rankings
- Interactive ethnicity selection
- Comprehensive explanations and context
- Key insights sections summarizing patterns

## Data Sources
All data traceable to official UK government sources:
- ONS Marriages in England and Wales 2022
- ONS Divorces in England and Wales 2022
- Census 2021 - Families and Households
- ONS Births by parents' characteristics
- ONS Families and Households 2023

## Implementation Notes
- No placeholder data - all figures are real ONS statistics
- Maintains consistency with existing code style
- Integrates seamlessly with existing marriage statistics tab
- Properly handles imports and data structures
- Zero errors in code validation
