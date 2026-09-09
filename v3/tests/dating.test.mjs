import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';
import {DATING_DEFAULT,calculateDating,normalCDF,chanceAtLeastOne,incomeRate,educationRate,jointRates,orientationRate} from '../dating-model.mjs';
const data=JSON.parse(readFileSync(new URL('../data/evidence.json',import.meta.url))),extra=JSON.parse(readFileSync(new URL('../data/filters.json',import.meta.url)));
const calc=s=>calculateDating(data,extra,{...DATING_DEFAULT,...s});
test('unfiltered adult pool is exactly its ONS denominator',()=>{const r=calc({min:18,max:90,relationship:'any'});assert.equal(r.count,28396397);assert.equal(r.p,1);assert.equal(r.oneIn,1);});
test('both-sex model is sum of sex-specific calculations',()=>{const filters={income:75000,height:true,bmi:'1',min:35,max:41};const r=calc({...filters,sex:'Persons'});assert.ok(Math.abs(r.count-calc({...filters,sex:'Males'}).count-calc({...filters,sex:'Females'}).count)<1e-8);});
test('income directly uses HMRC taxpayer units and explicit interpolation',()=>{const r=incomeRate(data,extra,'Males',1000000);assert.equal(r.rate,22000/26625856);assert.equal(r.refs[0],'Table_3_3_before_tax!C33');const a=incomeRate(data,extra,'Males',75000).rate,b=incomeRate(data,extra,'Males',100000).rate;assert.ok(Math.abs(a-b-1230000*(25/30)/26625856)<1e-12);});
test('tighter income and height requirements cannot increase the pool',()=>{assert.ok(calc({income:100000}).count<calc({income:30000}).count);assert.ok(calc({height:true,heightMin:175,heightMax:180}).count<calc({height:true,heightMin:160,heightMax:190}).count);});
test('joint relationship category is taken directly without double filtering',()=>{assert.ok(calc({relationship:'notCoupleNever'}).count<=calc({relationship:'notCouple'}).count);const r=calc({relationship:'notCoupleNever',sex:'Males',min:35,max:35});const first=r.rows[0];assert.ok(Math.abs(first.rates[0]-433916/(1155460+411517+18469+433916+72199))<1e-12);});
test('normal CDF and encounter formula have the expected boundaries',()=>{assert.ok(Math.abs(normalCDF(0)-.5)<1e-6);assert.ok(Math.abs(normalCDF(1.96)-.975)<1e-5);assert.equal(chanceAtLeastOne(0,100),0);assert.equal(chanceAtLeastOne(1,100),1);assert.ok(Math.abs(chanceAtLeastOne(.1,2)-.19)<1e-12);});
test('source means and fingerprints are independently anchored',()=>{assert.equal(extra.health.Males[2].mean,176.62552629382702);assert.equal(extra.health.Females[1].bmi[1],39.60845868523705/100);for(const source of extra.sources)assert.equal(createHash('sha256').update(readFileSync(new URL('../'+source.file,import.meta.url))).digest('hex'),source.sha256);});
test('invalid requirements and suppressed source values fail explicitly',()=>{for(const patch of [{min:17},{min:40,max:20},{income:-1},{heightMin:190,heightMax:170},{spread:0},{encounters:0},{encounters:NaN},{geo:'nope'}])assert.throws(()=>calc(patch));const broken=structuredClone(extra);broken.health.Females[1].bmi[1]=null;assert.throws(()=>calculateDating(data,broken,{...DATING_DEFAULT,bmi:'1'}),/unavailable/);});
test('all active model limitations accompany exports',()=>{const r=calc({height:true,income:75000,orientation:'straightBi',ethnicity:'Asian',education:'level4',bmi:'1'});assert.ok(r.notes.some(n=>n.includes('MODELLING ASSUMPTION')));assert.ok(r.notes.some(n=>n.includes('geographic extrapolation')));assert.ok(r.notes.some(n=>n.includes('joint Census 2021')));assert.ok(r.rows.every(row=>row.heightCell&&row.bmiCell&&row.relationshipCells.length));assert.equal(r.sources.length,7);});
test('qualification categories reconcile; minimum levels include higher levels without guessing apprenticeship levels',()=>{
 const keys=['none','level1','level2','apprenticeship','level3','level4','other'];const denominator=keys.reduce((n,k)=>n+extra.education[k].count,0);
 assert.equal(extra.education.level4.count,16413231);
 assert.equal(educationRate(extra,'level3plus'),(8225629+16413231)/denominator);
 assert.equal(educationRate(extra,'apprenticeship'),2590252/denominator);
 assert.ok(educationRate(extra,'level1plus')>educationRate(extra,'level2plus'));assert.ok(educationRate(extra,'level2plus')>educationRate(extra,'level3plus'));
 assert.ok(educationRate(extra,'level3plus')>educationRate(extra,'level4'));
 assert.equal(createHash('sha256').update(readFileSync(new URL('../'+extra.educationSource.file,import.meta.url))).digest('hex'),extra.educationSource.sha256);
});

test('married and partnered union combines disjoint legal marriage and unmarried cohabitation',()=>{
 const input={sex:'Males',min:40,max:40};const r=calc({...input,relationship:'marriedOrCouple'});
 const living=data.relationships.filter(x=>x.sex==='Males'&&x.mode==='living'&&x.age==='40 to 44');
 const cohabiting=living.filter(x=>x.category.startsWith('Living in a couple: Cohabiting'));
 const expected=calc({...input,relationship:'married'}).rows[0].rates[0]+cohabiting.reduce((n,x)=>n+x.count,0)/living.reduce((n,x)=>n+x.count,0);
 assert.ok(living.length);assert.ok(Math.abs(r.rows[0].rates[0]-expected)<1e-12);assert.ok(r.count>=calc({...input,relationship:'couple'}).count);
});

test('suppressed marital denominator is explicit, never silently zero',()=>assert.throws(()=>calc({relationship:'married',sex:'Males',min:35,max:35}),/unavailable/));

test('joint Census factors reproduce the direct joint count without multiplying marginals',()=>{
 const r=jointRates(extra,'Males',30,'K02000001','level4','Black');
 assert.equal(r.total,3913501);assert.equal(r.qualified,1684283);assert.equal(r.selected,82429);assert.ok(Math.abs(r.qualification*r.ethnicity-r.selected/r.total)<1e-14);
 const all=jointRates(extra,'Males',30,'K02000001','any','any');assert.equal(all.joint,1);
 const marginal=jointRates(extra,'Males',30,'K02000001','any','Black');assert.notEqual(r.ethnicity,marginal.ethnicity);
 for(const e of ['none','level1plus','level2plus','level3plus','level4','apprenticeship','other'])assert.ok(jointRates(extra,'Males',30,'K02000001',e,'Black').joint<=marginal.joint);
});
test('orientation uses observed age-sex cells, not pooled shares',()=>{
 const r=orientationRate(extra,'Males',30,'straightBi');assert.ok(Math.abs(r.rate-.926)<1e-12);assert.deepEqual(r.refs,['6b!G113','6b!G115']);
 assert.ok(Math.abs(orientationRate(extra,'Females',30,'straightBi').rate-.954)<1e-12);
 assert.ok(orientationRate(extra,'Males',35,'straightBi').rate!==r.rate);
});
test('new retained data fingerprints match and source grid is complete',()=>{
 assert.equal(extra.jointCensus.length,1120);
 for(const source of [extra.jointSource,extra.orientationSource])assert.equal(createHash('sha256').update(readFileSync(new URL('../'+source.file,import.meta.url))).digest('hex'),source.sha256);
 const w=jointRates(extra,'Females',30,'W92000004','level4','Black');assert.deepEqual(w.countries,['W92000004']);
 const e=jointRates(extra,'Females',30,'E92000001','level4','Black');assert.deepEqual(e.countries,['E92000001']);assert.notEqual(w.joint,e.joint);
});
