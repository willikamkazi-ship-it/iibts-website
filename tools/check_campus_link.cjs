const assert = require('node:assert/strict');
const {campusUrl} = require('../assets/js/campus-link.js');
const origin = 'https://odm-ai-asistant.onrender.com';
let checks = 0;
function test(name, fn) { fn(); checks++; console.log('PASS ' + name); }
test('dashboard keeps token and requests each website language', () => {
  for (const lang of ['sw','en','fr']) {
    const result = new URL(campusUrl(origin+'/dashboard?t=example.signed-token', origin, '/dashboard', lang));
    assert.equal(result.searchParams.get('t'), 'example.signed-token');
    assert.equal(result.searchParams.get('lang'), lang);
  }
});
test('library uses existing account link without changing the token', () => {
  const url = new URL(campusUrl(origin+'/dashboard?t=example.token&lang=sw&unexpected=remove',origin,'/library','fr'));
  assert.equal(url.pathname,'/library'); assert.equal(url.search,'?t=example.token&lang=fr');
});
test('untrusted origins and deceptive host suffixes are rejected', () => {
  for (const value of ['https://example.com/dashboard?t=a',origin+'.example.com/dashboard?t=a'])
    assert.equal(campusUrl(value,origin,'/dashboard','sw'),null);
});
test('plaintext transport, credentials and script URLs are rejected', () => {
  for (const value of [origin.replace('https:','http:')+'/dashboard?t=a',
    'https://name:password@odm-ai-asistant.onrender.com/dashboard?t=a','javascript:alert(1)'])
    assert.equal(campusUrl(value,origin,'/dashboard','sw'),null);
});
test('missing, duplicated and empty personal tokens are rejected', () => {
  for (const query of ['', '?t=', '?t=a&t=b'])
    assert.equal(campusUrl(origin+'/dashboard'+query,origin,'/dashboard','sw'),null);
});
test('unexpected paths and fragment data are rejected', () => {
  for (const value of [origin+'/staff/portal?t=a',origin+'/dashboard?t=a#private'])
    assert.equal(campusUrl(value,origin,'/dashboard','sw'),null);
});
test('encoded markup and oversized tokens are rejected', () => {
  for (const token of ['%3Cscript%3E', 'a'.repeat(4097)])
    assert.equal(campusUrl(origin+'/dashboard?t='+token,origin,'/dashboard','sw'),null);
});
test('destinations and languages are allowlisted', () => {
  assert.equal(campusUrl(origin+'/dashboard?t=a',origin,'/staff/portal','sw'),null);
  assert.equal(campusUrl(origin+'/dashboard?t=a',origin,'/dashboard','xx'),null);
});
console.log(`${checks} campus-link checks passed; no backend requests made`);
