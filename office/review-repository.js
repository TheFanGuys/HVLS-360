/* GitHub draft storage. Credentials live in memory only; no publication endpoints. */
(function (root) {
'use strict';
const base = 'https://api.github.com/repos/TheFanGuys/HVLS-360/contents/';
const valid = slug => /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug);
const encode = text => btoa(Array.from(new TextEncoder().encode(text), b => String.fromCharCode(b)).join(''));
const decode = text => new TextDecoder().decode(Uint8Array.from(atob(text.replace(/\s/g, '')), c => c.charCodeAt(0)));
function reviewOnly(text) {
 const front = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
 if (!front || !/^publication_allowed: false\s*$/m.test(front[1]) || !/^status: "EDITORIAL DRAFT — NOT APPROVED"\s*$/m.test(front[1])) throw Error('Save blocked: manuscript must remain an unapproved editorial draft.');
 return text;
}
function client(token, transport = fetch, readOnly = false) {
 token=token.trim();
 if (!token && !readOnly) throw Error('Enter a repository-scoped GitHub token.');
 async function request(slug, method = 'GET', body) {
  if (!valid(slug)) throw Error('Invalid article identifier');
  const response = await transport(base + 'editorial/drafts/' + slug + '.md' + (method === 'GET' ? '?ref=main' : ''), {
   method, cache: 'no-store', headers: {Accept:'application/vnd.github+json', ...(token?{Authorization:'Bearer '+token}:{}), 'X-GitHub-Api-Version':'2022-11-28', ...(body ? {'Content-Type':'application/json'} : {})},
   ...(body ? {body:JSON.stringify(body)} : {})
  });
  if (!response.ok) throw Error([409,422].includes(response.status) ? 'Conflict: repository draft changed. Your edit is retained; download it, reopen GitHub draft and reconcile before saving.' : 'GitHub request failed (HTTP '+response.status+'). Check repository access; your edit is retained.');
  return response.json();
 }
 async function read(slug) { const file = await request(slug); return {sha:file.sha, content:decode(file.content)}; }
 async function decisionRequest(slug,method='GET',body){
  if(!valid(slug))throw Error('Invalid article identifier');
  const response=await transport(base+'editorial/decisions/'+slug+'.json'+(method==='GET'?'?ref=main':''),{
   method,cache:'no-store',headers:{Accept:'application/vnd.github+json',...(token?{Authorization:'Bearer '+token}:{}),'X-GitHub-Api-Version':'2022-11-28',...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})
  });
  if(method==='GET'&&response.status===404)return null;
  if(!response.ok)throw Error([409,422].includes(response.status)?'Review conflict: another decision was recorded. Reopen and retry; your notes are retained.':'Review request failed (HTTP '+response.status+'). Your notes are retained.');
  return response.json();
 }
 return {read, async reviews(slug){
  const file=await decisionRequest(slug);if(!file)return [];
  const record=JSON.parse(decode(file.content));
  if(record.schema_version!==1||record.slug!==slug||record.publication_allowed!==false||!Array.isArray(record.events))throw Error('Review history requires Managing Editor inspection.');
  return record.events;
 }, async recordReview(slug,content,sha,decision,note){
  if(readOnly)throw Error('Connect to GitHub before recording a shared review.');
  if(!['revisions_requested','editorial_text_reviewed'].includes(decision))throw Error('Invalid editorial decision; publication approval is unavailable.');
  note=String(note||'').trim();if(!note||note.length>2000)throw Error('Enter review notes between 1 and 2000 characters.');
  reviewOnly(content);
  const current=await read(slug);
  if(!sha||current.sha!==sha||current.content!==content)throw Error('Review blocked: save your edits and reopen the current GitHub revision first.');
  const previous=await decisionRequest(slug);
  const record=previous?JSON.parse(decode(previous.content)):{schema_version:1,slug,publication_allowed:false,events:[]};
  if(record.schema_version!==1||record.slug!==slug||record.publication_allowed!==false||!Array.isArray(record.events)||record.events.length>=200)throw Error('Existing decision history needs Managing Editor review.');
  const event={decision,manuscript_blob_sha:sha,recorded_at:new Date().toISOString(),note,publication_allowed:false};
  record.events.push(event);
  const result=await decisionRequest(slug,'PUT',{branch:'main',...(previous?{sha:previous.sha}:{}),content:encode(JSON.stringify(record,null,2)+'\n'),message:'Editorial review: '+decision+' for '+slug+' (no publication approval)'});
  const verified=await decisionRequest(slug);
  if(!verified||verified.sha!==result.content.sha||decode(verified.content)!==JSON.stringify(record,null,2)+'\n')throw Error('Review commit created but readback differs; inspect GitHub history before retrying.');
  const latest=await read(slug);
  return {event,commit:result.commit.sha,current:latest.sha===sha&&latest.content===content};
 }, async save(slug, content, sha) {
  if(readOnly)throw Error('Connect to GitHub before saving a shared draft.');
  reviewOnly(content);
  if (!sha) throw Error('Open the GitHub draft before saving.');
  const result = await request(slug, 'PUT', {branch:'main', sha, content:encode(content), message:'Founder review: revise '+slug+' (unapproved)'});
  const verified = await read(slug);
  if (verified.content !== content || verified.sha !== result.content.sha) throw Error('Commit created, but latest draft differs. Reopen and reconcile before further edits.');
  return {...verified, commit:result.commit.sha};
 }};
}
root.HVLSReviewRepository = {client, reviewOnly, reader: transport=>client('',transport||fetch,true)};
})(globalThis);
