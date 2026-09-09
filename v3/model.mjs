export const DEFAULT = Object.freeze({mode:'population',geo:'K02000001',sex:'Females',min:25,max:39,band:'30 to 34',status:'not-couple'});
export const SEX_LABELS = {Persons:'All people',Males:'Men',Females:'Women'};
export const STATUS_LABELS = {'all':'All statuses','not-couple':'Not living in a couple','in-couple':'Living in a couple','never':'Never married / civil partnered','married':'Married','civil':'Civil partnered','divorced':'Divorced / dissolved partnership','widowed':'Widowed / surviving partner'};
export const sum = rows => rows.every(v=>typeof v==='number' && Number.isFinite(v)) ? rows.reduce((a,b)=>a+b,0) : null;
function ageCell(range,age) {
  let column=age+5,label='';
  while(column>0){column--;label=String.fromCharCode(65+column%26)+label;column=Math.floor(column/26);}
  return `${range.split('!')[0]}!${label}${range.split('!')[1].match(/\d+/)[0]}`;
}
export function bands(data,mode) {return [...new Set(data.relationships.filter(r=>r.mode===mode).map(r=>r.age))];}
export function validate(data,input) {
  const s={...DEFAULT,...input};
  if(!['population','living','marital'].includes(s.mode)) throw Error('Choose a supported dataset.');
  if(!Object.hasOwn(SEX_LABELS,s.sex)) throw Error('Choose a published sex category.');
  if(!Object.hasOwn(data.population,s.geo)) throw Error('Choose a supported geography.');
  if(!Number.isInteger(s.min)||!Number.isInteger(s.max)||s.min<18||s.max>90||s.min>s.max) throw Error('Enter whole ages from 18 to 90, with minimum no higher than maximum. 90 includes everyone aged 90 and over.');
  if(s.mode!=='population') {
    s.geo='K04000001';
    if(!bands(data,s.mode).includes(s.band)) throw Error('Choose a published age band.');
    const valid=s.mode==='living'?['all','not-couple','in-couple']:['all','never','married','civil','divorced','widowed'];
    if(!valid.includes(s.status)) throw Error('Choose a status from this dataset.');
  }
  return s;
}
export function matchesStatus(category,status) {
  if(status==='all') return true;
  if(status==='not-couple') return category.startsWith('Not living in a couple:');
  if(status==='in-couple') return category.startsWith('Living in a couple:');
  return category===({never:'Never married or civil partnered',married:'Married',civil:'Civil Partnered',divorced:'Divorced',widowed:'Widowed'}[status]);
}
export function calculate(data,input) {
  const state=validate(data,input);
  if(state.mode==='population') {
    const p=data.population[state.geo];
    const count=sum(p[state.sex].slice(state.min,state.max+1));
    const base=sum(p[state.sex].slice(18));
    return {state,count,base,share:count/base,allAdults:sum(p.Persons.slice(18)),
      label:`${SEX_LABELS[state.sex]} aged ${state.min}–${state.max===90?'90+':state.max}`,
      geography:p.name,reference:'Mid-2024',kind:'Population estimate',sourceId:'population',
      rows:p[state.sex].slice(state.min,state.max+1).map((count,i)=>({age:state.min+i===90?'90+':String(state.min+i),count,cell:ageCell(p.sourceRows[state.sex],state.min+i)})),
      warning:'These are residents in a demographic group. Relationship status, orientation, mutual interest and willingness to date are not measured.'};
  }
  const all=data.relationships.filter(r=>r.mode===state.mode&&r.sex===state.sex&&r.age===state.band);
  const rows=all.filter(r=>matchesStatus(r.category,state.status));
  if(!all.length||!rows.length) throw Error('No matching source cells are available.');
  const count=sum(rows.map(r=>r.count)),base=sum(all.map(r=>r.count));
  return {state,count,base,share:count!==null&&base>0?count/base:null,
    label:`${SEX_LABELS[state.sex]}, ${state.band.replace(' to ','–').replace(' and over','+')}`,
    geography:'England and Wales',reference:'2025',kind:'Survey estimate',sourceId:'relationships',rows,
    unreliable:rows.some(r=>r.cv==='d'),
    warning:state.mode==='living'?'Living arrangements describe whether someone lives with a partner. People living apart can still be in a relationship. This is not a count of available dates.':'Legal status does not establish whether someone has a partner or is dating. Married and civil partnered categories include separated people.'};
}
export function exportResult(data,result) {
 return {appVersion:data.version,exportedAt:new Date().toISOString(),selection:result.state,
   definition:result.label,geography:result.geography,referencePeriod:result.reference,
   estimate:result.count,denominator:result.base,share:result.share,
   denominatorDefinition:result.state.mode==='population'?'Selected sex, ages 18+, selected geography':'Selected sex and age band, all statuses in the same table',
   caveat:result.warning,unreliableSourceCell:result.unreliable??false,
   aggregation:'Sum of selected published cells; no independent probability multiplication. Source suppression is retained. No aggregate confidence interval is inferred.',
   source:data.sources.find(s=>s.id===result.sourceId),sourceRows:result.rows};
}
