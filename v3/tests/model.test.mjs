import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {DEFAULT,calculate,bands,exportResult,sum} from '../model.mjs';
const data=JSON.parse(readFileSync(new URL('../data/evidence.json',import.meta.url)));
test('UK totals independently reconcile to the ONS all-age and adult benchmarks',()=>{
 assert.equal(sum(data.population.K02000001.Persons),69281437);
 assert.equal(calculate(data,{...DEFAULT,sex:'Persons',min:18,max:90}).count,55022253);
 assert.equal(calculate(data,{...DEFAULT,sex:'Males',min:18,max:90}).count,26625856);
 assert.equal(calculate(data,{...DEFAULT,sex:'Females',min:18,max:90}).count,28396397);
});
test('every single-age count reconciles by sex and constituent country',()=>{
 const countries=['E92000001','W92000004','S92000003','N92000002'];
 for(let age=0;age<=90;age++){
  assert.equal(sum(countries.map(c=>data.population[c].Persons[age])),data.population.K02000001.Persons[age]);
  for(const p of Object.values(data.population))assert.equal(p.Persons[age],p.Males[age]+p.Females[age]);
 }
});
test('age selection is inclusive and 90 includes the whole open-ended group',()=>{
 assert.equal(calculate(data,{...DEFAULT,min:90,max:90}).count,data.population.K02000001.Females[90]);
 assert.equal(calculate(data,{...DEFAULT,min:35,max:35}).count,data.population.K02000001.Females[35]);
 assert.equal(calculate(data,{...DEFAULT,min:25,max:39}).count,calculate(data,{...DEFAULT,min:25,max:30}).count+calculate(data,{...DEFAULT,min:31,max:39}).count);
});
test('invalid ages, categories and geography cannot silently calculate',()=>{
 for(const patch of [{min:17},{max:91},{min:40,max:20},{min:NaN},{min:22.5},{geo:'__proto__'},{sex:'Other'},{mode:'bad'},{mode:'living',band:'35 to 41'},{mode:'marital',status:'not-couple'}])assert.throws(()=>calculate(data,{...DEFAULT,...patch}));
});
test('relationship result uses two direct 2025 male cells, not a UK multiplier',()=>{
 const r=calculate(data,{...DEFAULT,mode:'living',sex:'Males',band:'35 to 39',status:'not-couple'});
 assert.equal(r.count,433916+72199);assert.equal(r.geography,'England and Wales');assert.equal(r.state.geo,'K04000001');
 assert.equal(r.base,1155460+411517+18469+433916+72199);
 assert.deepEqual(r.rows.map(r=>r.cell),['5!C59','5!C73']);
});
test('suppression is unavailable, never zero; uncertainty is preserved',()=>{
 const r=calculate(data,{...DEFAULT,mode:'marital',sex:'Persons',band:'80 to 84',status:'civil'});
 assert.equal(r.count,null);assert.equal(r.share,null);assert.equal(sum([1,'[u]']),null);
 const low=calculate(data,{...DEFAULT,mode:'living',sex:'Males',band:'18 to 29',status:'not-couple'});
 assert.equal(low.unreliable,true);assert.equal(low.rows[1].ci,10654);
});
test('all supported views return coherent counts or explicit unavailability',()=>{
 for(const mode of ['living','marital'])for(const sex of ['Persons','Males','Females'])for(const band of bands(data,mode)){
  const r=calculate(data,{...DEFAULT,mode,sex,band,status:'all'});
  assert.equal(r.count,r.base);assert.ok(r.share===null||r.share===1);
 }
});
test('export retains definition, provenance, source rows and uncertainty',()=>{
 const r=calculate(data,{...DEFAULT,mode:'living'}),out=exportResult(data,r);
 assert.equal(out.source.reference,'2025');assert.ok(out.sourceRows.every(r=>r.cell&&r.ciCell));
 assert.ok(out.caveat.includes('not a count of available dates'));
 assert.equal(out.estimate,r.count);assert.equal(out.share,r.share);
});
test('retained source workbooks match the extraction fingerprints',()=>{
 for(const s of data.sources)assert.equal(createHash('sha256').update(readFileSync(new URL('../'+s.file,import.meta.url))).digest('hex'),s.sha256);
});
