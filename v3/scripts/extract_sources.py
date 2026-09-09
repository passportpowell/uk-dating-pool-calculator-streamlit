"""Rebuild browser data from retained, unmodified ONS workbooks. Requires openpyxl."""
from pathlib import Path
import hashlib
import json
import re
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
POP_URL = 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland/mid2024'
REL_URL = 'https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesbymaritalstatusandlivingarrangements'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    population = {}
    path = ROOT / 'sources/mye24tablesuk.xlsx'
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for sex in ['Persons', 'Males', 'Females']:
        sheet = f'MYE2 - {sex}'
        rows = list(book[sheet].values)
        assert rows[7][4] == '0' and rows[7][94] == '90+'
        for row_number, row in enumerate(rows[8:], 9):
            if row[2] not in ['Country', 'Region']:
                continue
            code, name, kind = row[:3]
            name = name.title().replace(' And ', ' and ').replace(' The ', ' the ')
            if name == 'East':
                name = 'East of England'
            record = population.setdefault(code, {'name': name, 'kind': kind})
            values = list(row[4:95])
            assert all(isinstance(v, int) and v >= 0 for v in values)
            assert sum(values) == row[3], (name, sex)
            record[sex] = values
            record.setdefault('sourceRows', {})[sex] = f'{sheet}!E{row_number}:CQ{row_number}'
    for record in population.values():
        assert all(p == m + f for p, m, f in zip(record['Persons'], record['Males'], record['Females']))
    assert sum(population['K02000001']['Persons']) == 69281437
    assert sum(population['K02000001']['Persons'][18:]) == 55022253
    book.close()

    relation_path = ROOT / 'sources/living-arrangements.xlsx'
    book = openpyxl.load_workbook(relation_path, read_only=True, data_only=True)
    assert '2025' in book['Cover_sheet']['A1'].value
    relationships = []
    for mode, sheets in [('marital', ['1', '2', '3']), ('living', ['4', '5', '6'])]:
        for sex, sheet in zip(['Persons', 'Males', 'Females'], sheets):
            rows = list(book[sheet].values)
            assert rows[9][2] == '2025 Estimate'
            for n, row in enumerate(rows[10:], 11):
                if not row[0] or not row[1]:
                    continue
                age = str(row[1]).strip()
                if age in ['All Ages', '0 to 15', '0 to 17', '16 to 19', '16 to 29', '20 to 24']:
                    continue
                category = re.sub(r'\s*\[note \d+\]', '', row[0]).strip()
                assert isinstance(row[2], (int, float)) or row[2] in ['[u]', '[x]', '[z]', '[w]'], (sheet, n, row[:5])
                relationships.append({'mode': mode, 'sex': sex, 'age': age, 'category': category,
                    'count': row[2], 'cv': row[3], 'ci': row[4], 'cell': f'{sheet}!C{n}',
                    'ciCell': f'{sheet}!E{n}'})
    assert len(relationships) > 300
    book.close()
    result = {'version': '3.0.0', 'checked': '2026-09-09', 'population': population,
        'relationships': relationships, 'sources': [
            {'id': 'population', 'title': 'Population by single year of age and sex', 'publisher': 'ONS',
             'reference': 'Mid-2024', 'released': '2025-09-26', 'geography': 'United Kingdom, countries and English regions',
             'url': POP_URL, 'file': 'sources/mye24tablesuk.xlsx', 'sha256': digest(path),
             'tables': 'MYE2 - Persons / Males / Females',
             'note': 'Pinned mid-2024 edition. Single ages 0–89 and the complete 90+ group. Later revisions are not automatically applied.'},
            {'id': 'relationships', 'title': 'Marital status and living arrangements', 'publisher': 'ONS',
             'reference': '2025', 'released': '2026-07-31', 'geography': 'England and Wales',
             'url': REL_URL, 'file': 'sources/living-arrangements.xlsx', 'sha256': digest(relation_path),
             'tables': '1–3 (legal status); 4–6 (living arrangements), 2025 columns C–E',
             'note': 'LFS survey estimates. Published age bands are retained. Confidence intervals and robustness codes are preserved per source cell.'}
        ]}
    (ROOT / 'data/evidence.json').write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Validated {len(population)} geographies; {len(relationships)} relationship cells. UK adults: 55,022,253.')

if __name__ == '__main__':
    main()
