from pathlib import Path
import json,hashlib,openpyxl
R=Path(__file__).resolve().parents[1]
p=R/'data/filters.json'; out=json.loads(p.read_text())
raw=json.loads((R/'sources/joint-census-api.json').read_text())
assert raw['total_observations']==len(raw['observations'])==2112 and not raw['blocked_areas']
bands={'4':(16,19),'5':(20,24),'6':(25,34),'7':(35,49),'8':(50,64),'9':(65,74),'10':(75,84),'11':(85,90)}
quals={'0':'none','1':'level1','2':'level2','3':'apprenticeship','4':'level3','5':'level4','6':'other'}
eth={'1':'Asian','2':'Black','3':'Mixed','4':'White','5':'Other'}
records=[]
for i,r in enumerate(raw['observations']):
 d={v['dimension_id']:v['option_id'] for v in r['dimensions']}
 if d['resident_age_11a'] not in bands:continue
 if d['highest_qualification']=='-8' or d['ethnic_group_tb_6a']=='-8':
  assert r['observation']==0;continue
 low,high=bands[d['resident_age_11a']]
 assert isinstance(r['observation'],int) and r['observation']>=0
 records.append(dict(country=d['ctry'],sex={'1':'Females','2':'Males'}[d['sex']],min=low,max=high,education=quals[d['highest_qualification']],ethnicity=eth[d['ethnic_group_tb_6a']],count=r['observation'],ref=f'observations[{i}]'))
assert len(records)==1120
out['jointCensus']=records
url='https://api.beta.ons.gov.uk/v1/population-types/UR/census-observations?area-type=ctry&dimensions=highest_qualification,sex,resident_age_11a,ethnic_group_tb_6a'
out['jointSource']=dict(id='ethnicity',title='ONS Census 2021: qualification, ethnicity, age and sex',reference='2021',geography='England and Wales; country, sex and age-band specific',url='https://www.ons.gov.uk/datasets/create',apiURL=url,file='sources/joint-census-api.json',tables='Census observations: ctry × highest_qualification × sex × resident_age_11a × ethnic_group_tb_6a; 2,112 observations',sha256=hashlib.sha256((R/'sources/joint-census-api.json').read_bytes()).hexdigest())
w=openpyxl.load_workbook(R/'sources/orientation-2024.xlsx',data_only=True)['6b'];orientation={}
for sex,start in [('Males',113),('Females',118)]:
 records=[]
 for low,high,col in [(16,24,4),(25,34,7),(35,49,10),(50,64,13),(65,90,16)]:
  cats={}
  for k,offset in [('straight',0),('gay',1),('bi',2)]:
   row=start+offset;cell=w.cell(row,col);assert w.cell(row,3).value==2024
   cats[k]=dict(rate=cell.value/100 if isinstance(cell.value,(int,float)) else None,cell='6b!'+cell.coordinate,cv=w.cell(row,col+1).value,ciPercentagePoints=w.cell(row,col+2).value)
  records.append(dict(min=low,max=high,categories=cats))
 orientation[sex]=records
out['orientationByAgeSex']=orientation
out['orientationSource']=dict(id='orientation',title='ONS Sexual orientation by age and sex',reference='2024',geography='UK household population, ages 16+',url='https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality/bulletins/sexualidentityuk/2024#sexual-orientation-by-age-and-sex',file='sources/orientation-2024.xlsx',tables='Table 6b, rows 113–115 (men), 118–120 (women); D/G/J/M/P percentages, adjacent CV and CI columns',sha256=hashlib.sha256((R/'sources/orientation-2024.xlsx').read_bytes()).hexdigest())
p.write_text(json.dumps(out,indent=2))
print('Extracted 1,120 adult joint Census cells and 30 orientation percentages')
