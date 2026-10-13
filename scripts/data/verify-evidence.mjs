import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const manifest=JSON.parse(readFileSync('public/evidence/manifest.json'));
for(const s of manifest.sources){assert.ok(s.url&&s.reference&&s.geography&&s.tables);assert.equal(createHash('sha256').update(readFileSync('public/evidence/'+s.file)).digest('hex'),s.sha256,s.file);}
const d=JSON.parse(readFileSync('public/evidence/evidence.json'));
const sum=a=>a.reduce((s,v)=>s+v,0);
assert.equal(sum(d.population.K02000001.Males.slice(18)),26625856);
assert.equal(sum(d.population.K02000001.Females.slice(18)),28396397);
const f=JSON.parse(readFileSync('public/evidence/filters.json'));
for(const rows of Object.values(f.orientationByAgeSex))for(const row of rows){const rates=Object.values(row.categories).map(c=>c.rate).filter(r=>r!==null);assert.ok(rates.every(r=>r>=0&&r<=1));assert.ok(sum(rates)<=1.000001);}
console.log(`Verified ${manifest.sources.length} original source fingerprints, population totals and orientation shares.`);
