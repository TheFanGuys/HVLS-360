const assert=require('node:assert/strict');
require('../office/shared-assignments.js');
const {read,category,field}=globalThis.HVLSSharedAssignments;
const item={number:84,state:'open',title:'[HVLS-01] Ventilation',body:'**Owner:** Managing Editor\n**Status:** Blocked — Technical review'};
(async()=>{
 assert.equal(field(item.body,'Owner'),'Managing Editor');
 assert.equal(field(item.body,'Status'),'Blocked — Technical review');
 assert.equal(category(item),'article');
 assert.equal(category({...item,pull_request:{}}),null);
 assert.equal(category({...item,state:'closed'}),null);
 assert.equal(category({...item,title:'HVLS 360 — board'}),null);
 let requests=0;
 const rows=await read(async(url)=>{
  requests++;assert.ok(url.includes('state=open&per_page=100&page='+requests));
  return {ok:true,json:async()=>requests===1?Array.from({length:100},(_,i)=>i===0?item:{...item,pull_request:{}}):[{...item,number:92,title:'[OPS-01] Save path'}]};
 });
 assert.equal(requests,2);assert.deepEqual(rows.map(x=>x.number),[84,92]);
 await assert.rejects(read(async()=>({ok:false,status:403})),/HTTP 403/);
 await assert.rejects(read(async()=>({ok:true,json:async()=>({message:'bad'})})),/Invalid assignment/);
 console.log('Shared assignments: pagination, PR/closed exclusion, owner/status extraction and failure handling passed.');
})().catch(e=>{console.error(e);process.exit(1)});
