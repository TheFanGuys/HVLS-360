// Execute the real Studio script with restricted storage and controlled GitHub responses.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const html=fs.readFileSync(process.argv[2]||'office/first-article-review.html','utf8');
class Element {
 constructor(){this.value='';this.textContent='';this.style={};this.children=[];this.listeners={};this.disabled=false;}
 append(...els){this.children.push(...els)} replaceChildren(){this.children=[]}
 addEventListener(type,handler){this.listeners[type]=handler} focus(){} setAttribute(){}
 async fire(type){return this.listeners[type]?.()}
}
(async()=>{
 const elements=new Map();const get=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id)};
 let commits=0;
 const content='---\nstatus: "EDITORIAL DRAFT — NOT APPROVED"\npublication_allowed: false\n---\n# Test manuscript';
 const session={read:async()=>({sha:'base',content}),save:async(slug,raw,sha)=>{assert.equal(sha,'base');commits++;return {sha:'next',content:raw,commit:'verifiedcommit'}}};
 const context={document:{getElementById:get,createElement:()=>new Element(),createTextNode:t=>t},
 localStorage:{getItem(){throw Error('Storage denied')},setItem(){throw Error('Storage denied')},removeItem(){throw Error('Storage denied')}},
 window:{addEventListener(){}},HVLSReviewRepository:{client:()=>session,reader:()=>session},HVLSReviewPacket:{packet:async()=>({review:'# Technical notes',media:[]})},confirm:()=>false,URL,console};
 vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
 const guestOpen=get('articleLibrary').children[0].children[1];await guestOpen.fire('click');
 assert.equal(get('editorText').value,content);assert.equal(get('saveRepo').disabled,true);
 assert.match(get('repoState').textContent,/Public reading mode/);
 get('repoToken').value='test-session';await get('connectRepo').fire('click');
 assert.match(get('repoState').textContent,/Credential loaded/, 'Denied local storage must not invalidate connection');
 const open=get('articleLibrary').children[0].children[1];await open.fire('click');
 assert.match(get('repoState').textContent,/Shared manuscript opened/, 'Denied local storage must not report a GitHub open failure');
 assert.equal(get('editorText').value,content);assert.equal(get('saveRepo').disabled,false);
 get('editorText').value=content+'\nEdited on phone';await get('editorText').fire('input');
 await get('saveRepo').fire('click');assert.equal(commits,1);assert.match(get('editState').textContent,/Saved to GitHub .* verified/);
 assert.equal(get('editorText').readOnly,false);
 console.log('Studio restricted-storage connection, open, edit and verified save passed (controlled GitHub transport).');
})().catch(e=>{console.error(e);process.exit(1)});
