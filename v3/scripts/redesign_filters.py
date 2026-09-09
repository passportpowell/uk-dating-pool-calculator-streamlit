from pathlib import Path
p=Path(__file__).resolve().parents[1]/'calculator.html'
html=p.read_text(encoding='utf-8-sig')
start=html.index('<aside class="panel filters">')
end=html.index('</aside>',start)+len('</aside>')
form='''<aside class="panel filters"><div class="panel-heading"><h2>Your preferences</h2><button id="reset" class="text-button">Reset ↺</button></div><p class="filter-intro">All filters are below. Leave any preference unrestricted.</p><form id="preferences">
<fieldset><legend>01 · Who & where</legend><div class="filter-grid">
<div class="field"><label for="sex">Looking for</label><select id="sex"><option value="Females">Women</option><option value="Males">Men</option><option value="Persons">Men and women</option></select></div>
<div class="field"><label for="geo">Location</label><select id="geo"></select></div>
<div class="field"><label>Age range</label><div class="age-inputs"><div><label for="min" class="small-label">From</label><input id="min" type="number" min="18" max="90" step="1" required></div><span>–</span><div><label for="max" class="small-label">To</label><input id="max" type="number" min="18" max="90" step="1" required></div></div><span class="help">90 includes everyone aged 90+.</span></div>
<div class="field"><label for="orientation">Their sexual orientation</label><select id="orientation"><option value="any">Any</option><option value="straightBi">Straight or bisexual</option><option value="gayBi">Gay / lesbian or bisexual</option><option value="straight">Straight</option><option value="gay">Gay / lesbian</option><option value="bi">Bisexual</option></select></div>
</div></fieldset>
<fieldset><legend>02 · Relationship & background</legend><div class="filter-grid">
<div class="field full"><label for="relationship">Relationship status</label><select id="relationship"><option value="any">Any</option><option value="notCouple">Not living with a partner</option><option value="notCoupleNever">Not living with a partner · never married</option><option value="notCouplePrevious">Not living with a partner · previously married*</option><option value="never">Never legally married / civil partnered</option><option value="divorced">Divorced / dissolved civil partnership</option><option value="widowed">Widowed / surviving civil partner</option></select><span class="help">Living apart does not always mean single. <a href="#model-notes">Definitions ↗</a></span></div>
<div class="field"><label for="income">Minimum yearly income</label><select id="income"></select><span class="help">Before tax; all income sources.</span></div>
<div class="field"><label for="ethnicity">Ethnic group</label><select id="ethnicity"><option value="any">Any</option><option>White</option><option>Asian</option><option>Black</option><option>Mixed</option><option>Other</option></select></div>
<div class="field full"><label for="education">Qualifications</label><select id="education"></select><span class="help" id="education-help">Minimum levels include higher levels.</span></div>
</div></fieldset>
<fieldset><legend>03 · Height & weight</legend><div class="filter-grid">
<div class="field full height-heading"><label class="check-label"><input type="checkbox" id="height"> Filter by height</label><span class="small-label">Optional estimate</span></div>
<div class="field full" id="height-fields"><div class="filter-grid"><div class="field"><label for="heightMin">Minimum height (cm)</label><input id="heightMin" type="number" min="100" max="229" step="0.1"></div><div class="field"><label for="heightMax">Maximum height (cm)</label><input id="heightMax" type="number" min="101" max="230" step="0.1"></div></div><span id="height-imperial" class="help"></span></div>
<div class="field full"><label for="bmi">Weight category (BMI)</label><select id="bmi"><option value="any">Any</option><option value="0">Underweight · BMI below 18.5</option><option value="1">Healthy weight · BMI 18.5–24.9</option><option value="2">Overweight · BMI 25–29.9</option><option value="3">Obesity · BMI 30+</option></select><span class="help">BMI is not a description of body shape.</span></div>
</div></fieldset>
<button class="calculate-button" type="submit">Calculate my pool ↗</button><p class="help">Updates automatically as you change a filter.</p><div id="input-error" class="error" role="alert" hidden></div></form></aside>'''
html=html[:start]+form+html[end:]
html=html.replace('V3.1','V3.2').replace('Who are you<br><em>looking for?</em>','Your preferences.<br><em>Your dating pool.</em>')
html=html.replace('Set your requirements. See the estimated pool, percentage,<br>and how much each preference changes the result.','Choose what matters to you. Explore the estimated match pool.')
html=html.replace('Estimated criteria match','Illustrative estimate')
html=html.replace('<p id="result-description"></p>','<p id="result-description"></p><div id="selected-filters" class="selected-filters" aria-label="Selected requirements"></div>')
html=html.replace('This is an estimate of people meeting your selected requirements. It is <strong>not your personal probability of finding a partner</strong>: attraction, availability, who you meet and whether they like you back are not measured.','<strong>The exact overlap is unknown.</strong> These figures combine separate datasets and assumptions—not a verified count or your chance of finding a partner.')
html=html.replace('<details class="panel model-notes" open>','<details class="panel model-notes" id="model-notes">')
html=html.replace('<summary>Assumptions for this result</summary>','<summary>How reliable is this estimate?</summary><p class="help">The inputs are sourced; their combined overlap is not measured. *The previously-married living-arrangement group can include someone whose spouse lives elsewhere.</p><label for="spread" class="small-label">Height-model spread (cm) · assumption, not NHS data</label><input id="spread" type="number" min="3" max="15" step="0.1"><p id="sensitivity" class="help"></p>')
html=html.replace('<section class="panel encounter-panel"><h2>What if you met more people?</h2><p class="muted">A hypothetical probability calculation: randomly meet adults from the same target group, independently. What is the chance at least one meets your filters?</p>','<section class="panel encounter-panel"><h2>If you met more people</h2><p class="muted">Hypothetical chance that at least one meets your filters.</p>')
html=html.replace('Uses 1 − (1 − p)<sup>n</sup>, with p equal to the modelled share above. Actual social circles and dating apps are not random samples; this is not a forecast of dating success.','Assumes independent, random encounters in your target group. Real dating is not random.')
html=html.replace('See what changes if you loosen a requirement','Loosen a preference')
p.write_text(html,encoding='utf-8')
