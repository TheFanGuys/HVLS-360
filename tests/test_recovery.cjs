const assert=require('node:assert/strict');require('../office/recovery.js');
(async()=>{
 const {prompt,read}=globalThis.HVLSRecovery;
 const startup=prompt();assert.match(startup,/No fresh checkpoint/);assert.match(startup,/\$0 added spending/);assert.match(startup,/Never publish/);assert.match(startup,/PROJECT-STATE.json/);
 const content='# HVLS 360 — durable COO handoff\nChris’s next task';
 let calls=0;const result=await read(async(url,options)=>{calls++;assert.match(url,/PROJECT-HANDOFF.md\?ref=main$/);assert.equal(options.cache,'no-store');assert.equal(options.method,undefined);assert.equal(options.headers.Authorization,undefined);return {ok:true,json:async()=>({sha:'abc1234',content:Buffer.from(content).toString('base64')})};});
 assert.equal(result.content,content);assert.equal(calls,1);assert.match(prompt(result.content),/Chris’s next task/);assert.doesNotMatch(prompt(result.content),/No fresh checkpoint is embedded/);
 await assert.rejects(read(async()=>({ok:false,status:403})),/HTTP 403/);
 await assert.rejects(read(async()=>({ok:true,json:async()=>({sha:'x'})})),/Invalid handoff/);
 await assert.rejects(read(async()=>({ok:true,json:async()=>({sha:'x',content:Buffer.from('unrelated page').toString('base64')})})),/Unexpected handoff/);
 console.log('Recovery: Unicode checkpoint, read-only request, source-only fallback, access error and invalid-content rejection passed.');
})().catch(e=>{console.error(e);process.exit(1)});
