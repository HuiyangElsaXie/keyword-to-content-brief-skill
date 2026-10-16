// Deterministic minimal DOM simulation. This is NOT a real browser or visual QA.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const text=fs.readFileSync(path.join(__dirname,'final2-awareness/cluster-map.html'),'utf8');
const payload=text.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const code=text.match(/<\/script><script>([\s\S]*?)<\/script>/)[1];
class El {constructor(){this.children=[];this.listeners={};this.attrs={};this.value='';this.textContent='';} append(...e){this.children.push(...e)} replaceChildren(){this.children=[]}setAttribute(k,v){this.attrs[k]=v}addEventListener(k,f){this.listeners[k]=f}}
const ids={}; for(const id of ['data','details','search','role','pages','graph'])ids[id]=new El();ids.data.textContent=payload;
const document={getElementById:id=>ids[id],createElement:()=>new El(),createElementNS:()=>new El()};
new vm.Script(code).runInNewContext({document,JSON,Set,Map,Math});
assert.equal(ids.pages.children.length,4);assert.equal(ids.graph.children.filter(x=>x.attrs.role==='button').length,4);
ids.pages.children[0].listeners.click();assert(ids.details.textContent.includes('page-001'));
ids.search.value='unlikely-no-result';ids.search.listeners.input();assert.equal(ids.pages.children.length,0);
ids.search.value='';ids.role.value='pillar';ids.role.listeners.change();assert.equal(ids.pages.children.length,1);
ids.role.value='spoke';ids.role.listeners.change();assert.equal(ids.pages.children.length,3);
ids.graph.children.find(x=>x.attrs.role==='button').listeners.keydown({key:'Enter'});assert(ids.details.textContent.includes('page-002'));
const result={method:'Node vm with minimal DOM simulation, not browser QA',syntax:'pass',initialCards:4,initialGraphNodes:4,clickDetails:'pass',searchFilter:'pass',roleFilters:'pass',keyboardDetails:'pass',networkCalls:0,visualQA:'not performed; Chromium socket launch denied'};
fs.writeFileSync(path.join(__dirname,'map-dom-final2-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
