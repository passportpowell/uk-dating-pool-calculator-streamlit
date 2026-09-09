import {usage} from './provenance.mjs';
import {DATING_DEFAULT,calculateDating,EDUCATION_LABELS} from './dating-model.mjs';
const $=id=>document.getElementById(id),esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number=v=>new Intl.NumberFormat('en-GB',{maximumSignificantDigits:3}).format(v);
const people=v=>v>0&&v<1?'<1':new Intl.NumberFormat('en-GB',{maximumSignificantDigits:v<100?1:2,maximumFractionDigits:0}).format(v);
const pct=p=>p>.9999?'>99.99%':p>0&&p<.000001?'<0.0001%':`${(p*100).toLocaleString('en-GB',{maximumSignificantDigits:2})}%`;
const opts=(v,l)=>`<option value="${esc(v)}">${esc(l)}</option>`;
let data,extra,result,saved=[];
const numeric=['min','max','income','heightMin','heightMax','spread','encounters'];
function read(){return Object.fromEntries(Object.keys(DATING_DEFAULT).map(key=>[key,key==='height'?true:numeric.includes(key)?Number($(key).value===''?NaN:$(key).value):$(key).value]));}
function fill(s){for(const [key,value] of Object.entries({...DATING_DEFAULT,...s}))if($(key)){if(key==='height')$(key).checked=value;else if(key==='relationship'&&!Array.from($(key).options).some(o=>o.value===value)){$(key).value='any';info('This saved relationship option is no longer offered. Choose a relationship status.');}else $(key).value=value;}syncHeightUnits();}
function syncHeightUnits(){
 const feet=$('height-unit').value==='ft';$('height-cm').hidden=feet;$('height-ft').hidden=!feet;
 for(const [prefix,id] of [['min','heightMin'],['max','heightMax']]){
  const total=Number($(id).value)/2.54;let ft=Math.floor(total/12),inch=Math.round((total-ft*12)*100)/100;if(inch>=12){ft++;inch=0;}
  $(prefix+'-feet').value=ft;$(prefix+'-inches').value=inch;
  $(id).disabled=feet;$(prefix+'-feet').disabled=!feet;$(prefix+'-inches').disabled=!feet;
 }
}
function readImperial(){for(const [prefix,id] of [['min','heightMin'],['max','heightMax']]){
 const f=$(prefix+'-feet'),i=$(prefix+'-inches');const ft=Number(f.value),inch=Number(i.value);
 $(id).value=f.value!==''&&i.value!==''&&Number.isInteger(ft)&&inch>=0&&inch<12?String(Math.round((ft*12+inch)*2.54*10000)/10000):'';
}}
function imperial(cm){const inch=Math.round(cm/2.54);return `${Math.floor(inch/12)}′ ${inch%12}″`;}
function info(t){$('status-message').textContent=t;}
function renderSaved(){
 $('saved').innerHTML=saved.length?saved.map((s,i)=>{const r=calculateDating(data,extra,s);return `<article class="compare-card"><header><strong>Scenario ${i+1}</strong><button class="text-button" data-remove="${i}">Remove ×</button></header><div class="compare-value">${pct(r.p)} · ≈ ${people(r.count)} people</div><p>${esc(data.population[s.geo].name)} · ${esc(s.sex)} · ages ${s.min}–${s.max===90?'90+':s.max}</p><p>${esc(s.relationship)} · income £${s.income.toLocaleString('en-GB')}+ · height ${s.height?`${s.heightMin}–${s.heightMax} cm (assumed spread ${s.spread})`:'any'} · BMI ${esc(s.bmi)} · orientation ${esc(s.orientation)} · education ${esc(EDUCATION_LABELS[s.education])} · ethnicity ${esc(s.ethnicity)}</p><p>Estimated share of the selected adult population. Load to inspect the source breakdown.</p><button class="text-button" data-load="${i}">Load requirements ↗</button></article>`;}).join(''):'<p class="empty">Save your current requirements with “Compare ＋”, then try another set.</p>';
}
function update(){
 const s=read();
 $('education-help').textContent=s.education==='level4'?'HNC/HND, degrees and postgraduate qualifications are grouped in the source.':['apprenticeship','none','other'].includes(s.education)?'Matches this highest-qualification category only.':'Includes higher numbered levels; apprenticeship levels are not specified in this source.';
 $('height-imperial').textContent=$('height-unit').value==='ft'?`${s.heightMin}–${s.heightMax} cm`:`${imperial(s.heightMin)} to ${imperial(s.heightMax)}`;
 try{
  result=calculateDating(data,extra,s);$('input-error').hidden=true;
  $('headline').textContent=pct(result.p);$('pool-count').textContent='≈ '+people(result.count);
  const selected=['sex','geo','relationship','income','orientation','bmi','education','ethnicity'].filter(id=>!['any','0'].includes(String(s[id]))).map(id=>$(id).selectedOptions[0].textContent);
  selected.push(`${s.min}–${s.max===90?'90+':s.max} years`);if(s.height)selected.push(`${s.heightMin}–${s.heightMax} cm`);
  $('selected-filters').innerHTML=selected.map(label=>`<span>${esc(label)}</span>`).join('');
  $('sensitivity').textContent=s.height?`Height sensitivity: changing only the assumed spread from ${Math.max(3,s.spread-2)} to ${Math.min(15,s.spread+2)} cm changes this estimate from approximately ${people(calculateDating(data,extra,{...s,spread:Math.max(3,s.spread-2)}).count)} to ${people(calculateDating(data,extra,{...s,spread:Math.min(15,s.spread+2)}).count)} people. This is a model sensitivity check, not a confidence interval.`:'Height filter is off. The spread is only used when it is enabled.';
  $('one-in').textContent=result.oneIn===null?'None estimated':'1 in '+people(result.oneIn);
  $('result-location').textContent=data.population[s.geo].name;
  $('result-description').textContent=`${s.sex==='Males'?'Men':s.sex==='Females'?'Women':'Men and women'}, aged ${s.min}–${s.max===90?'90+':s.max}, meeting the selected requirements.`;
  $('denominator').textContent=`Out of ${result.base.toLocaleString('en-GB')} ${s.sex==='Males'?'men':s.sex==='Females'?'women':'people'} aged 18+ in ${data.population[s.geo].name}.`;
  $('chance').textContent=pct(result.chance);
  const stageActive=[true,true,s.relationship!=='any',s.income>0,s.orientation!=='any',s.height,s.bmi!=='any',s.education!=='any',s.ethnicity!=='any'];
  $('funnel').innerHTML=result.stages.filter((_,i)=>stageActive[i]).map((r,i,visible)=>`<div class="funnel-row"><span>${esc(r.label)}<small>${i<2?'ONS population count':'Modelled remaining'}</small></span><div class="track"><div class="fill" style="width:${100*r.count/result.base}%"></div></div><strong>${number(r.count)}<small class="pool-percentage">${(100*r.count/result.base).toLocaleString('en-GB',{maximumSignificantDigits:3})}%</small><small class="step-drop">${i===0?'Starting pool':visible[i-1].count>0?`${(100*Math.max(0,1-r.count/visible[i-1].count)).toLocaleString('en-GB',{maximumSignificantDigits:3})}% drop`:'No pool remaining'}</small></strong></div>`).join('');
  const sourceIds=['population','population','relationships','income','orientation','health','health','education','ethnicity'];
  const fields=[null,null,'relationship','income','orientation',null,'bmi','education','ethnicity'];
  const plain=[
   'We start with all adults in your chosen group and location. This is the starting pool used for every percentage.',
   'We keep only people within your chosen ages, including both the youngest and oldest age you entered.',
   s.relationship==='notCouple'?'We use people who are not living with a partner as our best available estimate for single people. Some may still be dating someone who lives elsewhere.':s.relationship==='divorced'||s.relationship==='widowed'?'This counts legal marriage status. Someone who is divorced or widowed may have a new partner.':'We use the published marriage and living-arrangement figures for people of the same sex and age group. These figures come from England and Wales.',
   'We use tax records to estimate how many people earn at least this amount before tax. This includes pensions and other taxable income, not just wages. The figures are not specific to your chosen ages.',
   'We use the share of men or women in the same age group who reported your chosen sexual orientation in a UK survey.',
   'We estimate how many people fall between your chosen heights using measured average heights for their age and sex. The source does not directly count everyone in your exact height range.',
   'We use measured height and weight from an England health survey. BMI is a weight-to-height measure; it does not tell us what someone looks like.',
   'We use Census figures for people of the same sex and age group. Higher qualification levels count towards a minimum requirement. Degrees and postgraduate qualifications are grouped together in the source.',
   'We use Census figures that count ethnicity and qualifications together for the same age group and sex. This avoids treating those two preferences as unrelated.'
  ];
  $('filter-evidence').innerHTML='<p>Here is how each preference changes your result. Each step starts with the people left after the step above it.</p>'+result.stages.map((stage,i)=>{const source=result.sources.find(x=>x.id===sourceIds[i]),previous=i?result.stages[i-1].count:result.base,retained=previous?stage.count/previous:0;const cells=[...new Set(result.rows.flatMap(row=>i<2?[row.populationRow]:i===2?row.relationshipCells:i===3?row.incomeCells:i===4?row.orientationCells:i>=7?row.jointCensus.refs:i===5?[row.heightCell]:i===6?[row.bmiCell]:[]).filter(Boolean))];const choice=fields[i]?$(fields[i]).selectedOptions[0].textContent:i===1?`${s.min}–${s.max} years`:i===5?`${s.heightMin}–${s.heightMax} cm`:data.population[s.geo].name;const active=i<2||stageActive[i];return `<article class="filter-proof"><h3>${esc(['Starting population','Age','Relationship status','Income','Sexual orientation','Height','Weight category (BMI)','Qualifications','Ethnic group'][i])} · ${esc(choice)}</h3><p>${i?active?`About ${number(stage.count)} people remain — a ${number(Math.max(0,1-retained)*100)}% drop from the step above.`:'No preference selected, so this step does not reduce the pool.':`${result.base.toLocaleString('en-GB')} adults — your starting pool (100%).`}</p><p>${esc(plain[i])}</p>${i>=7?'<p class="help">These figures are from the 2021 Census. For locations outside England and Wales, we use England-and-Wales figures as an estimate.</p>':''}<p><a href="sources.html#${source.id}">About this source ↗</a> · <a href="${source.apiURL||source.url}" target="_blank" rel="noopener">View original data ↗</a></p><details><summary>How this is calculated</summary><p>${esc(usage[source.id])}</p><p>${i?`${number(previous)} × ${number(retained*100)}% = approximately ${number(stage.count)} people.`:'All selected-sex residents aged 18+ in the chosen geography.'}</p><p>${esc(source.title)} · ${esc(source.reference)} · ${esc(source.geography)}</p><p class="help">${esc(source.tables)}${cells.length?` · Selected source references: ${esc(cells.join(', '))}`:''}</p>${source.file?`<a href="${source.file}" download>Download source file ↓</a>`:''}</details></article>`;}).join('');
  $('assumptions').innerHTML=result.notes.map(n=>`<li>${esc(n)}</li>`).join('');
  const changes=[['Remove income minimum',{income:0},s.income>0],['Remove height filter',{height:false},s.height],['Any relationship status',{relationship:'any'},s.relationship!=='any'],['Any BMI category',{bmi:'any'},s.bmi!=='any'],['Any qualification',{education:'any'},s.education!=='any'],['Any ethnicity',{ethnicity:'any'},s.ethnicity!=='any'],['Any orientation',{orientation:'any'},s.orientation!=='any']];
  $('relax').innerHTML=changes.filter(x=>x[2]).map(([name,patch])=>{const alternative=calculateDating(data,extra,{...s,...patch});return `<div class="relax-item"><span>${name}</span><strong>${pct(alternative.p)} · ≈ ${people(alternative.count)} people</strong></div>`;}).join('')||'<p class="muted">Add a requirement to see its effect here.</p>';
  for(const key of ['save','download','share-link'])$(key).disabled=false;
 }catch(e){
  $('input-error').textContent=e.message;$('input-error').hidden=false;
  for(const key of ['headline','pool-count','one-in','chance'])$(key).textContent='—';
  $('result-description').textContent='Adjust the highlighted requirements to calculate your pool.';$('denominator').textContent='';$('funnel').innerHTML='';$('relax').innerHTML='';$('assumptions').innerHTML='';$('filter-evidence').innerHTML='';$('selected-filters').innerHTML='';$('sensitivity').textContent='';
  for(const key of ['save','download','share-link'])$(key).disabled=true;
 }
}
async function init(){
 try{
  [data,extra]=await Promise.all(['data/evidence.json','data/filters.json'].map(async path=>{const r=await fetch(path);if(!r.ok)throw Error('Source data unavailable');return r.json();}));
  $('geo').innerHTML=Object.entries(data.population).filter(([k])=>k!=='K03000001').map(([k,p])=>opts(k,p.name)).join('');
  $('income').innerHTML=[0,20000,30000,40000,50000,70000,75000,100000,150000,200000,300000,500000,1000000].map(v=>opts(v,v===0?'Any income':`£${v.toLocaleString('en-GB')}+`)).join('');
  $('education').innerHTML=Object.entries(EDUCATION_LABELS).map(([key,label])=>opts(key,label)).join('');
  fill(DATING_DEFAULT);
  const restore=()=>{if(location.hash.startsWith('#criteria=')){try{const incoming=JSON.parse(decodeURIComponent(location.hash.slice(10)));fill(calculateDating(data,extra,incoming).state);}catch{fill(DATING_DEFAULT);info('Invalid scenario link. Showing default requirements.');}}update();};
  restore();window.addEventListener('hashchange',restore);
  $('height-unit').addEventListener('change',syncHeightUnits);for(const id of ['min-feet','min-inches','max-feet','max-inches'])$(id).addEventListener('input',readImperial);$('preferences').addEventListener('input',update);$('preferences').addEventListener('change',update);$('encounters').addEventListener('input',update);$('spread').addEventListener('input',update);
  $('preferences').addEventListener('submit',e=>{e.preventDefault();update();document.querySelector('.result-card').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});});
  $('reset').onclick=()=>{fill(DATING_DEFAULT);update();history.replaceState(null,'',location.pathname);};
  $('save').onclick=()=>{if(saved.length>=3){info('Remove a saved scenario before adding a fourth.');return;}saved.push({...result.state});renderSaved();info('Requirements saved for comparison.');};
  $('clear').onclick=()=>{saved=[];renderSaved();};
  $('saved').onclick=e=>{if(e.target.dataset.remove!==undefined){saved.splice(Number(e.target.dataset.remove),1);renderSaved();}if(e.target.dataset.load!==undefined){fill(saved[Number(e.target.dataset.load)]);update();}};
  $('download').onclick=()=>{const blob=new Blob([JSON.stringify({...result,exportedAt:new Date().toISOString(),chanceDefinition:'Hypothetical independent random sampling: at least one person meeting filters; not dating success.'},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='dating-pool-calculation.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
  $('share-link').onclick=async()=>{history.replaceState(null,'','#criteria='+encodeURIComponent(JSON.stringify(result.state)));try{await navigator.clipboard.writeText(location.href);info('Scenario link copied. The localhost address works on this computer.');}catch{info('Requirements saved in the address bar. Copy that URL.');}};
  renderSaved();
 }catch(e){$('load-error').textContent='Could not load source data: '+e.message;$('load-error').hidden=false;document.querySelectorAll('button,input,select').forEach(el=>el.disabled=true);}
}
init();
