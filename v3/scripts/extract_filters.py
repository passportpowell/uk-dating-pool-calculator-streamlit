"""Extract source-backed marginal inputs; model assumptions live in dating-model.mjs."""
from pathlib import Path
import json,hashlib
import openpyxl
from inspect_extra import ods_tables
ROOT=Path(__file__).resolve().parents[1]
book=openpyxl.load_workbook(ROOT/'sources/hse-2024.xlsx',read_only=True,data_only=True)
health={}
for sex,start,bmi_start in [('Males',7,7),('Females',51,99)]:
    records=[]
    for i,(low,high) in enumerate([(18,24),(25,34),(35,44),(45,54),(55,64),(65,74),(75,90)]):
        row=start+i*3
        bmi_row=bmi_start+i*9
        mean=book['Table 1'].cell(row,31).value
        raw=[book['Table 3'].cell(bmi_row+j,31).value for j in range(4)]
        # Preserve suppression instead of fabricating numeric values.
        bmi=[v/100 if isinstance(v,(int,float)) else None for v in raw]
        assert isinstance(mean,(int,float))
        if all(v is not None for v in bmi):assert abs(sum(bmi)-1)<0.001
        records.append({'min':low,'max':high,'mean':mean,'heightCell':f'Table 1!AE{row}',
            'bmi':bmi,'bmiCells':[f'Table 3!AE{bmi_row+j}' for j in range(4)]})
    health[sex]=records
book.close()
rows=ods_tables(ROOT/'sources/hmrc-2023-24.ods')['Table_3_3_before_tax']
income={}
for sex,label in [('Males','Male'),('Females','Female')]:
    selected=[(i,r) for i,r in enumerate(rows,1) if len(r)>2 and r[1]==label and isinstance(r[0],(int,float))]
    income[sex]=[{'low':int(r[0]),'high':int(selected[k+1][1][0]) if k+1<len(selected) else None,
        'taxpayers':int(r[2]*1000),'cell':f'Table_3_3_before_tax!C{i}'} for k,(i,r) in enumerate(selected)]
assert income['Males'][-1]['taxpayers']==22000
assert income['Females'][-1]['taxpayers']==4000
def source(id,title,file,url,reference,geography,tables):
    return {'id':id,'title':title,'file':'sources/'+file,'url':url,'reference':reference,'geography':geography,'tables':tables,
        'sha256':hashlib.sha256((ROOT/'sources'/file).read_bytes()).hexdigest()}
out={'checked':'2026-09-09','health':health,'income':income,'sources':[
    source('health','NHS Health Survey for England 2024','hse-2024.xlsx','https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england/2024/health-survey-for-england-2024-data-tables','2024','England, ages 16+','Tables 1 and 3; 2024 column AE'),
    source('income','HMRC Personal Incomes Statistics','hmrc-2023-24.ods','https://www.gov.uk/government/statistics/personal-incomes-statistics-for-the-tax-year-2023-to-2024','2023/24','UK taxpayers','Table_3_3_before_tax; counts in thousands, converted to people')
]}
book=openpyxl.load_workbook(ROOT/'sources/qualifications-2021.xlsx',read_only=True,data_only=True)
sheet=book['Figure 2']
assert sheet['C8'].value=='2021 (number)'
keys=['none','level1','level2','apprenticeship','level3','level4','other']
out['education']={key:{'count':sheet.cell(i,3).value,'cell':f'Figure 2!C{i}'} for key,i in zip(keys,range(9,16))}
assert out['education']['level4']['count']==16413231
out['educationSource']=source('education','ONS Highest qualification, Census 2021','qualifications-2021.xlsx','https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare/bulletins/educationenglandandwales/census2021','2021','England and Wales, ages 16+','Figure 2!C9:C15; counts for seven highest-qualification categories')
book.close()
(ROOT/'data/filters.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Extracted HSE age/sex means and BMI; HMRC original income bands. No assumed spreads in source data.')

# Refresh subgroup inputs after rebuilding the base filters file.
import runpy
runpy.run_path(str(ROOT/"scripts/extract_subgroups.py"))
