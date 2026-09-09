import {DEFAULT,SEX_LABELS,STATUS_LABELS,bands,calculate,exportResult} from './model.mjs';
const $=id=>document.getElementById(id);
const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const exact=value=>typeof value==='number'?value.toLocaleString('en-GB'):String(value??'Unavailable');
const compact=value=>value===null?'Unavailable':new Intl.NumberFormat('en-GB',{notation:'compact',maximumSignificantDigits:3}).format(value).toUpperCase();
const percent=value=>value===null?'—':`${(value*100).toFixed(1)}%`;
const option=(value,label)=>`<option value="${esc(value)}">${esc(label)}</option>`;
let data,state={...DEFAULT},result,pins=[];
function message(text){$('status-message').textContent=text;}
function readState(){return {...state,mode:$('mode').value,geo:$('geo').value,sex:$('sex').value,min:$('min').valueAsNumber,max:$('max').valueAsNumber,band:$('band').value,status:$('status').value};}
function syncControls(){
 for(const key of ['mode','geo','sex','min','max']) $(key).value=state[key];
 const population=state.mode==='population';
 $('geo').disabled=!population;
 if(!population)$('geo').value='K04000001';
 $('population-age').hidden=!population;$('relationship-filters').hidden=population;
 $('mode-note').textContent=population?'Single-year age counts · mid-2024 snapshot':'Age-specific survey estimates · 2025';
 $('geo-note').textContent=population?'Published country and region totals.':'This dataset covers England and Wales only.';
 const opts=bands(data,state.mode==='population'?'living':state.mode);
 $('band').innerHTML=opts.map(v=>option(v,v.replace(' to ','–').replace(' and over','+'))).join('');
 if(!opts.includes(state.band))state.band=opts[0];
 $('band').value=state.band;
 const statuses=state.mode==='marital'?['all','never','married','civil','divorced','widowed']:['not-couple','in-couple','all'];
 if(!statuses.includes(state.status))state.status=statuses[0];
 $('status').innerHTML=statuses.map(s=>option(s,STATUS_LABELS[s])).join('');$('status').value=state.status;
}
function row(label,value,base){return `<div class="funnel-row"><span>${esc(label)}</span><div class="track"><div class="fill" style="width:${value===null||!base?0:100*value/base}%"></div></div><strong>${esc(compact(value))}</strong></div>`;}
function renderChart(){
 if(state.mode==='population'){
  $('chart-title').textContent='How the population narrows';$('chart-caption').textContent='Counted, not multiplied';
  $('funnel').innerHTML=row('All adults, 18+',result.allAdults,result.allAdults)+row(SEX_LABELS[state.sex]+', 18+',result.base,result.allAdults)+row('Your age range',result.count,result.allAdults);
  $('distribution-title').textContent='Population by single year of age';
  const values=data.population[state.geo][state.sex].slice(18),max=Math.max(...values);
  $('distribution').innerHTML=`<div class="bars" role="img" aria-label="Population by age. Dark green shows the selected age range; exact selected values are in Source values.">${values.map((v,i)=>`<div class="bar ${i+18>=state.min&&i+18<=state.max?'selected':''}" style="height:${v/max*100}%" title="Age ${i+18===90?'90+':i+18}: ${exact(v)}"></div>`).join('')}</div><div class="axis"><span>18</span><span>36</span><span>54</span><span>72</span><span>90+</span></div>`;
 }else{
  $('chart-title').textContent='Within the same age group';$('chart-caption').textContent='England and Wales · 2025';
  $('funnel').innerHTML=row('All statuses',result.base,result.base)+row(STATUS_LABELS[state.status],result.count,result.base);
  $('distribution-title').textContent='Selected status across age bands';
  const items=bands(data,state.mode).map(band=>calculate(data,{...state,band}));
  const max=Math.max(...items.map(r=>r.count??0));
  $('distribution').innerHTML=`<div class="bars" role="img" aria-label="Counts across published age bands. Bands have unequal widths; this chart compares counts, not rates. Exact selected values are in Source values.">${items.map(r=>`<div class="bar ${r.state.band===state.band?'selected':''}" style="height:${max&&r.count!==null?r.count/max*100:0}%" title="${esc(r.state.band)}: ${esc(exact(r.count))}"></div>`).join('')}</div><div class="axis"><span>${esc(items[0].state.band)}</span><span>Published age bands (unequal widths)</span><span>${esc(items.at(-1).state.band)}</span></div>`;
 }
 const source=data.sources.find(s=>s.id===result.sourceId);
 $('chart-source').innerHTML=`Source: <a class="source-link" href="${source.url}" target="_blank" rel="noopener noreferrer">ONS · ${esc(source.reference)} ↗</a>. ${state.mode==='population'?'The 90+ bar contains all ages 90 and over.':'Bar heights are counts. Wider age bands naturally contain more people; unavailable counts are not plotted.'}`;
}
function renderCells(){
 const population=state.mode==='population';
 const cv={a:'a · precise',b:'b · reasonably precise',c:'c · acceptable',d:'d · unreliable'};
 $('source-table').innerHTML=`<table><thead><tr><th>${population?'Age':'Status'}</th><th>Published count</th>${population?'':'<th>95% CI ±</th><th>Robustness</th>'}<th>Workbook cell${population?' / row':''}</th></tr></thead><tbody>${result.rows.map(r=>`<tr><td>${esc(population?r.age:r.category)}</td><td class="num">${esc(exact(r.count))}</td>${population?'':`<td class="num">${esc(exact(r.ci))}</td><td>${esc(cv[r.cv]??r.cv)}</td>`}<td class="source-cell">${esc(r.cell)}</td></tr>`).join('')}</tbody></table>`;
 $('confidence-note').textContent=population?'Counts sum the selected cells of the MYE2 table. The headline is rounded to three significant digits; the values here retain source precision.':'CI ± is the published margin for that individual cell, not for this app’s combined result. Codes: a = precise, b = reasonably precise, c = acceptable, d = unreliable. [u] = low reliability; [x] = unavailable; [z] = not applicable; [w] = no people estimated in that category; [low] = CI rounds to zero. Non-numeric counts are not treated as zero. Source cells are individually rounded, so totals may differ slightly.';
}
function renderPins(){
 $('compare-count').textContent=String(pins.length);
 $('comparison-cards').innerHTML=pins.length?pins.map((s,i)=>{const r=calculate(data,s);return `<article class="compare-card"><header><span class="small-label">SCENARIO ${i+1} · ${esc(r.kind)}</span><button class="text-button" data-remove="${i}" aria-label="Remove scenario ${i+1}">Remove ×</button></header><div class="compare-value">${esc(compact(r.count))}</div><strong>${esc(r.label)}</strong><p>${esc(r.geography)} · ${esc(r.reference)}${s.mode==='population'?'':` · ${esc(STATUS_LABELS[s.status])}`}</p><p>${percent(r.share)} of ${s.mode==='population'?'the selected sex, ages 18+':'the same sex and age band, all statuses'}. ${r.count!==null?'Rounded estimate.':'Source values unavailable.'}</p>${r.unreliable?'<p class="error">Includes a source cell marked unreliable by ONS. Review Source values.</p>':''}<p>${esc(r.warning)}</p><button class="text-button" data-load="${i}">Use this scenario ↗</button></article>`;}).join(''):'<p class="empty">A little context goes a long way.<br>Select “Compare ＋” above to save your first scenario.</p>';
}
function update(){
 try{
  result=calculate(data,readState());state=result.state;
  $('input-error').hidden=true;
  for(const id of ['pin','export','share-link'])$(id).disabled=false;
  $('headline').textContent=compact(result.count);
  $('result-kind').textContent=result.kind;$('result-period').textContent=result.reference+' · '+result.geography;
  $('result-title').textContent=state.mode==='population'?'Your selected population':STATUS_LABELS[state.status];
  $('result-description').textContent=`${result.label} · ${result.geography}. ${result.count===null?'The source does not provide all required values.':'People, rounded to three significant digits.'}`;
  $('share').textContent=percent(result.share);
  $('denominator-label').textContent=state.mode==='population'?`of ${exact(result.base)} ${SEX_LABELS[state.sex].toLowerCase()} aged 18+ in ${result.geography}`:`of ${exact(result.base)} people of this sex and age band, all statuses`;
  $('definition').textContent=result.warning;
  $('reliability').hidden=!result.unreliable&&result.count!==null&&result.base!==null;
  $('reliability').textContent=result.count===null||result.base===null?'A required source value is suppressed or unavailable. Affected totals or percentages are withheld; no missing value is replaced with zero.':'This selection includes a source cell marked unreliable by ONS (CV category d). Inspect Source values before interpreting the estimate; no combined confidence interval is claimed.';
  renderChart();renderCells();
 }catch(error){
  $('input-error').hidden=false;$('input-error').textContent=error.message;
  $('headline').textContent='—';$('share').textContent='—';$('result-description').textContent='Correct the input to update this result.';
  $('denominator-label').textContent='';$('result-kind').textContent='Input needs attention';$('result-period').textContent='';$('definition').textContent='The previous calculation is withheld while an input is invalid.';
  $('funnel').innerHTML='';$('distribution').innerHTML='';$('source-table').innerHTML='';$('reliability').hidden=true;
  for(const id of ['pin','export','share-link'])$(id).disabled=true;
 }
}
function tab(name){
 document.querySelectorAll('[data-tab]').forEach(b=>{const active=b.dataset.tab===name;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;$(b.dataset.tab).hidden=!active;});
}
function restoreHash(){
 if(!location.hash.startsWith('#scenario='))return;
 try{const incoming=JSON.parse(decodeURIComponent(location.hash.slice(10)));state=calculate(data,incoming).state;}
 catch{state={...DEFAULT};message('That scenario link was invalid. Showing the default selection.');}
 syncControls();update();
}
async function init(){
 try{
  const response=await fetch('data/evidence.json');if(!response.ok)throw Error('The source dataset could not be loaded.');data=await response.json();
  $('geo').innerHTML=Object.entries(data.population).filter(([code])=>code!=='K03000001').map(([code,r])=>option(code,r.name)).join('');
  $('source-cards').innerHTML=data.sources.map((s,i)=>`<article class="source-card"><span class="step">0${i+1} / OFFICE FOR NATIONAL STATISTICS</span><h3>${esc(s.title)}</h3><p>${esc(s.geography)}</p><div class="source-meta"><span>REFERENCE <strong>${esc(s.reference)}</strong></span><span>RELEASED <strong>${esc(s.released)}</strong></span></div><p>${esc(s.note)}</p><a href="${s.url}" target="_blank" rel="noopener noreferrer">Read the publication ↗</a><a href="${s.file}" download>Original workbook ↓</a><details><summary class="help">Tables & file fingerprint</summary><p>${esc(s.tables)}</p><p class="help" style="overflow-wrap:anywhere">SHA-256: ${s.sha256}</p></details></article>`).join('');
  syncControls();update();restoreHash();
  $('filters').addEventListener('submit',e=>e.preventDefault());
  $('filters').addEventListener('input',e=>{if(e.target.type==='number')update();});
  $('filters').addEventListener('change',e=>{
   if(e.target.id==='mode'){
    const previous=state.mode;state={...state,mode:e.target.value};
    if(state.mode==='population'&&previous!=='population')state.geo='K02000001';
    if(state.mode==='marital')state.status='never';else if(state.mode==='living')state.status='not-couple';
    syncControls();
   }
   update();
  });
  $('reset').onclick=()=>{state={...DEFAULT};syncControls();update();history.replaceState(null,'',location.pathname);message('Selection reset. Saved comparisons are unchanged.');};
  document.querySelectorAll('[data-ages]').forEach(b=>b.onclick=()=>{const [min,max]=b.dataset.ages.split(',');$('min').value=min;$('max').value=max;update();});
  $('pin').onclick=()=>{if(pins.length===3){tab('comparison');message('Three scenarios saved. Remove one before adding another.');return;}pins.push({...state});renderPins();message(`Scenario ${pins.length} saved. Change a filter to compare another view.`);};
  $('clear-comparison').onclick=()=>{pins=[];renderPins();message('Saved scenarios cleared.');};
  $('comparison-cards').onclick=e=>{if(e.target.dataset.remove!==undefined){pins.splice(Number(e.target.dataset.remove),1);renderPins();}if(e.target.dataset.load!==undefined){state={...pins[Number(e.target.dataset.load)]};syncControls();update();tab('breakdown');}};
  $('export').onclick=()=>{const blob=new Blob([JSON.stringify(exportResult(data,result),null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='dating-pool-evidence.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);message('Downloaded result, definition and source references.');};
  $('share-link').onclick=async()=>{const hash='#scenario='+encodeURIComponent(JSON.stringify(state));history.replaceState(null,'',hash);try{await navigator.clipboard.writeText(location.href);message('Scenario link copied. This local address works on this computer.');}catch{message('Scenario saved in the address bar. Copy the URL to share it.');}};
  document.querySelectorAll('[data-tab]').forEach((b,i,buttons)=>{b.onclick=()=>tab(b.dataset.tab);b.onkeydown=e=>{let index=i;if(e.key==='ArrowRight')index=(i+1)%buttons.length;else if(e.key==='ArrowLeft')index=(i+buttons.length-1)%buttons.length;else if(e.key==='Home')index=0;else if(e.key==='End')index=buttons.length-1;else return;e.preventDefault();buttons[index].focus();tab(buttons[index].dataset.tab);};});
  window.addEventListener('hashchange',restoreHash);renderPins();
 }catch(error){$('load-error').hidden=false;$('load-error').textContent='Unable to load verified data. '+error.message;document.querySelectorAll('button,input,select').forEach(el=>el.disabled=true);}
}
init();


