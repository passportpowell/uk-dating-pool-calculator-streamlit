// Browser QA uses Playwright from the configured Codex runtime; no app dependency.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'C:/Users/passp/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const url=process.env.PREVIEW_URL;
if(!url)throw Error('Set PREVIEW_URL to the running preview.');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(url+'/index.html');await page.locator('#headline').filter({hasText:/M|K/}).waitFor();
  assert.equal(await page.locator('#load-error').isVisible(),false);
  const original=await page.locator('#headline').innerText();
  await page.click('#pin');await page.selectOption('#sex','Males');await page.fill('#min','35');await page.fill('#max','39');
  assert.notEqual(await page.locator('#headline').innerText(),original);
  await page.click('#pin');await page.click('#tab-comparison');assert.equal(await page.locator('.compare-card').count(),2);
  await page.click('[data-load="0"]');assert.equal(await page.locator('#sex').inputValue(),'Females');
  await page.selectOption('#mode','living');assert.equal(await page.locator('#geo').isDisabled(),true);
  await page.selectOption('#sex','Males');await page.selectOption('#band','35 to 39');
  assert.equal(await page.locator('#headline').innerText(),'506K');
  await page.click('#tab-cells');assert.match(await page.locator('#source-table').innerText(),/433,916/);
  const downloadPromise=page.waitForEvent('download');await page.click('#export');const download=await downloadPromise;
  const payload=JSON.parse(await fs.readFile(await download.path(),'utf8'));assert.equal(payload.estimate,506115);assert.equal(payload.source.reference,'2025');
  await page.selectOption('#mode','marital');await page.selectOption('#sex','Persons');await page.selectOption('#band','80 to 84');await page.selectOption('#status','civil');
  assert.equal(await page.locator('#headline').innerText(),'Unavailable');assert.equal(await page.locator('#reliability').isVisible(),true);
  await page.selectOption('#mode','population');await page.fill('#min','70');await page.fill('#max','20');assert.equal(await page.locator('#input-error').isVisible(),true);assert.equal(await page.locator('#export').isDisabled(),true);assert.equal(await page.locator('#headline').innerText(),'—');
  await page.click('#reset');await page.click('#tab-breakdown');await page.locator('#tab-breakdown').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#tab-comparison').getAttribute('aria-selected'),'true');
  await page.click('#tab-breakdown');await page.selectOption('#geo','E12000007');await page.click('#share-link');const shared=page.url();assert.ok(shared.includes('#scenario='));await page.reload();await page.waitForFunction(()=>document.querySelector('#geo').value==='E12000007');
  await page.click('#reset');await page.screenshot({path:path.join(__dirname,'../desktop-qa.png'),fullPage:true});
  for(const width of [390,430,768]){
   await page.setViewportSize({width,height:844});
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`Overflow at ${width}`);
   await page.selectOption('#mode','living');await page.selectOption('#band','18 to 29');await page.click('#tab-cells');
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`Table overflow at ${width}`);
   if(width===390)await page.screenshot({path:path.join(__dirname,'../mobile-qa.png'),fullPage:true});
   await page.click('#reset');await page.click('#tab-breakdown');
  }
  assert.deepEqual(errors,[]);
  assert.equal((await page.request.get(url+'/health')).status(),200);
  assert.equal((await page.request.get(url+'/.env')).status(),404);
  assert.equal((await page.request.get(url+'/../data.py')).status(),404);
  assert.equal((await page.request.get(url+'/sources/mye24tablesuk.xlsx')).status(),200);
  await page.route('**/data/evidence.json',r=>r.abort());await page.reload();await page.locator('#load-error').waitFor({state:'visible'});assert.equal(await page.locator('#export').isDisabled(),true);
  console.log('Browser QA passed: interaction, comparison, download, source suppression, invalid input, keyboard tabs, share/reload, 3 viewport sizes, no JS errors, HTTP checks and dataset failure.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
