import {sum} from './model.mjs';
export const DATING_DEFAULT={geo:'K02000001',sex:'Females',min:25,max:39,relationship:'notCouple',income:0,orientation:'any',bmi:'any',education:'any',ethnicity:'any',height:false,heightMin:150,heightMax:180,spread:7,encounters:100};
export const MARGINALS={
 orientation:{straight:.934,gay:.021,bi:.016},
 ethnicity:{White:.817,Asian:.093,Black:.04,Mixed:.029,Other:.021},
 level4:.338,
 sources:[
 {id:'orientation',title:'ONS Sexual orientation, UK 2024',url:'https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality/bulletins/sexualidentityuk/2024',reference:'2024',geography:'UK household population, ages 16+',tables:'Main points: straight 93.4%, gay/lesbian 2.1%, bisexual 1.6%; no redistribution of non-response'},
 {id:'ethnicity',title:'ONS Ethnic group, Census 2021',url:'https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/ethnicity/bulletins/ethnicgroupenglandandwales/census2021',reference:'2021',geography:'England and Wales, all ages',tables:'Five broad groups: White 81.7%, Asian 9.3%, Black 4.0%, Mixed 2.9%, Other 2.1%'},
 {id:'education',title:'ONS Education, Census 2021',url:'https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare/bulletins/educationenglandandwales/census2021',reference:'2021',geography:'England and Wales, ages 16+',tables:'Highest qualification Level 4 or above: 33.8%; includes qualifications other than degrees'}
 ]};
export function normalCDF(x){
 const z=Math.abs(x)/Math.SQRT2,t=1/(1+.3275911*z);
 const erf=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-.284496736)*t+.254829592)*t*Math.exp(-z*z);
 return (1+(x<0?-erf:erf))/2;
}
function includesAge(band,age){const values=band.match(/\d+/g).map(Number);return age>=values[0]&&(values.length===1||age<=values[1]);}
function relationshipRate(data,sex,age,kind){
 if(kind==='any')return {rate:1,refs:[]};
 if(kind==='marriedOrCouple'){
  const legal=relationshipRate(data,sex,age,'married');
  const living=data.relationships.filter(r=>r.sex===sex&&r.mode==='living'&&includesAge(r.age,age));
  const cohabiting=living.filter(r=>r.category.startsWith('Living in a couple: Cohabiting'));
  const total=sum(living.map(r=>r.count)),count=sum(cohabiting.map(r=>r.count));
  if(total===null||count===null||!total||!cohabiting.length)throw Error('Relationship source values unavailable.');
  const rate=legal.rate+count/total;
  if(rate>1+1e-6)throw Error('Inconsistent relationship source totals.');
  return {rate:Math.min(1,rate),refs:[...legal.refs,...living.map(r=>r.cell)],unreliable:legal.unreliable||cohabiting.some(r=>r.cv==='d')};
 }
 const living=kind.startsWith('notCouple')||kind==='couple';
 const all=data.relationships.filter(r=>r.sex===sex&&r.mode===(living?'living':'marital')&&includesAge(r.age,age));
 const selected=all.filter(r=>kind==='couple'?r.category.startsWith('Living in a couple:'):kind==='married'?['Married','Civil Partnered'].includes(r.category):living?r.category.startsWith('Not living in a couple:')&&(kind==='notCouple'||(kind==='notCoupleNever'?r.category.includes(': Never'):r.category.includes(': Previously'))):r.category===({never:'Never married or civil partnered',divorced:'Divorced',widowed:'Widowed'}[kind]));
 const total=sum(all.map(r=>r.count)),count=sum(selected.map(r=>r.count));
 if(!all.length||!selected.length||total===null||count===null||total<=0)throw Error(`ONS relationship data is unavailable for ${sex.toLowerCase()} aged ${age}. Widen or change the relationship requirement; missing values are not zero.`);
 return {rate:count/total,refs:all.map(r=>r.cell),unreliable:selected.some(r=>r.cv==='d')};
}
export function incomeRate(data,extra,sex,threshold){
 if(threshold===0)return {rate:1,refs:[]};
 const brackets=extra.income[sex];
 let count=0;const refs=[];
 for(const b of brackets){
  if(threshold<=b.low){count+=b.taxpayers;refs.push(b.cell);}
  else if(b.high!==null&&threshold<b.high){count+=b.taxpayers*(b.high-threshold)/(b.high-b.low);refs.push(b.cell);}
 }
 return {rate:count/sum(data.population.K02000001[sex].slice(18)),refs};
}
export function chanceAtLeastOne(p,n){if(p===0)return 0;if(p===1)return 1;return -Math.expm1(n*Math.log1p(-p));}
export const EDUCATION_LABELS={any:'Any qualification',level1plus:'GCSEs / Level 1 or higher',level2plus:'5+ GCSE passes / Level 2 or higher',level3plus:'A-levels / Level 3 or higher',level4:'Higher: HNC/HND, degree or postgraduate',apprenticeship:'Apprenticeship as highest qualification',none:'No formal qualifications',other:'Other / unclassified qualification'};
export function educationRate(extra,key){
 if(key==='any')return 1;
 const groups={level1plus:['level1','level2','level3','level4'],level2plus:['level2','level3','level4'],level3plus:['level3','level4'],level4:['level4'],apprenticeship:['apprenticeship'],none:['none'],other:['other']};
 if(!Object.hasOwn(groups,key))throw Error('Choose a supported qualification.');
 return sum(groups[key].map(k=>extra.education[k].count))/sum(Object.values(extra.education).map(r=>r.count));
}
export function jointRates(extra,sex,age,geo,education,ethnicity){
 const countries=geo==='W92000004'?['W92000004']:geo==='E92000001'||geo.startsWith('E12')?['E92000001']:['E92000001','W92000004'];
 const rows=extra.jointCensus.filter(r=>r.sex===sex&&age>=r.min&&age<=r.max&&countries.includes(r.country));
 const groups={any:['none','level1','level2','apprenticeship','level3','level4','other'],level1plus:['level1','level2','level3','level4'],level2plus:['level2','level3','level4'],level3plus:['level3','level4'],level4:['level4'],none:['none'],apprenticeship:['apprenticeship'],other:['other']};
 const qualified=rows.filter(r=>groups[education].includes(r.education));
 const selected=qualified.filter(r=>ethnicity==='any'||r.ethnicity===ethnicity);
 const total=sum(rows.map(r=>r.count)),q=sum(qualified.map(r=>r.count)),joint=sum(selected.map(r=>r.count));
 if(!rows.length||total===null||q===null||joint===null||total<=0)throw Error('Joint Census data unavailable.');
 return {qualification:q/total,ethnicity:q?joint/q:0,joint:joint/total,total,qualified:q,selected:joint,countries,band:[rows[0].min,rows[0].max],refs:selected.map(r=>r.ref)};
}
export function orientationRate(extra,sex,age,key){
 if(key==='any')return {rate:1,refs:[],quality:[]};
 const band=extra.orientationByAgeSex[sex].find(r=>age>=r.min&&age<=r.max);
 const keys=key==='straightBi'?['straight','bi']:key==='gayBi'?['gay','bi']:[key];
 const values=keys.map(k=>band?.categories[k]);
 if(values.some(v=>!v||v.rate===null))throw Error('ONS orientation data unavailable for this age and sex.');
 return {rate:sum(values.map(v=>v.rate)),refs:values.map(v=>v.cell),quality:values,band:[band.min,band.max]};
}
export function datingSources(data,extra){return [...data.sources,...extra.sources,extra.orientationSource,extra.jointSource,{...extra.jointSource,id:'education',title:'Qualification within the joint Census dataset'}];}
export function calculateDating(data,extra,input){
 const s={...DATING_DEFAULT,...input};
 if(!Object.hasOwn(data.population,s.geo)||!['Males','Females','Persons'].includes(s.sex))throw Error('Choose a supported location and target group.');
 if(!Number.isInteger(s.min)||!Number.isInteger(s.max)||s.min<18||s.max>90||s.min>s.max)throw Error('Use whole ages 18–90, with From no greater than To. 90 means 90+.');
 if(!['any','marriedOrCouple','married','couple','notCouple','notCoupleNever','notCouplePrevious','never','divorced','widowed'].includes(s.relationship))throw Error('Choose a supported relationship requirement.');
 if(![0,20000,30000,40000,50000,70000,75000,100000,150000,200000,300000,500000,1000000].includes(s.income))throw Error('Choose a supported income threshold.');
 if(!['any','straight','gay','bi','straightBi','gayBi'].includes(s.orientation))throw Error('Choose a supported orientation requirement.');
 if(!['any','0','1','2','3'].includes(s.bmi)||!Object.hasOwn(EDUCATION_LABELS,s.education)||!['any',...Object.keys(MARGINALS.ethnicity)].includes(s.ethnicity))throw Error('Choose a supported preference.');
 if(typeof s.height!=='boolean'||!Number.isFinite(s.heightMin)||!Number.isFinite(s.heightMax)||s.heightMin<100||s.heightMax>230||s.heightMin>=s.heightMax||!Number.isFinite(s.spread)||s.spread<3||s.spread>15)throw Error('Height must have a lower bound below its upper bound (100–230 cm); spread must be 3–15 cm.');
 if(!Number.isInteger(s.encounters)||s.encounters<1||s.encounters>10000)throw Error('Choose 1–10,000 hypothetical encounters.');
 const base=sum(data.population[s.geo][s.sex].slice(18));
 const sexes=s.sex==='Persons'?['Males','Females']:[s.sex];
 const stages=[{label:'Adults in your target group',count:base,source:'ONS MYE2',type:'Sourced count'},
  ...['Age range','Relationship requirement','Income','Orientation identity','Height','BMI category','Qualification','Ethnicity'].map(label=>({label,count:0,type:'Modelled filter'}))];
 const rows=[];let unreliable=false;
 for(const sex of sexes){
  const inc=incomeRate(data,extra,sex,s.income);
  for(let age=s.min;age<=s.max;age++){
   let n=data.population[s.geo][sex][age];
   const original=n;stages[1].count+=n;
   const relation=relationshipRate(data,sex,age,s.relationship);unreliable ||= relation.unreliable;
   const health=extra.health[sex].find(r=>age>=r.min&&age<=r.max);
   const orientation=orientationRate(extra,sex,age,s.orientation);
   const joint=jointRates(extra,sex,age,s.geo,s.education,s.ethnicity);
   const height=s.height?Math.max(0,normalCDF((s.heightMax-health.mean)/s.spread)-normalCDF((s.heightMin-health.mean)/s.spread)):1;
   const bmi=s.bmi==='any'?1:health.bmi[Number(s.bmi)];
   if(bmi===null)throw Error(`NHS BMI data is unavailable for ${sex.toLowerCase()} aged ${age}. Choose another category or remove the BMI filter.`);
   const rates=[relation.rate,inc.rate,orientation.rate,height,bmi,joint.qualification,joint.ethnicity];
   rates.forEach((r,i)=>{n*=r;stages[i+2].count+=n;});
   rows.push({sex,age:age===90?'90+':age,population:original,estimated:n,rates,
    jointCensus:joint,orientationCells:orientation.refs,orientationQuality:orientation.quality,
    populationRow:data.population[s.geo].sourceRows[sex],relationshipCells:relation.refs,incomeCells:inc.refs,
    heightMean:s.height?health.mean:null,heightCell:s.height?health.heightCell:null,bmiCell:s.bmi==='any'?null:health.bmiCells[Number(s.bmi)]});
  }
 }
 const count=stages.at(-1).count,p=count/base;
 const notes=['A modelled population meeting your filters, not a measured joint count. The denominator is all adults of the selected sex in the selected location, including partnered adults.'];
 const modelled=s.relationship!=='any'||s.income>0||s.orientation!=='any'||s.height||s.bmi!=='any'||s.education!=='any'||s.ethnicity!=='any';
 if(modelled)notes.push('The model multiplies filter rates within each age/sex group, then adds the groups. Remaining correlations are unknown. No statistical confidence interval is claimed for the combined result.');
 if(s.relationship!=='any')notes.push('2025 England-and-Wales relationship rates are applied to each single age in its source band and to the mid-2024 population. Outside England and Wales, this is a geographic extrapolation. Not living in a couple can include people with a partner living elsewhere.');
 if(s.income>0)notes.push('HMRC 2023/24 UK taxpayer counts divided by UK adult sex populations approximate all-adult income shares. Taxpayers under 18 and non-taxable income are not separately resolved. Rates are not age- or region-specific; £75k uses linear interpolation inside £70k–£100k. Income includes taxable pensions and other sources, not just salary.');
 if(s.height)notes.push(`Height is an opt-in normal model around NHS age/sex mean heights. The ${s.spread} cm standard deviation is YOUR MODELLING ASSUMPTION, not an NHS estimate. Extreme-height results are particularly sensitive to it.`);
 if(s.height||s.bmi!=='any')notes.push('NHS data covers England, ages 16+. The 16–24 band is used for ages 18–24; other geographies use an explicit England proxy. BMI measures weight relative to height, not appearance.');
 if(s.orientation!=='any')notes.push('Orientation uses published UK household shares by age band and sex, Table 6b (2024). Ages 18–24 use the 16–24 band. Other identities and nonresponse are not redistributed; per-cell confidence intervals and reliability codes accompany the exported rows.');
 if(s.education!=='any')notes.push('Qualifications use joint Census 2021 country, age-band and sex counts. Minimum levels include higher numbered levels; apprenticeship and unknown-level qualifications are separate because their level cannot be inferred. HNC/HND, degrees and postgraduate qualifications share one published category. Ethnicity is then applied conditional on the chosen qualification, using the same joint table. Rates are not conditioned on income.');
 if(s.ethnicity!=='any')notes.push('Ethnicity uses joint Census 2021 age-band, sex and qualification counts. England/Wales selections use their country; English regions use England. UK, Scotland and Northern Ireland use England-and-Wales rates as a geographic proxy, not current local adult distributions.');
 if(s.income>0&&(s.education!=='any'||s.ethnicity!=='any'))notes.push('Important remaining gap: income is not jointly measured with qualification or ethnicity here. This combination remains approximate; it is neither a verified count nor a lower bound.');
 notes.push('Published age-band rates are constant within each band. Boundary changes reflect source grouping, not a sudden real-world change at a birthday. No speculative smoothing is applied.');
 if(rows.some(r=>r.orientationQuality.some(v=>v.cv==='d')))notes.push('Selected orientation cells include reliability category d (unreliable).');
 if(unreliable)notes.push('Selected relationship cells include ONS reliability category d (unreliable). Inspect source data before interpreting the estimate.');
 return {state:s,count,base,p,oneIn:p>0?1/p:null,chance:chanceAtLeastOne(p,s.encounters),stages,rows,notes,modelled,
  sources:datingSources(data,extra),version:'3.3.0'};
}
