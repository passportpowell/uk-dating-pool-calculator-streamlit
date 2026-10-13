import {copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const from='archive/v3_legacy/v3';
mkdirSync('public/evidence/sources',{recursive:true});
for (const name of ['evidence','filters']) copyFileSync(`${from}/data/${name}.json`,`public/evidence/${name}.json`);
const evidence=JSON.parse(readFileSync('public/evidence/evidence.json'));
const filters=JSON.parse(readFileSync('public/evidence/filters.json'));
const sources=[...evidence.sources,...filters.sources,filters.orientationSource,filters.jointSource];
const children=JSON.parse(readFileSync('public/evidence/children-ipsos-2025.json'));
const childBytes=readFileSync('public/evidence/children-ipsos-2025.json');
if(createHash('sha256').update(readFileSync(`${from}/sources/ipsos-parenthood-2025.pdf`)).digest('hex')!==children.sha256)throw Error('Ipsos original fingerprint mismatch');
sources.push({id:'children',title:children.title,url:children.sourceUrl+'#page=172',reference:'2025',geography:'UK adults16+; age-group proxy for each sex',tables:'QD6 Table636 page172',file:'children-ipsos-2025.json',sha256:createHash('sha256').update(childBytes).digest('hex')});
for(const source of sources){
 const bytes=source.id==='children'?childBytes:readFileSync(`${from}/${source.file}`);
 if(createHash('sha256').update(bytes).digest('hex')!==source.sha256)throw Error(`Evidence fingerprint mismatch: ${source.file}`);
 if(source.id!=='children')copyFileSync(`${from}/${source.file}`,`public/evidence/${source.file}`);
}
mkdirSync('docs/archive/pre-audit-20261013',{recursive:true});
for(const file of ['src/lib/data.ts','src/lib/calc.ts','src/lib/calc.test.ts','src/app/page.tsx','src/components/FertilityStatsTab.tsx','src/components/MarriageStatsTab.tsx','src/components/RegionalMapTab.tsx']){
 const to=`docs/archive/pre-audit-20261013/${file.replaceAll('/','-')}.txt`;
 if(existsSync(file)&&!existsSync(to))copyFileSync(file,to);
}
const manifest={checked:'2026-10-13',description:'Pinned official evidence recovered from V3. Source dates are preserved; these are not live population estimates.',sources};
writeFileSync('public/evidence/manifest.json',JSON.stringify(manifest,null,2));
console.log(`Preserved ${sources.length} verified source files and pre-remediation code.`);
