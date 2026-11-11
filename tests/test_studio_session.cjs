// Execute the real Studio script with restricted storage and controlled GitHub responses.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const html=fs.readFileSync(process.argv[2]||'office/first-article-review.html','utf8');
class Element {
 constructor(){this.value='';this.textContent='';this.style={};this.children=[];this.listeners={};this.disabled=false;}
 append(...els){this.children.push(...els)} replaceChildren(){this.children=[]}
 addEventListener(type,handler){this.listeners[type]=handler} focus(){this.focused=true} scrollIntoView(){this.scrolled=true} setAttribute(){}
 async fire(type){return this.listeners[type]?.()}
}
(async()=>{
 const elements=new Map();const get=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id)};
 let commits=0,conflict=false;
 const content='---\nstatus: "EDITORIAL DRAFT — NOT APPROVED"\npublication_allowed: false\n---\n# Test manuscript';
 const session={read:async()=>({sha:conflict?'remote':'base',content:conflict?content+'\nOther device edit':content}),reviews:async()=>[{decision:'editorial_text_reviewed',recorded_at:'2026-11-11',manuscript_blob_sha:'base',note:'Earlier review'}],save:async(slug,raw,sha)=>{if(conflict&&sha!=='remote')throw Error('Conflict: repository draft changed.');assert.equal(sha,conflict?'remote':'base');commits++;return {sha:'next',content:raw,commit:'verifiedcommit'}}};
 const context={document:{getElementById:get,createElement:()=>new Element(),createTextNode:t=>t},
 localStorage:{getItem(){throw Error('Storage denied')},setItem(){throw Error('Storage denied')},removeItem(){throw Error('Storage denied')}},
 window:{addEventListener(){}},HVLSReviewRepository:{client:()=>session,reader:()=>session},HVLSReviewPacket:{packet:async()=>({review:'# Technical notes',media:[]})},confirm:()=>false,URL,console};
 vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
 const guestOpen=get('articleLibrary').children[0].children[1];await guestOpen.fire('click');
 assert.equal(get('editorText').value,content);assert.equal(get('saveRepo').disabled,true);
 assert.match(get('repoState').textContent,/Public reading mode/);
 assert.equal(get('draft').scrolled,true);assert.equal(get('draft').focused,true);
 assert.match(get('openState').textContent,/Article opened below/);
 get('repoToken').value='test-session';await get('connectRepo').fire('click');
 assert.match(get('repoState').textContent,/Credential loaded/, 'Denied local storage must not invalidate connection');
 const open=get('articleLibrary').children[0].children[1];await open.fire('click');
 assert.match(get('repoState').textContent,/Shared manuscript opened/, 'Denied local storage must not report a GitHub open failure');
 assert.equal(get('editorText').value,content);assert.equal(get('saveRepo').disabled,false);
 get('editorText').value=content+'\nEdited on phone';await get('editorText').fire('input');
 await get('saveRepo').fire('click');assert.equal(commits,1);assert.match(get('editState').textContent,/Saved to GitHub .* verified/);
 assert.equal(get('editorText').readOnly,false);
 assert.match(get('editState').textContent,/Saved /);
 assert.match(get('reviewHistory').textContent,/Previous revision/,'A previous review must become stale immediately after save');
 conflict=true;const mine=content+'\nMy phone changes';get('editorText').value=mine;await get('editorText').fire('input');
 await get('saveRepo').fire('click');assert.equal(commits,1,'Conflict must not write');
 assert.equal(get('editorText').value,mine,'Keep the local edit');
 assert.equal(get('conflictText').value,content+'\nOther device edit','Show the other revision');
 assert.equal(get('conflictPanel').hidden,false);assert.equal(get('saveRepo').disabled,true);
 await get('saveRepo').fire('click');assert.equal(commits,1,'Save remains blocked until explicit reconciliation');
 get('editorText').value=mine+'\nOther device edit';await get('editorText').fire('input');
 await get('resolveConflict').fire('click');assert.equal(get('conflictPanel').hidden,true);
 assert.equal(get('saveRepo').disabled,false);await get('saveRepo').fire('click');assert.equal(commits,2);

 console.log('Studio restricted-storage connection, open, edit, timestamp, stale-review display, conflict comparison and reconciled save passed (controlled GitHub transport).');
})().catch(e=>{console.error(e);process.exit(1)});
