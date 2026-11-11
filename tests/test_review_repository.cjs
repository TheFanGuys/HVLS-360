const assert = require('node:assert/strict');
require('../office/review-repository.js');
const {client, reviewOnly} = globalThis.HVLSReviewRepository;
const draft = '---\nstatus: "EDITORIAL DRAFT — NOT APPROVED"\npublication_allowed: false\n---\n# Motor — 480 V · °F';
(async()=>{
 let content=draft, sha='one', writes=0;
 const transport=async(url,opts)=>{
  assert.match(url,/contents\/editorial\/drafts\/test-article.md/);
  assert.equal(opts.headers.Authorization,'Bearer session-secret');
  if(opts.method==='PUT'){
   const b=JSON.parse(opts.body);assert.equal(b.branch,'main');
   if(b.sha!==sha)return {ok:false,status:409};
   content=Buffer.from(b.content,'base64').toString('utf8');sha='rev'+(++writes);
   return {ok:true,json:async()=>({content:{sha},commit:{sha:'commit'+writes}})};
  }
  return {ok:true,json:async()=>({sha,content:Buffer.from(content).toString('base64')})};
 };
 const a=client('session-secret',transport), b=client('session-secret',transport);
 const first=await a.read('test-article'), stale=await b.read('test-article');
 const saved=await a.save('test-article',draft+'\nEdited on iPhone',first.sha);
 assert.equal(saved.content,(await b.read('test-article')).content);
 await assert.rejects(b.save('test-article',draft+'\nStale',stale.sha),/Conflict/);
 assert.equal(writes,1);
 await assert.rejects(a.save('test-article',draft.replace('false','true'),saved.sha),/unapproved/);
 assert.throws(()=>reviewOnly('# no metadata'),/unapproved/);
 await assert.rejects(a.read('../approvals/escape'),/identifier/);
 const denied=client('bad',async()=>({ok:false,status:403}));
 await assert.rejects(denied.read('test-article'),/HTTP 403/);
 let reads=0;
 const mismatch=client('session-secret',async(url,opts)=>opts.method==='PUT'?{ok:true,json:async()=>({content:{sha:'new'},commit:{sha:'ok'}})}:{ok:true,json:async()=>({sha:'changed',content:Buffer.from(draft).toString('base64')})});
 await assert.rejects(mismatch.save('test-article',draft+' changed','old'),/latest draft differs/);
 console.log('Repository save: Unicode, two clients, stale conflict, approval block, access denial, readback mismatch passed.');
})().catch(e=>{console.error(e);process.exit(1)});
