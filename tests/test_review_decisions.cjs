const assert=require('node:assert/strict');
require('../office/review-repository.js');
const {client}=globalThis.HVLSReviewRepository;
const draft='---\nstatus: "EDITORIAL DRAFT — NOT APPROVED"\npublication_allowed: false\n---\n# Review fixture';
(async()=>{
 let current={sha:'draft-one',content:draft},record=null,writes=0,conflict=false,race=false;
 const transport=async(url,options)=>{
  assert.ok(!/approvals|articles\//.test(url));
  if(url.includes('/drafts/')){assert.equal(options.method,'GET');return {ok:true,json:async()=>({sha:current.sha,content:Buffer.from(current.content).toString('base64')})};}
  assert.match(url,/editorial\/decisions\/test-article.json/);
  if(options.method==='GET')return record?{ok:true,json:async()=>record}:{ok:false,status:404};
  const payload=JSON.parse(options.body);
  if(conflict||payload.sha!==record?.sha)return {ok:false,status:409};
  writes++;record={sha:'review-'+writes,content:payload.content};
  if(race)current={...current,sha:'draft-concurrent'};
  return {ok:true,json:async()=>({content:{sha:record.sha},commit:{sha:'review-commit-'+writes}})};
 };
 const first=client('memory-only',transport),other=client('memory-only',transport);
 assert.deepEqual(await first.reviews('test-article'),[]);
 await assert.rejects(first.recordReview('test-article',draft,'draft-one','approved','Publish'),/Invalid editorial/);
 await assert.rejects(first.recordReview('test-article',draft,'draft-one','revisions_requested',''),/review notes/);
 await assert.rejects(first.recordReview('test-article',draft+' unsaved','draft-one','revisions_requested','Fix text'),/save your edits/);
 const saved=await first.recordReview('test-article',draft,'draft-one','revisions_requested','Clarify model generation.');
 assert.equal(saved.current,true);assert.equal(saved.event.publication_allowed,false);
 assert.equal((await other.reviews('test-article'))[0].manuscript_blob_sha,'draft-one');
 await other.recordReview('test-article',draft,'draft-one','editorial_text_reviewed','Copy reviewed; technical hold remains.');
 assert.equal((await first.reviews('test-article')).length,2);
 conflict=true;
 await assert.rejects(first.recordReview('test-article',draft,'draft-one','revisions_requested','Concurrent note'),/Review conflict/);
 assert.equal(writes,2);conflict=false;race=true;
 const raced=await first.recordReview('test-article',draft,'draft-one','revisions_requested','Last note on old revision');
 assert.equal(raced.current,false);
 await assert.rejects(first.recordReview('test-article',draft,'draft-one','editorial_text_reviewed','Stale'),/save your edits/);
 assert.equal(writes,3);
 console.log('Editorial decisions: shared history, exact saved text, conflicts, revision race and approval exclusion passed.');
})().catch(e=>{console.error(e);process.exit(1)});
