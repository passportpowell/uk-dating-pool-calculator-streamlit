const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:900}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(process.env.PREVIEW_URL||'http://127.0.0.1:3000');
  await page.locator('select').first().waitFor();
  await page.waitForFunction(()=>new URL(location.href).searchParams.has('c'));
  const optionSelect=value=>page.locator('select').filter({has:page.locator(`option[value="${value}"]`)});
  for(const value of ['100000','level4','Black','none']){const s=value==='none'?optionSelect('threePlus'):optionSelect(value);await s.selectOption(value);}
  await page.waitForFunction(()=>new URL(location.href).searchParams.get('c')?.includes('"children":"none"'));
  const url=page.url();await page.reload();
  await page.waitForFunction(()=>Array.from(document.querySelectorAll('select')).some(s=>Array.from(s.options).some(o=>o.value==='100000')&&s.value==='100000'));
  for(const value of ['100000','level4','Black'])assert.equal(await optionSelect(value).inputValue(),value);
  assert.equal(await optionSelect('threePlus').inputValue(),'none');
  const downloaded=page.waitForEvent('download');
  await page.getByRole('button',{name:/Download/i}).click();
  const payload=JSON.parse(require('node:fs').readFileSync(await (await downloaded).path(),'utf8'));
  assert.ok(payload.rows.length>0&&payload.rows[0].refs.length>0);
  assert.equal(payload.criteria.children,'none');
  assert.equal(await page.getByText('90% CI',{exact:true}).count(),0);
  await optionSelect('ft').selectOption('ft');
  await page.getByLabel('Minimum feet',{exact:true}).fill('6');
  await page.getByLabel('Minimum inches',{exact:true}).fill('0');
  await page.waitForFunction(()=>Math.abs(JSON.parse(new URL(location.href).searchParams.get('c')).criteria.heightMin-182.88)<1e-8);
  await optionSelect('cm').selectOption('cm');assert.ok(Math.abs(Number(await page.getByLabel('Minimum, cm',{exact:true}).inputValue())-182.88)<1e-8);
  for(const route of ['/sources','/methodology','/explorer']){await page.goto(new URL(route,url).href);assert.equal(await page.locator('h1').count(),1);}
  await page.goto(url);await page.getByRole('button',{name:/Apply/i}).first().click();
  for(const width of [390,430,768]){await page.setViewportSize({width,height:844});for(const route of ['/','/sources','/explorer']){await page.goto(new URL(route,url).href);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Overflow ${route} @${width}`);}}
  for(const colorScheme of ['light','dark']){await page.emulateMedia({colorScheme,reducedMotion:'reduce'});await page.goto(url);assert.ok(await page.locator('h1').isVisible());}
  assert.deepEqual(errors,[]);console.log('PASS: complete scenario reload, units, source pages, relaxation, mobile overflow and no page errors.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
