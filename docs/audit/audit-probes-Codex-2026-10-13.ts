import {ageProbability, calculateDatingPool, cmToFeetInches, getIncomeDistributionForAge, getEducationDistributionForAge, incomeProbability, orientationProbability} from '../../src/lib/calc';
import {AGE_SINGLE_YEAR_DISTRIBUTION, ETHNICITY_DISTRIBUTION, BODY_TYPE_DISTRIBUTION_MALE, CHILDREN_DISTRIBUTION} from '../../src/lib/data';
const base = {userGender:'Female', orientation:'Heterosexual/Straight', lookingFor:'Male', ageRange:[18,89], minHeightCm:100, maxHeightCm:230, minIncome:0, educationLevel:'Any', selectedEthnicities:Object.keys(ETHNICITY_DISTRIBUTION.value), selectedBodyTypes:Object.keys(BODY_TYPE_DISTRIBUTION_MALE.value), mustBeSingle:false, acceptableChildren:Object.keys(CHILDREN_DISTRIBUTION.value), acceptableMarriage:['Never married','Currently married','Divorced','Widowed'], baldnessPreference:'Any', skipSensitivity:true} as const;
const calc=(patch:any={})=>calculateDatingPool({...base,...patch} as any);
const weights=Object.entries(AGE_SINGLE_YEAR_DISTRIBUTION.value);
const integrate=(fn:(age:number)=>number)=>weights.reduce((s,[a,w])=>s+w*fn(a==='90+'?90:Number(a)),0);
console.log(JSON.stringify({
 age90:ageProbability(90,90), age99:ageProbability(99,99), age100:ageProbability(100,100),
 incomeWeighted75:integrate(a=>incomeProbability(75000,'Male',[a,a])), incomeFull75:incomeProbability(75000,'Male',[18,99]),
 educationWeightedPostgrad:integrate(a=>getEducationDistributionForAge([a,a])['Postgraduate degree']), educationFullPostgrad:getEducationDistributionForAge([18,99])['Postgraduate degree'],
 feet152_3:cmToFeetInches(152.3),
 broadCI:calc().confidenceInterval,
 childrenRatio:calc({acceptableChildren:['No children']}).estimatedMatches/calc().estimatedMatches,
 duplicateEthnicity:calc({selectedEthnicities:Array(10).fill('White British')}).steps.find(s=>s.criterion==='Ethnicity'),
 invertedHeight:calc({minHeightCm:200,maxHeightCm:150}).estimatedMatches,
 correlation: (()=>{const r=calc({minIncome:100000,educationLevel:'Undergraduate degree',correlationAdjustment:true});return {headline:r.estimatedMatches,lastFunnel:r.steps.at(-1)?.remaining,boost:r.correlationDiscount}})(),
 anyVsParts: (()=>{const opts={userGender:'Female',orientation:'Bisexual',ageRange:[25,35],minIncome:75000,minHeightCm:180,maxHeightCm:190}; return {any:calc({...opts,lookingFor:'Any'}).estimatedMatches, malePlusFemale:calc({...opts,lookingFor:'Male'}).estimatedMatches+calc({...opts,lookingFor:'Female'}).estimatedMatches}})(),
 orientationStraight:orientationProbability('Heterosexual/Straight','Male','Female'),
},null,2));
