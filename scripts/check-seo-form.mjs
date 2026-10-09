/* Exercise the shipped form handler with an isolated API; no leads are sent. */
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
import {strict as assert} from 'node:assert';

const source = readFileSync(new URL('../site-v2/js/main.js', import.meta.url), 'utf8');
const endpoint = 'https://becht-pride.adalandings.com/api/submit';

function fixture(location = 'Carmel') {
  const events = {}, requests = [], timers = [];
  const field = value => ({value, closest: () => ({classList:{add(){}}, querySelector: () => ({textContent:''})})});
  const fields = {name:field('Local QA'), email:field('qa@example.com'), phone:field('(317) 555-0100'), message:field('Local test only; no real submission.'), service:field('water-damage')};
  const button = {textContent:'Request my free estimate',disabled:false};
  const status = {textContent:''}, success = {style:{},focus(){this.focused=true;}};
  const form = {style:{},dataset:{location},addEventListener:(event, fn)=>events[event]=fn,querySelectorAll:()=>[],
    querySelector:s=>s==='.form-submit'?button:s==='.form-status'?status:fields[s.slice(1)],
    closest:()=>({querySelector:()=>success})};
  let reply = async()=>({ok:true,json:async()=>({success:true})});
  const context = {document:{addEventListener(){},querySelector:s=>s==='#contact-form'?form:null},
    AbortController, setTimeout:fn=>{timers.push(fn);return timers.length;},clearTimeout(){},
    alert(){throw Error('Accessible inline status expected');},
    fetch:async(url,options)=>{requests.push({url,options});return reply(options);}};
  runInNewContext(source+'\ninitContactForm();',context);
  return {events, requests, timers, fields, button, status, success, form, setReply:fn=>reply=fn};
}

for (const city of ['Indianapolis','Carmel','Fishers','Noblesville','Westfield','Greenwood','Zionsville','Avon','Plainfield','Brownsburg','Franklin','McCordsville','Fortville','Anderson']) {
  const f=fixture(city);
  await f.events.submit({preventDefault(){}});
  assert.equal(f.requests.length,1);
  assert.equal(f.requests[0].url,endpoint);
  assert.equal(f.requests[0].options.method,'POST');
  const payload=JSON.parse(f.requests[0].options.body);
  assert.equal(payload.slug,'becht-pride');
  assert.equal(payload.service,'water-damage');
  assert.equal(payload.message,`[Website request: ${city}]\nLocal test only; no real submission.`);
  assert.deepEqual(Object.keys(payload).sort(),['email','message','name','phone','service','slug']);
  assert.equal(f.form.style.display,'none');
  assert.equal(f.success.style.display,'block');
  assert.equal(f.success.focused,true);
}

for (const key of ['name','phone','email','message']) {
  const f=fixture(); f.fields[key].value='';
  await f.events.submit({preventDefault(){}});
  assert.equal(f.requests.length,0,`Invalid ${key} sent a request`);
}
const invalid=fixture();invalid.fields.email.value='not-an-email';
await invalid.events.submit({preventDefault(){}});assert.equal(invalid.requests.length,0);

for (const mode of ['http','rejected','json','network','timeout']) {
  const f=fixture();
  f.setReply(options=>{
    if(mode==='http')return {ok:false};
    if(mode==='rejected')return {ok:true,json:async()=>({success:false})};
    if(mode==='json')return {ok:true,json:async()=>{throw Error('Malformed JSON');}};
    if(mode==='network')throw Error('Network unavailable');
    return new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(Error('Timeout'))));
  });
  const attempt=f.events.submit({preventDefault(){}});
  if(mode==='timeout') f.timers[0]();
  await attempt;
  assert.match(f.status.textContent,/could not be confirmed/);
  assert.equal(f.form.style.display,undefined);
  assert.equal(f.button.disabled,false);
  assert.equal(f.fields.message.value,'Local test only; no real submission.');
  f.setReply(async()=>({ok:true,json:async()=>({success:true})}));
  await f.events.submit({preventDefault(){}});
  assert.equal(f.success.style.display,'block');
}

const pending=fixture();let release;
pending.setReply(()=>new Promise(resolve=>release=resolve));
const first=pending.events.submit({preventDefault(){}});
await pending.events.submit({preventDefault(){}});
assert.equal(pending.requests.length,1,'Duplicate in-flight request');
release({ok:true,json:async()=>({success:true})});await first;
console.log('PASS: 14 city payloads; required fields; invalid email; HTTP, API, JSON, network and timeout failures; retry; duplicate-submit prevention. No live API calls.');
