from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import openpyxl

NS={'t':'urn:oasis:names:tc:opendocument:xmlns:table:1.0','o':'urn:oasis:names:tc:opendocument:xmlns:office:1.0','text':'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
def ods_tables(path):
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read('content.xml'))
    result={}
    for table in root.findall('.//t:table',NS):
        rows=[]
        for row in table.findall('t:table-row',NS):
            vals=[]
            for cell in row:
                value=cell.get('{'+NS['o']+'}value')
                value=float(value) if value is not None else ''.join(cell.itertext()).strip()
                repeat=min(int(cell.get('{'+NS['t']+'}number-columns-repeated','1')),100)
                vals.extend([value]*repeat)
            if any(v!='' for v in vals):rows.append(vals)
            else:rows.append([])
        result[table.get('{'+NS['t']+'}name')]=rows
    return result

if __name__=='__main__':
    base=Path(__file__).resolve().parents[1]
    tables=ods_tables(base/'sources/hmrc-2023-24.ods')
    print('HMRC SHEETS',list(tables))
    for name,rows in tables.items():
        if '3.3' in name:
            for n,row in enumerate(rows,1):
                if row:print(name,n,row[:25])
    book=openpyxl.load_workbook(base/'sources/hse-2024.xlsx',read_only=True,data_only=True)
    for name in ['Table 1','Table 3']:
        for n,row in enumerate(book[name].values,1):
            if n<85 and any(v is not None for v in row):print(name,n,row[:13])
