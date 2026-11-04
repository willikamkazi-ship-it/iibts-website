// Exercise the shipped script with a minimal browser boundary and no network.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(require('node:path').join(__dirname, '../assets/js/site.js'), 'utf8');

function setup() {
  const handlers = {}, opened = [], attrs = {};
  const field = value => ({ value, attrs: {}, setAttribute(k,v) { this.attrs[k]=v; },
    removeAttribute(k) { delete this.attrs[k]; }, focus() { this.focused=true; } });
  const fields = {name:field('Test Student'),phone:field('+255 700 000 000'),place:field('Test Town'),
    language:field('Kiswahili'),message:field(''),consent:field('')};
  fields.consent.checked=true;
  const error={textContent:''}, prepared={hidden:true};
  const link={removeAttribute(k) { delete this[k]; }};
  let selected=[{value:'GB',disabled:false}];
  const form={elements:fields, querySelector() { return error; },
    querySelectorAll(selector) {
      if(selector==='[aria-invalid]') return Object.values(fields).filter(f=>f.attrs['aria-invalid']);
      return selected.filter(f=>!selector.includes(':not(:disabled)') || !f.disabled);
    },
    addEventListener(k,fn) {handlers[k]=fn;},
    getAttribute(k) {return k==='data-wa'?'255704686885':JSON.stringify({name:'Name',phone:'Phone',place:'Place',
      courses:'Courses',consent:'Consent',language:'Language',message:'Message',intro:'Hello OBTS',missing:'Complete:'});},
    setAttribute(k,v) {attrs[k]=v;}, removeAttribute(k) {delete attrs[k];}};
  const document={querySelector:()=>null,querySelectorAll:()=>[],getElementById(id) {
    return {registration:form,'registration-prepared':prepared,'registration-continue':link}[id];}};
  vm.runInNewContext(source,{document,window:{open(url){opened.push(url);return null;}}});
  return {fields,error,prepared,link,opened,attrs,handlers,select(rows){selected=rows;},
    submit(){handlers.submit({preventDefault(){}});}};
}

let checks=0;
const test=(name,fn)=>{fn();checks++;console.log('PASS '+name);};
test('valid request retains a continuation link when popup returns null',()=>{
  const s=setup();s.submit();assert.equal(s.opened.length,1);assert.equal(s.prepared.hidden,false);
  assert.equal(s.link.href,s.opened[0]);assert.match(decodeURIComponent(s.link.href),/Test Student/);
});
test('spaces cannot inflate a short phone number into a valid number',()=>{
  const s=setup();s.fields.phone.value='+2        5';s.submit();assert.equal(s.opened.length,0);
  assert.equal(s.fields.phone.attrs['aria-invalid'],'true');assert.equal(s.fields.phone.focused,true);
});
test('formatted international number works',()=>{
  const s=setup();s.fields.phone.value='+255 (700) 000-000';s.submit();assert.equal(s.opened.length,1);
});
test('editing clears the previous prepared message',()=>{
  const s=setup();s.submit();s.handlers.input();assert.equal(s.prepared.hidden,true);
  assert.equal(s.link.href,undefined);assert.equal(s.attrs['data-last-url'],undefined);
});
test('disabled course cannot be submitted',()=>{
  const s=setup();s.select([{value:'AI',disabled:true}]);s.submit();assert.equal(s.opened.length,0);
});
test('consent required; corrected fields lose invalid state',()=>{
  const s=setup();s.fields.consent.checked=false;s.submit();assert.equal(s.opened.length,0);
  s.fields.consent.checked=true;s.submit();assert.equal(s.opened.length,1);
  assert.equal(s.fields.consent.attrs['aria-invalid'],undefined);
});
console.log(`${checks} registration checks passed; no messages sent`);
